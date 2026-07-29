"""Cloud security assessment methodology."""

CLOUD_METHODOLOGY = {
    "name": "Cloud Security Assessment",
    "version": "1.0",
    "providers": ["aws", "azure", "gcp"],
    "phases": [
        {
            "name": "Reconnaissance",
            "techniques": [
                "service_discovery",
                "permission_enumeration",
                "resource_inventory",
                "public_exposure_audit",
            ],
        },
        {
            "name": "Identity and Access Management",
            "techniques": [
                "role_abuse",
                "policy_analysis",
                "trust_relationship",
                "federation_misconfiguration",
            ],
        },
        {
            "name": "Storage Security",
            "techniques": ["public_bucket_discovery", "encryption_audit", "access_control_audit"],
        },
    ],
}
