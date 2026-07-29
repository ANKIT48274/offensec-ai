"""Pipeline service — orchestrates multi-tool scan pipelines."""

from __future__ import annotations

from typing import Any

from backend.application.dto import PipelineJobResponseDTO, PipelineStartDTO
from backend.domain.entities.pipeline_job import PipelineJob
from backend.infrastructure.persistence.postgres.repositories.pipeline_repository import (
    PipelineJobRepository,
)
from backend.infrastructure.pipeline.runner import run_pipeline


class PipelineService:
    def __init__(self, repo: PipelineJobRepository) -> None:
        self._repo = repo

    async def start(self, dto: PipelineStartDTO) -> PipelineJobResponseDTO:
        job = PipelineJob(project_id=dto.project_id, target=dto.target.strip())
        job.start()
        job_data = await self._repo.create(job.to_dict())

        try:
            result = await run_pipeline(dto.target)
            nmap_data = result.get("nmap", {})
            httpx_data = result.get("httpx", {})

            if nmap_data and not nmap_data.get("error"):
                job.complete_step(0, {
                    "hosts": nmap_data.get("data", {}).get("hosts", []),
                    "scan_info": nmap_data.get("data", {}).get("scan_info", {}),
                })
            else:
                job.fail_step(0, nmap_data.get("error", "Nmap step failed"))
                updated = await self._repo.update(job_data.id, job.to_dict())
                return updated

            if httpx_data and not httpx_data.get("error"):
                job.complete_step(1, {"urls": httpx_data.get("data", [])})
            else:
                if httpx_data and httpx_data.get("error"):
                    job.fail_step(1, httpx_data["error"])
                else:
                    job.complete_step(1, {"urls": []})

            updated = await self._repo.update(job_data.id, job.to_dict())
            return updated

        except (TimeoutError, RuntimeError, ValueError) as e:
            job.fail_step(0, str(e))
            updated = await self._repo.update(job_data.id, job.to_dict())
            return updated

    async def get_by_id(self, job_id: str) -> PipelineJobResponseDTO:
        job = await self._repo.get_by_id(job_id)
        if not job:
            raise ValueError(f"Job {job_id} not found")
        return job

    async def list_by_project(
        self, project_id: str, page: int, page_size: int
    ) -> tuple[list[PipelineJobResponseDTO], int]:
        return await self._repo.list_by_project(project_id, page, page_size)
