"""Report writing agent — generates structured assessment reports."""

from __future__ import annotations

from typing import Any


class ReportWriterAgent:
    """AI agent responsible for report generation."""

    def __init__(self, model_client: Any) -> None:
        self._client = model_client

    async def generate_report(self, findings: list[dict[str, Any]], context: dict[str, Any] | None = None) -> str:
        lines = []
        lines.append("# Security Assessment Report")
        lines.append("")

        critical = [f for f in findings if f.get("severity") == "critical"]
        high = [f for f in findings if f.get("severity") == "high"]
        medium = [f for f in findings if f.get("severity") == "medium"]
        low = [f for f in findings if f.get("severity") == "low"]

        lines.append("## Summary")
        lines.append(f"Total findings: {len(findings)}")
        lines.append(f"Critical: {len(critical)}, High: {len(high)}, Medium: {len(medium)}, Low: {len(low)}")
        lines.append("")

        for idx, finding in enumerate(findings, 1):
            lines.append(f"## Finding {idx}: {finding.get('title', 'Untitled')}")
            lines.append(f"**Severity:** {finding.get('severity', 'none')}")
            lines.append(f"**Confidence:** {finding.get('confidence', 'low')}")
            lines.append(f"**Target:** {finding.get('target', 'N/A')}")
            lines.append("")
            lines.append(finding.get("description", ""))
            lines.append("")
            if finding.get("remediation"):
                lines.append("### Remediation")
                lines.append(finding["remediation"])
            lines.append("---")
            lines.append("")

        return "\n".join(lines)

    async def generate_executive_summary(self, findings: list[dict[str, Any]]) -> str:
        critical = len([f for f in findings if f.get("severity") == "critical"])
        high = len([f for f in findings if f.get("severity") == "high"])
        summary = (
            f"The assessment identified {len(findings)} security issues, "
            f"including {critical} critical and {high} high-severity findings. "
            "Priority remediation should focus on critical and high-severity findings."
        )
        return summary
