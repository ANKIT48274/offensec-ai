"""Web vulnerability signatures."""

WEB_SIGNATURES = {
    "sql_injection": {
        "patterns": ["' OR '1'='1", "' UNION SELECT", "'; DROP TABLE", "' WAITFOR DELAY", "1' AND 1=1--", "1' AND 1=2--"],
        "indicators": ["sql syntax error", "odbc driver", "mysql_fetch", "ora-", "unclosed quotation mark"],
        "severity": "critical",
    },
    "cross_site_scripting": {
        "patterns": ["<script>", "alert(", "onerror=", "onload=", "javascript:", "<img src=x"],
        "indicators": ["xss", "script>", "alert("],
        "severity": "high",
    },
    "path_traversal": {
        "patterns": ["../", "..\\", "%2e%2e%2f", "%252e%252e%252f"],
        "indicators": ["root:", "boot.ini", "etc/passwd", "windows\\system32"],
        "severity": "high",
    },
    "command_injection": {
        "patterns": ["; ls", "| id", "`whoami`", "$(cat /etc/passwd)", "&& ping"],
        "indicators": ["uid=", "root:", "bin/bash"],
        "severity": "critical",
    },
}
