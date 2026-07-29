"""Assessment planning strategies for different engagement types."""

from __future__ import annotations

from typing import Any


class PlanningStrategy:
    """Base class for assessment planning strategies."""

    async def generate_plan(
        self, scope: dict[str, Any], context: dict[str, Any] | None = None
    ) -> list[dict[str, Any]]:
        raise NotImplementedError


class WebAssessmentStrategy(PlanningStrategy):
    """Strategy for web application security assessments."""

    async def generate_plan(
        self, scope: dict[str, Any], context: dict[str, Any] | None = None
    ) -> list[dict[str, Any]]:
        return [
            {
                "phase": "reconnaissance",
                "techniques": [
                    "target_discovery",
                    "technology_fingerprinting",
                    "endpoint_discovery",
                ],
            },
            {
                "phase": "enumeration",
                "techniques": [
                    "directory_bruteforce",
                    "parameter_discovery",
                    "subdomain_enumeration",
                ],
            },
            {
                "phase": "vulnerability_analysis",
                "techniques": ["sqli", "xss", "csrf", "ssrf", "lfi", "authentication_bypass"],
            },
            {
                "phase": "exploitation_planning",
                "techniques": ["privilege_escalation", "data_exfiltration", "pivoting"],
            },
        ]


class NetworkAssessmentStrategy(PlanningStrategy):
    """Strategy for network infrastructure assessments."""

    async def generate_plan(
        self, scope: dict[str, Any], context: dict[str, Any] | None = None
    ) -> list[dict[str, Any]]:
        return [
            {
                "phase": "discovery",
                "techniques": ["host_discovery", "port_scanning", "service_detection"],
            },
            {
                "phase": "enumeration",
                "techniques": ["os_fingerprinting", "version_detection", "banner_grabbing"],
            },
            {
                "phase": "vulnerability_scanning",
                "techniques": [
                    "cve_matching",
                    "misconfiguration_audit",
                    "default_credential_check",
                ],
            },
            {
                "phase": "exploitation_planning",
                "techniques": ["network_pivoting", "vlan_hopping", "sniffing"],
            },
        ]


class ADAssessmentStrategy(PlanningStrategy):
    """Strategy for Active Directory security assessments."""

    async def generate_plan(
        self, scope: dict[str, Any], context: dict[str, Any] | None = None
    ) -> list[dict[str, Any]]:
        return [
            {
                "phase": "domain_enumeration",
                "techniques": ["ldap_query", "user_enumeration", "group_membership_analysis"],
            },
            {
                "phase": "authentication_testing",
                "techniques": ["asrep_roasting", "kerberoasting", "password_spraying"],
            },
            {
                "phase": "privilege_analysis",
                "techniques": ["acl_abuse", "delegation_abuse", "admin_sdholder"],
            },
            {
                "phase": "lateral_movement",
                "techniques": ["pass_the_hash", "pass_the_ticket", "dcsync", "silver_ticket"],
            },
        ]


class APIAssessmentStrategy(PlanningStrategy):
    """Strategy for API security assessments."""

    async def generate_plan(
        self, scope: dict[str, Any], context: dict[str, Any] | None = None
    ) -> list[dict[str, Any]]:
        return [
            {
                "phase": "api_discovery",
                "techniques": ["endpoint_crawling", "schema_extraction", "version_detection"],
            },
            {
                "phase": "authentication_testing",
                "techniques": ["token_analysis", "oauth_flow_bypass", "api_key_rotation"],
            },
            {
                "phase": "authorization_testing",
                "techniques": ["idors", "rbac_bypass", "mass_assignment"],
            },
            {
                "phase": "input_validation",
                "techniques": ["injection", "rate_limiting_bypass", "mass_operation_abuse"],
            },
        ]
