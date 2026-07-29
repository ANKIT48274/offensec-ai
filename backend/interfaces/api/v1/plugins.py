"""Plugin management API routes."""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter

from backend.interfaces.api.responses import success_response

router = APIRouter()


@router.get("")
async def list_plugins() -> Any:
    return success_response([])


@router.get("/{plugin_id}")
async def get_plugin(plugin_id: str) -> Any:
    return success_response({"id": plugin_id, "name": "", "version": "", "enabled": False})


@router.post("/{plugin_id}/enable")
async def enable_plugin(plugin_id: str) -> Any:
    return success_response({"id": plugin_id, "enabled": True})


@router.post("/{plugin_id}/disable")
async def disable_plugin(plugin_id: str) -> Any:
    return success_response({"id": plugin_id, "enabled": False})
