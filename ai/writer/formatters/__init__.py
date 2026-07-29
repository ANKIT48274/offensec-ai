"""Output formatters for various report formats."""

from __future__ import annotations

from typing import Any


class ReportFormatter:
    """Base formatter for report output."""

    def format(self, content: str, findings: list[dict[str, Any]]) -> str:
        raise NotImplementedError


class MarkdownFormatter(ReportFormatter):
    """Formats reports as Markdown."""

    def format(self, content: str, findings: list[dict[str, Any]]) -> str:
        return content


class PDFFormatter(ReportFormatter):
    """Formats reports for PDF conversion."""

    def format(self, content: str, findings: list[dict[str, Any]]) -> str:
        html = ["<html><body>"]
        html.append("<h1>Security Assessment Report</h1>")
        html.append(f"<p>Total Findings: {len(findings)}</p>")

        for f in findings:
            html.append(f"<h2>{f.get('title', '')}</h2>")
            html.append(f"<p>Severity: {f.get('severity', '')}</p>")
            html.append(f"<pre>{f.get('description', '')}</pre>")

        html.append("</body></html>")
        return "\n".join(html)


class JSONFormatter(ReportFormatter):
    """Formats reports as structured JSON."""

    def format(self, content: str, findings: list[dict[str, Any]]) -> str:
        import json
        data = {"findings": findings, "summary": {"total": len(findings)}}
        return json.dumps(data, indent=2)
