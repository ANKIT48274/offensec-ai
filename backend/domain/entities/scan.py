"""Scan entity for Nmap scan results."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any
from uuid import uuid4

from backend.domain.value_objects.scan_status import ScanStatus


@dataclass
class Scan:
    id: str = field(default_factory=lambda: uuid4().hex)
    project_id: str = ""
    target: str = ""
    status: ScanStatus = ScanStatus.PENDING
    started_at: datetime | None = None
    finished_at: datetime | None = None
    xml_path: str | None = None
    json_result: dict[str, Any] | None = None
    error_message: str | None = None
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    def start(self) -> None:
        self.status = ScanStatus.RUNNING
        self.started_at = datetime.now(UTC)
        self.updated_at = datetime.now(UTC)

    def complete(self, xml_path: str, json_result: dict[str, Any]) -> None:
        self.status = ScanStatus.COMPLETED
        self.finished_at = datetime.now(UTC)
        self.xml_path = xml_path
        self.json_result = json_result
        self.updated_at = datetime.now(UTC)

    def fail(self, error: str) -> None:
        self.status = ScanStatus.FAILED
        self.finished_at = datetime.now(UTC)
        self.error_message = error
        self.updated_at = datetime.now(UTC)

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "project_id": self.project_id,
            "target": self.target,
            "status": self.status.value,
            "started_at": self.started_at,
            "finished_at": self.finished_at,
            "xml_path": self.xml_path,
            "json_result": self.json_result,
            "error_message": self.error_message,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }
