"""Standard API response helpers."""

from __future__ import annotations

from typing import Any

from fastapi import status
from fastapi.responses import JSONResponse


def success_response(data: Any, status_code: int = status.HTTP_200_OK) -> JSONResponse:
    return JSONResponse(
        status_code=status_code,
        content={
            "success": True,
            "data": data,
        },
    )


def created_response(data: Any) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content={
            "success": True,
            "data": data,
        },
    )


def error_response(
    message: str,
    status_code: int = status.HTTP_400_BAD_REQUEST,
    code: str | None = None,
    details: Any = None,
) -> JSONResponse:
    content: dict[str, Any] = {
        "success": False,
        "error": {
            "message": message,
            "code": code or "ERROR",
        },
    }
    if details:
        content["error"]["details"] = details
    return JSONResponse(status_code=status_code, content=content)


def paginated_response(data: list[Any], total: int, page: int, page_size: int) -> JSONResponse:
    return JSONResponse(
        content={
            "success": True,
            "data": data,
            "pagination": {
                "page": page,
                "page_size": page_size,
                "total": total,
                "total_pages": (total + page_size - 1) // page_size if page_size > 0 else 0,
            },
        },
    )


def health_response() -> JSONResponse:
    return JSONResponse(
        content={
            "status": "ok",
            "version": "0.1.0",
        }
    )
