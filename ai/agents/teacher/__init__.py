"""Teaching agent — provides contextual explanations and methodology guidance."""

from __future__ import annotations

from typing import Any


class TeacherAgent:
    """AI agent responsible for educational guidance."""

    def __init__(self, model_client: Any) -> None:
        self._client = model_client

    async def explain_technique(self, technique: str, context: dict[str, Any] | None = None) -> str:
        explanations = {
            "port_scanning": (
                "Port scanning identifies open ports and services on a target. "
                "This is the first step in understanding the attack surface. "
                "Use nmap for comprehensive scans with service version detection (-sV) "
                "and default scripts (-sC). Start with top 1000 ports, then expand."
            ),
            "web_enumeration": (
                "Web enumeration discovers hidden directories, files, and parameters. "
                "Use ffuf or gobuster with a quality wordlist. "
                "Check for common paths, admin interfaces, and API endpoints."
            ),
            "sql_injection": (
                "SQL injection occurs when user input is unsafely concatenated into SQL queries. "
                "Test entry points with single quotes, time-based payloads, and UNION attacks. "
                "Use sqlmap for automated detection and exploitation."
            ),
            "privilege_escalation": (
                "Privilege escalation involves gaining higher-level access on a compromised host. "
                "Check for SUID binaries, writable scripts, kernel exploits, "
                "misconfigured sudo rules, and stored credentials."
            ),
            "active_directory": (
                "Active Directory assessments focus on domain trust relationships, "
                "Kerberos attacks (AS-REP roasting, Kerberoasting), ACL abuse, "
                "and lateral movement via WinRM, SMB, or scheduled tasks."
            ),
        }
        return explanations.get(technique.lower(), f"Technique '{technique}' explanation is not available.")

    async def assess_skill(self, actions: list[dict[str, Any]]) -> dict[str, Any]:
        return {
            "estimated_level": "intermediate",
            "strengths": [],
            "areas_for_improvement": [],
            "recommended_topics": [],
        }

    async def recommend_next_steps(self, completed_steps: list[str], available_techniques: list[str]) -> list[str]:
        recommendations = [t for t in available_techniques if t not in completed_steps]
        return recommendations[:3]
