# Portfolio — OffenSec AI

## Project Summary

| Field | Detail |
|-------|--------|
| **Project** | OffenSec AI |
| **Role** | Lead Software Architect / Security Engineer / DevOps |
| **Timeline** | July 2026 |
| **Stack** | Python, FastAPI, Next.js, TypeScript, PostgreSQL, Redis, Docker |
| **Lines of Code** | ~19,000+ |
| **Tests** | 179 unit tests |
| **API Endpoints** | 39 |
| **GitHub** | [github.com/ANKIT48274/offensec-ai](https://github.com/ANKIT48274/offensec-ai) |

## Architecture

Clean Architecture monorepo with 5 layers:

- **Domain** — Business entities, value objects, events, exceptions (no external dependencies)
- **Application** — Services, use cases, DTOs (orchestration logic)
- **Infrastructure** — Database, auth, scan engines, reporting, plugins, discovery tools
- **Interfaces** — REST API (FastAPI), WebSocket, CLI, webhooks
- **Frontend** — Next.js 15 SPA with App Router, TypeScript, Tailwind CSS, Zustand state management

## Engineering Challenges

### Challenge 1: Multi-Tool Pipeline Orchestration
Coordinating Nmap, HTTPX, and Nuclei asynchronously with state tracking, progress reporting, and error isolation. Each tool has different output formats (XML, JSONL, JSON), timeouts, and failure modes.

**Solution:** Async subprocess with async/await, intermediate temp file cleanup with try/finally, step-level status tracking in PipelineJob entity, and graceful SIGTERM → SIGKILL termination.

### Challenge 2: Command Injection Prevention
Security tools accept user-supplied targets that could contain injection payloads.

**Solution:** All subprocess calls use `asyncio.create_subprocess_exec` with literal argument arrays (no shell=True). Target inputs validated with `ipaddress.ip_address()` and strict hostname regex. Extracted hosts from Nmap XML output are re-validated before passing to subsequent tools.

### Challenge 3: Asset Deduplication
Concurrent scans produce overlapping assets that must be merged without duplicates.

**Solution:** Upsert pattern with merge logic for IPs, hostnames, ports (by port+protocol), technologies (set union), and OS guesses. `first_seen`/`last_seen` tracking with `scan_count` increment.

## Security Challenges

- **JWT auth bypass prevention** — Removed insecure `x-user-id` header pattern, replaced with Bearer token verification on all 39 endpoints
- **Subprocess isolation** — Graceful termination, stderr size limits, temp file cleanup
- **No hardcoded secrets** — All credentials via environment variables, startup fails if `JWT_SECRET` unset
- **ORM-only queries** — No raw SQL, preventing injection

## AI Challenges

- **Evidence-backed correlation** — Every AI conclusion references supporting findings
- **Rules-based scoring** — Risk score computed from vulnerability severity, exposure, and asset criticality without external API calls
- **Attack path mapping** — Automated chaining of critical/high findings into exploitable paths

## Lessons Learned

1. **Security-first design** — Authentication and input validation must be implemented before any feature work. Retrofitting is significantly more expensive.
2. **Async subprocess management** — `asyncio.create_subprocess_exec` requires careful lifecycle management. Always capture stderr, set timeouts, and clean up temp files in `finally` blocks.
3. **Database indexing upfront** — Adding indexes after data exists requires migrations. Plan indexes alongside schema design.
4. **Incremental testing** — Writing tests after each component saved significant debugging time.

## Interesting Problems Solved

- **XML parsing from Nmap** — Handles missing elements, nested port/service/script structures, variant OS match formats
- **JSONL line-by-line parsing** — Handles HTTPX and Nuclei JSONL output with per-line error isolation
- **Multi-format report generation** — Single data source rendered into 6 different output formats
- **Plugin discovery** — Filesystem-based plugin loading with manifest validation and capability declarations

## Interview Talking Points

- "I architected a Clean Architecture monorepo with 5 layers, serving 39 API endpoints from a single FastAPI application"
- "I implemented a multi-tool async pipeline orchestrating Nmap, HTTPX, and Nuclei with subprocess security hardening"
- "I built an AI correlation engine that processes scan findings into risk scores and attack paths without external API dependencies"
- "I hardened the entire application against command injection, SQL injection, and authentication bypass"
- "I designed an asset deduplication system that merges overlapping scan results with first/last seen tracking"
- "I maintained 179 passing tests with 85%+ core coverage"

## Resume Bullet Points

- Architected and delivered OffenSec AI, a production-grade open-source security platform (19K+ LOC, 179 tests)
- Implemented JWT authentication, role-based authorization, and input validation across 39 API endpoints
- Built async multi-tool pipeline orchestrating Nmap, HTTPX, and Nuclei with subprocess security hardening
- Designed AI correlation engine processing vulnerability data into risk scores and attack path maps
- Created Clean Architecture monorepo with domain, application, infrastructure, and interface layers
- Developed automated asset deduplication scanning 6 dimensions of overlap (IP, hostname, port, protocol, technology, OS)
- Containerized full stack with Docker Compose (6 services) and implemented CI/CD with security scanning
- Published and maintained documentation suite including architecture, deployment, security, plugin development guides

## LinkedIn Post

```
🚀 I'm excited to share OffenSec AI — an open-source, AI-powered offensive security platform!

Built with Python (FastAPI), Next.js, PostgreSQL, and Docker, it coordinates Nmap, HTTPX, 
and Nuclei through a single interface, correlates findings with an AI engine, and generates 
professional reports.

🔹 39 API endpoints
🔹 179 passing tests  
🔹 Clean Architecture monorepo
🔹 JWT-secured, hardened subprocess execution
🔹 MIT licensed

Check it out: https://github.com/ANKIT48274/offensec-ai

#cybersecurity #opensource #python #fastapi #nextjs #security #pentesting
```

## GitHub Description

**Short:** AI-Powered Offensive Security Platform — automate reconnaissance, scanning, correlation, and reporting.

**Long:** Open-source platform that coordinates Nmap, HTTPX, Nuclei, Katana, and FFUF through a unified interface. Features include multi-tool scan pipelines, AI-driven evidence correlation with risk scoring, professional reporting (Executive, Technical, OWASP, PTES), asset management with dedup, and a plugin system. Built with FastAPI, Next.js 15, PostgreSQL, and Docker.

**One-line elevator pitch:** The open-source copilot for security assessments — from scan to report, powered by AI.
