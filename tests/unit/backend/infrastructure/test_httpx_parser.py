"""Tests for HTTPX JSONL parser."""

from backend.infrastructure.pipeline.httpx_parser import parse_httpx_json, parse_httpx_jsonl


SAMPLE_JSONL = """{"url":"https://example.com","status_code":200,"title":"Example Domain","tech":["HTTP/3"],"webserver":"ECS","content_length":1256}
{"url":"http://test.local/login","status_code":302,"title":"Redirecting...","webserver":"nginx","content_length":0,"redirect":"http://test.local/dashboard"}
{"url":"https://secure.local","status_code":200,"title":"Secure App","tech":["React","Express"],"webserver":"nginx/1.24","content_length":4096,"websocket":"socket.io"}
"""

SAMPLE_JSON = """[{"url":"https://api.local","status_code":200,"title":"API","tech":["FastAPI","Python"],"webserver":"uvicorn"}]"""


class TestHttpxJsonlParser:
    def test_parse_single_entry(self):
        result = parse_httpx_jsonl(SAMPLE_JSONL)
        assert len(result) == 3

    def test_parse_url(self):
        result = parse_httpx_jsonl(SAMPLE_JSONL)
        assert result[0]["url"] == "https://example.com"

    def test_parse_status_code(self):
        result = parse_httpx_jsonl(SAMPLE_JSONL)
        assert result[0]["status_code"] == 200
        assert result[1]["status_code"] == 302

    def test_parse_title(self):
        result = parse_httpx_jsonl(SAMPLE_JSONL)
        assert result[0]["title"] == "Example Domain"
        assert result[2]["title"] == "Secure App"

    def test_parse_tech(self):
        result = parse_httpx_jsonl(SAMPLE_JSONL)
        assert "React" in result[2]["tech"]
        assert "Express" in result[2]["tech"]

    def test_parse_server(self):
        result = parse_httpx_jsonl(SAMPLE_JSONL)
        assert result[1]["server"] == "nginx"

    def test_parse_content_length(self):
        result = parse_httpx_jsonl(SAMPLE_JSONL)
        assert result[0]["content_length"] == 1256

    def test_parse_redirect(self):
        result = parse_httpx_jsonl(SAMPLE_JSONL)
        assert result[1]["redirect_url"] == "http://test.local/dashboard"

    def test_parse_websocket(self):
        result = parse_httpx_jsonl(SAMPLE_JSONL)
        assert result[2]["websocket"] == "socket.io"

    def test_parse_empty(self):
        assert parse_httpx_jsonl("") == []

    def test_parse_invalid_lines(self):
        assert parse_httpx_jsonl("not json\nstill not") == []

    def test_parse_json_format(self):
        result = parse_httpx_json(SAMPLE_JSON)
        assert len(result) == 1
        assert result[0]["title"] == "API"
        assert "FastAPI" in result[0]["tech"]

    def test_tls_data_not_present(self):
        result = parse_httpx_jsonl(SAMPLE_JSONL)
        assert result[0]["tls_data"] is None
