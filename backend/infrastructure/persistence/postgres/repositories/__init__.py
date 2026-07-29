"""Repository implementations for data access."""

from __future__ import annotations

from typing import Any

from backend.application.dto import (
    AssessmentResponseDTO,
    FindingResponseDTO,
    PaginatedResponseDTO,
    PaginationDTO,
    ProjectResponseDTO,
    UserResponseDTO,
)
from backend.infrastructure.persistence.postgres.models import (
    AssessmentModel,
    FindingModel,
    ProjectModel,
    UserModel,
)
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession


class UserRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create(self, data: dict[str, Any]) -> UserResponseDTO:
        model = UserModel(**data)
        self._session.add(model)
        await self._session.commit()
        await self._session.refresh(model)
        return self._to_dto(model)

    async def get_by_id(self, user_id: str) -> UserResponseDTO | None:
        result = await self._session.get(UserModel, user_id)
        return self._to_dto(result) if result else None

    async def get_by_email(self, email: str) -> UserResponseDTO | None:
        result = await self._session.execute(select(UserModel).where(UserModel.email == email))
        model = result.scalar_one_or_none()
        return self._to_dto(model) if model else None

    async def get_by_username(self, username: str) -> UserResponseDTO | None:
        result = await self._session.execute(
            select(UserModel).where(UserModel.username == username)
        )
        model = result.scalar_one_or_none()
        return self._to_dto(model) if model else None

    async def list(self, page: int, page_size: int) -> PaginatedResponseDTO:
        query = select(UserModel).offset((page - 1) * page_size).limit(page_size)
        result = await self._session.execute(query)
        models = result.scalars().all()

        count_query = select(func.count(UserModel.id))
        count_result = await self._session.execute(count_query)
        total = count_result.scalar() or 0

        return PaginatedResponseDTO(
            data=[self._to_dto(m) for m in models],
            pagination=PaginationDTO(
                page=page,
                page_size=page_size,
                total=total,
                total_pages=(total + page_size - 1) // page_size if page_size > 0 else 0,
            ),
        )

    async def update(self, user_id: str, data: dict[str, Any]) -> UserResponseDTO:
        model = await self._session.get(UserModel, user_id)
        if not model:
            raise ValueError(f"User {user_id} not found")
        for key, value in data.items():
            setattr(model, key, value)
        await self._session.commit()
        await self._session.refresh(model)
        return self._to_dto(model)

    async def delete(self, user_id: str) -> None:
        model = await self._session.get(UserModel, user_id)
        if model:
            await self._session.delete(model)
            await self._session.commit()

    def _to_dto(self, model: UserModel) -> UserResponseDTO:
        return UserResponseDTO(
            id=model.id,
            email=model.email,
            username=model.username,
            password_hash=model.password_hash,
            is_active=model.is_active,
            is_superuser=model.is_superuser,
            created_at=model.created_at,
            updated_at=model.updated_at,
            last_login_at=model.last_login_at,
        )


class ProjectRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create(self, data: dict[str, Any]) -> ProjectResponseDTO:
        model = ProjectModel(**data)
        self._session.add(model)
        await self._session.commit()
        await self._session.refresh(model)
        return self._to_dto(model)

    async def get_by_id(self, project_id: str) -> ProjectResponseDTO | None:
        result = await self._session.get(ProjectModel, project_id)
        return self._to_dto(result) if result else None

    async def list_by_owner(self, owner_id: str, page: int, page_size: int) -> PaginatedResponseDTO:
        query = (
            select(ProjectModel)
            .where(ProjectModel.owner_id == owner_id)
            .offset((page - 1) * page_size)
            .limit(page_size)
        )
        result = await self._session.execute(query)
        models = result.scalars().all()

        count_query = select(func.count(ProjectModel.id)).where(ProjectModel.owner_id == owner_id)
        count_result = await self._session.execute(count_query)
        total = count_result.scalar() or 0

        return PaginatedResponseDTO(
            data=[self._to_dto(m) for m in models],
            pagination=PaginationDTO(
                page=page,
                page_size=page_size,
                total=total,
                total_pages=(total + page_size - 1) // page_size if page_size > 0 else 0,
            ),
        )

    async def update(self, project_id: str, data: dict[str, Any]) -> ProjectResponseDTO:
        model = await self._session.get(ProjectModel, project_id)
        if not model:
            raise ValueError(f"Project {project_id} not found")
        for key, value in data.items():
            setattr(model, key, value)
        await self._session.commit()
        await self._session.refresh(model)
        return self._to_dto(model)

    async def delete(self, project_id: str) -> None:
        model = await self._session.get(ProjectModel, project_id)
        if model:
            await self._session.delete(model)
            await self._session.commit()

    def _to_dto(self, model: ProjectModel) -> ProjectResponseDTO:
        return ProjectResponseDTO(
            id=model.id,
            name=model.name,
            description=model.description,
            owner_id=model.owner_id,
            is_archived=model.is_archived,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )


class AssessmentRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create(self, data: dict[str, Any]) -> AssessmentResponseDTO:
        model = AssessmentModel(**data)
        self._session.add(model)
        await self._session.commit()
        await self._session.refresh(model)
        return self._to_dto(model)

    async def get_by_id(self, assessment_id: str) -> AssessmentResponseDTO | None:
        result = await self._session.get(AssessmentModel, assessment_id)
        return self._to_dto(result) if result else None

    async def list_by_project(
        self, project_id: str, page: int, page_size: int
    ) -> PaginatedResponseDTO:
        query = (
            select(AssessmentModel)
            .where(AssessmentModel.project_id == project_id)
            .offset((page - 1) * page_size)
            .limit(page_size)
        )
        result = await self._session.execute(query)
        models = result.scalars().all()

        count_query = select(func.count(AssessmentModel.id)).where(
            AssessmentModel.project_id == project_id
        )
        count_result = await self._session.execute(count_query)
        total = count_result.scalar() or 0

        return PaginatedResponseDTO(
            data=[self._to_dto(m) for m in models],
            pagination=PaginationDTO(
                page=page,
                page_size=page_size,
                total=total,
                total_pages=(total + page_size - 1) // page_size if page_size > 0 else 0,
            ),
        )

    async def update(self, assessment_id: str, data: dict[str, Any]) -> AssessmentResponseDTO:
        model = await self._session.get(AssessmentModel, assessment_id)
        if not model:
            raise ValueError(f"Assessment {assessment_id} not found")
        for key, value in data.items():
            setattr(model, key, value)
        await self._session.commit()
        await self._session.refresh(model)
        return self._to_dto(model)

    async def delete(self, assessment_id: str) -> None:
        model = await self._session.get(AssessmentModel, assessment_id)
        if model:
            await self._session.delete(model)
            await self._session.commit()

    def _to_dto(self, model: AssessmentModel) -> AssessmentResponseDTO:
        return AssessmentResponseDTO(
            id=model.id,
            project_id=model.project_id,
            name=model.name,
            status=model.status,
            scope=model.scope,
            started_by=model.started_by,
            started_at=model.started_at,
            completed_at=model.completed_at,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )


class FindingRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create(self, data: dict[str, Any]) -> FindingResponseDTO:
        if "references_data" not in data and "references" in data:
            data["references_data"] = data.pop("references", [])
        model = FindingModel(**data)
        self._session.add(model)
        await self._session.commit()
        await self._session.refresh(model)
        return self._to_dto(model)

    async def get_by_id(self, finding_id: str) -> FindingResponseDTO | None:
        result = await self._session.get(FindingModel, finding_id)
        return self._to_dto(result) if result else None

    async def list_by_assessment(
        self, assessment_id: str, page: int, page_size: int
    ) -> PaginatedResponseDTO:
        query = (
            select(FindingModel)
            .where(FindingModel.assessment_id == assessment_id)
            .order_by(FindingModel.created_at.desc())
            .offset((page - 1) * page_size)
            .limit(page_size)
        )
        result = await self._session.execute(query)
        models = result.scalars().all()

        count_query = select(func.count(FindingModel.id)).where(
            FindingModel.assessment_id == assessment_id
        )
        count_result = await self._session.execute(count_query)
        total = count_result.scalar() or 0

        return PaginatedResponseDTO(
            data=[self._to_dto(m) for m in models],
            pagination=PaginationDTO(
                page=page,
                page_size=page_size,
                total=total,
                total_pages=(total + page_size - 1) // page_size if page_size > 0 else 0,
            ),
        )

    async def update(self, finding_id: str, data: dict[str, Any]) -> FindingResponseDTO:
        model = await self._session.get(FindingModel, finding_id)
        if not model:
            raise ValueError(f"Finding {finding_id} not found")
        for key, value in data.items():
            setattr(model, key, value)
        await self._session.commit()
        await self._session.refresh(model)
        return self._to_dto(model)

    async def delete(self, finding_id: str) -> None:
        model = await self._session.get(FindingModel, finding_id)
        if model:
            await self._session.delete(model)
            await self._session.commit()

    def _to_dto(self, model: FindingModel) -> FindingResponseDTO:
        return FindingResponseDTO(
            id=model.id,
            assessment_id=model.assessment_id,
            title=model.title,
            description=model.description,
            severity=model.severity,
            confidence=model.confidence,
            status=model.status,
            target=model.target,
            evidence=model.evidence or [],
            references=model.references_data or [],
            owasp_id=model.owasp_id,
            cwe_id=model.cwe_id,
            cvss_score=model.cvss_score,
            attack_paths=model.attack_paths or [],
            remediation=model.remediation,
            created_by=model.created_by,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )
