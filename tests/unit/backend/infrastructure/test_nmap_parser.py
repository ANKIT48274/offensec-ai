"""Tests for Nmap XML parser."""

from backend.infrastructure.scan_engine.xml_parser import parse_nmap_xml


SAMPLE_XML = """<?xml version="1.0"?>
<nmaprun scanner="nmap" version="7.95" start="1700000000" args="nmap -Pn -sV -sC -O -oX scan.xml 192.168.1.1">
<verbose level="0"/>
<debugging level="0"/>
<runstats><finished time="1700000100" elapsed="100" summary="1 host scanned"/></runstats>
<host><status state="up" reason="syn-ack"/>
<address addr="192.168.1.1" addrtype="ipv4"/>
<hostnames><hostname name="router.local" type="PTR"/></hostnames>
<ports>
<port protocol="tcp" portid="22">
<state state="open"/>
<service name="ssh" product="OpenSSH" version="9.0" method="probed" conf="10"/>
</port>
<port protocol="tcp" portid="80">
<state state="open"/>
<service name="http" product="Apache" version="2.4.57" method="probed" conf="10"/>
</port>
<port protocol="tcp" portid="443">
<state state="filtered"/>
</port>
</ports>
<os>
<osmatch name="Linux 5.x" accuracy="95" line="1"/>
<osclass vendor="Linux" osfamily="Linux" osgen="5.x" accuracy="95" type="general purpose"/>
</os>
<hostscript><script id="http-title" output="Apache Default Page"/></hostscript>
</host>
</nmaprun>"""


def test_parse_valid_xml():
    result = parse_nmap_xml(SAMPLE_XML)
    assert result["scan_info"]["scanner"] == "nmap"
    assert len(result["hosts"]) == 1


def test_parse_host_ip():
    result = parse_nmap_xml(SAMPLE_XML)
    host = result["hosts"][0]
    assert "192.168.1.1" in host["ips"]


def test_parse_host_status():
    result = parse_nmap_xml(SAMPLE_XML)
    assert result["hosts"][0]["status"]["state"] == "up"


def test_parse_hostname():
    result = parse_nmap_xml(SAMPLE_XML)
    names = result["hosts"][0]["hostnames"]
    assert any(n["name"] == "router.local" for n in names)


def test_parse_open_ports():
    result = parse_nmap_xml(SAMPLE_XML)
    ports = result["hosts"][0]["ports"]
    assert len(ports) == 2


def test_parse_port_details():
    result = parse_nmap_xml(SAMPLE_XML)
    ports = result["hosts"][0]["ports"]
    ssh_port = next(p for p in ports if p["port"] == "22")
    assert ssh_port["state"] == "open"
    assert ssh_port["protocol"] == "tcp"
    assert ssh_port["service"] == "ssh"
    assert ssh_port["product"] == "OpenSSH"
    assert ssh_port["version"] == "9.0"


def test_parse_http_port():
    result = parse_nmap_xml(SAMPLE_XML)
    ports = result["hosts"][0]["ports"]
    http_port = next(p for p in ports if p["port"] == "80")
    assert http_port["service"] == "http"


def test_parse_filtered_port_not_returned():
    result = parse_nmap_xml(SAMPLE_XML)
    ports = result["hosts"][0]["ports"]
    port_ids = [p["port"] for p in ports]
    assert "443" not in port_ids


def test_parse_os_match():
    result = parse_nmap_xml(SAMPLE_XML)
    os_matches = result["hosts"][0]["os_matches"]
    assert len(os_matches) == 1
    assert "Linux" in os_matches[0]["name"]


def test_parse_os_guess():
    result = parse_nmap_xml(SAMPLE_XML)
    guesses = result["hosts"][0]["os_guesses"]
    assert len(guesses) == 1
    assert guesses[0]["vendor"] == "Linux"


def test_parse_host_scripts():
    result = parse_nmap_xml(SAMPLE_XML)
    scripts = result["hosts"][0]["scripts"]
    assert len(scripts) == 1
    assert scripts[0]["id"] == "http-title"


def test_parse_empty_xml():
    result = parse_nmap_xml("<nmaprun></nmaprun>")
    assert result["hosts"] == []


def test_parse_no_hosts():
    xml = """<?xml version="1.0"?><nmaprun><runstats><finished time="0" elapsed="1" summary=""/></runstats></nmaprun>"""
    result = parse_nmap_xml(xml)
    assert result["hosts"] == []


def test_parse_scan_info_defaults():
    result = parse_nmap_xml("<nmaprun/>")
    assert result["scan_info"]["scanner"] == "nmap"
