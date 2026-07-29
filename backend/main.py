"""
OffenSec AI — Backend Application Entry Point
"""

from __future__ import annotations

import os
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.infrastructure.ai_client import create_ai_client
from backend.infrastructure.auth import JWTService
from backend.infrastructure.logging import configure_logging, get_logger
from backend.infrastructure.password_hasher import BcryptHasher
from backend.infrastructure.persistence.postgres import create_session_factory, init_models
from backend.infrastructure.persistence.redis import create_redis_client
from backend.interfaces.api.middleware import register_middleware
from backend.interfaces.api.responses import health_response
from backend.interfaces.api.v1.router import api_v1_router
from backend.interfaces.api.ws import websocket_handler


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    configure_logging()
    logger = get_logger("startup")
    logger.info("Initializing OffenSec AI API")

    factory = create_session_factory()
    app.state.db_session_factory = factory
    app.state.redis = await create_redis_client()

    try:
        await init_models()
        logger.info("Database tables initialized")
    except Exception as e:
        logger.warning("Database init skipped (connect to PostgreSQL first): %s", e)

    app.state.password_hasher = BcryptHasher()
    app.state.token_service = JWTService()
    app.state.ai_client = create_ai_client()

    app.state.event_bus = _create_noop_event_bus()
    app.state.audit_logger = _create_noop_audit_logger()
    app.state.scope_validator = None
    app.state.cache = None

    logger.info("Application startup complete")
    yield
    logger.info("Shutting down")
    if app.state.redis:
        await app.state.redis.aclose()


class _NoopEventBus:
    async def publish(self, event: object) -> None:
        pass

    async def subscribe(self, event_type: type, handler: object) -> None:
        pass


class _NoopAuditLogger:
    async def log(self, actor_id: str, action: str, resource_type: str, resource_id: str, details: dict | None = None, ip_address: str | None = None) -> None:
        pass


def _create_noop_event_bus() -> _NoopEventBus:
    return _NoopEventBus()


def _create_noop_audit_logger() -> _NoopAuditLogger:
    return _NoopAuditLogger()


app = FastAPI(
    title="OffenSec AI API",
    version="0.1.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

origins = os.environ.get("CORS_ORIGINS", "")
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins.split(",") if origins else [],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

register_middleware(app)
app.include_router(api_v1_router, prefix="/api/v1")


@app.get("/health")
async def health():
    return health_response()


@app.websocket("/ws")
async def ws(websocket):
    await websocket_handler(websocket)
