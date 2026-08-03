# Release Notes — OffenSec AI v1.0.0

**Release Date:** July 30, 2026

## Highlights

- **39 API endpoints** for complete security assessment lifecycle management
- **6 scan engines** (Nmap, HTTPX, Nuclei, Katana, FFUF) integrated into a unified pipeline
- **179 unit tests** with automated CI/CD enforcement
- **Professional reporting** — 6 output formats (Executive, Technical, OWASP, PTES, CSV, JSON)
- **AI-driven correlation** — Automated risk scoring, attack path detection, and recommendations
- **Asset management** — Automatic deduplication with first/last seen tracking across scans
- **Security-hardened** — JWT authentication, input validation, no hardcoded secrets

## Major Features

### Scan Engines
- Nmap — port scanning, service detection, OS fingerprinting, script scanning
- HTTPX — web service probing, technology identification, TLS grab, favicon hashing
- Nuclei — template-based vulnerability scanning with CVE/CWE mappings
- Katana — web endpoint crawling and discovery
- FFUF — directory and file fuzzing with wordlist support

### Discovery Tools
- DNS enumeration (A, AAAA, MX, NS, TXT, CNAME records)
- WHOIS domain registration lookup
- DNS-based subdomain discovery
- TLS certificate analysis (subject, issuer, validity, SAN)

### Pipeline Automation
- One-click Nmap → HTTPX → Nuclei pipeline
- Per-step progress tracking
- Automatic URL extraction from Nmap results for downstream tools

### AI Correlation Engine
- Attack surface analysis (hosts, ports, high-risk services)
- Critical asset identification with supporting evidence
- Risk ranking (0–100 scoring)
- Attack path mapping with severity scoring
- Executive summary generation
- Automated remediation recommendations

### Reporting
- Executive Summary (non-technical stakeholder report)
- Technical Report (detailed findings with evidence)
- OWASP Style (OWASP Top 10 mapped findings)
- PTES Style (Penetration Testing Execution Standard format)
- CSV Export (spreadsheet-compatible)
- JSON Export (machine-readable format)

### Asset & Evidence Management
- Auto-deduplication: IPs, hostnames, ports (by port+protocol), technologies, OS fingerprints
- First/last seen tracking per asset
- Scan count accumulation
- Evidence storage with source, type, file path, and raw data

## Security Improvements

- **JWT Bearer authentication** enforced on all 39 endpoints (except register/login)
- **Removed hardcoded secrets** — `JWT_SECRET` must be set via environment
- **bcrypt password hashing** with 12 rounds
- **Command injection prevention** — all subprocesses use `create_subprocess_exec` with validated inputs
- **Graceful subprocess termination** — SIGTERM before SIGKILL on timeout
- **Stderr output capped** at 64KB to prevent memory exhaustion
- **Temp file cleanup** — try/finally on all paths, no file leaks
- **SQLAlchemy ORM only** — no raw SQL, no SQL injection vectors
- **CORS configurable** via environment variable

## Architecture

- Clean Architecture monorepo with 5 layers (Domain, Application, Infrastructure, Interfaces, Frontend)
- Async-first: FastAPI with `asyncio` for all I/O operations
- Database connection pooling (size 10, overflow 20)
- 20+ database indexes across all tables
- Structured JSON logging
- Plugin system with filesystem-based discovery

## Performance

| Metric | Value |
|--------|-------|
| API endpoints | 39 |
| Database indexes | 20+ |
| Connection pool | 10 + 20 overflow |
| Subprocess stderr limit | 64KB |
| Tests | 179 passing |
| Code style | Ruff (153 files formatted) |

## Breaking Changes

- **Authentication:** `x-user-id` header has been removed. All endpoints (except register/login) now require `Authorization: Bearer <token>`.
- **JWT_SECRET:** Must be set via environment variable. Application will not start without it.

## Known Issues

1. No token revocation mechanism (refresh token blacklist)
2. No API rate limiting (configure at reverse proxy level)
3. Scan operations block the request thread (future: Celery background tasks)
4. 153 line-too-long warnings in template strings (cosmetic)

## Upgrade Guide

### From v0.2.0

1. Set `JWT_SECRET` environment variable:
   ```bash
   echo "JWT_SECRET=$(python3 -c 'import secrets; print(secrets.token_hex(32))')" >> .env
   ```

2. Update API calls: Replace `x-user-id` headers with Bearer tokens obtained from `/auth/login`.

3. Apply new database migrations:
   ```bash
   alembic upgrade head
   ```

4. Restart services:
   ```bash
   docker compose down
   docker compose up -d
   ```

## Roadmap

### v1.1.0 (Planned — Q3 2026)
- Background task queue (Celery/Redis)
- WebSocket live scan progress
- PDF report generation (WeasyPrint)
- Light mode / dark mode theme toggle
- API rate limiting

### v2.0.0 (Future — 2027)
- Multi-tenant MSSP support
- Cloud security assessment (AWS, Azure, GCP)
- Mobile application assessment
- AI-driven penetration testing agent framework

## Acknowledgements

Built with open-source tools: FastAPI, Next.js, SQLAlchemy, PostgreSQL, Redis, Docker, and the security testing community.

**Author:** Ankit Patidar ([@ANKIT48274](https://github.com/ANKIT48274))
