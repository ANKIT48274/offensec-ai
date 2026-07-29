"""Evidence binding — ensures AI outputs reference verifiable evidence."""

from __future__ import annotations

from datetime import UTC, datetime, timezone
from typing import Any


class EvidenceBinder:
    def bind(self, finding: dict[str, Any], evidence: list[dict[str, Any]]) -> dict[str, Any]:
        finding["evidence"] = evidence
        finding["evidence_count"] = len(evidence)
        finding["evidenced_at"] = datetime.now(UTC).isoformat()
        return finding

    def validate_evidence(self, finding: dict[str, Any]) -> tuple[bool, list[str]]:
        errors = []
        evidence = finding.get("evidence", [])
        if not evidence:
            errors.append("Finding has no supporting evidence")
        for item in evidence:
            if not item.get("source"):
                errors.append("Evidence item missing source field")
        return len(errors) == 0, errors
