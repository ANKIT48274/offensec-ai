"""Discovery tool runners — Katana, FFUF, DNS, TLS, screenshots, WHOIS."""

from __future__ import annotations

import asyncio
import json
import os
import tempfile
from typing import Any

from backend.infrastructure.scan_engine.runner import _terminate_gracefully

KATANA_TIMEOUT = 180
FFUF_TIMEOUT = 300
DISCOVERY_TIMEOUT = 60
MAX_STDERR = 65536


def _cleanup(path: str) -> None:
    if not path:
        return
    try:
        if os.path.exists(path):
            os.unlink(path)
    except OSError:
        pass


async def run_katana(urls: list[str], timeout: int = KATANA_TIMEOUT) -> dict[str, Any]:
    if not urls:
        return {"error": "No URLs provided", "endpoints": []}
    fd, out_path = tempfile.mkstemp(suffix=".jsonl", prefix="katana_")
    os.close(fd)
    " ".join(urls[:5])
    cmd = ["katana", "-jsonl", "-o", out_path, "-d", "2", "-c", "30", *urls[:5]]
    try:
        proc = await asyncio.create_subprocess_exec(
            *cmd, stdout=asyncio.subprocess.DEVNULL, stderr=asyncio.subprocess.PIPE
        )
        try:
            _, _stderr = await asyncio.wait_for(proc.communicate(), timeout=timeout)
        except TimeoutError:
            await _terminate_gracefully(proc)
            _cleanup(out_path)
            return {"error": f"Katana timed out after {timeout}s", "endpoints": []}
        if not os.path.exists(out_path) or os.path.getsize(out_path) == 0:
            _cleanup(out_path)
            return {"endpoints": [], "error": None}
        with open(out_path) as f:
            raw = f.read()
        _cleanup(out_path)
        if not raw.strip():
            return {"endpoints": [], "error": None}
        endpoints = []
        for line in raw.strip().split("\n"):
            try:
                ep = json.loads(line)
                endpoints.append(
                    {
                        "url": ep.get("url", ""),
                        "status": ep.get("status"),
                        "tech": ep.get("tech", []),
                        "depth": ep.get("depth", 0),
                    }
                )
            except json.JSONDecodeError:
                continue
        return {"endpoints": endpoints, "count": len(endpoints), "error": None}
    except FileNotFoundError:
        _cleanup(out_path)
        return {"error": "Katana not found on system", "endpoints": []}
    except OSError as e:
        _cleanup(out_path)
        return {"error": f"OS error: {e}", "endpoints": []}


async def run_ffuf(
    target_url: str, wordlist: str | None = None, timeout: int = FFUF_TIMEOUT
) -> dict[str, Any]:
    if not target_url:
        return {"error": "No target URL", "results": []}
    wordlist_path = wordlist or "/usr/share/seclists/Discovery/Web-Content/common.txt"
    fd, out_path = tempfile.mkstemp(suffix=".json", prefix="ffuf_")
    os.close(fd)
    cmd = [
        "ffuf",
        "-u",
        f"{target_url.rstrip('/')}/FUZZ",
        "-w",
        wordlist_path,
        "-o",
        out_path,
        "-of",
        "json",
        "-c",
        "-t",
        "50",
        "-fc",
        "404",
    ]
    try:
        proc = await asyncio.create_subprocess_exec(
            *cmd, stdout=asyncio.subprocess.DEVNULL, stderr=asyncio.subprocess.PIPE
        )
        try:
            _, _stderr = await asyncio.wait_for(proc.communicate(), timeout=timeout)
        except TimeoutError:
            await _terminate_gracefully(proc)
            _cleanup(out_path)
            return {"error": f"FFUF timed out after {timeout}s", "results": []}
        if not os.path.exists(out_path):
            _cleanup(out_path)
            return {"results": [], "error": None}
        with open(out_path) as f:
            data = json.load(f)
        _cleanup(out_path)
        results = data.get("results", []) if isinstance(data, dict) else data
        return {
            "results": [
                {"url": r.get("url", ""), "status": r.get("status"), "length": r.get("length")}
                for r in (results if isinstance(results, list) else [])
            ],
            "count": len(results) if isinstance(results, list) else 0,
            "error": None,
        }
    except FileNotFoundError:
        _cleanup(out_path)
        return {"error": "FFUF not found on system", "results": []}
    except (json.JSONDecodeError, OSError) as e:
        _cleanup(out_path)
        return {"error": str(e), "results": []}


