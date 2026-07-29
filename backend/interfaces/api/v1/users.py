"""User management API routes."""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Depends, Query

from backend.infrastructure.di import get_user_service
from backend.interfaces.api.responses import error_response, paginated_response, success_response

router = APIRouter()


@router.get("/{user_id}")
async def get_user(
    user_id: str,
    user_service: Any = Depends(get_user_service),
) -> Any:
    try:
        user = await user_service._user_repo.get_by_id(user_id)
        if not user:
            return error_response("User not found", code="NOT_FOUND")
        return success_response(user.model_dump(mode="json"))
    except Exception as e:
        return error_response(str(e), code="USER_ERROR")


@router.get("")
async def list_users(
    page: int = Query(1, ge=1),
    page_size: int = Query(50, ge=1, le=100),
    user_service: Any = Depends(get_user_service),
) -> Any:
    result = await user_service._user_repo.list(page, page_size)
    return paginated_response([d.model_dump(mode="json") for d in result.data], result.pagination.total, page, page_size)
