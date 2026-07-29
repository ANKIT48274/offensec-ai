"""Tests for tool execution infrastructure."""

import pytest

from backend.domain.exceptions import ToolExecutionError
from backend.infrastructure.tool_execution import CommandBuilder, ToolExecutor


class TestCommandBuilder:
    def test_nmap_command(self):
        cmd = CommandBuilder.nmap("192.168.1.1")
        assert "-sV" in cmd
        assert "-sC" in cmd
        assert "192.168.1.1" in cmd

    def test_nmap_with_ports(self):
        cmd = CommandBuilder.nmap("10.0.0.1", ports="-p 80,443")
        assert "-p 80,443" in cmd

    def test_gobuster_command(self):
        cmd = CommandBuilder.gobuster("http://example.com", "/usr/share/wordlists/common.txt")
        assert "-u" in cmd
        assert "-w" in cmd

    def test_ffuf_command(self):
        cmd = CommandBuilder.ffuf("http://example.com/FUZZ", "/usr/share/wordlists/common.txt")
        assert "FUZZ" in str(cmd)

    def test_hydra_command(self):
        cmd = CommandBuilder.hydra("192.168.1.1", "ssh", "/usr/share/wordlists/users.txt", "/usr/share/wordlists/passwords.txt")
        assert "-L" in cmd
        assert "-P" in cmd


class TestToolExecutor:
    def setup_method(self):
        self.executor = ToolExecutor(allowed_tools=["echo", "python3"])

    @pytest.mark.asyncio
    async def test_execute_allowed_tool(self):
        result = await self.executor.execute("echo", ["hello"])
        assert result["returncode"] == 0
        assert "hello" in result["stdout"]

    @pytest.mark.asyncio
    async def test_execute_disallowed_tool_raises_error(self):
        with pytest.raises(ToolExecutionError) as exc:
            await self.executor.execute("nmap", ["-v"])
        assert "nmap" in str(exc.value)
        assert "not in the allowed list" in str(exc.value.message)

    @pytest.mark.asyncio
    async def test_execute_nonexistent_tool_raises_error(self):
        with pytest.raises(ToolExecutionError):
            await self.executor.execute("nonexistent_tool_xyz", [])
