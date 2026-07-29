"""Sandbox runtime — manages plugin lifecycle in isolated environments."""

from __future__ import annotations

from typing import Any


class SandboxRuntime:
    def __init__(self, allowed_capabilities: list[str] | None = None) -> None:
        self._allowed = allowed_capabilities or []
        self._running: dict[str, Any] = {}

    async def start_plugin(self, plugin_name: str, plugin_instance: Any) -> None:
        caps = getattr(plugin_instance, "capabilities", [])
        for cap in caps:
            self._check_capability(cap)
        await plugin_instance.initialize()
        self._running[plugin_name] = plugin_instance

    async def execute_plugin(self, plugin_name: str, context: dict[str, Any]) -> dict[str, Any]:
        plugin = self._running.get(plugin_name)
        if not plugin:
            raise ValueError(f"Plugin '{plugin_name}' is not running")
        return await plugin.execute(context)

    async def stop_plugin(self, plugin_name: str) -> None:
        plugin = self._running.pop(plugin_name, None)
        if plugin:
            await plugin.cleanup()

    def _check_capability(self, capability: str) -> None:
        if self._allowed and capability not in self._allowed:
            raise PermissionError(f"Capability '{capability}' is not allowed")
