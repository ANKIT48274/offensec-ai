"""Domain entity definitions for OffenSec AI."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime, timezone
from typing import Any
from uuid import uuid4

from backend.domain.value_objects import (
    AssessmentStatus,
    Confidence,
    Credential,
    FindingReference,
    FindingStatus,
    ScopeDefinition,
    Severity,
)


@dataclass
class User:
    """Represents a platform user."""

    id: str = field(default_factory=lambda: uuid4().hex)
    email: str = ""
    username: str = ""
    password_hash: str = ""
    is_active: bool = True
    is_superuser: bool = False
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    last_login_at: datetime | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "email": self.email,
            "username": self.username,
            "is_active": self.is_active,
            "is_superuser": self.is_superuser,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "last_login_at": self.last_login_at.isoformat() if self.last_login_at else None,
        }


@dataclass
class Project:
    """Represents a security assessment project."""

    id: str = field(default_factory=lambda: uuid4().hex)
    name: str = ""
    description: str = ""
    owner_id: str = ""
    is_archived: bool = False
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "owner_id": self.owner_id,
            "is_archived": self.is_archived,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }


@dataclass
class Assessment:
    """Represents a single security assessment within a project."""

    id: str = field(default_factory=lambda: uuid4().hex)
    project_id: str = ""
    name: str = ""
    status: AssessmentStatus = AssessmentStatus.DRAFT
    scope: ScopeDefinition | None = None
    started_by: str = ""
    started_at: datetime | None = None
    completed_at: datetime | None = None
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    def start(self) -> None:
        from backend.domain.exceptions import AssessmentStateError

        if self.status not in (AssessmentStatus.DRAFT, AssessmentStatus.PAUSED):
            raise AssessmentStateError(
                self.id, self.status.value, f"{AssessmentStatus.DRAFT.value} or {AssessmentStatus.PAUSED.value}"
            )
        self.status = AssessmentStatus.IN_PROGRESS
        self.started_at = datetime.now(UTC)
        self.updated_at = datetime.now(UTC)

    def complete(self) -> None:
        from backend.domain.exceptions import AssessmentStateError

        if self.status != AssessmentStatus.IN_PROGRESS:
            raise AssessmentStateError(self.id, self.status.value, AssessmentStatus.IN_PROGRESS.value)
        self.status = AssessmentStatus.COMPLETED
        self.completed_at = datetime.now(UTC)
        self.updated_at = datetime.now(UTC)

    def pause(self) -> None:
        from backend.domain.exceptions import AssessmentStateError

        if self.status != AssessmentStatus.IN_PROGRESS:
            raise AssessmentStateError(self.id, self.status.value, AssessmentStatus.IN_PROGRESS.value)
        self.status = AssessmentStatus.PAUSED
        self.updated_at = datetime.now(UTC)

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "project_id": self.project_id,
            "name": self.name,
            "status": self.status.value,
            "scope": self.scope.__dict__ if self.scope else None,
            "started_by": self.started_by,
            "started_at": self.started_at.isoformat() if self.started_at else None,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }


@dataclass
class Target:
    """Represents a target within an assessment scope."""

    id: str = field(default_factory=lambda: uuid4().hex)
    assessment_id: str = ""
    value: str = ""
    type: str = ""
    label: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)
    discovered_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "assessment_id": self.assessment_id,
            "value": self.value,
            "type": self.type,
            "label": self.label,
            "metadata": self.metadata,
            "discovered_at": self.discovered_at.isoformat(),
        }


@dataclass
class Finding:
    """Represents a security finding discovered during an assessment."""

    id: str = field(default_factory=lambda: uuid4().hex)
    assessment_id: str = ""
    title: str = ""
    description: str = ""
    severity: Severity = Severity.NONE
    confidence: Confidence = Confidence.LOW
    status: FindingStatus = FindingStatus.OPEN
    target: str = ""
    evidence: list[dict[str, Any]] = field(default_factory=list)
    references: list[FindingReference] = field(default_factory=list)
    owasp_id: str | None = None
    cwe_id: str | None = None
    cvss_score: float | None = None
    attack_paths: list[dict[str, Any]] = field(default_factory=list)
    remediation: str | None = None
    created_by: str = ""
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "assessment_id": self.assessment_id,
            "title": self.title,
            "description": self.description,
            "severity": self.severity.value,
            "confidence": self.confidence.value,
            "status": self.status.value,
            "target": self.target,
            "evidence": self.evidence,
            "references": [r.__dict__ for r in self.references],
            "owasp_id": self.owasp_id,
            "cwe_id": self.cwe_id,
            "cvss_score": self.cvss_score,
            "attack_paths": self.attack_paths,
            "remediation": self.remediation,
            "created_by": self.created_by,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }


@dataclass
class Evidence:
    """Represents a piece of evidence attached to a finding."""

    id: str = field(default_factory=lambda: uuid4().hex)
    finding_id: str = ""
    type: str = ""
    source: str = ""
    content: str = ""
    file_path: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)
    captured_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "finding_id": self.finding_id,
            "type": self.type,
            "source": self.source,
            "content": self.content[:1000] if self.content else "",
            "file_path": self.file_path,
            "metadata": self.metadata,
            "captured_at": self.captured_at.isoformat(),
        }


@dataclass
class Report:
    """Represents a generated assessment report."""

    id: str = field(default_factory=lambda: uuid4().hex)
    assessment_id: str = ""
    format: str = ""
    title: str = ""
    content: str = ""
    finding_count: int = 0
    critical_count: int = 0
    generated_by: str = ""
    generated_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "assessment_id": self.assessment_id,
            "format": self.format,
            "title": self.title,
            "finding_count": self.finding_count,
            "critical_count": self.critical_count,
            "generated_by": self.generated_by,
            "generated_at": self.generated_at.isoformat(),
        }


@dataclass
class AIPlan:
    """Represents an AI-generated assessment plan."""

    id: str = field(default_factory=lambda: uuid4().hex)
    assessment_id: str = ""
    agent_type: str = ""
    steps: list[dict[str, Any]] = field(default_factory=list)
    reasoning: str = ""
    confidence_score: float = 0.0
    approved: bool = False
    approved_by: str | None = None
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "assessment_id": self.assessment_id,
            "agent_type": self.agent_type,
            "steps": self.steps,
            "reasoning": self.reasoning,
            "confidence_score": self.confidence_score,
            "approved": self.approved,
            "approved_by": self.approved_by,
            "created_at": self.created_at.isoformat(),
        }


@dataclass
class AuditLog:
    """Represents an auditable action record."""

    id: str = field(default_factory=lambda: uuid4().hex)
    actor_id: str = ""
    action: str = ""
    resource_type: str = ""
    resource_id: str = ""
    details: dict[str, Any] = field(default_factory=dict)
    ip_address: str | None = None
    occurred_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "actor_id": self.actor_id,
            "action": self.action,
            "resource_type": self.resource_type,
            "resource_id": self.resource_id,
            "details": self.details,
            "ip_address": self.ip_address,
            "occurred_at": self.occurred_at.isoformat(),
        }


@dataclass
class Plugin:
    """Represents a registered plugin."""

    id: str = field(default_factory=lambda: uuid4().hex)
    name: str = ""
    version: str = ""
    description: str = ""
    author: str = ""
    capabilities: list[str] = field(default_factory=list)
    is_enabled: bool = False
    signature: str | None = None
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "version": self.version,
            "description": self.description,
            "author": self.author,
            "capabilities": self.capabilities,
            "is_enabled": self.is_enabled,
            "signature": self.signature,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }
