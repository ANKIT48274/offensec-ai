"""Evidence API routes."""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Depends, Query

from backend.infrastructure.di import get_asset_service
from backend.interfaces.api.responses import (
    error_response,
    paginated_response,
    success_response,
)

router = APIRouter()


@router.get("")
async def list_evidence(
    project_id: str = Query(""),
    source: str | None = Query(None),
    page: int = Query(1, ge=1),
    page_size: int = Query(50, ge=1, le=100),
    asset_service: Any = Depends(get_asset_service),
) -> Any:
    try:
        items, total = await asset_service.evidence_list(project_id, page, page_size, source)
        return paginated_response(items, total, page, page_size)
    except Exception as e:
        return error_response(str(e), code="EVIDENCE_LIST_ERROR")


@router.get("/{evidence_id}")
async def get_evidence(
    evidence_id: str,
    asset_service: Any = Depends(get_asset_service),
) -> Any:
    try:
        item = await asset_service.evidence_get(evidence_id)
        if not item:
            return error_response("Not found", code="NOT_FOUND")
        return success_response(item)
    except Exception as e:
        return error_response(str(e), code="EVIDENCE_GET_ERROR")