async def run_dns_enum(domain: str, timeout: int = DISCOVERY_TIMEOUT) -> dict[str, Any]:
    records = {"a": [], "aaaa": [], "mx": [], "ns": [], "txt": [], "cname": []}
    for qtype in ["a", "aaaa", "mx", "ns", "txt", "cname"]:
        try:
            proc = await asyncio.create_subprocess_exec(
                "dig",
                "+short",
                "-t",
                qtype,
                domain,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.DEVNULL,
            )
            try:
                stdout, _ = await asyncio.wait_for(proc.communicate(), timeout=timeout)
            except TimeoutError:
                await _terminate_gracefully(proc)
                continue
            values = stdout.decode(errors="replace").strip().split("\n")
            records[qtype] = [v.strip() for v in values if v.strip()]
        except FileNotFoundError:
            continue
    return {"domain": domain, "records": records, "error": None}


async def run_whois(target: str, timeout: int = DISCOVERY_TIMEOUT) -> dict[str, Any]:
    try:
        proc = await asyncio.create_subprocess_exec(
            "whois", target, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.DEVNULL
        )
        try:
            stdout, _ = await asyncio.wait_for(proc.communicate(), timeout=timeout)
        except TimeoutError:
            await _terminate_gracefully(proc)
            return {"target": target, "error": "WHOIS timed out"}
        output = stdout.decode(errors="replace")
        return {"target": target, "raw": output[:5000], "error": None}
    except FileNotFoundError:
        return {"target": target, "error": "WHOIS not found on system"}


async def run_tls_analyze(
    hostname: str, port: int = 443, timeout: int = DISCOVERY_TIMEOUT
) -> dict[str, Any]:
    try:
        import socket
        import ssl

        context = ssl.create_default_context()
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE
        loop = asyncio.get_event_loop()
        sock = await loop.run_in_executor(
            None, lambda: socket.create_connection((hostname, port), timeout=10)
        )
        ssock = await loop.run_in_executor(
            None, lambda: context.wrap_socket(sock, server_hostname=hostname)
        )
        cert = ssock.getpeercert()
        ssock.close()
        return {
            "hostname": hostname,
            "port": port,
            "subject": dict(cert.get("subject", [])[0]) if cert.get("subject") else {},
            "issuer": dict(cert.get("issuer", [])[0]) if cert.get("issuer") else {},
            "valid_from": cert.get("notBefore", ""),
            "valid_to": cert.get("notAfter", ""),
            "serial": cert.get("serialNumber", ""),
            "san": cert.get("subjectAltName", []),
            "version": cert.get("version", ""),
            "error": None,
        }
    except Exception as e:
        return {"hostname": hostname, "port": port, "error": str(e)}


async def run_subdomain_enum(
    domain: str, wordlist: str | None = None, timeout: int = DISCOVERY_TIMEOUT
) -> dict[str, Any]:
    wordlist_path = wordlist or "/usr/share/seclists/Discovery/DNS/subdomains-top1million-5000.txt"
    results: list[str] = []
    try:
        with open(wordlist_path) as f:
            subs = [line.strip() for line in f if line.strip()][:500]
    except FileNotFoundError:
        return {"domain": domain, "error": f"Wordlist not found: {wordlist_path}", "subdomains": []}

    async def check_sub(sub: str) -> str | None:
        try:
            proc = await asyncio.create_subprocess_exec(
                "dig",
                "+short",
                f"{sub}.{domain}",
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.DEVNULL,
            )
            try:
                stdout, _ = await asyncio.wait_for(proc.communicate(), timeout=5)
            except TimeoutError:
                await _terminate_gracefully(proc)
                return None
            result = stdout.decode(errors="replace").strip()
            return f"{sub}.{domain}" if result and not result.startswith(";;") else None
        except FileNotFoundError:
            return None

    tasks = [check_sub(s) for s in subs[:100]]
    for coro in asyncio.as_completed(tasks):
        try:
            r = await coro
            if r:
                results.append(r)
        except Exception:
            continue
    return {"domain": domain, "subdomains": results, "count": len(results), "error": None}
