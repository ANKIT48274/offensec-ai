"""Initial database schema.

Revision ID: 001
Revises:
Create Date: 2026-07-29
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import JSONB


revision: str = "001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.String(64), primary_key=True),
        sa.Column("email", sa.String(255), unique=True, nullable=False),
        sa.Column("username", sa.String(64), unique=True, nullable=False),
        sa.Column("password_hash", sa.String(255), nullable=False),
        sa.Column("is_active", sa.Boolean(), default=True, nullable=False),
        sa.Column("is_superuser", sa.Boolean(), default=False, nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("last_login_at", sa.DateTime(timezone=True), nullable=True),
    )

    op.create_table(
        "projects",
        sa.Column("id", sa.String(64), primary_key=True),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("description", sa.Text(), default=""),
        sa.Column("owner_id", sa.String(64), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("is_archived", sa.Boolean(), default=False, nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )

    op.create_table(
        "audit_logs",
        sa.Column("id", sa.String(64), primary_key=True),
        sa.Column("actor_id", sa.String(64), nullable=False),
        sa.Column("action", sa.String(255), nullable=False),
        sa.Column("resource_type", sa.String(64), nullable=False),
        sa.Column("resource_id", sa.String(64), nullable=False),
        sa.Column("details", JSONB(), default=dict),
        sa.Column("ip_address", sa.String(45), nullable=True),
        sa.Column("occurred_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )

    op.create_table(
        "plugins",
        sa.Column("id", sa.String(64), primary_key=True),
        sa.Column("name", sa.String(255), unique=True, nullable=False),
        sa.Column("version", sa.String(32), nullable=False),
        sa.Column("description", sa.Text(), default=""),
        sa.Column("author", sa.String(255), default=""),
        sa.Column("capabilities", JSONB(), default=list),
        sa.Column("is_enabled", sa.Boolean(), default=False),
        sa.Column("signature", sa.String(512), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )

    op.create_table(
        "assessments",
        sa.Column("id", sa.String(64), primary_key=True),
        sa.Column("project_id", sa.String(64), sa.ForeignKey("projects.id"), nullable=False),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("status", sa.String(32), default="draft", nullable=False),
        sa.Column("scope", JSONB(), default=dict),
        sa.Column("started_by", sa.String(64), default=""),
        sa.Column("started_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("completed_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )

    op.create_table(
        "targets",
        sa.Column("id", sa.String(64), primary_key=True),
        sa.Column("assessment_id", sa.String(64), sa.ForeignKey("assessments.id"), nullable=False),
        sa.Column("value", sa.String(255), nullable=False),
        sa.Column("type", sa.String(32), nullable=False),
        sa.Column("label", sa.String(255), default=""),
        sa.Column("metadata", JSONB(), default=dict),
        sa.Column("discovered_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )

    op.create_table(
        "reports",
        sa.Column("id", sa.String(64), primary_key=True),
        sa.Column("assessment_id", sa.String(64), sa.ForeignKey("assessments.id"), nullable=False),
        sa.Column("format", sa.String(16), nullable=False),
        sa.Column("title", sa.String(255), nullable=False),
        sa.Column("content", sa.Text(), default=""),
        sa.Column("finding_count", sa.Integer(), default=0),
        sa.Column("critical_count", sa.Integer(), default=0),
        sa.Column("generated_by", sa.String(64), default=""),
        sa.Column("generated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )

    op.create_table(
        "ai_plans",
        sa.Column("id", sa.String(64), primary_key=True),
        sa.Column("assessment_id", sa.String(64), sa.ForeignKey("assessments.id"), nullable=False),
        sa.Column("agent_type", sa.String(64), nullable=False),
        sa.Column("steps", JSONB(), default=list),
        sa.Column("reasoning", sa.Text(), default=""),
        sa.Column("confidence_score", sa.Float(), default=0.0),
        sa.Column("approved", sa.Boolean(), default=False),
        sa.Column("approved_by", sa.String(64), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )

    op.create_table(
        "findings",
        sa.Column("id", sa.String(64), primary_key=True),
        sa.Column("assessment_id", sa.String(64), sa.ForeignKey("assessments.id"), nullable=False),
        sa.Column("title", sa.String(500), nullable=False),
        sa.Column("description", sa.Text(), default=""),
        sa.Column("severity", sa.String(16), default="medium", nullable=False),
        sa.Column("confidence", sa.String(16), default="medium", nullable=False),
        sa.Column("status", sa.String(32), default="open", nullable=False),
        sa.Column("target", sa.String(255), default=""),
        sa.Column("evidence", JSONB(), default=list),
        sa.Column("references", JSONB(), default=list),
        sa.Column("owasp_id", sa.String(32), nullable=True),
        sa.Column("cwe_id", sa.String(32), nullable=True),
        sa.Column("cvss_score", sa.Float(), nullable=True),
        sa.Column("attack_paths", JSONB(), default=list),
        sa.Column("remediation", sa.Text(), nullable=True),
        sa.Column("created_by", sa.String(64), default=""),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )

    op.create_table(
        "evidences",
        sa.Column("id", sa.String(64), primary_key=True),
        sa.Column("finding_id", sa.String(64), sa.ForeignKey("findings.id"), nullable=False),
        sa.Column("type", sa.String(64), nullable=False),
        sa.Column("source", sa.String(255), nullable=False),
        sa.Column("content", sa.Text(), default=""),
        sa.Column("file_path", sa.String(500), nullable=True),
        sa.Column("metadata", JSONB(), default=dict),
        sa.Column("captured_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )


def downgrade() -> None:
    op.drop_table("evidences")
    op.drop_table("findings")
    op.drop_table("ai_plans")
    op.drop_table("reports")
    op.drop_table("targets")
    op.drop_table("assessments")
    op.drop_table("plugins")
    op.drop_table("audit_logs")
    op.drop_table("projects")
    op.drop_table("users")
