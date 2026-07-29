"""Scan management API routes."""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Depends, Query

from backend.application.dto import ScanCreateDTO
from backend.application.services.scan_service import ScanService
from backend.infrastructure.auth_deps import get_current_user_id
from backend.infrastructure.di import get_scan_service
from backend.interfaces.api.responses import (
    created_response,
    error_response,
    paginated_response,
    success_response,
)

router = APIRouter()


@router.post("")
async def create_scan(
    body: ScanCreateDTO,
    user_id: str = Depends(get_current_user_id),
    scan_service: ScanService = Depends(get_scan_service),
) -> Any:
    try:
        scan = await scan_service.create_and_run(body)
        return created_response(scan.model_dump(mode="json"))
    except Exception as e:
        return error_response(str(e), code="SCAN_CREATE_ERROR")


@router.get("")
async def list_scans(
    project_id: str = Query(""),
    page: int = Query(1, ge=1),
    page_size: int = Query(50, ge=1, le=100),
    scan_service: ScanService = Depends(get_scan_service),
) -> Any:
    try:
        scans, total = await scan_service.list_by_project(project_id, page, page_size)
        return paginated_response(
            [s.model_dump(mode="json") for s in scans],
            total,
            page,
            page_size,
        )
    except Exception as e:
        return error_response(str(e), code="SCAN_LIST_ERROR")


@router.get("/{scan_id}")
async def get_scan(
    scan_id: str,
    scan_service: ScanService = Depends(get_scan_service),
) -> Any:
    try:
        scan = await scan_service.get_by_id(scan_id)
        return success_response(scan.model_dump(mode="json"))
    except Exception as e:
        return error_response(str(e), code="SCAN_GET_ERROR")
