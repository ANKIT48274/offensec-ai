"""Assessment management API routes."""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Depends, Query

from backend.application.dto import AssessmentCreateDTO
from backend.infrastructure.auth_deps import get_current_user_id
from backend.infrastructure.di import get_assessment_service
from backend.interfaces.api.responses import (
    created_response,
    error_response,
    paginated_response,
    success_response,
)

router = APIRouter()


@router.post("")
async def create_assessment(
    body: AssessmentCreateDTO,
    user_id: str = Depends(get_current_user_id),
    assessment_service: Any = Depends(get_assessment_service),
) -> Any:
    try:
        assessment = await assessment_service.create(body, user_id)
        return created_response(assessment.model_dump(mode="json"))
    except Exception as e:
        return error_response(str(e), code="ASSESSMENT_CREATE_ERROR")


@router.get("")
async def list_assessments(
    project_id: str = Query(""),
    page: int = Query(1, ge=1),
    page_size: int = Query(50, ge=1, le=100),
    assessment_service: Any = Depends(get_assessment_service),
) -> Any:
    result = await assessment_service.list_by_project(project_id, page, page_size)
    return paginated_response(
        [d.model_dump(mode="json") for d in result.data],
        result.pagination.total,
        page,
        page_size,
    )


@router.get("/{assessment_id}")
async def get_assessment(
    assessment_id: str,
    user_id: str = Depends(get_current_user_id),
    assessment_service: Any = Depends(get_assessment_service),
) -> Any:
    try:
        assessment = await assessment_service.get_by_id(assessment_id, user_id)
        return success_response(assessment.model_dump(mode="json"))
    except Exception as e:
        return error_response(str(e), code="ASSESSMENT_GET_ERROR")


@router.post("/{assessment_id}/start")
async def start_assessment(
    assessment_id: str,
    user_id: str = Depends(get_current_user_id),
    assessment_service: Any = Depends(get_assessment_service),
) -> Any:
    try:
        assessment = await assessment_service.start(assessment_id, user_id)
        return success_response(assessment.model_dump(mode="json"))
    except Exception as e:
        return error_response(str(e), code="ASSESSMENT_START_ERROR")


@router.post("/{assessment_id}/complete")
async def complete_assessment(
    assessment_id: str,
    user_id: str = Depends(get_current_user_id),
    assessment_service: Any = Depends(get_assessment_service),
) -> Any:
    try:
        assessment = await assessment_service.complete(assessment_id, user_id)
        return success_response(assessment.model_dump(mode="json"))
    except Exception as e:
        return error_response(str(e), code="ASSESSMENT_COMPLETE_ERROR")
