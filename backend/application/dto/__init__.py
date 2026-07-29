"""Data transfer objects for the application layer."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any

from pydantic import BaseModel, EmailStr, Field


class UserRegisterDTO(BaseModel):
    """DTO for user registration."""

    email: str = Field(..., min_length=5, max_length=255)
    username: str = Field(..., min_length=3, max_length=64)
    password: str = Field(..., min_length=8, max_length=128)


class UserLoginDTO(BaseModel):
    """DTO for user authentication."""

    email: str = Field(..., max_length=255)
    password: str = Field(..., max_length=128)


class UserResponseDTO(BaseModel):
    """DTO for user data returned to clients."""

    id: str
    email: str
    username: str
    is_active: bool
    is_superuser: bool
    created_at: datetime
    updated_at: datetime
    last_login_at: datetime | None = None


class TokenResponseDTO(BaseModel):
    """DTO for JWT token response."""

    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int = 3600


class ProjectCreateDTO(BaseModel):
    """DTO for project creation."""

    name: str = Field(..., min_length=1, max_length=255)
    description: str = Field("", max_length=5000)


class ProjectUpdateDTO(BaseModel):
    """DTO for project updates."""

    name: str | None = Field(None, min_length=1, max_length=255)
    description: str | None = Field(None, max_length=5000)
    is_archived: bool | None = None


class ProjectResponseDTO(BaseModel):
    """DTO for project data returned to clients."""

    id: str
    name: str
    description: str
    owner_id: str
    is_archived: bool
    created_at: datetime
    updated_at: datetime
    assessment_count: int = 0


class AssessmentCreateDTO(BaseModel):
    """DTO for assessment creation."""

    project_id: str
    name: str = Field(..., min_length=1, max_length=255)
    targets: list[str] = Field(default_factory=list)
    scope: dict[str, Any] | None = None


class AssessmentResponseDTO(BaseModel):
    """DTO for assessment data returned to clients."""

    id: str
    project_id: str
    name: str
    status: str
    scope: dict[str, Any] | None = None
    started_by: str
    started_at: datetime | None = None
    completed_at: datetime | None = None
    created_at: datetime
    updated_at: datetime


class FindingCreateDTO(BaseModel):
    """DTO for finding creation."""

    assessment_id: str
    title: str = Field(..., min_length=1, max_length=500)
    description: str = Field("", max_length=10000)
    severity: str = "medium"
    confidence: str = "medium"
    target: str | None = None
    evidence: list[dict[str, Any]] = field(default_factory=list)
    references: list[dict[str, Any]] = field(default_factory=list)
    owasp_id: str | None = None
    cwe_id: str | None = None
    cvss_score: float | None = Field(None, ge=0.0, le=10.0)
    remediation: str | None = None


class FindingResponseDTO(BaseModel):
    """DTO for finding data returned to clients."""

    id: str
    assessment_id: str
    title: str
    description: str
    severity: str
    confidence: str
    status: str
    target: str | None = None
    evidence: list[dict[str, Any]] = field(default_factory=list)
    references: list[dict[str, Any]] = field(default_factory=list)
    owasp_id: str | None = None
    cwe_id: str | None = None
    cvss_score: float | None = None
    attack_paths: list[dict[str, Any]] = field(default_factory=list)
    remediation: str | None = None
    created_by: str
    created_at: datetime
    updated_at: datetime


class ReportGenerateDTO(BaseModel):
    """DTO for report generation request."""

    assessment_id: str
    format: str = "pdf"
    include_evidence: bool = True
    include_remediation: bool = True


class AIPlanRequestDTO(BaseModel):
    """DTO for AI plan generation request."""

    assessment_id: str
    agent_type: str = "recon"
    context: dict[str, Any] = field(default_factory=dict)


class AIPlanResponseDTO(BaseModel):
    """DTO for AI plan response."""

    id: str
    assessment_id: str
    agent_type: str
    steps: list[dict[str, Any]]
    reasoning: str
    confidence_score: float
    approved: bool
    created_at: datetime


class PaginationDTO(BaseModel):
    """DTO for paginated responses."""

    page: int = 1
    page_size: int = 50
    total: int = 0
    total_pages: int = 0


class PaginatedResponseDTO(BaseModel):
    """Generic paginated response wrapper."""

    data: list[Any]
    pagination: PaginationDTO
