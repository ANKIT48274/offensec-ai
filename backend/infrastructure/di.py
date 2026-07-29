"""Dependency injection container for the application."""

from __future__ import annotations

from collections.abc import AsyncGenerator
from typing import Any

from fastapi import Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from backend.application.services import (
    AssessmentService,
    FindingService,
    ProjectService,
    UserService,
)
from backend.infrastructure.persistence.postgres.repositories import (
    AssessmentRepository,
    FindingRepository,
    ProjectRepository,
    UserRepository,
)
from backend.infrastructure.persistence.redis import RedisCache, TokenBlacklist
from backend.infrastructure.reporting import MarkdownReportGenerator


from backend.application.services.scan_service import ScanService
from backend.application.services.pipeline_service import PipelineService
from backend.infrastructure.persistence.postgres.repositories.scan_repository import (
    ScanRepository,
)
from backend.infrastructure.persistence.postgres.repositories.pipeline_repository import (
    PipelineJobRepository,
)

__all__ = [
    "get_user_service",
    "get_project_service",
    "get_assessment_service",
    "get_finding_service",
    "get_report_generator_service",
    "get_scan_service",
    "get_pipeline_service",
    "get_ai_client",
    "get_cache",
    "get_token_blacklist",
]


async def get_db_session(request: Request) -> AsyncGenerator[AsyncSession, None]:
    factory = request.app.state.db_session_factory
    async with factory() as session:
        yield session


async def get_pipeline_service(
    session: AsyncSession = Depends(get_db_session),
) -> PipelineService:
    repo = PipelineJobRepository(session)
    return PipelineService(repo=repo)


async def get_scan_service(
    session: AsyncSession = Depends(get_db_session),
) -> ScanService:
    repo = ScanRepository(session)
    return ScanService(scan_repo=repo)


async def get_user_service(
    session: AsyncSession = Depends(get_db_session),
    request: Request = None,
) -> UserService:
    repo = UserRepository(session)
    return UserService(
        user_repo=repo,
        password_hasher=request.app.state.password_hasher,
        token_service=request.app.state.token_service,
        audit_logger=request.app.state.audit_logger,
        event_bus=request.app.state.event_bus,
    )


async def get_project_service(
    session: AsyncSession = Depends(get_db_session),
    request: Request = None,
) -> ProjectService:
    repo = ProjectRepository(session)
    return ProjectService(
        project_repo=repo,
        audit_logger=request.app.state.audit_logger,
        event_bus=request.app.state.event_bus,
    )


async def get_assessment_service(
    session: AsyncSession = Depends(get_db_session),
    request: Request = None,
) -> AssessmentService:
    repo = AssessmentRepository(session)
    return AssessmentService(
        assessment_repo=repo,
        scope_validator=request.app.state.scope_validator,
        audit_logger=request.app.state.audit_logger,
        event_bus=request.app.state.event_bus,
    )


async def get_finding_service(
    session: AsyncSession = Depends(get_db_session),
    request: Request = None,
) -> FindingService:
    repo = FindingRepository(session)
    return FindingService(
        finding_repo=repo,
        ai_client=request.app.state.ai_client,
        audit_logger=request.app.state.audit_logger,
        event_bus=request.app.state.event_bus,
    )


async def get_report_generator_service(
    session: AsyncSession = Depends(get_db_session),
    request: Request = None,
) -> Any:
    from backend.application.use_cases import GenerateReportUseCase
    repo = FindingRepository(session)
    finding_service = FindingService(
        finding_repo=repo,
        ai_client=request.app.state.ai_client,
        audit_logger=request.app.state.audit_logger,
        event_bus=request.app.state.event_bus,
    )
    return GenerateReportUseCase(
        finding_service=finding_service,
        report_generator=MarkdownReportGenerator(),
    )


def get_cache() -> RedisCache:
    return RedisCache()


def get_token_blacklist() -> TokenBlacklist:
    return TokenBlacklist()
