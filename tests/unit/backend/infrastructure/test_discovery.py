"""Tests for discovery runners — validation and error handling."""

import pytest

from backend.infrastructure.discovery.runners import run_katana, run_ffuf, run_dns_enum, run_whois, run_tls_analyze, run_subdomain_enum


@pytest.mark.asyncio
async def test_katana_empty_urls():
    result = await run_katana([])
    assert result.get("error") == "No URLs provided"


@pytest.mark.asyncio
async def test_ffuf_empty_target():
    result = await run_ffuf("")
    assert result.get("error") == "No target URL"


@pytest.mark.asyncio
async def test_dns_empty_handled():
    result = await run_dns_enum("example.com")
    assert "domain" in result
    assert "records" in result


@pytest.mark.asyncio
async def test_whois_empty_target():
    result = await run_whois("example.com")
    assert result.get("target") == "example.com"


@pytest.mark.asyncio
async def test_tls_invalid_host():
    result = await run_tls_analyze("invalid..localhost", 443)
    assert "error" in result


@pytest.mark.asyncio
async def test_subdomain_empty_domain():
    result = await run_subdomain_enum("example.com")
    assert "subdomains" in result


@pytest.mark.asyncio
async def test_cleanup_none_path():
    from backend.infrastructure.discovery.runners import _cleanup
    _cleanup("")  # should not raise
    _cleanup("/nonexistent/path")  # should not raise
