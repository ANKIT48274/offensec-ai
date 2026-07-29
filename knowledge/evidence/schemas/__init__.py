"""Evidence schema definitions."""

EVIDENCE_SCHEMA = {
    "type": "object",
    "properties": {
        "id": {"type": "string"},
        "finding_id": {"type": "string"},
        "type": {
            "type": "string",
            "enum": [
                "screenshot",
                "command_output",
                "log_entry",
                "network_capture",
                "file_sample",
                "manual_note",
            ],
        },
        "source": {"type": "string"},
        "content": {"type": "string"},
        "file_path": {"type": ["string", "null"]},
        "metadata": {"type": "object"},
        "captured_at": {"type": "string", "format": "date-time"},
    },
    "required": ["type", "source", "content"],
}

FINDING_SCHEMA = {
    "type": "object",
    "properties": {
        "id": {"type": "string"},
        "assessment_id": {"type": "string"},
        "title": {"type": "string"},
        "description": {"type": "string"},
        "severity": {"type": "string", "enum": ["none", "low", "medium", "high", "critical"]},
        "confidence": {"type": "string", "enum": ["low", "medium", "high", "confirmed"]},
        "status": {
            "type": "string",
            "enum": [
                "open",
                "in_review",
                "confirmed",
                "false_positive",
                "accepted_risk",
                "remediated",
            ],
        },
        "target": {"type": "string"},
        "evidence": {"type": "array", "items": {"$ref": "#/definitions/Evidence"}},
        "cwe_id": {"type": ["string", "null"]},
        "cvss_score": {"type": ["number", "null"]},
        "remediation": {"type": ["string", "null"]},
    },
    "required": ["title", "severity", "assessment_id"],
}
