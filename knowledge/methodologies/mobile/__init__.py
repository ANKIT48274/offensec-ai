"""Mobile application assessment methodology."""

MOBILE_METHODOLOGY = {
    "name": "Mobile Application Security Assessment",
    "version": "1.0",
    "platforms": ["android", "ios"],
    "phases": [
        {
            "name": "Static Analysis",
            "techniques": [
                "binary_analysis",
                "manifest_audit",
                "permission_analysis",
                "hardcoded_secret_detection",
            ],
        },
        {
            "name": "Dynamic Analysis",
            "techniques": [
                "traffic_interception",
                "ssl_pinning_bypass",
                "runtime_injection",
                "memory_dump_analysis",
            ],
        },
        {
            "name": "API Testing",
            "techniques": [
                "endpoint_security",
                "authentication_flow",
                "data_storage",
                "session_management",
            ],
        },
    ],
}
