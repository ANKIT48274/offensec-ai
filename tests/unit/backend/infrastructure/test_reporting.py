"""Tests for report generation infrastructure."""

import pytest

from backend.infrastructure.reporting import MarkdownReportGenerator, PDFReportGenerator


class TestMarkdownReportGenerator:
    @pytest.mark.asyncio
    async def test_generates_empty_report(self):
        gen = MarkdownReportGenerator()
        report = await gen.generate([])
        assert "# Security Assessment Report" in report
        assert "**Total Findings:** 0" in report

    @pytest.mark.asyncio
    async def test_generates_report_with_findings(self):
        gen = MarkdownReportGenerator()
        findings = [
            {"title": "SQL Injection", "severity": "critical", "confidence": "high", "target": "10.0.0.1", "description": "SQLi in login", "remediation": "Use parameterized queries"},
            {"title": "XSS", "severity": "medium", "confidence": "medium", "target": "10.0.0.2", "description": "XSS in search"},
        ]
        report = await gen.generate(findings)
        assert "SQL Injection" in report
        assert "XSS" in report
        assert "| Critical | 1 |" in report
        assert "| Medium | 1 |" in report

    @pytest.mark.asyncio
    async def test_generates_report_with_assessment_data(self):
        gen = MarkdownReportGenerator()
        report = await gen.generate([], assessment={"name": "Test Assessment"})
        assert "Test Assessment" in report

    @pytest.mark.asyncio
    async def test_includes_remediation_when_present(self):
        gen = MarkdownReportGenerator()
        findings = [{"title": "SQLi", "severity": "high", "confidence": "high", "target": "", "description": "", "remediation": "Fix it"}]
        report = await gen.generate(findings)
        assert "### Remediation" in report
        assert "Fix it" in report


class TestPDFReportGenerator:
    @pytest.mark.asyncio
    async def test_generates_html_structure(self):
        gen = PDFReportGenerator()
        report = await gen.generate([])
        assert "<html>" in report
        assert "</html>" in report
        assert "Security Assessment Report" in report

    @pytest.mark.asyncio
    async def test_includes_finding_in_html(self):
        gen = PDFReportGenerator()
        findings = [{"title": "Test Finding", "severity": "high", "confidence": "high", "target": "host", "description": "Desc"}]
        report = await gen.generate(findings)
        assert "Test Finding" in report
        assert "Severity: high" in report
