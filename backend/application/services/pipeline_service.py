"""Pipeline service — orchestrates multi-tool scan pipelines."""

from __future__ import annotations

from typing import Any

from backend.application.dto import PipelineJobResponseDTO, PipelineStartDTO
from backend.domain.entities.pipeline_job import PipelineJob
from backend.infrastructure.nuclei.runner import run_nuclei
from backend.infrastructure.persistence.postgres.repositories.nuclei_repository import (
    NucleiResultRepository,
)
from backend.infrastructure.persistence.postgres.repositories.pipeline_repository import (
    PipelineJobRepository,
)
from backend.infrastructure.pipeline.runner import run_pipeline


class PipelineService:
    def __init__(
        self,
        repo: PipelineJobRepository,
        nuclei_repo: NucleiResultRepository,
    ) -> None:
        self._repo = repo
        self._nuclei_repo = nuclei_repo

    async def start(self, dto: PipelineStartDTO) -> PipelineJobResponseDTO:
        job = PipelineJob(project_id=dto.project_id, target=dto.target.strip())
        job.start()
        job_data = await self._repo.create(job.to_dict())

        try:
            result = await run_pipeline(dto.target)
            nmap_data = result.get("nmap", {})
            httpx_data = result.get("httpx", {})

            if nmap_data and not nmap_data.get("error"):
                job.complete_step(
                    0,
                    {
                        "hosts": nmap_data.get("data", {}).get("hosts", []),
                        "scan_info": nmap_data.get("data", {}).get("scan_info", {}),
                    },
                )
            else:
                job.fail_step(0, nmap_data.get("error", "Nmap step failed"))
                return await self._repo.update(job_data.id, job.to_dict())

            if httpx_data and not httpx_data.get("error"):
                job.complete_step(1, {"urls": httpx_data.get("data", [])})
            else:
                if httpx_data and httpx_data.get("error"):
                    job.fail_step(1, httpx_data["error"])
                    return await self._repo.update(job_data.id, job.to_dict())
                job.complete_step(1, {"urls": []})

            urls = (httpx_data.get("data", []) if httpx_data else []) + [dto.target.strip()]
            nuclei_findings: list[dict[str, Any]] = []

            for url in urls[:5]:
                nresult = await run_nuclei(url.get("url", url) if isinstance(url, dict) else url)
                if nresult.get("findings"):
                    for f in nresult["findings"]:
                        f["job_id"] = job_data.id
                        f["project_id"] = dto.project_id
                        f["target"] = url.get("url", url) if isinstance(url, dict) else url
                    nuclei_findings.extend(nresult["findings"])

            if nuclei_findings:
                db_entries = []
                for f in nuclei_findings:
                    db_entries.append(
                        {
                            "id": __import__("uuid").uuid4().hex,
                            "job_id": job_data.id,
                            "project_id": dto.project_id,
                            "target": f.get("target", dto.target.strip()),
                            "template_id": f.get("template_id", "unknown"),
                            "template_name": f.get("template_name"),
                            "severity": f.get("severity", "unknown"),
                            "matched_url": f.get("matched_url"),
                            "matched_at": f.get("matched_at"),
                            "protocol": f.get("protocol"),
                            "tags": f.get("tags", []),
                            "ref_url": f.get("reference"),
                            "cwe_ids": f.get("cwe", []),
                            "cve_ids": f.get("cve", []),
                            "cvss_score": f.get("cvss_score"),
                            "description": f.get("description"),
                            "remediation": f.get("remediation"),
                            "extracted_results": f.get("extracted_results", []),
                            "raw_data": f,
                        }
                    )
                await self._nuclei_repo.bulk_create(db_entries)

            job.complete_step(2, {"count": len(nuclei_findings)})
            return await self._repo.update(job_data.id, job.to_dict())

        except (TimeoutError, RuntimeError, ValueError) as e:
            job.fail_step(0, str(e))
            return await self._repo.update(job_data.id, job.to_dict())

    async def get_by_id(self, job_id: str) -> PipelineJobResponseDTO:
        job = await self._repo.get_by_id(job_id)
        if not job:
            raise ValueError(f"Job {job_id} not found")
        return job

    async def list_by_project(
        self, project_id: str, page: int, page_size: int
    ) -> tuple[list[PipelineJobResponseDTO], int]:
        return await self._repo.list_by_project(project_id, page, page_size)
