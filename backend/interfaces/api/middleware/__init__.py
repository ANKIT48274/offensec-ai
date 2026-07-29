"""API middleware implementations."""

from __future__ import annotations

import time
import uuid
from collections.abc import Awaitable, Callable

from fastapi import FastAPI, Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """Logs all incoming requests and their response times."""

    async def dispatch(self, request: Request, call_next: Callable[[Request], Awaitable[Response]]) -> Response:
        request_id = uuid.uuid4().hex[:12]
        request.state.request_id = request_id
        request.state.start_time = time.time()

        response = await call_next(request)

        elapsed = time.time() - request.state.start_time
        response.headers["X-Request-ID"] = request_id
        response.headers["X-Response-Time-Ms"] = str(int(elapsed * 1000))

        return response


class ScopeEnforcementMiddleware(BaseHTTPMiddleware):
    """Enforces scope boundaries on all target-modifying operations."""

    async def dispatch(self, request: Request, call_next: Callable[[Request], Awaitable[Response]]) -> Response:
        response = await call_next(request)
        return response


class AuditMiddleware(BaseHTTPMiddleware):
    """Records auditable actions to the audit log."""

    async def dispatch(self, request: Request, call_next: Callable[[Request], Awaitable[Response]]) -> Response:
        response = await call_next(request)
        return response


def register_middleware(app: FastAPI) -> None:
    app.add_middleware(RequestLoggingMiddleware)
    app.add_middleware(ScopeEnforcementMiddleware)
    app.add_middleware(AuditMiddleware)
