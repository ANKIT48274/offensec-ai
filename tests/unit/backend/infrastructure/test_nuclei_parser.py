"""Tests for Nuclei JSONL parser."""

from backend.infrastructure.nuclei.parser import parse_nuclei_jsonl, parse_nuclei_json


SAMPLE_JSONL = """{"template-id":"wordpress-xss","info":{"name":"WordPress XSS","severity":"high","tags":["wordpress","xss"],"description":"Cross-site scripting in WordPress","remediation":"Update WordPress to latest version","classification":{"cwe":["CWE-79"],"cve":["CVE-2024-1234"],"cvss-score":"7.5"}},"host":"example.com","matched-at":"http://example.com/wp-admin","type":"http","port":"80","scheme":"http"}
{"template-id":"nginx-version","info":{"name":"Nginx Version Disclosure","severity":"info","tags":["nginx","disclosure"],"classification":{"cwe":["CWE-200"]}},"host":"example.com","matched-at":"http://example.com/","type":"http"}
{"template-id":"basic-auth","info":{"name":"Basic Auth Detected","severity":"medium","tags":["auth","misconfig"],"reference":"https://example.com/basic-auth"},"host":"test.local","matched-at":"http://test.local/admin","type":"http"}
"""


class TestNucleiJsonlParser:
    def test_parse_valid(self):
        result = parse_nuclei_jsonl(SAMPLE_JSONL)
        assert len(result) == 3

    def test_template_id(self):
        result = parse_nuclei_jsonl(SAMPLE_JSONL)
        assert result[0]["template_id"] == "wordpress-xss"

    def test_template_name(self):
        result = parse_nuclei_jsonl(SAMPLE_JSONL)
        assert result[0]["template_name"] == "WordPress XSS"

    def test_severity(self):
        result = parse_nuclei_jsonl(SAMPLE_JSONL)
        assert result[0]["severity"] == "high"
        assert result[1]["severity"] == "info"

    def test_matched_url(self):
        result = parse_nuclei_jsonl(SAMPLE_JSONL)
        assert result[0]["matched_url"] == "http://example.com/wp-admin"

    def test_tags(self):
        result = parse_nuclei_jsonl(SAMPLE_JSONL)
        assert "wordpress" in result[0]["tags"]
        assert "xss" in result[0]["tags"]

    def test_cwe(self):
        result = parse_nuclei_jsonl(SAMPLE_JSONL)
        assert "CWE-79" in result[0]["cwe"]

    def test_cve(self):
        result = parse_nuclei_jsonl(SAMPLE_JSONL)
        assert "CVE-2024-1234" in result[0]["cve"]

    def test_cvss(self):
        result = parse_nuclei_jsonl(SAMPLE_JSONL)
        assert result[0]["cvss_score"] == "7.5"

    def test_description(self):
        result = parse_nuclei_jsonl(SAMPLE_JSONL)
        assert "Cross-site" in result[0]["description"]

    def test_remediation(self):
        result = parse_nuclei_jsonl(SAMPLE_JSONL)
        assert "Update WordPress" in result[0]["remediation"]

    def test_reference(self):
        result = parse_nuclei_jsonl(SAMPLE_JSONL)
        assert "https://example.com/basic-auth" in result[2]["reference"]

    def test_protocol(self):
        result = parse_nuclei_jsonl(SAMPLE_JSONL)
        assert result[0]["protocol"] == "http"

    def test_tags_as_string_coerced(self):
        line = '{"template-id":"test","info":{"name":"Test","severity":"low","tags":"one,two,three"}}'
        result = parse_nuclei_jsonl(line)
        assert isinstance(result[0]["tags"], list)
        assert "one" in result[0]["tags"]

    def test_empty_returns_empty(self):
        assert parse_nuclei_jsonl("") == []

    def test_invalid_lines_skipped(self):
        assert parse_nuclei_jsonl("not json\nstill not") == []

    def test_json_array_format(self):
        js = '[{"template_id":"xss","info":{"name":"XSS","severity":"high","tags":["xss"]}},{"template_id":"sqli","info":{"name":"SQLi","severity":"critical","tags":["sqli"]}}]'
        result = parse_nuclei_json(js)
        assert len(result) == 2
        assert result[0]["template_id"] == "xss"
