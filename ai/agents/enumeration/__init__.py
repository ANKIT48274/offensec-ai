"""Enumeration agent — guides detailed service and protocol enumeration."""

from __future__ import annotations

from typing import Any


class EnumerationAgent:
    """AI agent responsible for service enumeration guidance."""

    def __init__(self, model_client: Any) -> None:
        self._client = model_client

    async def generate_plan(self, services: list[dict[str, Any]], context: dict[str, Any] | None = None) -> dict[str, Any]:
        plan = {
            "agent": "enumeration",
            "services": services,
            "steps": [],
        }

        for service in services:
            name = service.get("name", "").lower()
            port = service.get("port", 0)

            if name in ("http", "https") or port in (80, 443, 8080, 8443):
                plan["steps"].append({
                    "technique": "web_enumeration",
                    "target": service.get("host", ""),
                    "port": port,
                    "tools": ["gobuster", "ffuf", "nikto", "whatweb"],
                })
            elif name == "smb" or port in (139, 445):
                plan["steps"].append({
                    "technique": "smb_enumeration",
                    "target": service.get("host", ""),
                    "port": port,
                    "tools": ["enum4linux", "smbclient", "crackmapexec"],
                })
            elif name in ("ldap", "ldaps") or port in (389, 636):
                plan["steps"].append({
                    "technique": "ldap_enumeration",
                    "target": service.get("host", ""),
                    "port": port,
                    "tools": ["ldapsearch", "ldapdomaindump"],
                })
            elif name == "mysql" or port == 3306:
                plan["steps"].append({
                    "technique": "database_enumeration",
                    "target": service.get("host", ""),
                    "port": port,
                    "tools": ["mysql"],
                })
            elif name in ("ssh", "ftp", "telnet", "rdp"):
                plan["steps"].append({
                    "technique": f"{name}_enumeration",
                    "target": service.get("host", ""),
                    "port": port,
                    "tools": [name, "hydra"],
                })

        return plan
