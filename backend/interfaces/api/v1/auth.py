"""Authentication API routes."""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Depends, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from backend.application.dto import UserLoginDTO, UserRegisterDTO
from backend.infrastructure.di import get_user_service
from backend.interfaces.api.responses import created_response, error_response, success_response

router = APIRouter()
security = HTTPBearer()


@router.post("/register")
async def register(
    body: UserRegisterDTO,
    request: Request,
    user_service: Any = Depends(get_user_service),
) -> Any:
    try:
        user = await user_service.register(body, ip=request.client.host if request.client else None)
        return created_response(user.model_dump())
    except Exception as e:
        return error_response(str(e), code=getattr(e, "code", "REGISTRATION_ERROR"))


@router.post("/login")
async def login(
    body: UserLoginDTO,
    request: Request,
    user_service: Any = Depends(get_user_service),
) -> Any:
    try:
        access_token, refresh_token = await user_service.authenticate(
            body.email, body.password,
            ip=request.client.host if request.client else None,
        )
        return success_response({
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
            "expires_in": 3600,
        })
    except Exception:
        return error_response("Invalid credentials", code="AUTHENTICATION_ERROR")


@router.get("/me")
async def me(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> Any:
    return success_response({"message": "Authenticated"})
