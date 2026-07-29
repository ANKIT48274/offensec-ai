"""AI analysis API routes — correlation and reporting."""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Depends, Header, Query

from backend.infrastructure.di import get_correlation_service
from backend.interfaces.api.responses import (
    created_response,
    error_response,
    success_response,
)

router = APIRouter()


@router.post("/analyze")
async def run_ai_analysis(
    project_id: str = Query(""),
    force: bool = Query(False),
    correlation_service: Any = Depends(get_correlation_service),
) -> Any:
    try:
        result = await correlation_service.analyze(project_id)
        return created_response(result)
    except Exception as e:
        return error_response(str(e), code="AI_ANALYSIS_ERROR")


@router.get("/report/{project_id}")
async def get_ai_report(
    project_id: str,
    correlation_service: Any = Depends(get_correlation_service),
) -> Any:
    try:
        report = await correlation_service.get_report(project_id)
        if not report:
            return success_response({"message": "No analysis available. Run /ai/analyze first."})
        return success_response(report)
    except Exception as e:
        return error_response(str(e), code="AI_REPORT_ERROR")


@router.get("/attack-paths/{project_id}")
async def get_attack_paths(
    project_id: str,
    correlation_service: Any = Depends(get_correlation_service),
) -> Any:
    try:
        paths = await correlation_service.get_attack_paths(project_id)
        return success_response(paths)
    except Exception as e:
        return error_response(str(e), code="ATTACK_PATH_ERROR")
