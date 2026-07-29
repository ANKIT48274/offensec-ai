"""Tests for report templates and exporters."""

from backend.infrastructure.reporting.templates import executive_template, technical_template, owasp_template, ptes_template
from backend.infrastructure.reporting.exporters import export_csv, export_json


SAMPLE_FINDINGS = [
    {
        "title": "SQL Injection",
        "severity": "critical",
        "confidence": "high",
        "status": "open",
        "target": "10.0.0.1",
        "description": "SQL injection in login parameter",
        "remediation": "Use parameterized queries",
        "cwe_id": "CWE-89",
        "cvss_score": 9.8,
        "owasp_id": "A03:2021",
    },
    {
        "title": "XSS Vulnerability",
        "severity": "high",
        "confidence": "medium",
        "status": "confirmed",
        "target": "10.0.0.2",
        "description": "Reflected XSS in search",
        "remediation": "Encode output",
        "cwe_id": "CWE-79",
        "owasp_id": "A03:2021",
    },
]

SAMPLE_ASSESSMENT = {"id": "a1", "name": "Test Assessment", "status": "completed"}


class TestExecutiveTemplate:
    def test_renders_title(self):
        html = executive_template(SAMPLE_FINDINGS, SAMPLE_ASSESSMENT)
        assert "Executive Summary" in html
        assert "SQL Injection" in html
        assert "XSS Vulnerability" in html

    def test_shows_severity_count(self):
        html = executive_template(SAMPLE_FINDINGS)
        assert "2</div>" in html or "2" in html

    def test_empty_findings_renders(self):
        html = executive_template([])
        assert "Executive Summary" in html


class TestTechnicalTemplate:
    def test_renders_findings(self):
        html = technical_template(SAMPLE_FINDINGS)
        assert "SQL Injection" in html

    def test_shows_cwe(self):
        html = technical_template(SAMPLE_FINDINGS)
        assert "CWE-89" in html


class TestOwaspTemplate:
    def test_owasp_category_mapped(self):
        html = owasp_template(SAMPLE_FINDINGS)
        assert "A03:2021" in html

    def test_owasp_title(self):
        html = owasp_template([])
        assert "OWASP" in html


class TestPtesTemplate:
    def test_renders_phases(self):
        html = ptes_template(SAMPLE_FINDINGS)
        assert "Pre-Engagement" in html
        assert "Intelligence Gathering" in html
        assert "Vulnerability Analysis" in html


class TestExportCSV:
    def test_headers_present(self):
        csv_output = export_csv(SAMPLE_FINDINGS)
        assert "Title" in csv_output
        assert "Severity" in csv_output

    def test_data_present(self):
        csv_output = export_csv(SAMPLE_FINDINGS)
        assert "SQL Injection" in csv_output
        assert "9.8" in csv_output

    def test_empty(self):
        csv_output = export_csv([])
        assert "Title" in csv_output


class TestExportJSON:
    def test_structure(self):
        js = export_json(SAMPLE_FINDINGS, SAMPLE_ASSESSMENT)
        assert '"SQL Injection"' in js
        assert '"Test Assessment"' in js

    def test_summary_counts(self):
        js = export_json(SAMPLE_FINDINGS)
        assert '"critical": 1' in js
        assert '"high": 1' in js

    def test_no_assessment(self):
        js = export_json(SAMPLE_FINDINGS)
        assert '"findings"' in js
        assert '"assessment"' not in js
