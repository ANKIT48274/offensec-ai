"""Report generation API routes."""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Depends

from backend.application.dto import ReportGenerateDTO
from backend.infrastructure.di import get_report_generator_service
from backend.interfaces.api.responses import error_response, success_response

router = APIRouter()


@router.post("/generate")
async def generate_report(
    body: ReportGenerateDTO,
    report_service: Any = Depends(get_report_generator_service),
) -> Any:
    try:
        report = await report_service.execute(body)
        return success_response({"content": report})
    except Exception as e:
        return error_response(str(e), code="REPORT_GENERATE_ERROR")
