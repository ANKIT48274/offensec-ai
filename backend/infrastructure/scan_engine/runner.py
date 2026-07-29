"""Nmap scan runner — executes scans via subprocess."""

from __future__ import annotations

import asyncio
import os
import tempfile
from datetime import UTC, datetime
from typing import Any

from backend.infrastructure.scan_engine.xml_parser import parse_nmap_xml

NMAP_TIMEOUT = 600
NMAP_BASE_ARGS = ["-Pn", "-sV", "-sC", "-O", "-oX"]
MAX_STDERR_BYTES = 65536


async def _terminate_gracefully(proc: asyncio.subprocess.Process, timeout: float = 5.0) -> None:
    try:
        proc.terminate()
        await asyncio.wait_for(proc.wait(), timeout=timeout)
    except TimeoutError:
        proc.kill()
        await proc.wait()


async def run_nmap_scan(target: str, timeout: int = NMAP_TIMEOUT) -> dict[str, Any]:
    if not target or not target.strip():
        raise ValueError("Target cannot be empty")

    if not _is_valid_target(target):
        raise ValueError(f"Invalid target: {target}")

    fd, xml_path = tempfile.mkstemp(suffix=".xml", prefix="nmap_")
    os.close(fd)

    cmd = ["nmap", *NMAP_BASE_ARGS, xml_path, target.strip()]

    try:
        proc = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.DEVNULL,
            stderr=asyncio.subprocess.PIPE,
        )

        try:
            _, stderr = await asyncio.wait_for(proc.communicate(), timeout=timeout)
        except TimeoutError:
            await _terminate_gracefully(proc)
            _cleanup_file(xml_path)
            raise TimeoutError(f"Nmap scan timed out after {timeout}s for target: {target}")

        if proc.returncode != 0:
            error_msg = stderr.decode("utf-8", errors="replace")[:MAX_STDERR_BYTES].strip()
            _cleanup_file(xml_path)
            raise RuntimeError(
                f"Nmap failed (exit {proc.returncode}): {error_msg or 'Unknown error'}"
            )

        with open(xml_path, encoding="utf-8", errors="replace") as f:
            xml_content = f.read()

        if not xml_content.strip():
            _cleanup_file(xml_path)
            raise RuntimeError("Nmap produced empty output")

        parsed = parse_nmap_xml(xml_content)

        _cleanup_file(xml_path)

        return {
            "xml_content": xml_content,
            "parsed": parsed,
            "target": target.strip(),
            "finished_at": datetime.now(UTC).isoformat(),
        }

    except FileNotFoundError as e:
        _cleanup_file(xml_path)
        raise RuntimeError(f"Nmap not found on system: {e}")
    except OSError as e:
        _cleanup_file(xml_path)
        raise RuntimeError(f"OS error executing nmap: {e}")


def _is_valid_target(target: str) -> bool:
    import ipaddress

    try:
        ipaddress.ip_address(target)
        return True
    except ValueError:
        pass
    try:
        ipaddress.ip_network(target, strict=False)
        return True
    except ValueError:
        pass
    import re

    hostname_re = re.compile(
        r"^(?:[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)\.)*(?:[a-zA-Z]{2,63})$"
    )
    return bool(hostname_re.match(target))


def _cleanup_file(path: str) -> None:
    if not path:
        return
    try:
        if os.path.exists(path):
            os.unlink(path)
    except OSError:
        pass
