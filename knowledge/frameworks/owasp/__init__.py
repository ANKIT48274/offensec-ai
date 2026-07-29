"""OWASP Top 10 and ASVS mappings."""

OWASP_TOP_10_2021 = {
    "A01": {"id": "A01:2021", "name": "Broken Access Control", "cwes": ["CWE-22", "CWE-23", "CWE-35", "CWE-73", "CWE-284", "CWE-285", "CWE-639", "CWE-862", "CWE-863"]},
    "A02": {"id": "A02:2021", "name": "Cryptographic Failures", "cwes": ["CWE-295", "CWE-296", "CWE-297", "CWE-310", "CWE-319", "CWE-321", "CWE-322", "CWE-323", "CWE-324", "CWE-325", "CWE-326", "CWE-327"]},
    "A03": {"id": "A03:2021", "name": "Injection", "cwes": ["CWE-20", "CWE-74", "CWE-75", "CWE-77", "CWE-78", "CWE-79", "CWE-80", "CWE-83", "CWE-87", "CWE-88", "CWE-89", "CWE-90", "CWE-91"]},
    "A04": {"id": "A04:2021", "name": "Insecure Design", "cwes": ["CWE-73", "CWE-183", "CWE-209", "CWE-213", "CWE-235", "CWE-256", "CWE-257", "CWE-266", "CWE-269", "CWE-280", "CWE-302", "CWE-319", "CWE-346", "CWE-362", "CWE-384"]},
    "A05": {"id": "A05:2021", "name": "Security Misconfiguration", "cwes": ["CWE-2", "CWE-11", "CWE-13", "CWE-15", "CWE-16", "CWE-260", "CWE-315", "CWE-520", "CWE-526", "CWE-537", "CWE-538", "CWE-540", "CWE-547", "CWE-611", "CWE-614", "CWE-756"]},
    "A06": {"id": "A06:2021", "name": "Vulnerable and Outdated Components", "cwes": ["CWE-937", "CWE-1035", "CWE-1104"]},
    "A07": {"id": "A07:2021", "name": "Identification and Authentication Failures", "cwes": ["CWE-255", "CWE-259", "CWE-287", "CWE-288", "CWE-290", "CWE-291", "CWE-292", "CWE-293", "CWE-294", "CWE-295", "CWE-296", "CWE-297", "CWE-298", "CWE-299"]},
    "A08": {"id": "A08:2021", "name": "Software and Data Integrity Failures", "cwes": ["CWE-345", "CWE-353", "CWE-426", "CWE-494", "CWE-502", "CWE-565", "CWE-784", "CWE-829", "CWE-830", "CWE-915"]},
    "A09": {"id": "A09:2021", "name": "Security Logging and Monitoring Failures", "cwes": ["CWE-117", "CWE-223", "CWE-532", "CWE-778"]},
    "A10": {"id": "A10:2021", "name": "Server-Side Request Forgery", "cwes": ["CWE-918"]},
}

OWASP_ASVS = {
    "V1": "Architecture, Design and Threat Modeling",
    "V2": "Authentication Verification Requirements",
    "V3": "Session Management Verification Requirements",
    "V4": "Access Control Verification Requirements",
    "V5": "Validation, Sanitization and Encoding Verification Requirements",
    "V6": "Stored Cryptography Verification Requirements",
    "V7": "Error Handling and Logging Verification Requirements",
    "V8": "Data Protection Verification Requirements",
    "V9": "Communications Verification Requirements",
    "V10": "Malicious Code Verification Requirements",
    "V11": "Business Logic Verification Requirements",
    "V12": "File and Resources Verification Requirements",
    "V13": "API and Web Service Verification Requirements",
    "V14": "Configuration Verification Requirements",
}
