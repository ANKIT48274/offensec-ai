"""Add nuclei results table.

Revision ID: 004
Revises: 003
Create Date: 2026-07-29
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import JSONB


revision: str = "004"
down_revision: Union[str, None] = "003"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "nuclei_results",
        sa.Column("id", sa.String(64), primary_key=True),
        sa.Column("job_id", sa.String(64), sa.ForeignKey("scan_jobs.id"), nullable=False),
        sa.Column("project_id", sa.String(64), sa.ForeignKey("projects.id"), nullable=False),
        sa.Column("target", sa.String(255), nullable=False),
        sa.Column("template_id", sa.String(255), nullable=False),
        sa.Column("template_name", sa.String(500), nullable=True),
        sa.Column("severity", sa.String(32), nullable=False),
        sa.Column("matched_url", sa.String(500), nullable=True),
        sa.Column("matched_at", sa.String(255), nullable=True),
        sa.Column("protocol", sa.String(32), nullable=True),
        sa.Column("tags", JSONB(), default=list),
        sa.Column("ref_url", sa.String(500), nullable=True),
        sa.Column("cwe_ids", JSONB(), default=list),
        sa.Column("cve_ids", JSONB(), default=list),
        sa.Column("cvss_score", sa.String(16), nullable=True),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("remediation", sa.Text(), nullable=True),
        sa.Column("extracted_results", JSONB(), default=list),
        sa.Column("raw_data", JSONB(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )


def downgrade() -> None:
    op.drop_table("nuclei_results")
