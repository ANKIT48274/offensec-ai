"""Report HTML templates for multiple styles."""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any


def _base_html(content: str, title: str = "Security Assessment Report", css: str = "") -> str:
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>{title}</title>
<style>
body {{ font-family: 'Segoe UI', Arial, sans-serif; color: #1a1a2e; margin: 0; padding: 20px; background: #f8f9fa; }}
h1 {{ color: #1a1a2e; border-bottom: 3px solid #e94560; padding-bottom: 10px; }}
h2 {{ color: #16213e; margin-top: 30px; }}
h3 {{ color: #0f3460; }}
table {{ width: 100%; border-collapse: collapse; margin: 15px 0; }}
th, td {{ padding: 10px 12px; text-align: left; border-bottom: 1px solid #dee2e6; }}
th {{ background: #16213e; color: white; }}
.finding {{ background: white; border: 1px solid #dee2e6; border-radius: 8px; padding: 16px; margin: 12px 0; }}
.severity-critical {{ border-left: 4px solid #dc3545; }} .severity-high {{ border-left: 4px solid #fd7e14; }}
.severity-medium {{ border-left: 4px solid #ffc107; }} .severity-low {{ border-left: 4px solid #28a745; }}
.badge {{ display: inline-block; padding: 2px 8px; border-radius: 4px; font-size: 11px; font-weight: 700; text-transform: uppercase; }}
.critical {{ background: #dc3545; color: white; }} .high {{ background: #fd7e14; color: white; }}
.medium {{ background: #ffc107; color: #212529; }} .low {{ background: #28a745; color: white; }}
.info {{ background: #17a2b8; color: white; }}
.summary-box {{ display: flex; gap: 16px; margin: 20px 0; flex-wrap: wrap; }}
.stat {{ background: white; border: 1px solid #dee2e6; border-radius: 8px; padding: 20px; text-align: center; min-width: 120px; }}
.stat-value {{ font-size: 28px; font-weight: 700; }} .stat-label {{ font-size: 12px; color: #6c757d; }}
.remediation {{ background: #fff3cd; border: 1px solid #ffc107; border-radius: 4px; padding: 10px; margin-top: 8px; }}
.evidence {{ background: #f8f9fa; border: 1px solid #dee2e6; border-radius: 4px; padding: 8px; font-family: monospace; font-size: 12px; white-space: pre-wrap; }}
.header {{ background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%); color: white; padding: 30px; border-radius: 8px; margin-bottom: 20px; }}
.header h1 {{ color: white; border: none; }} .header p {{ color: #a8b2c1; }}
.footer {{ text-align: center; color: #6c757d; font-size: 11px; margin-top: 40px; padding-top: 20px; border-top: 1px solid #dee2e6; }}
</style>
{css}
</head>
<body>
{content}
</body>
</html>"""


def _severity_badge(severity: str) -> str:
    return f'<span class="badge {severity}">{severity}</span>'


def _stat_card(value: str | int, label: str) -> str:
    return f'<div class="stat"><div class="stat-value">{value}</div><div class="stat-label">{label}</div></div>'


def executive_template(
    findings: list[dict[str, Any]], assessment: dict[str, Any] | None = None
) -> str:
    critical = len([f for f in findings if f.get("severity") == "critical"])
    high = len([f for f in findings if f.get("severity") == "high"])
    medium = len([f for f in findings if f.get("severity") == "medium"])
    low = len([f for f in findings if f.get("severity") == "low"])
    total = len(findings)

    body = f"""<div class="header">
<h1>Executive Summary</h1>
<p>Security Assessment Report — {assessment.get("name", "N/A") if assessment else "N/A"} | Generated: {datetime.now(UTC).strftime("%Y-%m-%d %H:%M UTC")}</p>
</div>
<div class="summary-box">
{_stat_card(total, "Total Findings")}{_stat_card(critical, "Critical")}{_stat_card(high, "High")}{_stat_card(medium, "Medium")}{_stat_card(low, "Low")}
</div>
<h2>Risk Overview</h2>
<p>This assessment identified <strong>{total}</strong> findings: {critical} critical, {high} high, {medium} medium, and {low} low severity.</p>
{"<p><strong>Immediate action required:</strong> Critical findings demand urgent remediation.</p>" if critical > 0 else ""}
{"<p>High-severity findings should be addressed within the next remediation cycle.</p>" if high > 0 else ""}
<h2>Top Findings</h2>
"""
    for f in sorted(
        findings,
        key=lambda x: {"critical": 0, "high": 1, "medium": 2, "low": 3}.get(x.get("severity"), 99),
    )[:10]:
        body += f"""<div class="finding severity-{f.get("severity")}">
<h3>{f.get("title", "Untitled")} {_severity_badge(f.get("severity", "none"))}</h3>
<p>{f.get("description", "")[:300]}</p>
{"<p><strong>Target:</strong> " + f.get("target", "") + "</p>" if f.get("target") else ""}
</div>"""

    body += f"""<h2>Recommendations</h2>
<ol>
{"<li>Remediate all critical and high-severity findings immediately.</li>" if critical + high > 0 else ""}
<li>Conduct a follow-up assessment after remediation to verify fixes.</li>
<li>Implement a regular security assessment schedule.</li>
<li>Ensure all systems are patched and up to date.</li>
</ol>
<div class="footer"><p>Confidential — For authorized recipients only.</p></div>"""
    return _base_html(body, "Executive Summary — Security Assessment")


def technical_template(
    findings: list[dict[str, Any]], assessment: dict[str, Any] | None = None
) -> str:
    critical = len([f for f in findings if f.get("severity") == "critical"])
    high = len([f for f in findings if f.get("severity") == "high"])
    total = len(findings)

    body = f"""<div class="header">
<h1>Technical Security Assessment Report</h1>
<p>{assessment.get("name", "N/A") if assessment else "N/A"} | Generated: {datetime.now(UTC).strftime("%Y-%m-%d %H:%M UTC")}</p>
</div>
<div class="summary-box">
{_stat_card(total, "Total Findings")}{_stat_card(critical, "Critical")}{_stat_card(high, "High")}
</div>
<h2>Summary</h2>
<table><tr><th>Severity</th><th>Count</th></tr>
<tr><td>Critical</td><td>{critical}</td></tr>
<tr><td>High</td><td>{high}</td></tr>
<tr><td>Medium</td><td>{medium if "medium" in dir() else 0}</td></tr>
<tr><td>Low</td><td>{low if "low" in dir() else 0}</td></tr>
</table>
<h2>Detailed Findings</h2>
"""
    for idx, f in enumerate(findings, 1):
        body += f"""<div class="finding severity-{f.get("severity")}">
<h3>#{idx} {f.get("title", "Untitled")} {_severity_badge(f.get("severity", "none"))}</h3>
<table>
<tr><th>Target</th><td>{f.get("target", "N/A")}</td></tr>
<tr><th>Severity</th><td>{f.get("severity", "none")}</td></tr>
<tr><th>Confidence</th><td>{f.get("confidence", "low")}</td></tr>
{"<tr><th>CWE</th><td>" + f.get("cwe_id", "") + "</td></tr>" if f.get("cwe_id") else ""}
{"<tr><th>CVSS</th><td>" + str(f.get("cvss_score", "")) + "</td></tr>" if f.get("cvss_score") is not None else ""}
</table>
<p>{f.get("description", "")}</p>
{'<div class="remediation"><strong>Remediation:</strong> ' + f.get("remediation", "") + "</div>" if f.get("remediation") else ""}
{'<div class="evidence"><strong>Evidence:</strong><br>' + "\n".join(str(e)[:200] for e in (f.get("evidence") or [])[:3]) + "</div>" if f.get("evidence") else ""}
</div>"""
    body += '<div class="footer"><p>Generated by OffenSec AI.</p></div>'
    return _base_html(body, "Technical Report")


def owasp_template(findings: list[dict[str, Any]], assessment: dict[str, Any] | None = None) -> str:
    body = f"""<div class="header">
<h1>OWASP Style Assessment Report</h1>
<p>OWASP Top 10 Mapping | {datetime.now(UTC).strftime("%Y-%m-%d %H:%M UTC")}</p>
</div>
<h2>OWASP Top 10 Coverage</h2>
<table><tr><th>Category</th><th>Findings</th></tr>
"""
    owasp_map: dict[str, list[str]] = {}
    for f in findings:
        cat = f.get("owasp_id", "Uncategorized")
        owasp_map.setdefault(cat, []).append(f.get("title", ""))

    for cat, items in sorted(owasp_map.items()):
        body += f"<tr><td>{cat}</td><td>{', '.join(items[:3])}{'...' if len(items) > 3 else ''}</td></tr>"
    body += "</table><h2>Findings by OWASP Category</h2>"

    for f in findings:
        body += f"""<div class="finding severity-{f.get("severity")}">
<h3>{f.get("title", "")} {_severity_badge(f.get("severity", "none"))}</h3>
<p><strong>OWASP:</strong> {f.get("owasp_id", "N/A")} | <strong>CWE:</strong> {f.get("cwe_id", "N/A")}</p>
<p>{f.get("description", "")}</p>
{'<div class="remediation">' + f.get("remediation", "") + "</div>" if f.get("remediation") else ""}
</div>"""
    return _base_html(body, "OWASP Report")


def ptes_template(findings: list[dict[str, Any]], assessment: dict[str, Any] | None = None) -> str:
    phases = {
        "Pre-Engagement": [],
        "Intelligence Gathering": [],
        "Threat Modeling": [],
        "Vulnerability Analysis": [],
        "Exploitation": [],
        "Post-Exploitation": [],
        "Reporting": [],
    }
    for f in findings:
        phases["Vulnerability Analysis"].append(f)

    body = f"""<div class="header">
<h1>PTES Style Assessment Report</h1>
<p>Penetration Testing Execution Standard | {datetime.now(UTC).strftime("%Y-%m-%d %H:%M UTC")}</p>
</div>
"""
    for phase_name, phase_findings in phases.items():
        body += f"<h2>{phase_name}</h2>"
        if not phase_findings and phase_name != "Vulnerability Analysis":
            body += "<p>Phase completed. See detailed findings below.</p>"
            continue
        for f in phase_findings:
            body += f"""<div class="finding severity-{f.get("severity")}">
<h3>{f.get("title", "")}</h3>
<p><strong>Target:</strong> {f.get("target", "N/A")} | <strong>Severity:</strong> {f.get("severity", "none")}</p>
<p>{f.get("description", "")}</p>
</div>"""
    body += '<div class="footer"><p>PTES Methodology v2.0 | Generated by OffenSec AI.</p></div>'
    return _base_html(body, "PTES Report")
