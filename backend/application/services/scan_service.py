"""Scan service — orchestrates Nmap scans."""

from __future__ import annotations

from typing import Any

from backend.application.dto import ScanCreateDTO, ScanResponseDTO
from backend.domain.entities.scan import Scan
from backend.infrastructure.persistence.postgres.repositories.scan_repository import (
    ScanRepository,
)
from backend.infrastructure.scan_engine.runner import run_nmap_scan


class ScanService:
    def __init__(self, scan_repo: ScanRepository) -> None:
        self._scan_repo = scan_repo

    async def create_and_run(self, dto: ScanCreateDTO) -> ScanResponseDTO:
        scan = Scan(project_id=dto.project_id, target=dto.target.strip())
        scan.start()
        scan_data = await self._scan_repo.create(scan.to_dict())

        try:
            result = await run_nmap_scan(dto.target)
            parsed = (result.get("parsed") or {}).get("hosts") or []
            scan.complete(
                xml_path=result["xml_path"],
                json_result={
                    "hosts": parsed,
                    "scan_info": result.get("parsed", {}).get("scan_info", {}),
                    "target": dto.target.strip(),
                },
            )
            updated = await self._scan_repo.update(scan_data.id, scan.to_dict())
            return updated
        except (TimeoutError, RuntimeError, ValueError) as e:
            scan.fail(str(e))
            updated = await self._scan_repo.update(scan_data.id, scan.to_dict())
            return updated

    async def get_by_id(self, scan_id: str) -> ScanResponseDTO:
        scan = await self._scan_repo.get_by_id(scan_id)
        if not scan:
            raise ValueError(f"Scan {scan_id} not found")
        return scan

    async def list_by_project(
        self, project_id: str, page: int, page_size: int
    ) -> tuple[list[ScanResponseDTO], int]:
        return await self._scan_repo.list_by_project(project_id, page, page_size)

    async def delete(self, scan_id: str) -> None:
        await self._scan_repo.delete(scan_id)
