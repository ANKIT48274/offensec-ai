"""Report templates for different assessment types and audiences."""

from __future__ import annotations

from typing import Any


class ReportTemplate:
    """Base report template."""

    def render(self, findings: list[dict[str, Any]], assessment: dict[str, Any] | None = None) -> str:
        raise NotImplementedError


class ExecutiveTemplate(ReportTemplate):
    """Executive summary template for non-technical stakeholders."""

    def render(self, findings: list[dict[str, Any]], assessment: dict[str, Any] | None = None) -> str:
        critical = len([f for f in findings if f.get("severity") == "critical"])
        high = len([f for f in findings if f.get("severity") == "high"])

        lines = [
            "# Executive Summary",
            "",
            f"Total findings: {len(findings)}",
            f"Critical: {critical}",
            f"High: {high}",
            "",
            "## Risk Overview",
            "",
        ]

        if critical > 0:
            lines.append(f"There are {critical} critical findings requiring immediate attention.")
        if high > 0:
            lines.append(f"{high} high-severity findings should be addressed within the next remediation cycle.")

        lines.append("")
        lines.append("## Recommendations")
        lines.append("")
        lines.append("1. Remediate all critical findings immediately.")
        lines.append("2. Address high-severity findings within 30 days.")
        lines.append("3. Conduct a follow-up assessment after remediation.")

        return "\n".join(lines)


class TechnicalTemplate(ReportTemplate):
    """Detailed technical report for security teams."""

    def render(self, findings: list[dict[str, Any]], assessment: dict[str, Any] | None = None) -> str:
        lines = [
            "# Technical Assessment Report",
            "",
            f"## Findings: {len(findings)}",
            "",
        ]

        for idx, f in enumerate(findings, 1):
            lines.extend([
                f"### {idx}. {f.get('title', 'Untitled')}",
                "",
                f"**Severity:** {f.get('severity', 'none')}",
                f"**Confidence:** {f.get('confidence', 'low')}",
                f"**Target:** {f.get('target', 'N/A')}",
                f"**CWE:** {f.get('cwe_id', 'N/A')}",
                f"**CVSS:** {f.get('cvss_score', 'N/A')}",
                "",
                f.get("description", ""),
                "",
            ])
            if f.get("remediation"):
                lines.extend(["**Remediation:**", "", f["remediation"], ""])
            lines.append("---")
            lines.append("")

        return "\n".join(lines)
