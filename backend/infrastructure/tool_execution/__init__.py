"""External security tool execution with sandboxing and result parsing."""

from __future__ import annotations

import asyncio
import os
import subprocess
from pathlib import Path
from typing import Any

from backend.domain.exceptions import ToolExecutionError


class ToolExecutor:
    """Executes external security tools in a controlled environment."""

    def __init__(
        self,
        timeout: int = 300,
        working_dir: str | None = None,
        allowed_tools: list[str] | None = None,
    ) -> None:
        self._timeout = timeout
        self._working_dir = working_dir or "/tmp/offensec_tools"
        self._allowed_tools = allowed_tools or self._default_allowed_tools()
        Path(self._working_dir).mkdir(parents=True, exist_ok=True)

    def _default_allowed_tools(self) -> list[str]:
        return [
            "nmap", "masscan", "ffuf", "gobuster", "dirb",
            "nikto", "sqlmap", "hydra", "john", "hashcat",
            "curl", "wget", "dig", "nslookup", "whois",
            "sslscan", "testssl", "enum4linux", "smbclient",
            "ldapsearch", "crackmapexec", "bloodhound-python",
            "dnsrecon", "dnsenum", "wpscan", "joomscan",
            "whatweb", "wafw00f", "jq", "grep", "awk",
            "python3", "msfconsole",
        ]

    async def execute(
        self,
        tool: str,
        args: list[str],
        timeout: int | None = None,
    ) -> dict[str, Any]:
        if tool not in self._allowed_tools:
            raise ToolExecutionError(tool, -1, f"Tool '{tool}' is not in the allowed list")

        cmd = [tool, *args]
        timeout = timeout or self._timeout

        try:
            proc = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                cwd=self._working_dir,
                env={**os.environ, "PYTHONUNBUFFERED": "1"},
            )

            try:
                stdout, stderr = await asyncio.wait_for(
                    proc.communicate(), timeout=timeout
                )
            except TimeoutError:
                proc.kill()
                await proc.wait()
                raise ToolExecutionError(tool, -1, f"Tool execution timed out after {timeout}s")

            if proc.returncode != 0:
                raise ToolExecutionError(
                    tool,
                    proc.returncode or -1,
                    stderr.decode("utf-8", errors="replace"),
                )

            return {
                "tool": tool,
                "args": args,
                "returncode": proc.returncode,
                "stdout": stdout.decode("utf-8", errors="replace"),
                "stderr": stderr.decode("utf-8", errors="replace"),
                "timeout": timeout,
            }

        except FileNotFoundError as e:
            raise ToolExecutionError(tool, -1, f"Tool not found: {e}")
        except OSError as e:
            raise ToolExecutionError(tool, -1, f"OS error executing tool: {e}")


class CommandBuilder:
    """Builds safe command arguments for security tools."""

    @staticmethod
    def nmap(target: str, ports: str | None = "-p-", options: list[str] | None = None) -> list[str]:
        cmd = ["-sV", "-sC", "-O"]
        if ports:
            cmd.extend([ports])
        if options:
            cmd.extend(options)
        cmd.append(target)
        return cmd

    @staticmethod
    def gobuster(target_url: str, wordlist: str, extensions: list[str] | None = None) -> list[str]:
        cmd = ["dir", "-u", target_url, "-w", wordlist]
        if extensions:
            cmd.extend(["-x", ",".join(extensions)])
        return cmd

    @staticmethod
    def ffuf(target_url: str, wordlist: str, extensions: list[str] | None = None) -> list[str]:
        cmd = ["-u", f"{target_url}/FUZZ", "-w", wordlist]
        if extensions:
            cmd.extend(["-e", ",".join(f".{e}" for e in extensions)])
        return cmd

    @staticmethod
    def hydra(target: str, service: str, username_list: str, password_list: str) -> list[str]:
        return ["-L", username_list, "-P", password_list, f"{target}", service]
