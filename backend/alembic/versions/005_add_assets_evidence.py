"""Add assets, evidence, asset_history tables.

Revision ID: 005
Revises: 004
Create Date: 2026-07-29
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import JSONB


revision: str = "005"
down_revision: Union[str, None] = "004"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "assets",
        sa.Column("id", sa.String(64), primary_key=True),
        sa.Column("project_id", sa.String(64), sa.ForeignKey("projects.id"), nullable=False),
        sa.Column("asset_type", sa.String(32), nullable=False),
        sa.Column("value", sa.String(500), nullable=False),
        sa.Column("label", sa.String(255), nullable=True),
        sa.Column("ips", JSONB(), default=list),
        sa.Column("hostnames", JSONB(), default=list),
        sa.Column("domains", JSONB(), default=list),
        sa.Column("ports", JSONB(), default=list),
        sa.Column("technologies", JSONB(), default=list),
        sa.Column("os_guesses", JSONB(), default=list),
        sa.Column("first_seen", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("last_seen", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("scan_count", sa.Integer(), default=1),
        sa.Column("metadata", JSONB(), default=dict),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    op.create_index("idx_assets_project", "assets", ["project_id"])
    op.create_index("idx_assets_value", "assets", ["project_id", "value"], unique=True)

    op.create_table(
        "asset_history",
        sa.Column("id", sa.String(64), primary_key=True),
        sa.Column("asset_id", sa.String(64), sa.ForeignKey("assets.id"), nullable=False),
        sa.Column("project_id", sa.String(64), sa.ForeignKey("projects.id"), nullable=False),
        sa.Column("event", sa.String(64), nullable=False),
        sa.Column("detail", JSONB(), default=dict),
        sa.Column("occurred_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )

    op.create_table(
        "evidence",
        sa.Column("id", sa.String(64), primary_key=True),
        sa.Column("asset_id", sa.String(64), sa.ForeignKey("assets.id"), nullable=False),
        sa.Column("project_id", sa.String(64), sa.ForeignKey("projects.id"), nullable=False),
        sa.Column("finding_id", sa.String(64), nullable=True),
        sa.Column("source", sa.String(64), nullable=False),
        sa.Column("evidence_type", sa.String(64), nullable=False),
        sa.Column("content", sa.Text(), nullable=True),
        sa.Column("file_path", sa.String(500), nullable=True),
        sa.Column("raw_data", JSONB(), nullable=True),
        sa.Column("captured_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    op.create_index("idx_evidence_project", "evidence", ["project_id"])


def downgrade() -> None:
    op.drop_table("evidence")
    op.drop_table("asset_history")
    op.drop_table("assets")
