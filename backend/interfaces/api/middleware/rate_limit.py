"""API rate limiting middleware using Redis sliding-window counters.

Limits requests per client IP per fixed window. Falls back to allow-all
when Redis is unavailable so a Redis outage never takes the API down.
"""

from __future__ import annotations

import os
import time
from collections.abc import Awaitable, Callable

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse, Response
from starlette.types import ASGIApp

DEFAULT_RATE_LIMIT = 120  # requests per window
DEFAULT_WINDOW_SECONDS = 60

# Stricter limits for auth endpoints (login/register) to deter brute force.
AUTH_RATE_LIMIT = 10
AUTH_WINDOW_SECONDS = 60

# Config via env: RATE_LIMIT_REQUESTS, RATE_LIMIT_WINDOW_SECONDS, AUTH_RATE_LIMIT_REQUESTS
def _int_env(name: str, default: int) -> int:
    raw = os.environ.get(name, "")
    try:
        return int(raw)
    except ValueError:
        return default


class RateLimitMiddleware(BaseHTTPMiddleware):
    """Enforces per-IP rate limits using Redis INCR + EXPIRE."""

    def __init__(
        self,
        app: ASGIApp,
        requests: int | None = None,
        window_seconds: int | None = None,
        auth_requests: int | None = None,
    ) -> None:
        super().__init__(app)
        self._requests = requests or _int_env("RATE_LIMIT_REQUESTS", DEFAULT_RATE_LIMIT)
        self._window = window_seconds or _int_env("RATE_LIMIT_WINDOW_SECONDS", DEFAULT_WINDOW_SECONDS)
        self._auth_requests = auth_requests or _int_env(
            "AUTH_RATE_LIMIT_REQUESTS", AUTH_RATE_LIMIT
        )
        self._auth_window = _int_env("AUTH_RATE_LIMIT_WINDOW_SECONDS", AUTH_WINDOW_SECONDS)

    def _is_auth_path(self, path: str) -> bool:
        return path.startswith("/api/v1/auth/")

    async def _client_key(self, request: Request) -> str:
        ip = request.client.host if request.client else "unknown"
        forwarded = request.headers.get("x-forwarded-for", "")
        if forwarded:
            ip = forwarded.split(",")[0].strip()
        return ip

    async def dispatch(
        self, request: Request, call_next: Callable[[Request], Awaitable[Response]]
    ) -> Response:
        path = request.url.path

        # Only rate-limit API routes; skip health/static/docs.
        if not path.startswith("/api/"):
            return await call_next(request)

        redis = getattr(request.app.state, "redis", None)
        if redis is None:
            return await call_next(request)

        client = await self._client_key(request)
        window = self._auth_window if self._is_auth_path(path) else self._window
        limit = self._auth_requests if self._is_auth_path(path) else self._requests

        bucket = f"offensec:ratelimit:{client}:{int(time.time()) // window}"

        try:
            count = await redis.incr(bucket)
            if count == 1:
                await redis.expire(bucket, window)
        except Exception:
            # Redis unavailable — fail open to keep the API functional.
            return await call_next(request)

        remaining = max(0, limit - count)
        response: Response = await call_next(request)
        response.headers["X-RateLimit-Limit"] = str(limit)
        response.headers["X-RateLimit-Remaining"] = str(remaining)

        if count > limit:
            retry_after = window - (int(time.time()) % window)
            return JSONResponse(
                status_code=429,
                content={
                    "success": False,
                    "error": {
                        "message": "Rate limit exceeded. Please try again later.",
                        "code": "RATE_LIMITED",
                    },
                },
                headers={
                    "Retry-After": str(retry_after),
                    "X-RateLimit-Limit": str(limit),
                    "X-RateLimit-Remaining": "0",
                },
            )

        return response
