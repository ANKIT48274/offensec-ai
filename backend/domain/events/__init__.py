"""Domain events for OffenSec AI."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime, timezone
from enum import Enum
from typing import Any, ClassVar
from uuid import uuid4


class EventPriority(Enum):
    LOW = "low"
    NORMAL = "normal"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass
class DomainEvent:
    """Base class for all domain events."""

    event_id: str = field(default_factory=lambda: uuid4().hex)
    occurred_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    version: ClassVar[int] = 1
    priority: EventPriority = EventPriority.NORMAL

    def to_dict(self) -> dict[str, Any]:
        return {
            "event_type": type(self).__name__,
            "event_id": self.event_id,
            "occurred_at": self.occurred_at.isoformat(),
            "version": self.version,
            "priority": self.priority.value,
        }


@dataclass
class ProjectCreated(DomainEvent):
    project_id: str = ""
    name: str = ""
    owner_id: str = ""

    def to_dict(self) -> dict[str, Any]:
        data = super().to_dict()
        data.update({"project_id": self.project_id, "name": self.name, "owner_id": self.owner_id})
        return data


@dataclass
class AssessmentStarted(DomainEvent):
    assessment_id: str = ""
    project_id: str = ""
    scope_id: str = ""
    started_by: str = ""

    def to_dict(self) -> dict[str, Any]:
        data = super().to_dict()
        data.update(
            {
                "assessment_id": self.assessment_id,
                "project_id": self.project_id,
                "scope_id": self.scope_id,
                "started_by": self.started_by,
            }
        )
        return data


@dataclass
class AssessmentCompleted(DomainEvent):
    assessment_id: str = ""
    project_id: str = ""
    finding_count: int = 0
    critical_count: int = 0

    def to_dict(self) -> dict[str, Any]:
        data = super().to_dict()
        data.update(
            {
                "assessment_id": self.assessment_id,
                "project_id": self.project_id,
                "finding_count": self.finding_count,
                "critical_count": self.critical_count,
            }
        )
        return data


@dataclass
class FindingCreated(DomainEvent):
    finding_id: str = ""
    assessment_id: str = ""
    title: str = ""
    severity: str = ""
    target: str = ""
    priority: EventPriority = EventPriority.HIGH

    def to_dict(self) -> dict[str, Any]:
        data = super().to_dict()
        data.update(
            {
                "finding_id": self.finding_id,
                "assessment_id": self.assessment_id,
                "title": self.title,
                "severity": self.severity,
                "target": self.target,
            }
        )
        return data


@dataclass
class ScopeViolationDetected(DomainEvent):
    scope_id: str = ""
    target: str = ""
    reason: str = ""
    attempted_by: str = ""
    priority: EventPriority = EventPriority.CRITICAL

    def to_dict(self) -> dict[str, Any]:
        data = super().to_dict()
        data.update(
            {
                "scope_id": self.scope_id,
                "target": self.target,
                "reason": self.reason,
                "attempted_by": self.attempted_by,
            }
        )
        return data


@dataclass
class UserAuthenticated(DomainEvent):
    user_id: str = ""
    method: str = ""
    ip_address: str | None = None


@dataclass
class AIPlanGenerated(DomainEvent):
    assessment_id: str = ""
    agent_type: str = ""
    step_count: int = 0
    priority: EventPriority = EventPriority.LOW


@dataclass
class ReportGenerated(DomainEvent):
    assessment_id: str = ""
    format: str = ""
    finding_count: int = 0
