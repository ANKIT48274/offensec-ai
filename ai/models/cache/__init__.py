"""Model response cache — reduces redundant inference calls."""

from __future__ import annotations

import hashlib
import json
from typing import Any

from backend.infrastructure.persistence.redis import RedisCache


class ModelCache:
    def __init__(self, ttl: int = 3600) -> None:
        self._cache = RedisCache(prefix="offensec:model:")
        self._ttl = ttl

    def _make_key(self, prompt: str, context: dict[str, Any] | None = None) -> str:
        data = {"prompt": prompt, "context": context or {}}
        raw = json.dumps(data, sort_keys=True)
        return hashlib.sha256(raw.encode()).hexdigest()[:32]

    async def get(self, prompt: str, context: dict[str, Any] | None = None) -> str | None:
        key = self._make_key(prompt, context)
        return await self._cache.get(key)

    async def set(self, prompt: str, response: str, context: dict[str, Any] | None = None) -> None:
        key = self._make_key(prompt, context)
        await self._cache.set(key, response, ttl=self._ttl)
