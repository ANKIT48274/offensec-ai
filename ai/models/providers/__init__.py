"""AI model provider implementations."""

from __future__ import annotations

from typing import Any


class ModelProvider:
    name: str = ""
    async def complete(self, prompt: str, options: dict[str, Any] | None = None) -> str:
        raise NotImplementedError


class LocalModelProvider(ModelProvider):
    name = "local"
    async def complete(self, prompt: str, options: dict[str, Any] | None = None) -> str:
        return ""

    def format_messages(self, system: str, user: str) -> list[dict[str, str]]:
        return [{"role": "system", "content": system}, {"role": "user", "content": user}]


class OpenAIProvider(ModelProvider):
    name = "openai"
    async def complete(self, prompt: str, options: dict[str, Any] | None = None) -> str:
        return ""

    def format_messages(self, system: str, user: str) -> list[dict[str, str]]:
        return [{"role": "system", "content": system}, {"role": "user", "content": user}]


class AnthropicProvider(ModelProvider):
    name = "anthropic"
    async def complete(self, prompt: str, options: dict[str, Any] | None = None) -> str:
        return ""

    def format_messages(self, system: str, user: str) -> list[dict[str, str]]:
        return [{"role": "user", "content": user}]
