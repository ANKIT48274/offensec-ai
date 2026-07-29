"""Evidence repository."""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from backend.application.dto import EvidenceResponseDTO
from backend.infrastructure.persistence.postgres.models import EvidenceModelNew


class EvidenceRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create(self, data: dict[str, Any]) -> EvidenceResponseDTO:
        if "id" not in data:
            import uuid
            data["id"] = uuid.uuid4().hex
        model = EvidenceModelNew(**data)
        self._session.add(model)
        await self._session.commit()
        await self._session.refresh(model)
        return self._to_dto(model)

    async def bulk_create(self, entries: list[dict[str, Any]]) -> list[EvidenceResponseDTO]:
        import uuid
        models = []
        for e in entries:
            if "id" not in e:
                e["id"] = uuid.uuid4().hex
            m = EvidenceModelNew(**e)
            self._session.add(m)
            models.append(m)
        await self._session.commit()
        return [self._to_dto(m) for m in models]

    async def get_by_id(self, evidence_id: str) -> EvidenceResponseDTO | None:
        model = await self._session.get(EvidenceModelNew, evidence_id)
        return self._to_dto(model) if model else None

    async def list_by_project(
        self, project_id: str, page: int, page_size: int, source: str | None = None
    ) -> tuple[list[EvidenceResponseDTO], int]:
        query = select(EvidenceModelNew).where(EvidenceModelNew.project_id == project_id)
        count_query = select(func.count(EvidenceModelNew.id)).where(EvidenceModelNew.project_id == project_id)

        if source and source != "all":
            query = query.where(EvidenceModelNew.source == source)
            count_query = count_query.where(EvidenceModelNew.source == source)

        query = query.order_by(EvidenceModelNew.captured_at.desc()).offset((page - 1) * page_size).limit(page_size)
        result = await self._session.execute(query)
        models = list(result.scalars().all())

        count_result = await self._session.execute(count_query)
        total = count_result.scalar() or 0

        return [self._to_dto(m) for m in models], total

    async def list_by_asset(self, asset_id: str) -> list[EvidenceResponseDTO]:
        result = await self._session.execute(
            select(EvidenceModelNew).where(EvidenceModelNew.asset_id == asset_id)
            .order_by(EvidenceModelNew.captured_at.desc())
        )
        return [self._to_dto(m) for m in result.scalars().all()]

    def _to_dto(self, model: EvidenceModelNew) -> EvidenceResponseDTO:
        return EvidenceResponseDTO(
            id=model.id,
            asset_id=model.asset_id,
            project_id=model.project_id,
            finding_id=model.finding_id,
            source=model.source,
            evidence_type=model.evidence_type,
            content=model.content,
            file_path=model.file_path,
            raw_data=model.raw_data,
            captured_at=model.captured_at,
        )
