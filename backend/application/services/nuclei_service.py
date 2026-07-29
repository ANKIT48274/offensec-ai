"""Nuclei results service."""

from __future__ import annotations

from typing import Any

from backend.infrastructure.persistence.postgres.repositories.nuclei_repository import (
    NucleiResultRepository,
)


class NucleiResultsService:
    def __init__(self, repo: NucleiResultRepository) -> None:
        self._repo = repo

    async def list_by_project(
        self,
        project_id: str,
        page: int,
        page_size: int,
        severity: str | None = None,
        search: str | None = None,
    ) -> tuple[list[Any], int]:
        return await self._repo.list_by_project(project_id, page, page_size, severity, search)

    async def get_by_id(self, result_id: str) -> Any:
        return await self._repo.get_by_id(result_id)

    async def severity_counts(self, project_id: str) -> dict[str, int]:
        return await self._repo.severity_counts(project_id)
