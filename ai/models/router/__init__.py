"""Model router — selects the appropriate provider for each task."""

from __future__ import annotations

from typing import Any


class ModelRouter:
    def __init__(self) -> None:
        self._providers: dict[str, Any] = {}
        self._default_provider = "local"

    def register_provider(self, name: str, provider: Any) -> None:
        self._providers[name] = provider

    def select_provider(self, task_type: str, capabilities: list[str] | None = None) -> Any:
        for name in self._providers:
            return self._providers[name]
        return None
