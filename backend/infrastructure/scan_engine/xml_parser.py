"""Nmap XML output parser."""

from __future__ import annotations

import xml.etree.ElementTree as ET
from typing import Any


def parse_nmap_xml(xml_content: str) -> dict[str, Any]:
    root = ET.fromstring(xml_content)
    result: dict[str, Any] = {
        "scan_info": _parse_scan_info(root),
        "hosts": [],
    }

    for host in root.findall("host"):
        host_data = _parse_host(host)
        if host_data:
            result["hosts"].append(host_data)

    return result


def _parse_scan_info(root: ET.Element) -> dict[str, str]:
    info: dict[str, str] = {}
    nmaprun = root
    info["scanner"] = nmaprun.get("scanner", "nmap")
    info["version"] = nmaprun.get("version", "")
    info["start_time"] = nmaprun.get("start", "")
    info["args"] = nmaprun.get("args", "")

    for child in root:
        if child.tag == "verbose":
            info["verbosity"] = child.get("level", "0")
        elif child.tag == "debugging":
            info["debugging"] = child.get("level", "0")
        elif child.tag == "runstats":
            finished = child.find("finished")
            if finished is not None:
                info["finished_time"] = finished.get("time", "")
                info["elapsed"] = finished.get("elapsed", "")
                info["summary"] = finished.get("summary", "")

    return info


def _parse_host(host: ET.Element) -> dict[str, Any] | None:
    host_data: dict[str, Any] = {
        "ips": [],
        "hostnames": [],
        "ports": [],
        "os_matches": [],
        "os_guesses": [],
        "status": {},
        "scripts": [],
    }

    status = host.find("status")
    if status is not None:
        host_data["status"] = {
            "state": status.get("state", "unknown"),
            "reason": status.get("reason", ""),
        }

    for addr in host.findall("address"):
        if addr.get("addrtype") == "ipv4":
            host_data["ips"].append(addr.get("addr", ""))
        elif addr.get("addrtype") == "ipv6":
            host_data["ips"].append(addr.get("addr", ""))
        elif addr.get("addrtype") == "mac":
            host_data["mac"] = addr.get("addr", "")

    for hostname in host.findall("hostnames/hostname"):
        host_data["hostnames"].append({
            "name": hostname.get("name", ""),
            "type": hostname.get("type", ""),
        })

    for port in host.findall("ports/port"):
        port_data = _parse_port(port)
        if port_data:
            host_data["ports"].append(port_data)

    for os_match in host.findall("os/osmatch"):
        host_data["os_matches"].append({
            "name": os_match.get("name", ""),
            "accuracy": os_match.get("accuracy", ""),
            "line": os_match.get("line", ""),
        })

    for os_guess in host.findall("os/osclass"):
        host_data["os_guesses"].append({
            "vendor": os_guess.get("vendor", ""),
            "os_family": os_guess.get("osfamily", ""),
            "os_gen": os_guess.get("osgen", ""),
            "accuracy": os_guess.get("accuracy", ""),
            "type": os_guess.get("type", ""),
        })

    for script in host.findall("hostscript/script"):
        host_data["scripts"].append({
            "id": script.get("id", ""),
            "output": script.get("output", ""),
            "table": _parse_script_tables(script),
        })

    return host_data


def _parse_port(port: ET.Element) -> dict[str, Any] | None:
    if port.get("state") == "closed":
        return None

    port_data: dict[str, Any] = {
        "port": port.get("portid", ""),
        "protocol": port.get("protocol", "tcp"),
    }

    state_el = port.find("state")
    if state_el is not None:
        port_data["state"] = state_el.get("state", "unknown")
    else:
        port_data["state"] = port.get("state", "unknown")

    if port_data.get("state") in ("closed", "filtered"):
        return None

    service = port.find("service")
    if service is not None:
        port_data["service"] = service.get("name", "")
        port_data["product"] = service.get("product", "")
        port_data["version"] = service.get("version", "")
        port_data["extrainfo"] = service.get("extrainfo", "")
        port_data["tunnel"] = service.get("tunnel", "")
        port_data["method"] = service.get("method", "")
        port_data["conf"] = service.get("conf", "")

    for script in port.findall("script"):
        if "scripts" not in port_data:
            port_data["scripts"] = []
        port_data["scripts"].append({
            "id": script.get("id", ""),
            "output": script.get("output", ""),
        })

    return port_data


def _parse_script_tables(element: ET.Element) -> list[dict[str, Any]]:
    tables = []
    for table in element.findall("table"):
        table_data: dict[str, Any] = {}
        for child in table:
            if child.tag == "elem":
                key = child.get("key", "value")
                table_data[key] = child.text or ""
            elif child.tag == "table":
                if "subtables" not in table_data:
                    table_data["subtables"] = []
                sub = {e.get("key", "value"): e.text or "" for e in child.findall("elem")}
                table_data["subtables"].append(sub)
        tables.append(table_data)
    return tables
