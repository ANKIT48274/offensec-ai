"""Tests for dashboard API."""

from backend.interfaces.api.v1.dashboard import router

def test_router_exists():
    routes = [r.path for r in router.routes]
    assert "/overview" in routes
    assert "/findings-trend" in routes
    assert "/asset-graph" in routes
