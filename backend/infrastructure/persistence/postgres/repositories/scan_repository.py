"""Scan repository for database operations."""

from __future__ import annotations

from typing import Any

from backend.application.dto import ScanResponseDTO
from backend.infrastructure.persistence.postgres.models import ScanModel
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession


class ScanRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create(self, data: dict[str, Any]) -> ScanResponseDTO:
        model = ScanModel(**data)
        self._session.add(model)
        await self._session.commit()
        await self._session.refresh(model)
        return self._to_dto(model)

    async def get_by_id(self, scan_id: str) -> ScanResponseDTO | None:
        result = await self._session.get(ScanModel, scan_id)
        return self._to_dto(result) if result else None

    async def update(self, scan_id: str, data: dict[str, Any]) -> ScanResponseDTO:
        model = await self._session.get(ScanModel, scan_id)
        if not model:
            raise ValueError(f"Scan {scan_id} not found")
        for key, value in data.items():
            setattr(model, key, value)
        await self._session.commit()
        await self._session.refresh(model)
        return self._to_dto(model)

    async def list_by_project(
        self, project_id: str, page: int, page_size: int
    ) -> tuple[list[ScanResponseDTO], int]:
        query = (
            select(ScanModel)
            .where(ScanModel.project_id == project_id)
            .order_by(ScanModel.created_at.desc())
            .offset((page - 1) * page_size)
            .limit(page_size)
        )
        result = await self._session.execute(query)
        models = result.scalars().all()

        count_query = select(func.count(ScanModel.id)).where(ScanModel.project_id == project_id)
        count_result = await self._session.execute(count_query)
        total = count_result.scalar() or 0

        return [self._to_dto(m) for m in models], total

    async def delete(self, scan_id: str) -> None:
        model = await self._session.get(ScanModel, scan_id)
        if model:
            await self._session.delete(model)
            await self._session.commit()

    def _to_dto(self, model: ScanModel) -> ScanResponseDTO:
        return ScanResponseDTO(
            id=model.id,
            project_id=model.project_id,
            target=model.target,
            status=model.status,
            started_at=model.started_at,
            finished_at=model.finished_at,
            xml_path=model.xml_path,
            json_result=model.json_result,
            error_message=model.error_message,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )
