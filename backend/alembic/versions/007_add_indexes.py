"""Add missing database indexes for production performance.

Revision ID: 007
Revises: 006
Create Date: 2026-07-29
"""

from typing import Sequence, Union

from alembic import op


revision: str = "007"
down_revision: Union[str, None] = "006"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


INDEXES = [
    # Findings
    ("idx_findings_assessment", "findings", ["assessment_id"]),
    ("idx_findings_severity", "findings", ["severity"]),
    ("idx_findings_created", "findings", ["created_at"]),
    # Assessments
    ("idx_assessments_project", "assessments", ["project_id"]),
    ("idx_assessments_status", "assessments", ["status"]),
    # Scans
    ("idx_scans_project", "scans", ["project_id"]),
    ("idx_scans_status", "scans", ["status"]),
    # Scan jobs
    ("idx_scan_jobs_project", "scan_jobs", ["project_id"]),
    ("idx_scan_jobs_status", "scan_jobs", ["status"]),
    # Nuclei results
    ("idx_nuclei_project", "nuclei_results", ["project_id"]),
    ("idx_nuclei_severity", "nuclei_results", ["severity"]),
    ("idx_nuclei_template", "nuclei_results", ["template_id"]),
    # AI analysis
    ("idx_ai_analysis_project", "ai_analysis", ["project_id"]),
    # Attack paths
    ("idx_attack_paths_project", "attack_paths", ["project_id"]),
    # Reports
    ("idx_reports_assessment", "reports", ["assessment_id"]),
    # Targets
    ("idx_targets_assessment", "targets", ["assessment_id"]),
    # Audit logs
    ("idx_audit_logs_actor", "audit_logs", ["actor_id"]),
    ("idx_audit_logs_action", "audit_logs", ["action"]),
    # Users
    ("idx_users_email", "users", ["email"]),
    ("idx_users_username", "users", ["username"]),
]


def upgrade() -> None:
    for idx_name, table, columns in INDEXES:
        try:
            op.create_index(idx_name, table, columns)
        except Exception:
            pass


def downgrade() -> None:
    for idx_name, table, columns in reversed(INDEXES):
        try:
            op.drop_index(idx_name)
        except Exception:
            pass
