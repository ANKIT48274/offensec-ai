"""Nuclei result repository."""

from __future__ import annotations

from typing import Any

from backend.infrastructure.persistence.postgres.models import NucleiResultModel
from sqlalchemy import func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession


class NucleiResultRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def bulk_create(self, entries: list[dict[str, Any]]) -> list[NucleiResultModel]:
        models = [NucleiResultModel(**e) for e in entries]
        for m in models:
            self._session.add(m)
        await self._session.commit()
        for m in models:
            await self._session.refresh(m)
        return models

    async def get_by_id(self, result_id: str) -> NucleiResultModel | None:
        return await self._session.get(NucleiResultModel, result_id)

    async def list_by_job(self, job_id: str) -> list[NucleiResultModel]:
        result = await self._session.execute(
            select(NucleiResultModel)
            .where(NucleiResultModel.job_id == job_id)
            .order_by(NucleiResultModel.created_at.desc())
        )
        return list(result.scalars().all())

    async def list_by_project(
        self,
        project_id: str,
        page: int,
        page_size: int,
        severity: str | None = None,
        search: str | None = None,
    ) -> tuple[list[NucleiResultModel], int]:
        query = select(NucleiResultModel).where(NucleiResultModel.project_id == project_id)
        count_query = select(func.count(NucleiResultModel.id)).where(
            NucleiResultModel.project_id == project_id
        )

        if severity and severity != "all":
            query = query.where(NucleiResultModel.severity == severity)
            count_query = count_query.where(NucleiResultModel.severity == severity)

        if search:
            like = f"%{search}%"
            query = query.where(
                or_(
                    NucleiResultModel.template_id.ilike(like),
                    NucleiResultModel.template_name.ilike(like),
                    NucleiResultModel.matched_url.ilike(like),
                    NucleiResultModel.description.ilike(like),
                )
            )
            count_query = count_query.where(
                or_(
                    NucleiResultModel.template_id.ilike(like),
                    NucleiResultModel.template_name.ilike(like),
                    NucleiResultModel.matched_url.ilike(like),
                    NucleiResultModel.description.ilike(like),
                )
            )

        query = (
            query.order_by(NucleiResultModel.created_at.desc())
            .offset((page - 1) * page_size)
            .limit(page_size)
        )
        result = await self._session.execute(query)
        models = list(result.scalars().all())

        count_result = await self._session.execute(count_query)
        total = count_result.scalar() or 0

        return models, total

    async def severity_counts(self, project_id: str) -> dict[str, int]:
        counts: dict[str, int] = {}
        for sev in ("critical", "high", "medium", "low", "info"):
            result = await self._session.execute(
                select(func.count(NucleiResultModel.id)).where(
                    NucleiResultModel.project_id == project_id, NucleiResultModel.severity == sev
                )
            )
            counts[sev] = result.scalar() or 0
        return counts
