"""File-based persistence for raw evidence, report artifacts, and tool output."""

from __future__ import annotations

import os
from pathlib import Path

EVIDENCE_BASE_DIR = "/var/lib/offensec/evidence"
REPORT_BASE_DIR = "/var/lib/offensec/reports"
TOOL_OUTPUT_DIR = "/var/lib/offensec/tool_output"


def ensure_directories() -> None:
    for directory in (EVIDENCE_BASE_DIR, REPORT_BASE_DIR, TOOL_OUTPUT_DIR):
        Path(directory).mkdir(parents=True, exist_ok=True)


def write_evidence(assessment_id: str, finding_id: str, filename: str, content: str | bytes) -> str:
    ensure_directories()
    directory = Path(EVIDENCE_BASE_DIR) / assessment_id / finding_id
    directory.mkdir(parents=True, exist_ok=True)
    filepath = directory / filename

    if isinstance(content, str):
        filepath.write_text(content)
    else:
        filepath.write_bytes(content)

    return str(filepath)


def read_evidence(filepath: str) -> str | None:
    path = Path(filepath)
    if not path.exists():
        return None
    return path.read_text()


def write_report(assessment_id: str, filename: str, content: str | bytes) -> str:
    ensure_directories()
    directory = Path(REPORT_BASE_DIR) / assessment_id
    directory.mkdir(parents=True, exist_ok=True)
    filepath = directory / filename

    if isinstance(content, str):
        filepath.write_text(content)
    else:
        filepath.write_bytes(content)

    return str(filepath)


def write_tool_output(assessment_id: str, tool_name: str, content: str) -> str:
    ensure_directories()
    directory = Path(TOOL_OUTPUT_DIR) / assessment_id / tool_name
    directory.mkdir(parents=True, exist_ok=True)
    filepath = directory / "output.txt"
    filepath.write_text(content)
    return str(filepath)


def list_evidence(assessment_id: str, finding_id: str) -> list[str]:
    directory = Path(EVIDENCE_BASE_DIR) / assessment_id / finding_id
    if not directory.exists():
        return []
    return [str(f) for f in directory.iterdir() if f.is_file()]


def delete_evidence(assessment_id: str, finding_id: str) -> None:
    directory = Path(EVIDENCE_BASE_DIR) / assessment_id / finding_id
    if directory.exists():
        import shutil
        shutil.rmtree(directory)
