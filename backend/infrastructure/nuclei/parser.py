"""Nuclei JSONL result parser."""

from __future__ import annotations

import json
from typing import Any


def parse_nuclei_jsonl(output: str) -> list[dict[str, Any]]:
    results: list[dict[str, Any]] = []
    for line in output.strip().split("\n"):
        line = line.strip()
        if not line:
            continue
        try:
            entry = json.loads(line)
        except json.JSONDecodeError:
            continue

        result: dict[str, Any] = {
            "template_id": entry.get("template-id", entry.get("template_id", "")),
            "template_name": entry.get("info", {}).get("name", entry.get("template", "")),
            "severity": entry.get("info", {}).get("severity", entry.get("severity", "unknown")),
            "matched_url": entry.get("matched-at", entry.get("matched_at", entry.get("url", ""))),
            "matched_at": entry.get("matched-at", entry.get("matched_at", "")),
            "protocol": entry.get("type", entry.get("protocol", "")),
            "tags": entry.get("info", {}).get("tags", []),
            "reference": entry.get("info", {}).get("reference", ""),
            "cwe": entry.get("info", {}).get("classification", {}).get("cwe", []),
            "cve": entry.get("info", {}).get("classification", {}).get("cve", []),
            "cvss_score": entry.get("info", {}).get("classification", {}).get("cvss-score", None),
            "description": entry.get("info", {}).get("description", ""),
            "remediation": entry.get("info", {}).get("remediation", ""),
            "extracted_results": entry.get("extracted-results", entry.get("extracted_results", [])),
            "host": entry.get("host", ""),
            "ip": entry.get("ip", ""),
            "port": entry.get("port", ""),
            "scheme": entry.get("scheme", ""),
            "curl_command": entry.get("curl-command", entry.get("curl_command", "")),
            "raw": entry,
        }

        if isinstance(result["tags"], str):
            result["tags"] = [t.strip() for t in result["tags"].split(",") if t.strip()]

        if isinstance(result["cwe"], str):
            result["cwe"] = [c.strip() for c in result["cwe"].split(",") if c.strip()]
        if isinstance(result["cve"], str):
            result["cve"] = [c.strip() for c in result["cve"].split(",") if c.strip()]

        results.append(result)

    return results


def parse_nuclei_json(input_str: str) -> list[dict[str, Any]]:
    stripped = input_str.strip()
    if stripped.startswith("["):
        try:
            entries = json.loads(stripped)
            flat: list[dict[str, Any]] = []
            for entry in entries:
                flat.append({
                    "template_id": entry.get("template_id", ""),
                    "template_name": entry.get("info", {}).get("name", ""),
                    "severity": entry.get("info", {}).get("severity", "unknown"),
                    "matched_url": entry.get("matched_at", ""),
                    "tags": entry.get("info", {}).get("tags", []),
                    "description": entry.get("info", {}).get("description", ""),
                    "remediation": entry.get("info", {}).get("remediation", ""),
                })
            return flat
        except json.JSONDecodeError:
            pass
    return parse_nuclei_jsonl(input_str)
