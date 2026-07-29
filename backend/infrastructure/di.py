"""Dependency injection container for the application."""

from __future__ import annotations

from typing import Any

from fastapi import Request

from backend.application.services import (
    AssessmentService,
    FindingService,
    ProjectService,
    UserService,
)
from backend.infrastructure.ai_client import BaseAIClient, create_ai_client
from backend.infrastructure.logging import get_logger
from backend.infrastructure.persistence.redis import RedisCache, TokenBlacklist
from backend.infrastructure.reporting import MarkdownReportGenerator


async def get_user_service(request: Request) -> UserService:
    logger = get_logger("di")
    logger.debug("Resolving UserService")
    return UserService(
        user_repo=request.app.state.user_repo,
        password_hasher=request.app.state.password_hasher,
        token_service=request.app.state.token_service,
        audit_logger=request.app.state.audit_logger,
        event_bus=request.app.state.event_bus,
    )


async def get_project_service(request: Request) -> ProjectService:
    return ProjectService(
        project_repo=request.app.state.project_repo,
        audit_logger=request.app.state.audit_logger,
        event_bus=request.app.state.event_bus,
    )


async def get_assessment_service(request: Request) -> AssessmentService:
    return AssessmentService(
        assessment_repo=request.app.state.assessment_repo,
        scope_validator=request.app.state.scope_validator,
        audit_logger=request.app.state.audit_logger,
        event_bus=request.app.state.event_bus,
    )


async def get_finding_service(request: Request) -> FindingService:
    return FindingService(
        finding_repo=request.app.state.finding_repo,
        ai_client=request.app.state.ai_client,
        audit_logger=request.app.state.audit_logger,
        event_bus=request.app.state.event_bus,
    )


async def get_report_generator_service(request: Request) -> Any:
    from backend.application.use_cases import GenerateReportUseCase
    return GenerateReportUseCase(
        finding_service=FindingService(
            finding_repo=request.app.state.finding_repo,
            ai_client=request.app.state.ai_client,
            audit_logger=request.app.state.audit_logger,
            event_bus=request.app.state.event_bus,
        ),
        report_generator=MarkdownReportGenerator(),
    )


async def get_ai_client() -> BaseAIClient:
    return create_ai_client()


def get_cache() -> RedisCache:
    return RedisCache()


def get_token_blacklist() -> TokenBlacklist:
    return TokenBlacklist()
