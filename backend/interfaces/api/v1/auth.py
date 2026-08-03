"""Authentication API routes."""

from __future__ import annotations

import time
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Request

from backend.application.dto import UserLoginDTO, UserRegisterDTO
from backend.infrastructure.auth_deps import get_current_user_id
from backend.infrastructure.auth import JWTService
from backend.infrastructure.di import get_user_service
from backend.interfaces.api.responses import created_response, error_response, success_response

router = APIRouter()


@router.post("/register")
async def register(
    body: UserRegisterDTO,
    request: Request,
    user_service: Any = Depends(get_user_service),
) -> Any:
    try:
        user = await user_service.register(body, ip=request.client.host if request.client else None)
        return created_response(user.to_safe_dict())
    except Exception as e:
        return error_response(str(e), code=getattr(e, "code", "REGISTRATION_ERROR"))


@router.post("/login")
async def login(
    body: UserLoginDTO,
    request: Request,
    user_service: Any = Depends(get_user_service),
) -> Any:
    try:
        access_token, refresh_token, user_id = await user_service.authenticate(
            body.email,
            body.password,
            ip=request.client.host if request.client else None,
        )
        return success_response(
            {
                "access_token": access_token,
                "refresh_token": refresh_token,
                "user_id": user_id,
                "token_type": "bearer",
                "expires_in": 3600,
            }
        )
    except Exception as e:
        return error_response(f"Authentication failed: {e}", code="AUTHENTICATION_ERROR")


@router.get("/me")
async def me(
    user_id: str = Depends(get_current_user_id),
    user_service: Any = Depends(get_user_service),
) -> Any:
    try:
        user = await user_service.get_by_id(user_id)
        return success_response(user.to_safe_dict())
    except Exception as e:
        return error_response(str(e), code="USER_GET_ERROR")


@router.post("/logout")
async def logout(request: Request) -> Any:
    """Revoke the presented bearer token so it can no longer be used."""
    auth_header = request.headers.get("authorization", "")
    if not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing bearer token")

    token = auth_header[7:]

    try:
        token_service: JWTService = request.app.state.token_service
        blacklist = request.app.state.token_blacklist

        payload = token_service.decode_token(token)
        jti = payload.get("jti")
        if jti and blacklist is not None:
            exp = payload.get("exp")
            ttl = max(int(exp) - int(time.time()), 1) if exp else 86400
            await blacklist.blacklist(jti, ttl=ttl)
        return success_response({"message": "Logged out successfully"})
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))
