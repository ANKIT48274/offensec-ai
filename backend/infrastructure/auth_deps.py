"""Authentication dependencies for FastAPI routes."""

from __future__ import annotations

from fastapi import Depends, HTTPException, Request, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from backend.infrastructure.auth import JWTService

_security = HTTPBearer(auto_error=False)


def get_token_service(request: Request) -> JWTService:
    return request.app.state.token_service


async def get_current_user_id(
    request: Request,
    credentials: HTTPAuthorizationCredentials | None = Depends(_security),
) -> str:
    auth_header = request.headers.get("authorization", "")
    if auth_header.startswith("Bearer "):
        token = auth_header[7:]
    elif credentials:
        token = credentials.credentials
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required. Provide a Bearer token in the Authorization header.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    try:
        token_service: JWTService = request.app.state.token_service
        user_id = token_service.get_user_id_from_token(token)
        return user_id
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"},
        )
