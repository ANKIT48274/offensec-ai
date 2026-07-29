"""AI evidence correlator — analyzes scan results and generates findings."""

from __future__ import annotations

from typing import Any

WEAK_PROTOCOLS = {"ftp", "telnet", "rlogin", "rsh", "tftp"}
HIGH_RISK_PORTS = {"23": "telnet", "21": "ftp", "445": "smb", "135": "rpc", "139": "netbios", "3389": "rdp"}
OUTDATED_SIGNATURES = {"OpenSSH_7", "Apache/2.2", "Apache/2.4", "nginx/1.1.", "nginx/1.2.", "nginx/1.3.", "nginx/1.4."}


def correlate(assets: list[dict[str, Any]], nuclei: list[dict[str, Any]], scans: list[dict[str, Any]], httpx_data: list[dict[str, Any]]) -> dict[str, Any]:
    analysis: dict[str, Any] = {
        "executive_summary": "",
        "attack_surface": _analyze_attack_surface(assets),
        "critical_assets": _find_critical_assets(assets, nuclei),
        "top_risks": _rank_risks(nuclei, assets),
        "attack_paths": _build_attack_paths(assets, nuclei),
        "recommendations": [],
        "risk_score": 0,
    }

    score = analysis["attack_surface"]["score"]
    for risk in analysis["top_risks"]:
        score = max(score, risk.get("score", 0))

    tech_stack = _extract_tech_stack(assets)
    outdated = _detect_outdated(assets, httpx_data)
    weak_protos = _detect_weak_protocols(assets)
    exposed = _detect_exposed_services(assets)

    recs = list(analysis.get("recommendations", []))
    for o in outdated:
        recs.append(f"Upgrade {o['name']} ({o['version']}) to latest version")
    if exposed:
        recs.append("Restrict access to sensitive services using firewall rules")
    for p in weak_protos:
        recs.append(f"Disable or replace weak protocol: {p}")
    if nuclei:
        critical_count = len([n for n in nuclei if n.get("severity") == "critical"])
        if critical_count > 0:
            recs.insert(0, f"Address {critical_count} critical vulnerabilities immediately")
    recs.append("Run authenticated scans to identify deep vulnerabilities")
    recs.append("Implement Web Application Firewall (WAF) for exposed web services")
    analysis["recommendations"] = recs[:8]

    analysis["risk_score"] = min(score, 100)

    analysis["executive_summary"] = _build_summary(analysis["risk_score"], assets, nuclei, outdated, tech_stack)

    return analysis


def _build_summary(risk_score: int, assets: list, nuclei: list, outdated: list, tech_stack: list) -> str:
    parts = []
    if risk_score >= 70:
        parts.append("High-risk environment identified.")
    elif risk_score >= 40:
        parts.append("Moderate security risk detected.")
    else:
        parts.append("Low immediate risk, with improvement opportunities.")

    host_count = len(assets)
    vuln_count = len(nuclei)
    parts.append(f"Assessment covered {host_count} assets and identified {vuln_count} findings.")

    if outdated:
        names = ", ".join(set(o["name"] for o in outdated[:3]))
        parts.append(f"Outdated software detected: {names}.")

    high_ports = sum(1 for a in assets for p in (a.get("ports") or []) if str(p.get("port")) in HIGH_RISK_PORTS)
    if high_ports:
        parts.append(f"{high_ports} high-risk services exposed ({', '.join(HIGH_RISK_PORTS[str(p.get('port'))] for a in assets for p in (a.get('ports') or []) if str(p.get('port')) in HIGH_RISK_PORTS)}).")

    if tech_stack:
        parts.append(f"Technology stack includes {', '.join(tech_stack[:4])}.")

    return " ".join(parts)


