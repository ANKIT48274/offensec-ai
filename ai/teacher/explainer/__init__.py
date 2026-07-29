"""Explainer — generates human-readable explanations of security concepts."""

from __future__ import annotations

from typing import Any


class Explainer:
    def explain_finding(self, finding: dict[str, Any]) -> str:
        severity = finding.get("severity", "unknown")
        technique = finding.get("technique", "")
        target = finding.get("target", "")
        parts = [f"A {severity}-severity issue was identified"]
        if technique:
            parts.append(f"involving {technique.replace('_', ' ')}")
        if target:
            parts.append(f"on {target}")
        parts.append(".")
        return " ".join(parts)

    def explain_technique_steps(self, technique: str) -> list[str]:
        guides = {
            "port_scanning": [
                "Identify the target IP range or hostname",
                "Run nmap with -sV for version detection",
                "Analyze open ports and running services",
            ],
            "sql_injection": [
                "Identify input parameters in the application",
                "Inject test payloads (single quote, time-based)",
                "Observe response differences to confirm vulnerability",
            ],
            "privilege_escalation": [
                "Gather system information (kernel, OS, users)",
                "Check for SUID/GUID binaries",
                "Search for stored credentials and configuration files",
            ],
        }
        return guides.get(technique, ["No step-by-step guide available."])
