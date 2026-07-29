"""Pipeline scan job repository for database operations."""

from __future__ import annotations

from typing import Any

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from backend.application.dto import PipelineJobResponseDTO
from backend.infrastructure.persistence.postgres.models import ScanJobModel


class PipelineJobRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create(self, data: dict[str, Any]) -> PipelineJobResponseDTO:
        model = ScanJobModel(**data)
        self._session.add(model)
        await self._session.commit()
        await self._session.refresh(model)
        return self._to_dto(model)

    async def get_by_id(self, job_id: str) -> PipelineJobResponseDTO | None:
        result = await self._session.get(ScanJobModel, job_id)
        return self._to_dto(result) if result else None

    async def update(self, job_id: str, data: dict[str, Any]) -> PipelineJobResponseDTO:
        model = await self._session.get(ScanJobModel, job_id)
        if not model:
            raise ValueError(f"Job {job_id} not found")
        for key, value in data.items():
            setattr(model, key, value)
        await self._session.commit()
        await self._session.refresh(model)
        return self._to_dto(model)

    async def list_by_project(
        self, project_id: str, page: int, page_size: int
    ) -> tuple[list[PipelineJobResponseDTO], int]:
        query = (
            select(ScanJobModel)
            .where(ScanJobModel.project_id == project_id)
            .order_by(ScanJobModel.created_at.desc())
            .offset((page - 1) * page_size)
            .limit(page_size)
        )
        result = await self._session.execute(query)
        models = result.scalars().all()

        count_query = select(func.count(ScanJobModel.id)).where(ScanJobModel.project_id == project_id)
        count_result = await self._session.execute(count_query)
        total = count_result.scalar() or 0

        return [self._to_dto(m) for m in models], total

    def _to_dto(self, model: ScanJobModel) -> PipelineJobResponseDTO:
        return PipelineJobResponseDTO(
            id=model.id,
            project_id=model.project_id,
            target=model.target,
            status=model.status,
            steps=model.steps or [],
            results=model.results or {},
            error_message=model.error_message,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )
