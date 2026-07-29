"""Asset service — manages discovered assets with dedup."""

from __future__ import annotations

from typing import Any

from backend.infrastructure.persistence.postgres.repositories.asset_repository import (
    AssetRepository,
)
from backend.infrastructure.persistence.postgres.repositories.evidence_repository import (
    EvidenceRepository,
)


class AssetService:
    def __init__(self, asset_repo: AssetRepository, evidence_repo: EvidenceRepository) -> None:
        self._asset_repo = asset_repo
        self._evidence_repo = evidence_repo

    async def upsert_from_scan(
        self,
        project_id: str,
        asset_type: str,
        value: str,
        data: dict[str, Any],
    ) -> dict[str, Any]:
        asset = await self._asset_repo.upsert(project_id, asset_type, value, data)
        return asset.model_dump(mode="json")

    async def get_by_id(self, asset_id: str) -> dict[str, Any] | None:
        asset = await self._asset_repo.get_by_id(asset_id)
        if not asset:
            return None
        d = asset.model_dump(mode="json")
        evidence = await self._evidence_repo.list_by_asset(asset_id)
        d["evidence"] = [e.model_dump(mode="json") for e in evidence]
        return d

    async def list_by_project(
        self, project_id: str, page: int, page_size: int, asset_type: str | None = None, search: str | None = None
    ) -> tuple[list[dict[str, Any]], int]:
        assets, total = await self._asset_repo.list_by_project(project_id, page, page_size, asset_type, search)
        return [a.model_dump(mode="json") for a in assets], total

    async def evidence_list(
        self, project_id: str, page: int, page_size: int, source: str | None = None
    ) -> tuple[list[dict[str, Any]], int]:
        items, total = await self._evidence_repo.list_by_project(project_id, page, page_size, source)
        return [e.model_dump(mode="json") for e in items], total

    async def evidence_get(self, evidence_id: str) -> dict[str, Any] | None:
        e = await self._evidence_repo.get_by_id(evidence_id)
        return e.model_dump(mode="json") if e else None
