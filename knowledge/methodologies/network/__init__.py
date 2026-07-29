"""Network infrastructure assessment methodology."""

NETWORK_METHODOLOGY = {
    "name": "Network Infrastructure Security Assessment",
    "version": "1.0",
    "phases": [
        {"name": "Discovery", "techniques": ["host_discovery", "port_scanning", "service_detection", "os_fingerprinting"]},
        {"name": "Enumeration", "techniques": ["version_detection", "banner_grabbing", "vulnerability_scanning", "default_credential_check"]},
        {"name": "Network Architecture Analysis", "techniques": ["firewall_rule_detection", "vlan_segmentation", "network_topology_mapping"]},
    ],
}
