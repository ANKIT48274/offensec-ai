"""Finding management API routes."""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Depends, Header, Query

from backend.application.dto import FindingCreateDTO
from backend.infrastructure.di import get_finding_service
from backend.interfaces.api.responses import (
    created_response,
    error_response,
    paginated_response,
    success_response,
)

router = APIRouter()


@router.post("")
async def create_finding(
    body: FindingCreateDTO,
    x_user_id: str = Header(""),
    finding_service: Any = Depends(get_finding_service),
) -> Any:
    try:
        finding = await finding_service.create(body, x_user_id)
        return created_response(finding.model_dump())
    except Exception as e:
        return error_response(str(e), code="FINDING_CREATE_ERROR")


@router.get("")
async def list_findings(
    assessment_id: str = Query(""),
    page: int = Query(1, ge=1),
    page_size: int = Query(50, ge=1, le=100),
    finding_service: Any = Depends(get_finding_service),
) -> Any:
    result = await finding_service.list_by_assessment(assessment_id, page, page_size)
    return paginated_response(result.data, result.pagination.total, page, page_size)


@router.get("/{finding_id}")
async def get_finding(
    finding_id: str,
    finding_service: Any = Depends(get_finding_service),
) -> Any:
    try:
        finding = await finding_service.get_by_id(finding_id)
        return success_response(finding.model_dump())
    except Exception as e:
        return error_response(str(e), code="FINDING_GET_ERROR")
