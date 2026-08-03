"""End-to-end smoke tests against a running backend stack.

These tests exercise the full user journey: register → login → project →
assessment → finding → report → logout/revocation. They require a running
backend on ``BACKEND_URL`` (default http://localhost:8000).

Run with:
    BACKEND_URL=http://localhost:8000 pytest tests/e2e -v
"""

from __future__ import annotations

import os
import time
import uuid
from typing import Any

import httpx
import pytest

BACKEND_URL = os.environ.get("BACKEND_URL", "http://localhost:8000")
API = f"{BACKEND_URL}/api/v1"

pytestmark = pytest.mark.e2e


def _unique(prefix: str) -> str:
    return f"{prefix}-{uuid.uuid4().hex[:8]}"


def _client() -> httpx.Client:
    return httpx.Client(base_url=API, timeout=60.0)


def _fwd_ip() -> dict[str, str]:
    """Return a unique X-Forwarded-For header so the rate limiter treats
    each test as a distinct client. Keeps the suite repeatable."""
    return {"X-Forwarded-For": f"198.51.100.{int(uuid.uuid4().int % 250) + 1}"}


@pytest.fixture(scope="module")
def client() -> httpx.Client:
    with _client() as c:
        yield c


@pytest.fixture(scope="module")
def auth(client: httpx.Client) -> dict[str, Any]:
    """Register a fresh user and return auth tokens."""
    email = f"{_unique('e2e')}@test.com"
    username = _unique("e2euser")
    password = "E2EPass!12345"
    fwd = _fwd_ip()

    r = client.post(
        "/auth/register",
        headers=fwd,
        json={"email": email, "username": username, "password": password},
    )
    assert r.status_code in (200, 201), f"register failed: {r.text}"
    assert r.json()["success"] is True

    # Register response must NOT leak the password hash.
    assert "password_hash" not in r.json()["data"], "password_hash leaked in register response"

    r = client.post("/auth/login", headers=fwd, json={"email": email, "password": password})
    assert r.status_code == 200, f"login failed: {r.text}"
    data = r.json()["data"]
    assert data["access_token"] and data["refresh_token"]

    return {"email": email, "password": password, **data}


@pytest.fixture()
def headers(auth: dict[str, Any]) -> dict[str, str]:
    return {"Authorization": f"Bearer {auth['access_token']}"}


def test_health(client: httpx.Client) -> None:
    r = client.get(f"{BACKEND_URL}/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"


def test_me_returns_safe_user(
    client: httpx.Client, auth: dict[str, Any], headers: dict[str, str]
) -> None:
    r = client.get("/auth/me", headers=headers)
    assert r.status_code == 200
    assert r.json()["data"]["email"] == auth["email"]
    assert "password_hash" not in r.json()["data"], "password_hash leaked in /me"


def test_project_crud(client: httpx.Client, headers: dict[str, str]) -> None:
    r = client.post(
        "/projects",
        headers=headers,
        json={"name": _unique("e2e-project"), "description": "E2E smoke test"},
    )
    assert r.status_code == 201, f"project create failed: {r.text}"
    project_id = r.json()["data"]["id"]

    r = client.get("/projects", headers=headers)
    assert r.status_code == 200
    assert any(p["id"] == project_id for p in r.json()["data"])

    r = client.get(f"/projects/{project_id}", headers=headers)
    assert r.status_code == 200
    assert r.json()["data"]["id"] == project_id


def test_assessment_lifecycle(client: httpx.Client, headers: dict[str, str]) -> None:
    project_id = client.post(
        "/projects", headers=headers, json={"name": _unique("proj")}
    ).json()["data"]["id"]

    r = client.post(
        "/assessments",
        headers=headers,
        json={"project_id": project_id, "name": _unique("assessment")},
    )
    assert r.status_code == 201, f"assessment create failed: {r.text}"
    assessment_id = r.json()["data"]["id"]

    r = client.post(f"/assessments/{assessment_id}/start", headers=headers)
    assert r.status_code == 200, f"assessment start failed: {r.text}"

    r = client.post(
        "/findings",
        headers=headers,
        json={
            "assessment_id": assessment_id,
            "title": _unique("e2e-finding"),
            "severity": "medium",
        },
    )
    assert r.status_code == 201, f"finding create failed: {r.text}"

    r = client.post(f"/assessments/{assessment_id}/complete", headers=headers)
    assert r.status_code == 200, f"assessment complete failed: {r.text}"

    # Generate a report.
    r = client.post(
        "/reports/generate",
        headers=headers,
        json={"assessment_id": assessment_id},
    )
    assert r.status_code == 200, f"report generation failed: {r.text}"
    assert r.json()["data"]


def test_dashboard(client: httpx.Client, headers: dict[str, str]) -> None:
    r = client.get("/dashboard/overview", headers=headers)
    assert r.status_code == 200
    assert r.json()["data"]["total_findings"] >= 0


def test_unauthorized_rejected(client: httpx.Client) -> None:
    r = client.get("/projects")
    assert r.status_code == 401, "unauthenticated request should be rejected"


def test_logout_revokes_token(client: httpx.Client, auth: dict[str, Any]) -> None:
    fwd = _fwd_ip()
    headers = {"Authorization": f"Bearer {auth['access_token']}", **_fwd_ip()}

    r = client.post("/auth/logout", headers={**headers, **fwd})
    assert r.status_code == 200, f"logout failed: {r.text}"

    # Revoked token must now be rejected.
    r = client.get("/projects", headers=headers)
    assert r.status_code == 401, "revoked token should be rejected after logout"