def _analyze_attack_surface(assets: list) -> dict:
    total_hosts = len(assets)
    total_ports = sum(len(a.get("ports") or []) for a in assets)
    open_ports = sum(1 for a in assets for p in (a.get("ports") or []) if "open" in str(p.get("state", "")).lower())

    score = 10
    if total_hosts > 5:
        score += 10
    if total_ports > 20:
        score += 10
    if open_ports > 10:
        score += 10
    high = sum(1 for a in assets for p in (a.get("ports") or []) if str(p.get("port")) in HIGH_RISK_PORTS)
    score += high * 5

    return {"total_hosts": total_hosts, "total_ports": total_ports, "open_ports": open_ports, "high_risk_ports": high, "score": min(score, 100)}


def _find_critical_assets(assets: list, nuclei: list) -> list:
    critical_ids = set(n.get("matched_url", n.get("target", "")) for n in nuclei if n.get("severity") == "critical")

    critical = []
    for a in assets:
        val = a.get("value", "")
        if val in critical_ids:
            critical.append({"value": val, "type": a.get("asset_type", "unknown"), "reason": "Critical vulnerability found"})
            continue
        for p in (a.get("ports") or []):
            if str(p.get("port")) in HIGH_RISK_PORTS:
                critical.append({"value": val, "type": a.get("asset_type", "unknown"), "reason": f"High-risk port {p.get('port')}/{p.get('protocol')} exposed"})
                break

    return critical


def _rank_risks(nuclei: list, assets: list) -> list:
    sev_order = {"critical": 0, "high": 1, "medium": 2, "low": 3, "info": 4}
    sorted_nuc = sorted(nuclei, key=lambda n: sev_order.get(n.get("severity", "info"), 99))

    risks = []
    for n in sorted_nuc[:10]:
        score = 90 if n.get("severity") == "critical" else 70 if n.get("severity") == "high" else 50 if n.get("severity") == "medium" else 20
        risks.append({
            "title": n.get("template_name", n.get("template_id", "Unknown")),
            "severity": n.get("severity"),
            "target": n.get("matched_url", n.get("target", "")),
            "score": score,
        })
    return risks


def _build_attack_paths(assets: list, nuclei: list) -> list:
    paths = []
    for n in nuclei:
        if n.get("severity") in ("critical", "high"):
            paths.append({
                "source": "external",
                "destination": n.get("matched_url", n.get("target", "")),
                "technique": n.get("template_id", "Unknown"),
                "score": 85 if n.get("severity") == "critical" else 60,
                "evidence": [n.get("template_name", ""), n.get("description", "")][:2],
            })
    return paths


def _extract_tech_stack(assets: list) -> list:
    seen = set()
    stack = []
    for a in assets:
        for t in (a.get("technologies") or []):
            if t not in seen:
                seen.add(t)
                stack.append(t)
    return stack


def _detect_outdated(assets: list, httpx_data: list) -> list:
    outdated = []
    for h in httpx_data:
        server = (h.get("server") or "").lower()
        for sig in OUTDATED_SIGNATURES:
            if server.startswith(sig.lower()):
                outdated.append({"name": h.get("server", "unknown"), "version": h.get("server", ""), "target": h.get("url", "")})
                break
    for a in assets:
        for p in (a.get("ports") or []):
            svc = str(p.get("service", ""))
            for sig in OUTDATED_SIGNATURES:
                if svc.lower().startswith(sig.lower()):
                    outdated.append({"name": svc, "version": svc, "target": str(a.get("value", ""))})
    return outdated[:5]


def _detect_weak_protocols(assets: list) -> list:
    weak = []
    for a in assets:
        for p in (a.get("ports") or []):
            svc = (p.get("service") or "").lower()
            if svc in WEAK_PROTOCOLS:
                weak.append(f"{svc} on {a.get('value', '')}:{p.get('port')}")
    return weak


def _detect_exposed_services(assets: list) -> list:
    exposed = []
    for a in assets:
        for p in (a.get("ports") or []):
            port = str(p.get("port"))
            if port in HIGH_RISK_PORTS:
                exposed.append({"service": HIGH_RISK_PORTS[port], "port": port, "host": a.get("value", "")})
    return exposed
