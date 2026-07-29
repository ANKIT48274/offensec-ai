# OffenSec AI — v1.0.0

**AI-Powered Offensive Security Platform**

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                      Frontend (Next.js 15)                   │
│  Auth │ Projects │ Scans │ Pipeline │ Assets │ Nuclei │ AI  │
├─────────────────────────────────────────────────────────────┤
│                    API Layer (FastAPI)                       │
│  Auth │ CRUD │ Scan │ Pipeline │ Nuclei │ Assets │ AI/Dash  │
├─────────────────────────────────────────────────────────────┤
│                    Application Layer                         │
│  Services │ Use Cases │ DTOs │ Correlation Engine           │
├─────────────────────────────────────────────────────────────┤
│                    Domain Layer                              │
│  Entities │ Value Objects │ Events │ Exceptions             │
├─────────────────────────────────────────────────────────────┤
│                 Infrastructure Layer                         │
│  Scan Engine │ Pipeline │ Nuclei │ Discovery │ Plugins      │
│  Reporting  │ Auth/JWT │ DB (PostgreSQL) │ Redis           │
├─────────────────────────────────────────────────────────────┤
│              External Tools (subprocess)                     │
│  Nmap │ HTTPX │ Nuclei │ Katana │ FFUF │ dig │ whois       │
└─────────────────────────────────────────────────────────────┘
```

### Clean Architecture Layers

| Layer | Directory | Responsibility |
|-------|-----------|----------------|
| **Domain** | `backend/domain/` | Business entities, value objects, events, exceptions |
| **Application** | `backend/application/` | Services, use cases, DTOs, port interfaces |
| **Infrastructure** | `backend/infrastructure/` | DB, auth, scan engines, reporting, plugins, discovery |
| **Interfaces** | `backend/interfaces/` | REST API, WebSocket, CLI, webhooks |
| **Frontend** | `frontend/` | Next.js SPA with App Router |

---

## Implemented Features

### Core Platform
- ✅ User authentication (JWT + bcrypt)
- ✅ Project management (CRUD)
- ✅ Assessment lifecycle (Draft → Active → Complete)
- ✅ Finding management with severity/confidence scoring
- ✅ Report generation (Executive, Technical, OWASP, PTES)
- ✅ CSV and JSON data export

### Scan Engines
- ✅ **Nmap Engine** — Port scanning, service detection, OS fingerprinting, XML parsing
- ✅ **HTTPX Engine** — Web service probing, technology detection, TLS grab, favicon hash
- ✅ **Nuclei Engine** — Vulnerability scanning with template-based detection, CVE/CWE mapping
- ✅ **Pipeline Engine** — Multi-tool orchestration: Nmap → HTTPX → Nuclei → Store

### Discovery Tools (Phase 2)
- ✅ **Katana** — Web endpoint crawling and discovery
- ✅ **FFUF** — Directory and file fuzzing
- ✅ **DNS Enumeration** — A/AAAA/MX/NS/TXT/CNAME record lookup
- ✅ **WHOIS Lookup** — Domain registration information
- ✅ **Subdomain Enumeration** — DNS-based subdomain discovery
- ✅ **TLS Analysis** — Certificate inspection, validity, SAN, issuer

### Asset & Evidence Management
- ✅ Asset tracking with dedup (IPs, hostnames, ports, technologies, OS)
- ✅ Evidence storage (raw output, file paths, metadata)
- ✅ First/last seen tracking with scan count
- ✅ Asset → Evidence → Finding relationships

### AI Correlation Engine
- ✅ Attack surface analysis (hosts, ports, high-risk services)
- ✅ Critical asset identification
- ✅ Risk ranking and scoring (0–100)
- ✅ Attack path mapping
- ✅ Executive summary generation
- ✅ Automated recommendations

### Reporting
- ✅ Executive Summary — Non-technical stakeholder report
- ✅ Technical Report — Detailed technical findings
- ✅ OWASP Style — OWASP Top 10 mapped findings
- ✅ PTES Style — Penetration Testing Execution Standard format
- ✅ CSV Export — Spreadsheet-compatible format
- ✅ JSON Export — Machine-readable format
- ✅ PDF Generation (via WeasyPrint)

### Security (Phase 5)
- ✅ JWT Bearer authentication on all endpoints
- ✅ No hardcoded secrets — all via environment
- ✅ Subprocess input validation (command injection prevention)
- ✅ Graceful process termination (SIGTERM → SIGKILL)
- ✅ Stderr capped at 64KB (OOM prevention)
- ✅ Temp file cleanup with try/finally
- ✅ CORS configuration via environment

### Performance (Phase 6)
- ✅ Database indexes on all foreign keys and filtered columns
- ✅ Connection pooling (pool_size=10, max_overflow=20)
- ✅ Pagination on all list endpoints
- ✅ Alembic migration `007_add_indexes.py`

### CI/CD (Phase 5)
- ✅ GitHub Actions CI (lint, test, build)
- ✅ Security scanning (`pip-audit`, `npm audit`)
- ✅ Docker Compose health checks
- ✅ Release workflow with GHCR publishing

### Plugin System (Phase 4)
- ✅ Plugin SDK with manifest.json discovery
- ✅ Plugin loader with filesystem scanning
- ✅ Plugin capability declarations
- ✅ Plugin sandbox Docker container

### Frontend
- ✅ 17 routed pages (auth, projects, scans, pipeline, assets, nuclei, reports, analytics, settings)
- ✅ Dark mode UI with Tailwind CSS
- ✅ API proxy configuration
- ✅ Login/register flow
- ✅ Toast/error notifications
- ✅ Suspense boundary wrapping

---

## Security Summary

| Category | Status |
|----------|--------|
| Authentication | JWT Bearer tokens, 60min access, 7-day refresh |
| Authorization | Token-verified user identity on all endpoints |
| Command Injection | Blocked — `create_subprocess_exec` with validated inputs |
| SQL Injection | Blocked — SQLAlchemy ORM throughout |
| XSS | Mitigated — No raw HTML rendering, React escaping |
| Secrets Management | No hardcoded secrets, all via `JWT_SECRET` env var |
| Subprocess Safety | Graceful SIGTERM/SIGKILL, stderr limits, temp cleanup |
| CORS | Configurable via environment, no wildcard in production |

---

## Performance Summary

| Metric | Target | Current |
|--------|--------|---------|
| DB connection pool | 10-30 | 10+20 overflow |
| List endpoint pagination | Required | Implemented |
| Database indexes | All FKs + filtered | 20+ indexes (migration 007) |
| Subprocess stderr limit | 64KB | Implemented |
| API request timeout | Configurable | Per-tool configurable |
| Async operations | Full async | SQLAlchemy AsyncSession, asyncio |

---

## Remaining Known Issues

### P2: High Priority
| Issue | File | Description |
|-------|------|-------------|
| No token revocation | `auth.py` | No refresh token blacklist |
| No rate limiting | `main.py` | No API rate limiting middleware |
| Duplicate nmap code | `scan_engine/` vs `pipeline/` | Similar but different configurations |

### P3: Medium Priority
| Issue | File | Description |
|-------|------|-------------|
| Blanket except Exception | All route files | Should catch specific exceptions |
| Transaction management | `di.py` | No explicit transaction boundaries |
| Unused imports | Various | 111 ruff warnings (mostly F401) |

### P4: Low Priority
| Issue | Description |
|-------|-------------|
| No error boundary in frontend | Add `global-error.tsx` |
| `any` types in Zustand stores | Use typed interfaces |
| Duplicate cleanup functions | Extract to shared utility |

---

## Version

**v1.0.0**

---

## Release Notes

### Added
- Full authentication system with JWT Bearer tokens
- Project, Assessment, Finding, Report CRUD APIs
- Nmap, HTTPX, Nuclei scan engines with async subprocess execution
- Multi-tool pipeline (Nmap → HTTPX → Nuclei)
- Katana endpoint crawling, FFUF directory fuzzing
- DNS enumeration, WHOIS, subdomain discovery, TLS analysis
- Asset management with dedup and evidence tracking
- AI correlation engine with risk scoring and attack path analysis
- Report templates (Executive, Technical, OWASP, PTES)
- CSV and JSON data export
- Plugin system with SDK and loader
- Dashboard API with overview statistics
- Production Docker Compose with health checks
- Database indexing migration (20+ indexes)
- Comprehensive CI/CD with security scanning
- Security guide and deployment documentation

### Fixed
- Authentication bypass via x-user-id header
- Hardcoded JWT secret default
- Temp file leaks on exception paths
- Subprocess SIGKILL without grace period
- Multiple SQLAlchemy model relationship errors
- Redis shutdown method compatibility

### Tests
- 179 unit tests
- Test categories: domain entities, value objects, events, exceptions,
  services, auth, reporting, scan pipelines, parsers (nmap, httpx, nuclei),
  discovery runners, plugin loader, dashboard

---

## Production Checklist

- [ ] Generate and set `JWT_SECRET` (min 32 random characters)
- [ ] Configure `DATABASE_URL` with production PostgreSQL credentials
- [ ] Set `CORS_ORIGINS` to comma-separated list of allowed origins
- [ ] Run `pip-audit` to check Python dependency vulnerabilities
- [ ] Run `npm audit` to check Node.js dependency vulnerabilities
- [ ] Configure `LOG_LEVEL=INFO` in production
- [ ] Enable `SCOPE_ENFORCEMENT=true`
- [ ] Create non-root Docker user
- [ ] Set up PostgreSQL backup schedule
- [ ] Configure reverse proxy TLS/SSL
- [ ] Set up log aggregation (ELK/Loki)
- [ ] Configure monitoring alerts
- [ ] Run `alembic upgrade head` for schema migrations
- [ ] Verify health endpoint returns 200
- [ ] Run full test suite: `PYTHONPATH=. pytest tests/ -v`
