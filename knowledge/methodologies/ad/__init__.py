"""Active Directory assessment methodology."""

AD_METHODOLOGY = {
    "name": "Active Directory Security Assessment",
    "version": "1.0",
    "phases": [
        {
            "name": "Domain Enumeration",
            "techniques": [
                "ldap_anonymous_query",
                "user_enumeration",
                "group_membership_analysis",
                "computer_object_enumeration",
            ],
        },
        {
            "name": "Authentication Testing",
            "techniques": [
                "password_spraying",
                "asrep_roasting",
                "kerberoasting",
                "golden_ticket_analysis",
            ],
        },
        {
            "name": "Privilege Analysis",
            "techniques": [
                "acl_abuse",
                "delegation_abuse",
                "admin_sdholder",
                "group_policy_analysis",
            ],
        },
        {
            "name": "Lateral Movement",
            "techniques": [
                "pass_the_hash",
                "pass_the_ticket",
                "overpass_the_hash",
                "dcsync",
                "silver_ticket",
            ],
        },
        {
            "name": "Domain Dominance",
            "techniques": ["dcsync", "ntds_dump", "skeleton_key", "dcshadow"],
        },
    ],
}
