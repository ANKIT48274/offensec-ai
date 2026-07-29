"""Finding prioritizer — scores and ranks findings by risk."""

from __future__ import annotations

from typing import Any


class FindingPrioritizer:
    """Prioritizes findings based on severity, confidence, and exploitability."""

    def prioritize(self, findings: list[dict[str, Any]]) -> list[dict[str, Any]]:
        scored = []

        for finding in findings:
            severity_score = {"critical": 4, "high": 3, "medium": 2, "low": 1}.get(
                finding.get("severity", "low"), 0
            )
            confidence_score = {"confirmed": 1.0, "high": 0.75, "medium": 0.5, "low": 0.25}.get(
                finding.get("confidence", "low"), 0
            )
            priority_score = severity_score * confidence_score

            scored.append(
                {
                    **finding,
                    "priority_score": priority_score,
                }
            )

        scored.sort(key=lambda x: x["priority_score"], reverse=True)
        return scored
