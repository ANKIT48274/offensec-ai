"""PostgreSQL database session management."""

from __future__ import annotations

import os
from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


_engine = None
_session_factory = None


def get_database_url() -> str:
    return os.environ.get(
        "DATABASE_URL",
        "postgresql+asyncpg://offensec:changeme@localhost:5432/offensec",
    )


def create_session_factory() -> async_sessionmaker[AsyncSession]:
    global _engine, _session_factory

    if _session_factory is not None:
        return _session_factory

    _engine = create_async_engine(
        get_database_url(),
        pool_size=10,
        max_overflow=20,
        pool_pre_ping=True,
        pool_recycle=3600,
        echo=False,
    )

    _session_factory = async_sessionmaker(
        bind=_engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )
    return _session_factory


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    factory = create_session_factory()
    async with factory() as session:
        yield session


async def init_models() -> None:
    from backend.infrastructure.persistence.postgres.models import (  # noqa: F401
        AIPlanModel,
        AssessmentModel,
        AuditLogModel,
        EvidenceModel,
        FindingModel,
        PluginModel,
        ProjectModel,
        ReportModel,
        TargetModel,
        UserModel,
    )

    async with _engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
