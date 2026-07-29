"""Report generation infrastructure for multiple output formats."""

from __future__ import annotations

from datetime import UTC, datetime, timezone
from typing import Any


class PDFReportGenerator:
    """Generates PDF reports from assessment findings."""

    async def generate(
        self, findings: list[dict[str, Any]], assessment: dict[str, Any] | None = None
    ) -> str:
        html = self._build_html(findings, assessment)
        return html

    def _build_html(
        self, findings: list[dict[str, Any]], assessment: dict[str, Any] | None = None
    ) -> str:
        sections = []
        sections.append("<html><body>")
        sections.append("<h1>Security Assessment Report</h1>")
        sections.append(f"<p>Generated: {datetime.now(UTC).isoformat()}</p>")

        if assessment:
            sections.append(f"<h2>Assessment: {assessment.get('name', 'N/A')}</h2>")

        sections.append(f"<p>Total Findings: {len(findings)}</p>")
        sections.append("<hr/>")

        critical = [f for f in findings if f.get("severity") == "critical"]
        high = [f for f in findings if f.get("severity") == "high"]
        medium = [f for f in findings if f.get("severity") == "medium"]
        low = [f for f in findings if f.get("severity") == "low"]

        sections.append("<h2>Summary</h2>")
        sections.append(
            f"<p>Critical: {len(critical)} | High: {len(high)} | Medium: {len(medium)} | Low: {len(low)}</p>"
        )

        for f in findings:
            sections.append("<div class='finding'>")
            sections.append(f"<h3>{f.get('title', 'Untitled')}</h3>")
            sections.append(
                f"<p>Severity: {f.get('severity', 'none')} | Confidence: {f.get('confidence', 'low')} | Status: {f.get('status', 'open')}</p>"
            )
            sections.append(f"<p>Target: {f.get('target', 'N/A')}</p>")
            sections.append(f"<p>{f.get('description', '')}</p>")
            if f.get("remediation"):
                sections.append(f"<h4>Remediation</h4><p>{f['remediation']}</p>")
            sections.append("</div>")

        sections.append("</body></html>")
        return "\n".join(sections)


class MarkdownReportGenerator:
    """Generates Markdown reports from assessment findings."""

    async def generate(
        self, findings: list[dict[str, Any]], assessment: dict[str, Any] | None = None
    ) -> str:
        lines = []

        lines.append("# Security Assessment Report")
        lines.append("")
        lines.append(f"**Generated:** {datetime.now(UTC).isoformat()}")
        lines.append("")

        if assessment:
            lines.append(f"**Assessment:** {assessment.get('name', 'N/A')}")
            lines.append("")

        lines.append(f"**Total Findings:** {len(findings)}")
        lines.append("")

        critical = [f for f in findings if f.get("severity") == "critical"]
        high = [f for f in findings if f.get("severity") == "high"]
        medium = [f for f in findings if f.get("severity") == "medium"]
        low = [f for f in findings if f.get("severity") == "low"]

        lines.append("## Summary")
        lines.append("")
        lines.append("| Severity | Count |")
        lines.append("| --- | --- |")
        lines.append(f"| Critical | {len(critical)} |")
        lines.append(f"| High | {len(high)} |")
        lines.append(f"| Medium | {len(medium)} |")
        lines.append(f"| Low | {len(low)} |")
        lines.append("")

        for f in findings:
            lines.append(f"## {f.get('title', 'Untitled')}")
            lines.append("")
            lines.append(f"- **Severity:** {f.get('severity', 'none')}")
            lines.append(f"- **Confidence:** {f.get('confidence', 'low')}")
            lines.append(f"- **Status:** {f.get('status', 'open')}")
            lines.append(f"- **Target:** {f.get('target', 'N/A')}")
            lines.append("")
            lines.append(f.get("description", ""))
            lines.append("")
            if f.get("remediation"):
                lines.append("### Remediation")
                lines.append("")
                lines.append(f["remediation"])
                lines.append("")
            lines.append("---")
            lines.append("")

        return "\n".join(lines)
