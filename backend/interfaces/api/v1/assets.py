"""Asset and Evidence API routes."""

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
async def list_assets(
    project_id: str = Query(""),
    asset_type: str | None = Query(None),
    search: str | None = Query(None),
    page: int = Query(1, ge=1),
    page_size: int = Query(50, ge=1, le=100),
    asset_service: Any = Depends(get_asset_service),
) -> Any:
    try:
        assets, total = await asset_service.list_by_project(
            project_id, page, page_size, asset_type, search
        )
        return paginated_response(assets, total, page, page_size)
    except Exception as e:
        return error_response(str(e), code="ASSET_LIST_ERROR")


@router.get("/{asset_id}")
async def get_asset(
    asset_id: str,
    asset_service: Any = Depends(get_asset_service),
) -> Any:
    try:
        asset = await asset_service.get_by_id(asset_id)
        if not asset:
            return error_response("Not found", code="NOT_FOUND")
        return success_response(asset)
    except Exception as e:
        return error_response(str(e), code="ASSET_GET_ERROR")
