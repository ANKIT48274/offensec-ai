"""Web application assessment methodology."""

WEB_METHODOLOGY = {
    "name": "Web Application Security Assessment",
    "version": "1.0",
    "phases": [
        {
            "name": "Information Gathering",
            "techniques": [
                "technology_fingerprinting",
                "endpoint_discovery",
                "parameter_discovery",
                "authentication_mechanism_analysis",
            ],
        },
        {
            "name": "Configuration Testing",
            "techniques": [
                "ssl_tls_testing",
                "security_headers_audit",
                "cors_configuration",
                "cookie_analysis",
            ],
        },
        {
            "name": "Input Validation Testing",
            "techniques": [
                "sql_injection",
                "cross_site_scripting",
                "cross_site_request_forgery",
                "server_side_request_forgery",
                "local_file_inclusion",
                "command_injection",
                "open_redirect",
            ],
        },
        {
            "name": "Authentication Testing",
            "techniques": [
                "credential_strength",
                "brute_force_protection",
                "session_management",
                "password_reset_flow",
            ],
        },
        {
            "name": "Authorization Testing",
            "techniques": [
                "horizontal_privilege_escalation",
                "vertical_privilege_escalation",
                "insecure_direct_object_reference",
            ],
        },
        {
            "name": "Business Logic Testing",
            "techniques": [
                "workflow_bypass",
                "race_condition",
                "integer_overflow",
                "mass_assignment",
            ],
        },
        {
            "name": "API Testing",
            "techniques": ["rate_limiting", "mass_assignment", "authentication_bypass", "injection"],
        },
    ],
}
