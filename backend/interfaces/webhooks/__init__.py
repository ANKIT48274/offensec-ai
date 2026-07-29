"""Webhook handlers for external integrations."""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Request

from backend.interfaces.api.responses import success_response

router = APIRouter()


@router.post("/generic")
async def generic_webhook(request: Request) -> Any:
    payload = await request.json()
    return success_response({"received": True, "payload_type": type(payload).__name__})
