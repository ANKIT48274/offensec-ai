# Plugin Development Guide

## Overview

OffenSec AI supports plugins for extending scan capabilities, adding custom tools, and integrating third-party services. Plugins are loaded from the filesystem and discovered via manifest files.

## Plugin Structure

```
/opt/offensec/plugins/my-plugin/
├── manifest.json
└── main.py
```

### manifest.json

```json
{
    "name": "my-plugin",
    "version": "1.0.0",
    "description": "Custom vulnerability scanner",
    "author": "Your Name",
    "entry_point": "main.py",
    "capabilities": ["scan", "report"]
}
```

### Capability Types

| Capability | Description |
|------------|-------------|
| `scan` | Adds a new scan engine |
| `report` | Adds a new report format |
| `tool` | Integrates an external tool |
| `methodology` | Adds assessment methodology |

## API Reference

### Plugin Registration

```python
# main.py
def register(api):
    api.register_scan_engine("my_scan", MyScanEngine())
```

### Available Hooks

| Hook | Parameters | Description |
|------|------------|-------------|
| `on_scan_start` | `target: str` | Called when a scan begins |
| `on_scan_complete` | `results: dict` | Called when a scan finishes |
| `on_finding_created` | `finding: dict` | Called when a finding is created |
| `on_report_generate` | `findings: list` | Called during report generation |

## Installation

```bash
# User plugins
mkdir -p ~/.offensec/plugins
cp -r my-plugin ~/.offensec/plugins/

# System plugins
sudo mkdir -p /opt/offensec/plugins
sudo cp -r my-plugin /opt/offensec/plugins/
```

## Testing

```python
# test_my_plugin.py
from offensec.plugins import PluginLoader

def test_discovery():
    loader = PluginLoader()
    manifests = loader.discover(["/path/to/plugins"])
    assert any(m.name == "my-plugin" for m in manifests)
```
