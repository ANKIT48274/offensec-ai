"""Asset repository with merge and dedup."""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

from backend.application.dto import AssetResponseDTO
from backend.infrastructure.persistence.postgres.models import AssetModel
from sqlalchemy import func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession


class AssetRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def upsert(
        self, project_id: str, asset_type: str, value: str, data: dict[str, Any]
    ) -> AssetResponseDTO:
        existing = await self._find_exact(project_id, value)
        if existing:
            return await self._merge(existing, data)
        model = AssetModel(
            project_id=project_id,
            asset_type=asset_type,
            value=value,
            ips=data.get("ips", []),
            hostnames=data.get("hostnames", []),
            domains=data.get("domains", []),
            ports=data.get("ports", []),
            technologies=data.get("technologies", []),
            os_guesses=data.get("os_guesses", []),
            label=data.get("label"),
            first_seen=datetime.now(UTC),
            last_seen=datetime.now(UTC),
            scan_count=1,
            asset_meta=data.get("metadata", {}),
        )
        self._session.add(model)
        await self._session.commit()
        await self._session.refresh(model)
        return self._to_dto(model)

    async def _find_exact(self, project_id: str, value: str) -> AssetModel | None:
        result = await self._session.execute(
            select(AssetModel).where(
                AssetModel.project_id == project_id,
                AssetModel.value == value,
            )
        )
        return result.scalar_one_or_none()

    async def _merge(self, existing: AssetModel, data: dict[str, Any]) -> AssetResponseDTO:
        now = datetime.now(UTC)

        new_ips = list(set(existing.ips or []) | set(data.get("ips", [])))
        new_hosts = list(set(existing.hostnames or []) | set(data.get("hostnames", [])))
        new_domains = list(set(existing.domains or []) | set(data.get("domains", [])))
        new_ports = _merge_ports(existing.ports or [], data.get("ports", []))
        new_tech = list(set(existing.technologies or []) | set(data.get("technologies", [])))
        new_os = list(set(existing.os_guesses or []) | set(data.get("os_guesses", [])))

        existing.ips = new_ips
        existing.hostnames = new_hosts
        existing.domains = new_domains
        existing.ports = new_ports
        existing.technologies = new_tech
        existing.os_guesses = new_os
        existing.last_seen = now
        existing.scan_count = (existing.scan_count or 0) + 1
        if data.get("label"):
            existing.label = data["label"]

        await self._session.commit()
        await self._session.refresh(existing)
        return self._to_dto(existing)

    async def get_by_id(self, asset_id: str) -> AssetResponseDTO | None:
        model = await self._session.get(AssetModel, asset_id)
        return self._to_dto(model) if model else None

    async def list_by_project(
        self,
        project_id: str,
        page: int,
        page_size: int,
        asset_type: str | None = None,
        search: str | None = None,
    ) -> tuple[list[AssetResponseDTO], int]:
        query = select(AssetModel).where(AssetModel.project_id == project_id)
        count_query = select(func.count(AssetModel.id)).where(AssetModel.project_id == project_id)

        if asset_type and asset_type != "all":
            query = query.where(AssetModel.asset_type == asset_type)
            count_query = count_query.where(AssetModel.asset_type == asset_type)

        if search:
            like = f"%{search}%"
            query = query.where(
                or_(
                    AssetModel.value.ilike(like),
                    AssetModel.label.ilike(like),
                )
            )
            count_query = count_query.where(
                or_(
                    AssetModel.value.ilike(like),
                    AssetModel.label.ilike(like),
                )
            )

        query = (
            query.order_by(AssetModel.last_seen.desc())
            .offset((page - 1) * page_size)
            .limit(page_size)
        )
        result = await self._session.execute(query)
        models = list(result.scalars().all())

        count_result = await self._session.execute(count_query)
        total = count_result.scalar() or 0

        return [self._to_dto(m) for m in models], total

    def _to_dto(self, model: AssetModel) -> AssetResponseDTO:
        return AssetResponseDTO(
            id=model.id,
            project_id=model.project_id,
            asset_type=model.asset_type,
            value=model.value,
            label=model.label,
            ips=model.ips or [],
            hostnames=model.hostnames or [],
            domains=model.domains or [],
            ports=model.ports or [],
            technologies=model.technologies or [],
            os_guesses=model.os_guesses or [],
            first_seen=model.first_seen,
            last_seen=model.last_seen,
            scan_count=model.scan_count or 1,
            metadata=model.asset_meta or {},
            created_at=model.created_at,
            updated_at=model.updated_at,
        )


def _merge_ports(
    existing: list[dict[str, Any]], incoming: list[dict[str, Any]]
) -> list[dict[str, Any]]:
    seen = {(p.get("port"), p.get("protocol")) for p in existing}
    merged = list(existing)
    for p in incoming:
        key = (p.get("port"), p.get("protocol"))
        if key not in seen:
            seen.add(key)
            merged.append(p)
    return merged
