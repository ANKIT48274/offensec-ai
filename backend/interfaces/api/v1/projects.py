"""Project management API routes."""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Depends, Header, Query

from backend.application.dto import ProjectCreateDTO, ProjectUpdateDTO
from backend.infrastructure.di import get_project_service
from backend.interfaces.api.responses import (
    created_response,
    error_response,
    paginated_response,
    success_response,
)

router = APIRouter()


@router.post("")
async def create_project(
    body: ProjectCreateDTO,
    x_user_id: str = Header(""),
    project_service: Any = Depends(get_project_service),
) -> Any:
    try:
        project = await project_service.create(body, x_user_id)
        return created_response(project.model_dump())
    except Exception as e:
        return error_response(str(e), code="PROJECT_CREATE_ERROR")


@router.get("")
async def list_projects(
    x_user_id: str = Header(""),
    page: int = Query(1, ge=1),
    page_size: int = Query(50, ge=1, le=100),
    project_service: Any = Depends(get_project_service),
) -> Any:
    result = await project_service.list_by_user(x_user_id, page, page_size)
    return paginated_response(result.data, result.pagination.total, page, page_size)


@router.get("/{project_id}")
async def get_project(
    project_id: str,
    x_user_id: str = Header(""),
    project_service: Any = Depends(get_project_service),
) -> Any:
    try:
        project = await project_service.get_by_id(project_id, x_user_id)
        return success_response(project.model_dump())
    except Exception as e:
        return error_response(str(e), code="PROJECT_GET_ERROR")


@router.patch("/{project_id}")
async def update_project(
    project_id: str,
    body: ProjectUpdateDTO,
    x_user_id: str = Header(""),
    project_service: Any = Depends(get_project_service),
) -> Any:
    try:
        project = await project_service.update(project_id, body, x_user_id)
        return success_response(project.model_dump())
    except Exception as e:
        return error_response(str(e), code="PROJECT_UPDATE_ERROR")


@router.delete("/{project_id}")
async def delete_project(
    project_id: str,
    x_user_id: str = Header(""),
    project_service: Any = Depends(get_project_service),
) -> Any:
    try:
        await project_service.delete(project_id, x_user_id)
        return success_response({"deleted": True})
    except Exception as e:
        return error_response(str(e), code="PROJECT_DELETE_ERROR")
