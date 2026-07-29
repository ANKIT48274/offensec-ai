"""CSV and JSON exporters for assessment findings."""

from __future__ import annotations

import csv
import io
import json
from typing import Any


def export_csv(findings: list[dict[str, Any]]) -> str:
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow([
        "Title", "Severity", "Confidence", "Status", "Target", "CWE", "CVSS",
        "Description", "Remediation", "Created",
    ])
    for f in findings:
        writer.writerow([
            f.get("title", ""),
            f.get("severity", ""),
            f.get("confidence", ""),
            f.get("status", ""),
            f.get("target", ""),
            f.get("cwe_id", ""),
            f.get("cvss_score", ""),
            f.get("description", ""),
            f.get("remediation", ""),
            f.get("created_at", ""),
        ])
    return output.getvalue()


def export_json(findings: list[dict[str, Any]], assessment: dict[str, Any] | None = None) -> str:
    output: dict[str, Any] = {
        "report": {
            "generated_at": __import__("datetime").datetime.now(__import__("datetime").timezone.utc).isoformat(),
            "tool": "OffenSec AI",
        },
        "summary": {
            "total": len(findings),
            "critical": len([f for f in findings if f.get("severity") == "critical"]),
            "high": len([f for f in findings if f.get("severity") == "high"]),
            "medium": len([f for f in findings if f.get("severity") == "medium"]),
            "low": len([f for f in findings if f.get("severity") == "low"]),
        },
        "findings": [
            {
                "title": f.get("title"),
                "severity": f.get("severity"),
                "confidence": f.get("confidence"),
                "status": f.get("status"),
                "target": f.get("target"),
                "description": f.get("description"),
                "remediation": f.get("remediation"),
                "cwe_id": f.get("cwe_id"),
                "cvss_score": f.get("cvss_score"),
            }
            for f in findings
        ],
    }
    if assessment:
        output["assessment"] = {
            "id": assessment.get("id"),
            "name": assessment.get("name"),
            "status": assessment.get("status"),
        }
    return json.dumps(output, indent=2, default=str)
