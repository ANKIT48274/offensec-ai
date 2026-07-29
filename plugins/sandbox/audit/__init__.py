"""Sandbox audit logger — records all plugin actions for security review."""

from __future__ import annotations

from datetime import UTC, datetime, timezone
from typing import Any


class SandboxAuditLog:
    def __init__(self) -> None:
        self._entries: list[dict[str, Any]] = []

    def record(self, plugin_name: str, action: str, details: dict[str, Any] | None = None) -> None:
        self._entries.append({
            "plugin": plugin_name,
            "action": action,
            "details": details or {},
            "timestamp": datetime.now(UTC).isoformat(),
        })

    def get_entries(self, plugin_name: str | None = None) -> list[dict[str, Any]]:
        if plugin_name:
            return [e for e in self._entries if e["plugin"] == plugin_name]
        return list(self._entries)
