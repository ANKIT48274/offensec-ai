"""Plugin loader — discovers, validates, and loads plugins from filesystem."""

from __future__ import annotations

import importlib
import importlib.util
import os
import sys
from pathlib import Path
from typing import Any

PLUGIN_DIRS = [
    "/opt/offensec/plugins",
    os.path.expanduser("~/.offensec/plugins"),
]


class PluginManifest:
    def __init__(self, name: str, version: str, description: str, author: str, entry_point: str, capabilities: list[str] | None = None) -> None:
        self.name = name
        self.version = version
        self.description = description
        self.author = author
        self.entry_point = entry_point
        self.capabilities = capabilities or []


class PluginLoader:
    def __init__(self) -> None:
        self._plugins: dict[str, Any] = {}
        self._manifests: dict[str, PluginManifest] = {}

    def discover(self, extra_dirs: list[str] | None = None) -> list[PluginManifest]:
        manifests: list[PluginManifest] = []
        search_dirs = list(PLUGIN_DIRS) + (extra_dirs or [])
        for plugin_dir in search_dirs:
            path = Path(plugin_dir)
            if not path.exists():
                continue
            for subdir in path.iterdir():
                if not subdir.is_dir():
                    continue
                manifest_path = subdir / "manifest.json"
                if not manifest_path.exists():
                    continue
                try:
                    import json
                    data = json.loads(manifest_path.read_text())
                    manifest = PluginManifest(
                        name=data.get("name", subdir.name),
                        version=data.get("version", "0.1.0"),
                        description=data.get("description", ""),
                        author=data.get("author", "Unknown"),
                        entry_point=data.get("entry_point", "main.py"),
                        capabilities=data.get("capabilities", []),
                    )
                    self._manifests[manifest.name] = manifest
                    manifests.append(manifest)
                except (json.JSONDecodeError, KeyError):
                    continue
        return manifests

    def load(self, name: str) -> Any | None:
        if name in self._plugins:
            return self._plugins[name]

        manifest = self._manifests.get(name)
        if not manifest:
            return None

        search_dirs = list(PLUGIN_DIRS)
        for plugin_dir in search_dirs:
            plugin_path = Path(plugin_dir) / name / manifest.entry_point
            if plugin_path.exists():
                spec = importlib.util.spec_from_file_location(f"offensec_plugin_{name}", plugin_path)
                if spec and spec.loader:
                    module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(module)
                    self._plugins[name] = module
                    return module
        return None

    def list_loaded(self) -> list[tuple[str, str]]:
        return [(name, self._manifests[name].version if name in self._manifests else "?") for name in self._plugins]
