"""Pipeline API routes — manage multi-tool scan pipelines."""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Depends, Header, Query

from backend.application.dto import PipelineStartDTO
from backend.infrastructure.di import get_pipeline_service
from backend.interfaces.api.responses import (
    created_response,
    error_response,
    paginated_response,
    success_response,
)
from backend.application.services.pipeline_service import PipelineService

router = APIRouter()


@router.post("/start")
async def start_pipeline(
    body: PipelineStartDTO,
    x_user_id: str | None = Header(default=None),
    pipeline_service: PipelineService = Depends(get_pipeline_service),
) -> Any:
    try:
        job = await pipeline_service.start(body)
        return created_response(job.model_dump(mode="json"))
    except Exception as e:
        return error_response(str(e), code="PIPELINE_START_ERROR")


@router.get("/jobs")
async def list_jobs(
    project_id: str = Query(""),
    page: int = Query(1, ge=1),
    page_size: int = Query(50, ge=1, le=100),
    pipeline_service: PipelineService = Depends(get_pipeline_service),
) -> Any:
    try:
        jobs, total = await pipeline_service.list_by_project(project_id, page, page_size)
        return paginated_response(
            [j.model_dump(mode="json") for j in jobs],
            total,
            page,
            page_size,
        )
    except Exception as e:
        return error_response(str(e), code="PIPELINE_LIST_ERROR")


@router.get("/jobs/{job_id}")
async def get_job(
    job_id: str,
    pipeline_service: PipelineService = Depends(get_pipeline_service),
) -> Any:
    try:
        job = await pipeline_service.get_by_id(job_id)
        return success_response(job.model_dump(mode="json"))
    except Exception as e:
        return error_response(str(e), code="PIPELINE_GET_ERROR")
