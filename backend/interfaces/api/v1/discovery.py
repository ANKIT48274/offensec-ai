"""Discovery tool API routes — Katana, FFUF, DNS, WHOIS, TLS, Subdomain."""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel, Field

from backend.infrastructure.auth_deps import get_current_user_id
from backend.infrastructure.discovery import runners
from backend.interfaces.api.responses import error_response, success_response

router = APIRouter()


class FfufRequest(BaseModel):
    target_url: str = Field(..., min_length=1, max_length=255)
    wordlist: str | None = Field(None, max_length=500)


@router.get("/dns")
async def dns_enum(
    domain: str = Query(..., min_length=1, max_length=255, description="Domain to enumerate"),
    _user_id: str = Depends(get_current_user_id),
) -> Any:
    """Enumerate DNS records (A, AAAA, MX, NS, TXT, CNAME) for a domain."""
    try:
        result = await runners.run_dns_enum(domain)
        if result.get("error"):
            return error_response(result["error"], code="DNS_ENUM_ERROR")
        return success_response(result)
    except Exception as e:
        return error_response(str(e), code="DNS_ENUM_ERROR")


@router.get("/whois")
async def whois_lookup(
    target: str = Query(..., min_length=1, max_length=255, description="Domain or IP"),
    _user_id: str = Depends(get_current_user_id),
) -> Any:
    """Look up domain registration / WHOIS information."""
    try:
        result = await runners.run_whois(target)
        if result.get("error"):
            return error_response(result["error"], code="WHOIS_ERROR")
        return success_response(result)
    except Exception as e:
        return error_response(str(e), code="WHOIS_ERROR")


@router.get("/subdomains")
async def subdomain_enum(
    domain: str = Query(..., min_length=1, max_length=255, description="Parent domain"),
    _user_id: str = Depends(get_current_user_id),
) -> Any:
    """Discover subdomains for a domain via DNS brute-force."""
    try:
        result = await runners.run_subdomain_enum(domain)
        if result.get("error"):
            return error_response(result["error"], code="SUBDOMAIN_ERROR")
        return success_response(result)
    except Exception as e:
        return error_response(str(e), code="SUBDOMAIN_ERROR")


@router.get("/tls")
async def tls_analyze(
    hostname: str = Query(..., min_length=1, max_length=255, description="Host (hostname or IP)"),
    port: int = Query(443, ge=1, le=65535, description="TLS port"),
    _user_id: str = Depends(get_current_user_id),
) -> Any:
    """Analyze a TLS certificate (issuer, validity, SAN)."""
    try:
        result = await runners.run_tls_analyze(hostname, port)
        if result.get("error"):
            return error_response(result["error"], code="TLS_ERROR")
        return success_response(result)
    except Exception as e:
        return error_response(str(e), code="TLS_ERROR")


@router.post("/katana")
async def katana_crawl(
    urls: list[str],
    _user_id: str = Depends(get_current_user_id),
) -> Any:
    """Crawl web endpoints with Katana."""
    try:
        result = await runners.run_katana(urls)
        if result.get("error"):
            return error_response(result["error"], code="KATANA_ERROR")
        return success_response(result)
    except Exception as e:
        return error_response(str(e), code="KATANA_ERROR")


@router.post("/ffuf")
async def ffuf_fuzz(
    body: FfufRequest,
    _user_id: str = Depends(get_current_user_id),
) -> Any:
    """Fuzz directories/files with FFUF."""
    try:
        result = await runners.run_ffuf(body.target_url, wordlist=body.wordlist)
        if result.get("error"):
            return error_response(result["error"], code="FFUF_ERROR")
        return success_response(result)
    except Exception as e:
        return error_response(str(e), code="FFUF_ERROR")
