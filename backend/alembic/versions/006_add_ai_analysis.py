"""Add AI analysis tables.

Revision ID: 006
Revises: 005
Create Date: 2026-07-29
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import JSONB


revision: str = "006"
down_revision: Union[str, None] = "005"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "ai_analysis",
        sa.Column("id", sa.String(64), primary_key=True),
        sa.Column("project_id", sa.String(64), sa.ForeignKey("projects.id"), nullable=False),
        sa.Column("analysis_type", sa.String(64), nullable=False),
        sa.Column("title", sa.String(500), nullable=False),
        sa.Column("summary", sa.Text(), nullable=True),
        sa.Column("severity", sa.String(32), nullable=True),
        sa.Column("risk_score", sa.Integer(), nullable=True),
        sa.Column("assets", JSONB(), default=list),
        sa.Column("findings", JSONB(), default=list),
        sa.Column("attack_paths", JSONB(), default=list),
        sa.Column("recommendations", JSONB(), default=list),
        sa.Column("raw_analysis", JSONB(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )

    op.create_table(
        "attack_paths",
        sa.Column("id", sa.String(64), primary_key=True),
        sa.Column("project_id", sa.String(64), sa.ForeignKey("projects.id"), nullable=False),
        sa.Column("source", sa.String(255), nullable=False),
        sa.Column("destination", sa.String(255), nullable=False),
        sa.Column("technique", sa.String(255), nullable=False),
        sa.Column("score", sa.Integer(), default=50),
        sa.Column("evidence", JSONB(), default=list),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )


def downgrade() -> None:
    op.drop_table("attack_paths")
    op.drop_table("ai_analysis")
