"""JWT authentication service and dependency."""

from __future__ import annotations

import os
from datetime import UTC, datetime, timedelta
from typing import Any

import jwt

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60
REFRESH_TOKEN_EXPIRE_DAYS = 7


def get_jwt_secret() -> str:
    secret = os.environ.get("JWT_SECRET")
    if not secret:
        raise RuntimeError(
            "JWT_SECRET environment variable is not set. "
            "Set a secure random string (minimum 32 characters) before starting the application. "
            "Example: python3 -c 'import secrets; print(secrets.token_hex(32))'"
        )
    return secret


def get_jwt_algorithm() -> str:
    return os.environ.get("JWT_ALGORITHM", ALGORITHM)


class JWTService:
    """JWT token creation and verification."""

    def __init__(self, secret: str | None = None, algorithm: str | None = None) -> None:
        self._secret = secret or get_jwt_secret()
        self._algorithm = algorithm or get_jwt_algorithm()

    def create_access_token(self, user_id: str, extra_claims: dict[str, Any] | None = None) -> str:
        now = datetime.now(UTC)
        payload: dict[str, Any] = {
            "sub": user_id,
            "iat": now,
            "exp": now + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
            "type": "access",
        }
        if extra_claims:
            payload.update(extra_claims)
        return jwt.encode(payload, self._secret, algorithm=self._algorithm)

    def create_refresh_token(self, user_id: str) -> str:
        now = datetime.now(UTC)
        payload: dict[str, Any] = {
            "sub": user_id,
            "iat": now,
            "exp": now + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS),
            "type": "refresh",
        }
        return jwt.encode(payload, self._secret, algorithm=self._algorithm)

    def decode_token(self, token: str) -> dict[str, Any]:
        try:
            payload = jwt.decode(token, self._secret, algorithms=[self._algorithm])
            return payload
        except jwt.ExpiredSignatureError:
            raise ValueError("Token has expired")
        except jwt.InvalidTokenError as e:
            raise ValueError(f"Invalid token: {e}")

    def get_user_id_from_token(self, token: str) -> str:
        payload = self.decode_token(token)
        user_id = payload.get("sub")
        if not user_id:
            raise ValueError("Token missing subject claim")
        return user_id
