"""ScanStatus value object for scan lifecycle."""

from __future__ import annotations

from enum import Enum


class ScanStatus(Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    TIMEOUT = "timeout"
    CANCELLED = "cancelled"
