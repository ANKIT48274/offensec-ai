"""WebSocket handler for real-time assessment updates."""

from __future__ import annotations

import json
from typing import Any

from fastapi import WebSocket, WebSocketDisconnect


class ConnectionManager:
    """Manages WebSocket connections for real-time communication."""

    def __init__(self) -> None:
        self._connections: dict[str, set[WebSocket]] = {}

    async def connect(self, assessment_id: str, websocket: WebSocket) -> None:
        await websocket.accept()
        if assessment_id not in self._connections:
            self._connections[assessment_id] = set()
        self._connections[assessment_id].add(websocket)

    def disconnect(self, assessment_id: str, websocket: WebSocket) -> None:
        if assessment_id in self._connections:
            self._connections[assessment_id].discard(websocket)
            if not self._connections[assessment_id]:
                del self._connections[assessment_id]

    async def broadcast(self, assessment_id: str, event: dict[str, Any]) -> None:
        if assessment_id not in self._connections:
            return
        message = json.dumps(event)
        disconnected = set()
        for ws in self._connections[assessment_id]:
            try:
                await ws.send_text(message)
            except Exception:
                disconnected.add(ws)
        for ws in disconnected:
            self._connections[assessment_id].discard(ws)


manager = ConnectionManager()


async def websocket_handler(websocket: WebSocket) -> None:
    await websocket.accept()
    assessment_id = ""
    try:
        while True:
            data = await websocket.receive_text()
            try:
                payload = json.loads(data)
                assessment_id = payload.get("assessment_id", assessment_id)
                if assessment_id:
                    await manager.connect(assessment_id, websocket)
                event_type = payload.get("type", "unknown")
                if event_type == "ping":
                    await websocket.send_text(json.dumps({"type": "pong"}))
            except json.JSONDecodeError:
                await websocket.send_text(json.dumps({"type": "error", "message": "Invalid JSON"}))
    except WebSocketDisconnect:
        if assessment_id:
            manager.disconnect(assessment_id, websocket)
    except Exception:
        if assessment_id:
            manager.disconnect(assessment_id, websocket)
