"""Confidence scoring — quantifies certainty of AI outputs."""

from __future__ import annotations

from typing import Any


class ConfidenceScorer:
    def score(self, finding: dict[str, Any]) -> float:
        s = 0.5
        if finding.get("evidence"):
            s += 0.2
        if finding.get("cve_id"):
            s += 0.15
        if finding.get("cvss_score") is not None:
            s += 0.1
        if finding.get("remediation"):
            s += 0.05
        return min(s, 1.0)

    def categorize(self, score: float) -> str:
        if score >= 0.8:
            return "high"
        if score >= 0.5:
            return "medium"
        return "low"
