"""Model capability negotiation — queries providers for supported features."""

from __future__ import annotations

from typing import Any


class CapabilityRegistry:
    def __init__(self) -> None:
        self._capabilities: dict[str, list[str]] = {}

    def register(self, provider: str, capabilities: list[str]) -> None:
        self._capabilities[provider] = capabilities

    def supports(self, provider: str, capability: str) -> bool:
        caps = self._capabilities.get(provider, [])
        return capability in caps

    def select_providers(self, required_capability: str) -> list[str]:
        return [p for p, caps in self._capabilities.items() if required_capability in caps]
