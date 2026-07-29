"""Redis client management for caching, sessions, and task queues."""

from __future__ import annotations

import os
from typing import Any

import redis.asyncio as aioredis

_redis: aioredis.Redis | None = None


def get_redis_url() -> str:
    return os.environ.get("REDIS_URL", "redis://localhost:6379/0")


async def create_redis_client() -> aioredis.Redis:
    global _redis

    if _redis is not None:
        return _redis

    _redis = aioredis.from_url(
        get_redis_url(),
        encoding="utf-8",
        decode_responses=True,
        socket_timeout=5,
        socket_connect_timeout=5,
        retry_on_timeout=True,
        health_check_interval=30,
    )
    return _redis


async def get_redis() -> aioredis.Redis:
    if _redis is None:
        return await create_redis_client()
    return _redis


async def close_redis() -> None:
    global _redis
    if _redis:
        await _redis.close()
        _redis = None


class RedisCache:
    """Generic Redis cache with serialization."""

    def __init__(self, prefix: str = "offensec:") -> None:
        self._prefix = prefix
        self._redis = None

    async def _get_client(self) -> aioredis.Redis:
        if self._redis is None:
            self._redis = await get_redis()
        return self._redis

    def _key(self, key: str) -> str:
        return f"{self._prefix}{key}"

    async def get(self, key: str) -> Any:
        client = await self._get_client()
        return await client.get(self._key(key))

    async def set(self, key: str, value: str, ttl: int = 3600) -> None:
        client = await self._get_client()
        await client.setex(self._key(key), ttl, value)

    async def delete(self, key: str) -> None:
        client = await self._get_client()
        await client.delete(self._key(key))

    async def exists(self, key: str) -> bool:
        client = await self._get_client()
        return await client.exists(self._key(key)) > 0


class TokenBlacklist:
    """Redis-backed token blacklist for logout/invalidation."""

    def __init__(self) -> None:
        self._cache = RedisCache(prefix="offensec:token:blacklist:")

    async def blacklist(self, jti: str, ttl: int = 86400) -> None:
        await self._cache.set(jti, "1", ttl=ttl)

    async def is_blacklisted(self, jti: str) -> bool:
        return await self._cache.exists(jti)
