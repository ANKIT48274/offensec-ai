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
        payload = token_service.decode_token(token)

        # Reject revoked (logged-out) tokens.
        jti = payload.get("jti")
        if jti:
            blacklist = getattr(request.app.state, "token_blacklist", None)
            if blacklist is not None:
                if await blacklist.is_blacklisted(jti):
                    raise ValueError("Token has been revoked")

        user_id = payload.get("sub")
        if not user_id:
            raise ValueError("Token missing subject claim")
        return user_id
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"},
        )
