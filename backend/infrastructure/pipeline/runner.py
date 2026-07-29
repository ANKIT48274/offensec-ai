"""Pipeline runner — executes multi-tool scan pipeline asynchronously."""

from __future__ import annotations

import asyncio
import ipaddress
import os
import re
import tempfile
from typing import Any

from backend.infrastructure.pipeline.httpx_parser import parse_httpx_json
from backend.infrastructure.scan_engine.runner import _is_valid_target, _terminate_gracefully
from backend.infrastructure.scan_engine.xml_parser import parse_nmap_xml


NMAP_TIMEOUT = 300
HTTPX_TIMEOUT = 300
MAX_STDERR_BYTES = 65536


async def run_pipeline(target: str) -> dict[str, Any]:
    if not target or not target.strip():
        raise ValueError("Target cannot be empty")

    result: dict[str, Any] = {
        "target": target.strip(),
        "nmap": None,
        "httpx": None,
        "error": None,
    }

    nmap_result = await _run_nmap_step(target)
    result["nmap"] = nmap_result

    if nmap_result.get("error"):
        result["error"] = f"Nmap failed: {nmap_result['error']}"
        return result

    live_hosts = _extract_live_hosts(nmap_result)

    if not live_hosts:
        result["error"] = "No live hosts found"
        return result

    httpx_result = await _run_httpx_step(live_hosts)
    result["httpx"] = httpx_result

    if httpx_result.get("error"):
        result["error"] = f"HTTPX failed: {httpx_result['error']}"

    return result


async def _run_nmap_step(target: str) -> dict[str, Any]:
    if not _is_valid_target(target):
        return {"error": f"Invalid target: {target}"}

    fd, xml_path = tempfile.mkstemp(suffix=".xml", prefix="pipeline_nmap_")
    os.close(fd)

    cmd = ["nmap", "-Pn", "-sV", "--top-ports", "100", "-oX", xml_path, target.strip()]

    try:
        proc = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.DEVNULL,
            stderr=asyncio.subprocess.PIPE,
        )
        try:
            _, stderr = await asyncio.wait_for(proc.communicate(), timeout=NMAP_TIMEOUT)
        except asyncio.TimeoutError:
            await _terminate_gracefully(proc)
            _cleanup(xml_path)
            return {"error": f"Nmap timed out after {NMAP_TIMEOUT}s"}

        if proc.returncode != 0:
            err = stderr.decode("utf-8", errors="replace")[:MAX_STDERR_BYTES].strip()
            _cleanup(xml_path)
            return {"error": f"Nmap failed (exit {proc.returncode}): {err}"}

        with open(xml_path, "r", encoding="utf-8", errors="replace") as f:
            xml_content = f.read()

        _cleanup(xml_path)

        if not xml_content.strip():
            return {"error": "Nmap produced empty output"}

        parsed = parse_nmap_xml(xml_content)
        return {"data": parsed, "xml": xml_content}

    except FileNotFoundError:
        _cleanup(xml_path)
        return {"error": "Nmap not found on system"}
    except OSError as e:
        _cleanup(xml_path)
        return {"error": f"OS error: {e}"}


def _extract_live_hosts(nmap_result: dict[str, Any]) -> list[str]:
    hosts: list[str] = []
    data = nmap_result.get("data", {})
    for host in data.get("hosts", []):
        if host.get("status", {}).get("state") == "up":
            for ip in host.get("ips", []):
                try:
                    ipaddress.ip_address(ip)
                    hosts.append(ip)
                except ValueError:
                    continue
            for port in host.get("ports", []):
                if not port.get("port", "").isdigit():
                    continue
                if port.get("service") in ("http", "https", None):
                    ips = host.get("ips", [])
                    if ips:
                        try:
                            ipaddress.ip_address(ips[0])
                        except ValueError:
                            continue
                        scheme = "https" if port.get("port") in ("443", "8443") else "http"
                        hosts.append(f"{scheme}://{ips[0]}:{port['port']}")
    return hosts


async def _run_httpx_step(targets: list[str]) -> dict[str, Any]:
    if not targets:
        return {"error": "No targets for httpx"}

    fd, out_path = tempfile.mkstemp(suffix=".json", prefix="pipeline_httpx_")
    os.close(fd)

    cmd = [
        "httpx", "-json", "-o", out_path,
        "-title", "-tech-detect", "-status-code", "-server",
        "-content-length", "-web-server", "-websocket",
        "-tls-grab", "-favicon",
    ] + list(targets[:20])

    try:
        proc = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.DEVNULL,
            stderr=asyncio.subprocess.PIPE,
        )
        try:
            _, stderr = await asyncio.wait_for(proc.communicate(), timeout=HTTPX_TIMEOUT)
        except asyncio.TimeoutError:
            await _terminate_gracefully(proc)
            _cleanup(out_path)
            return {"error": f"HTTPX timed out after {HTTPX_TIMEOUT}s"}

        err_text = stderr.decode("utf-8", errors="replace")[:MAX_STDERR_BYTES].strip()

        if not os.path.exists(out_path) or os.path.getsize(out_path) == 0:
            if proc.returncode != 0 and proc.returncode is not None:
                _cleanup(out_path)
                return {"error": f"HTTPX failed (exit {proc.returncode}): {err_text or 'unknown error'}"}
            _cleanup(out_path)
            return {"data": [], "error": None}

        with open(out_path, "r", encoding="utf-8", errors="replace") as f:
            raw = f.read()

        _cleanup(out_path)

        if not raw.strip():
            return {"data": [], "error": None}

        parsed = parse_httpx_json(raw)
        return {"data": parsed, "raw": raw}

    except FileNotFoundError:
        _cleanup(out_path)
        return {"error": "HTTPX not found on system"}
    except OSError as e:
        _cleanup(out_path)
        return {"error": f"OS error: {e}"}


def _cleanup(path: str) -> None:
    if not path:
        return
    try:
        if os.path.exists(path):
            os.unlink(path)
    except OSError:
        pass
