"""PDF report generator using weasyprint for production-quality PDFs."""

from __future__ import annotations

import os
import tempfile
from typing import Any

from backend.infrastructure.reporting.templates import (
    executive_template,
    owasp_template,
    ptes_template,
    technical_template,
)


class PDFReportGenerator:
    """Generates PDF reports from assessment findings using HTML-to-PDF conversion."""

    def __init__(self, output_dir: str | None = None) -> None:
        self._output_dir = output_dir or "/tmp/offensec_reports"
        os.makedirs(self._output_dir, exist_ok=True)

    async def generate(
        self,
        findings: list[dict[str, Any]],
        assessment: dict[str, Any] | None = None,
        style: str = "technical",
    ) -> str:
        style_map = {
            "executive": executive_template,
            "technical": technical_template,
            "owasp": owasp_template,
            "ptes": ptes_template,
        }
        template_fn = style_map.get(style, technical_template)
        html = template_fn(findings, assessment)

        fd, pdf_path = tempfile.mkstemp(
            suffix=".pdf", prefix=f"report_{style}_", dir=self._output_dir
        )
        os.close(fd)

        try:
            from weasyprint import HTML as WeasyHTML

            WeasyHTML(string=html).write_pdf(pdf_path)
        except ImportError:
            html_path = pdf_path.replace(".pdf", ".html")
            with open(html_path, "w", encoding="utf-8") as f:
                f.write(html)
            return html_path

        return pdf_path

    async def generate_html(
        self,
        findings: list[dict[str, Any]],
        assessment: dict[str, Any] | None = None,
        style: str = "technical",
    ) -> str:
        style_map = {
            "executive": executive_template,
            "technical": technical_template,
            "owasp": owasp_template,
            "ptes": ptes_template,
        }
        template_fn = style_map.get(style, technical_template)
        return template_fn(findings, assessment)
