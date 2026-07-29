"""Nuclei scan runner — executes nuclei via subprocess."""

from __future__ import annotations

import asyncio
import os
import tempfile
from typing import Any

from backend.infrastructure.nuclei.parser import parse_nuclei_jsonl
from backend.infrastructure.scan_engine.runner import _terminate_gracefully

NUCLEI_TIMEOUT = 600
MAX_STDERR_BYTES = 65536


async def run_nuclei(target_url: str, timeout: int = NUCLEI_TIMEOUT) -> dict[str, Any]:
    if not target_url or not target_url.strip():
        return {"error": "Target URL cannot be empty", "findings": []}

    if not target_url.startswith(("http://", "https://")):
        return {"error": f"Invalid URL scheme: {target_url}", "findings": []}

    fd, out_path = tempfile.mkstemp(suffix=".jsonl", prefix="nuclei_")
    os.close(fd)

    cmd = [
        "nuclei",
        "-target", target_url.strip(),
        "-jsonl", "-o", out_path,
        "-severity", "info,low,medium,high,critical",
    ]

    try:
        proc = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.DEVNULL,
            stderr=asyncio.subprocess.PIPE,
        )
        try:
            _, stderr = await asyncio.wait_for(proc.communicate(), timeout=timeout)
        except asyncio.TimeoutError:
            await _terminate_gracefully(proc)
            _cleanup(out_path)
            return {"error": f"Nuclei timed out after {timeout}s", "findings": []}

        err_text = stderr.decode("utf-8", errors="replace")[:MAX_STDERR_BYTES].strip()

        if not os.path.exists(out_path):
            if proc.returncode and proc.returncode != 0:
                return {"error": f"Nuclei failed (exit {proc.returncode}): {err_text or 'unknown'}", "findings": []}
            return {"findings": [], "error": None}

        if os.path.getsize(out_path) == 0:
            _cleanup(out_path)
            return {"findings": [], "error": None}

        with open(out_path, "r", encoding="utf-8", errors="replace") as f:
            raw = f.read()

        _cleanup(out_path)

        if not raw.strip():
            return {"findings": [], "error": None}

        parsed = parse_nuclei_jsonl(raw)
        return {"findings": parsed, "count": len(parsed), "raw_output": raw, "error": None}

    except FileNotFoundError:
        _cleanup(out_path)
        return {"error": "Nuclei not found on system", "findings": []}
    except OSError as e:
        _cleanup(out_path)
        return {"error": f"OS error: {e}", "findings": []}


def _cleanup(path: str) -> None:
    if not path:
        return
    try:
        if os.path.exists(path):
            os.unlink(path)
    except OSError:
        pass
