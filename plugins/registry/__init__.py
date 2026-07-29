"""Plugin registry — manages plugin metadata, indexing, and verification."""

from __future__ import annotations

from datetime import UTC, datetime, timezone
from typing import Any


class PluginMetadata:
    def __init__(
        self,
        name: str,
        version: str,
        description: str,
        author: str,
        capabilities: list[str],
        signature: str | None = None,
    ) -> None:
        self.name = name
        self.version = version
        self.description = description
        self.author = author
        self.capabilities = capabilities
        self.signature = signature
        self.installed_at = datetime.now(UTC)


class PluginRegistry:
    def __init__(self) -> None:
        self._plugins: dict[str, PluginMetadata] = {}

    def register(self, plugin: PluginMetadata) -> None:
        self._plugins[plugin.name] = plugin

    def unregister(self, name: str) -> None:
        self._plugins.pop(name, None)

    def get(self, name: str) -> PluginMetadata | None:
        return self._plugins.get(name)

    def list(self) -> list[PluginMetadata]:
        return list(self._plugins.values())

    def get_by_capability(self, capability: str) -> list[PluginMetadata]:
        return [p for p in self._plugins.values() if capability in p.capabilities]
