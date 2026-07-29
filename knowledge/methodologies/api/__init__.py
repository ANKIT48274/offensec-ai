"""API security assessment methodology."""

API_METHODOLOGY = {
    "name": "API Security Assessment",
    "version": "1.0",
    "phases": [
        {"name": "Discovery", "techniques": ["endpoint_crawling", "schema_extraction", "version_detection", "authentication_mechanism_identification"]},
        {"name": "Authentication Testing", "techniques": ["token_analysis", "oauth_flow_bypass", "api_key_leakage", "jwt_weakness_analysis"]},
        {"name": "Authorization Testing", "techniques": ["idor", "rbac_bypass", "mass_assignment"]},
        {"name": "Input Validation", "techniques": ["injection", "rate_limiting_bypass", "mass_operation_abuse", "parameter_pollution"]},
    ],
}
