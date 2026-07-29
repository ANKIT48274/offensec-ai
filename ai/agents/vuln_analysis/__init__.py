"""Vulnerability analysis agent — identifies and classifies security issues."""

from __future__ import annotations

from typing import Any


class VulnerabilityAnalysisAgent:
    """AI agent responsible for vulnerability identification and classification."""

    def __init__(self, model_client: Any) -> None:
        self._client = model_client

    async def analyze(
        self, evidence: list[dict[str, Any]], context: dict[str, Any] | None = None
    ) -> list[dict[str, Any]]:
        findings = []

        for item in evidence:
            service = item.get("service", "").lower()
            version = item.get("version", "")

            finding = self._check_known_vulnerabilities(service, version)
            if finding:
                findings.append(finding)

        return findings

    def _check_known_vulnerabilities(self, service: str, version: str) -> dict[str, Any] | None:
        checks = {
            "openssh": {"vulnerable_versions": ["< 8.9"], "severity": "high", "cwe": "CWE-787"},
            "apache httpd": {
                "vulnerable_versions": ["< 2.4.54"],
                "severity": "high",
                "cwe": "CWE-416",
            },
            "nginx": {"vulnerable_versions": ["< 1.22.1"], "severity": "medium", "cwe": "CWE-200"},
            "mysql": {"vulnerable_versions": ["< 8.0.30"], "severity": "high", "cwe": "CWE-89"},
            "samba": {"vulnerable_versions": ["< 4.15.0"], "severity": "critical", "cwe": "CWE-94"},
        }

        check = checks.get(service)
        if not check:
            return None

        return {
            "title": f"Outdated {service} version detected",
            "description": f"{service} version {version} may contain known vulnerabilities including CWE-{check['cwe']}",
            "severity": check["severity"],
            "confidence": "medium",
            "service": service,
            "version": version,
            "cwe_id": check["cwe"],
            "remediation": f"Upgrade {service} to the latest stable version",
        }
