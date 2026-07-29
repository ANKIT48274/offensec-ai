"""Nuclei results API routes."""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Depends, Query

from backend.application.services.nuclei_service import NucleiResultsService
from backend.infrastructure.di import get_nuclei_service
from backend.interfaces.api.responses import (
    error_response,
    paginated_response,
    success_response,
)

router = APIRouter()


@router.get("/results")
async def list_nuclei_results(
    project_id: str = Query(""),
    severity: str | None = Query(None),
    search: str | None = Query(None),
    page: int = Query(1, ge=1),
    page_size: int = Query(50, ge=1, le=100),
    nuclei_service: NucleiResultsService = Depends(get_nuclei_service),
) -> Any:
    try:
        rows, total = await nuclei_service.list_by_project(
            project_id, page, page_size, severity, search
        )
        return paginated_response(
            [_model_to_dict(r) for r in rows],
            total,
            page,
            page_size,
        )
    except Exception as e:
        return error_response(str(e), code="NUCLEI_LIST_ERROR")


@router.get("/results/{result_id}")
async def get_nuclei_result(
    result_id: str,
    nuclei_service: NucleiResultsService = Depends(get_nuclei_service),
) -> Any:
    try:
        row = await nuclei_service.get_by_id(result_id)
        if not row:
            return error_response("Not found", code="NOT_FOUND")
        return success_response(_model_to_dict(row))
    except Exception as e:
        return error_response(str(e), code="NUCLEI_GET_ERROR")


@router.get("/stats")
async def nuclei_stats(
    project_id: str = Query(""),
    nuclei_service: NucleiResultsService = Depends(get_nuclei_service),
) -> Any:
    try:
        counts = await nuclei_service.severity_counts(project_id)
        return success_response(counts)
    except Exception as e:
        return error_response(str(e), code="NUCLEI_STATS_ERROR")


def _model_to_dict(m: Any) -> dict[str, Any]:
    return {
        "id": m.id,
        "job_id": m.job_id,
        "project_id": m.project_id,
        "target": m.target,
        "template_id": m.template_id,
        "template_name": m.template_name,
        "severity": m.severity,
        "matched_url": m.matched_url,
        "matched_at": m.matched_at,
        "protocol": m.protocol,
        "tags": m.tags or [],
        "ref_url": m.ref_url,
        "cwe_ids": m.cwe_ids or [],
        "cve_ids": m.cve_ids or [],
        "cvss_score": m.cvss_score,
        "description": m.description,
        "remediation": m.remediation,
        "created_at": m.created_at.isoformat() if m.created_at else None,
    }
