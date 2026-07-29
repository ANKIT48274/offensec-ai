"""SQLAlchemy ORM models for OffenSec AI."""

from __future__ import annotations

from backend.infrastructure.persistence.postgres import Base
from sqlalchemy import Boolean, Column, DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func


class UserModel(Base):
    __tablename__ = "users"

    id = Column(String(64), primary_key=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    username = Column(String(64), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    is_superuser = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    last_login_at = Column(DateTime(timezone=True), nullable=True)

    projects = relationship("ProjectModel", back_populates="owner", cascade="all, delete-orphan")


class ProjectModel(Base):
    __tablename__ = "projects"

    id = Column(String(64), primary_key=True)
    name = Column(String(255), nullable=False)
    description = Column(Text, default="")
    owner_id = Column(String(64), ForeignKey("users.id"), nullable=False)
    is_archived = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    owner = relationship("UserModel", back_populates="projects")
    assessments = relationship("AssessmentModel", back_populates="project", cascade="all, delete-orphan")
    scans = relationship("ScanModel", back_populates="project", cascade="all, delete-orphan")
    scan_jobs = relationship("ScanJobModel", back_populates="project", cascade="all, delete-orphan")


class AssessmentModel(Base):
    __tablename__ = "assessments"

    id = Column(String(64), primary_key=True)
    project_id = Column(String(64), ForeignKey("projects.id"), nullable=False)
    name = Column(String(255), nullable=False)
    status = Column(String(32), default="draft", nullable=False)
    scope = Column(JSONB, default=dict)
    started_by = Column(String(64), default="")
    started_at = Column(DateTime(timezone=True), nullable=True)
    completed_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    project = relationship("ProjectModel", back_populates="assessments")
    findings = relationship("FindingModel", back_populates="assessment", cascade="all, delete-orphan")
    targets = relationship("TargetModel", back_populates="assessment", cascade="all, delete-orphan")
    reports = relationship("ReportModel", back_populates="assessment", cascade="all, delete-orphan")
    ai_plans = relationship("AIPlanModel", back_populates="assessment", cascade="all, delete-orphan")


class TargetModel(Base):
    __tablename__ = "targets"

    id = Column(String(64), primary_key=True)
    assessment_id = Column(String(64), ForeignKey("assessments.id"), nullable=False)
    value = Column(String(255), nullable=False)
    type = Column(String(32), nullable=False)
    label = Column(String(255), default="")
    target_meta = Column("metadata", JSONB, default=dict)
    discovered_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    assessment = relationship("AssessmentModel", back_populates="targets")


class FindingModel(Base):
    __tablename__ = "findings"

    id = Column(String(64), primary_key=True)
    assessment_id = Column(String(64), ForeignKey("assessments.id"), nullable=False)
    title = Column(String(500), nullable=False)
    description = Column(Text, default="")
    severity = Column(String(16), default="medium", nullable=False)
    confidence = Column(String(16), default="medium", nullable=False)
    status = Column(String(32), default="open", nullable=False)
    target = Column(String(255), default="")
    evidence_data = Column("evidence", JSONB, default=list)
    references_data = Column("references", JSONB, default=list)
    owasp_id = Column(String(32), nullable=True)
    cwe_id = Column(String(32), nullable=True)
    cvss_score = Column(Float, nullable=True)
    attack_paths = Column(JSONB, default=list)
    remediation = Column(Text, nullable=True)
    created_by = Column(String(64), default="")
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    assessment = relationship("AssessmentModel", back_populates="findings")
    evidences = relationship("EvidenceModel", back_populates="finding", cascade="all, delete-orphan")


class EvidenceModel(Base):
    __tablename__ = "evidences"

    id = Column(String(64), primary_key=True)
    finding_id = Column(String(64), ForeignKey("findings.id"), nullable=False)
    type = Column(String(64), nullable=False)
    source = Column(String(255), nullable=False)
    content = Column(Text, default="")
    file_path = Column(String(500), nullable=True)
    evidence_meta = Column("metadata", JSONB, default=dict)
    captured_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    finding = relationship("FindingModel", back_populates="evidences")


class ReportModel(Base):
    __tablename__ = "reports"

    id = Column(String(64), primary_key=True)
    assessment_id = Column(String(64), ForeignKey("assessments.id"), nullable=False)
    format = Column(String(16), nullable=False)
    title = Column(String(255), nullable=False)
    content = Column(Text, default="")
    finding_count = Column(Integer, default=0)
    critical_count = Column(Integer, default=0)
    generated_by = Column(String(64), default="")
    generated_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    assessment = relationship("AssessmentModel", back_populates="reports")


class AIPlanModel(Base):
    __tablename__ = "ai_plans"

    id = Column(String(64), primary_key=True)
    assessment_id = Column(String(64), ForeignKey("assessments.id"), nullable=False)
    agent_type = Column(String(64), nullable=False)
    steps = Column(JSONB, default=list)
    reasoning = Column(Text, default="")
    confidence_score = Column(Float, default=0.0)
    approved = Column(Boolean, default=False)
    approved_by = Column(String(64), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    assessment = relationship("AssessmentModel", back_populates="ai_plans")


class AuditLogModel(Base):
    __tablename__ = "audit_logs"

    id = Column(String(64), primary_key=True)
    actor_id = Column(String(64), nullable=False)
    action = Column(String(255), nullable=False)
    resource_type = Column(String(64), nullable=False)
    resource_id = Column(String(64), nullable=False)
    details = Column(JSONB, default=dict)
    ip_address = Column(String(45), nullable=True)
    occurred_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)


class PluginModel(Base):
    __tablename__ = "plugins"

    id = Column(String(64), primary_key=True)
    name = Column(String(255), unique=True, nullable=False)
    version = Column(String(32), nullable=False)
    description = Column(Text, default="")
    author = Column(String(255), default="")
    capabilities = Column(JSONB, default=list)
    is_enabled = Column(Boolean, default=False)
    signature = Column(String(512), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)


class ScanModel(Base):
    __tablename__ = "scans"

    id = Column(String(64), primary_key=True)
    project_id = Column(String(64), ForeignKey("projects.id"), nullable=False)
    target = Column(String(255), nullable=False)
    status = Column(String(32), default="pending", nullable=False)
    started_at = Column(DateTime(timezone=True), nullable=True)
    finished_at = Column(DateTime(timezone=True), nullable=True)
    xml_path = Column(String(500), nullable=True)
    json_result = Column(JSONB, nullable=True)
    error_message = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    project = relationship("ProjectModel", back_populates="scans")


class ScanJobModel(Base):
    __tablename__ = "scan_jobs"

    id = Column(String(64), primary_key=True)
    project_id = Column(String(64), ForeignKey("projects.id"), nullable=False)
    target = Column(String(255), nullable=False)
    status = Column(String(32), default="pending", nullable=False)
    steps = Column(JSONB, default=list)
    results = Column(JSONB, default=dict)
    error_message = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    project = relationship("ProjectModel", back_populates="scan_jobs")


class HttpxResultModel(Base):
    __tablename__ = "httpx_results"

    id = Column(String(64), primary_key=True)
    job_id = Column(String(64), ForeignKey("scan_jobs.id"), nullable=False)
    url = Column(String(500), nullable=False)
    status_code = Column(Integer, nullable=True)
    title = Column(String(500), nullable=True)
    tech = Column(JSONB, default=list)
    server = Column(String(255), nullable=True)
    content_length = Column(Integer, nullable=True)
    redirect_url = Column(String(500), nullable=True)
    websocket = Column(String(255), nullable=True)
    tls_data = Column(JSONB, nullable=True)
    favicon_hash = Column(String(64), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
