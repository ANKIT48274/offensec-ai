"""Tests for plugin loader."""

import tempfile
from pathlib import Path

from backend.infrastructure.plugins.loader import PluginLoader, PluginManifest


def test_manifest_creation():
    m = PluginManifest("test", "1.0", "A test plugin", "Tester", "run.py", ["scan"])
    assert m.name == "test"
    assert "scan" in m.capabilities


def test_discover_empty_dir():
    with tempfile.TemporaryDirectory() as tmp:
        loader = PluginLoader()
        manifests = loader.discover([tmp])
        assert len(manifests) == 0


def test_discover_with_manifest():
    with tempfile.TemporaryDirectory() as tmp:
        plugin_dir = Path(tmp) / "test_plugin"
        plugin_dir.mkdir()
        (plugin_dir / "manifest.json").write_text(
            '{"name": "test_plugin", "version": "1.0", "description": "desc", "author": "auth", "entry_point": "main.py"}'
        )
        (plugin_dir / "main.py").write_text("def run(): pass")
        manifests = PluginLoader().discover([tmp])
        assert len(manifests) == 1
        assert manifests[0].name == "test_plugin"


def test_load_nonexistent():
    loader = PluginLoader()
    assert loader.load("nonexistent") is None


def test_list_loaded_empty():
    loader = PluginLoader()
    assert loader.list_loaded() == []
