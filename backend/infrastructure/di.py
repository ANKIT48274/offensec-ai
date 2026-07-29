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
from backend.application.services.asset_service import AssetService
from backend.application.services.correlation_service import CorrelationService
from backend.application.services.nuclei_service import NucleiResultsService
from backend.application.services.pipeline_service import PipelineService
from backend.application.services.scan_service import ScanService
from backend.infrastructure.persistence.postgres.repositories import (
    AssessmentRepository,
    FindingRepository,
    ProjectRepository,
    UserRepository,
)
from backend.infrastructure.persistence.postgres.repositories.asset_repository import (
    AssetRepository,
)
from backend.infrastructure.persistence.postgres.repositories.evidence_repository import (
    EvidenceRepository,
)
from backend.infrastructure.persistence.postgres.repositories.nuclei_repository import (
    NucleiResultRepository,
)
from backend.infrastructure.persistence.postgres.repositories.pipeline_repository import (
    PipelineJobRepository,
)
from backend.infrastructure.persistence.postgres.repositories.scan_repository import (
    ScanRepository,
)
from backend.infrastructure.persistence.redis import RedisCache, TokenBlacklist
from backend.infrastructure.reporting import MarkdownReportGenerator

__all__ = [
    "get_ai_client",
    "get_assessment_service",
    "get_asset_service",
    "get_cache",
    "get_correlation_service",
    "get_finding_service",
    "get_nuclei_service",
    "get_pipeline_service",
    "get_project_service",
    "get_report_generator_service",
    "get_scan_service",
    "get_token_blacklist",
    "get_user_service",
]


async def get_db_session(request: Request) -> AsyncGenerator[AsyncSession, None]:
    factory = request.app.state.db_session_factory
    async with factory() as session:
        yield session


async def get_correlation_service(
    session: AsyncSession = Depends(get_db_session),
) -> CorrelationService:
    return CorrelationService(session=session)


async def get_asset_service(
    session: AsyncSession = Depends(get_db_session),
) -> AssetService:
    asset_repo = AssetRepository(session)
    evidence_repo = EvidenceRepository(session)
    return AssetService(asset_repo=asset_repo, evidence_repo=evidence_repo)


async def get_nuclei_service(
    session: AsyncSession = Depends(get_db_session),
) -> NucleiResultsService:
    repo = NucleiResultRepository(session)
    return NucleiResultsService(repo=repo)


async def get_pipeline_service(
    session: AsyncSession = Depends(get_db_session),
) -> PipelineService:
    job_repo = PipelineJobRepository(session)
    nuclei_repo = NucleiResultRepository(session)
    return PipelineService(repo=job_repo, nuclei_repo=nuclei_repo)


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
