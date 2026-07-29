"""HTTPX result parser — parses JSONL output from httpx tool."""

from __future__ import annotations

import json
from typing import Any


def parse_httpx_jsonl(output: str) -> list[dict[str, Any]]:
    results: list[dict[str, Any]] = []
    for line in output.strip().split("\n"):
        line = line.strip()
        if not line:
            continue
        try:
            entry = json.loads(line)
        except json.JSONDecodeError:
            continue

        results.append({
            "url": entry.get("url", ""),
            "status_code": entry.get("status_code"),
            "title": entry.get("title"),
            "tech": entry.get("tech", []),
            "server": entry.get("webserver", entry.get("server")),
            "content_length": entry.get("content_length"),
            "redirect_url": entry.get("redirect", entry.get("location")),
            "websocket": entry.get("websocket"),
            "tls_data": {
                "subject_cn": entry.get("tls_subject_cn"),
                "issuer_cn": entry.get("tls_issuer_cn"),
                "not_before": entry.get("tls_not_before"),
                "not_after": entry.get("tls_not_after"),
                "dns_names": entry.get("tls_dns_names", []),
            } if entry.get("tls_subject_cn") else None,
            "favicon_hash": entry.get("favicon_hash", entry.get("favicon")),
            "raw": entry,
        })
    return results


def parse_httpx_json(input_str: str) -> list[dict[str, Any]]:
    if input_str.startswith("["):
        try:
            return json.loads(input_str)
        except json.JSONDecodeError:
            pass
    return parse_httpx_jsonl(input_str)
