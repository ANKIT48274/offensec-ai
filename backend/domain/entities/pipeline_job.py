"""PipelineJob entity for scan pipeline execution."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any
from uuid import uuid4


@dataclass
class PipelineJob:
    id: str = field(default_factory=lambda: uuid4().hex)
    project_id: str = ""
    target: str = ""
    status: str = "pending"
    steps: list[dict[str, Any]] = field(
        default_factory=lambda: [
            {"name": "nmap", "status": "pending"},
            {"name": "httpx", "status": "pending"},
            {"name": "nuclei", "status": "pending"},
        ]
    )
    results: dict[str, Any] = field(default_factory=dict)
    error_message: str | None = None
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    def start(self) -> None:
        self.status = "running"
        self.steps[0]["status"] = "running"
        self.updated_at = datetime.now(UTC)

    def complete_step(self, step_index: int, result: dict[str, Any]) -> None:
        self.steps[step_index]["status"] = "completed"
        self.results[self.steps[step_index]["name"]] = result
        next_index = step_index + 1
        if next_index < len(self.steps):
            self.steps[next_index]["status"] = "running"
        else:
            self.status = "completed"
        self.updated_at = datetime.now(UTC)

    def fail_step(self, step_index: int, error: str) -> None:
        self.steps[step_index]["status"] = "failed"
        self.steps[step_index]["error"] = error
        self.status = "failed"
        self.error_message = error
        self.updated_at = datetime.now(UTC)

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "project_id": self.project_id,
            "target": self.target,
            "status": self.status,
            "steps": self.steps,
            "results": self.results,
            "error_message": self.error_message,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }
