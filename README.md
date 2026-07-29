# OffenSec AI

> **AI-Powered Offensive Security Platform** — Automate reconnaissance, vulnerability scanning, correlation, and reporting with structured AI reasoning.

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.12+](https://img.shields.io/badge/Python-3.12%2B-blue?logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115%2B-009688?logo=fastapi)](https://fastapi.tiangolo.com)
[![Next.js](https://img.shields.io/badge/Next.js-15-000000?logo=next.js)](https://nextjs.org)
[![Docker](https://img.shields.io/badge/Docker-24%2B-2496ED?logo=docker)](https://docker.com)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-4169E1?logo=postgresql)](https://postgresql.org)
[![Redis](https://img.shields.io/badge/Redis-7-DC382D?logo=redis)](https://redis.io)
[![Tests](https://img.shields.io/badge/Tests-179%20passing-brightgreen)](https://github.com/ANKIT48274/offensec-ai/actions)
[![Code Style](https://img.shields.io/badge/Code%20Style-Ruff-black)](https://astral.sh/ruff)
[![Security](https://img.shields.io/badge/Security-JWT_%7C_bcrypt_%7C_CORS-important)](SECURITY.md)
[![GitHub Release](https://img.shields.io/github/v/release/ANKIT48274/offensec-ai?logo=github)](https://github.com/ANKIT48274/offensec-ai/releases)
[![Open Source](https://img.shields.io/badge/Open%20Source-MIT-green)](LICENSE)

---

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [Technology Stack](#technology-stack)
- [Quick Start](#quick-start)
- [Screenshots](#screenshots)
- [API Overview](#api-overview)
- [Security Features](#security-features)
- [Roadmap](#roadmap)
- [Project Structure](#project-structure)
- [FAQ](#faq)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

---

## Overview

OffenSec AI is an open-source, AI-augmented offensive security assessment platform. It coordinates multiple security tools — Nmap, HTTPX, Nuclei, Katana, FFUF — through a single interface, automates reconnaissance and vulnerability detection, and uses a structured AI correlation engine to analyze findings, rank risks, and generate professional reports.

**Why OffenSec AI?**

- **Unified interface** — Control Nmap, HTTPX, Nuclei, and discovery tools from one platform
- **AI-powered correlation** — Automatically connects findings across tools to identify attack paths and prioritise risks
- **Pipeline automation** — One-click runs Nmap → HTTPX → Nuclei with progress tracking
- **Professional reporting** — Executive, Technical, OWASP, PTES, CSV, and JSON export
- **Asset management** — Automatic deduplication with first/last seen tracking
- **Plugin system** — Extend with custom tools and methodologies
- **Open source** — MIT license, self-hosted, full control of your data

---

## Features

### Scan Engines
| Engine | Description |
|--------|-------------|
| **Nmap** | Port scanning, service detection, OS fingerprinting, script scanning |
| **HTTPX** | Web probing, technology detection, TLS grab, favicon hash |
| **Nuclei** | Template-based vulnerability scanning with CVE/CWE mapping |
| **Katana** | Web endpoint crawling and discovery |
| **FFUF** | Directory and file fuzzing |

### Discovery Tools
| Tool | Description |
|------|-------------|
| **DNS Enumeration** | A, AAAA, MX, NS, TXT, CNAME record lookup |
| **WHOIS** | Domain registration information |
| **Subdomain Enumeration** | DNS-based subdomain discovery |
| **TLS Analysis** | Certificate inspection, validity, SAN, issuer |

### AI Correlation
- Attack surface analysis (hosts, ports, high-risk services)
- Critical asset identification
- Risk ranking (0–100 scoring)
- Attack path mapping
- Executive summary generation
- Automated remediation recommendations

### Reporting
| Format | Style |
|--------|-------|
| Executive Summary | Non-technical stakeholder report |
| Technical Report | Detailed findings with evidence |
| OWASP Style | OWASP Top 10 mapped findings |
| PTES Style | PTES methodology format |
| CSV Export | Spreadsheet-compatible |
| JSON Export | Machine-readable format |

### Asset & Evidence
- Auto-deduplication with IP, hostname, port, technology, and OS merge
- First/last seen tracking with scan count
- Per-asset evidence timeline
- Technology badge aggregation

---

## Architecture

```mermaid
graph TB
    subgraph Frontend
        NEXT[Next.js 15 App]
        UI[Tailwind CSS UI]
        API_CLIENT[API Client]
    end

    subgraph Backend
        FASTAPI[FastAPI Server]
        JWT[JWT Auth]
        ROUTER[API Router]
        
        subgraph Services
            SCAN[Scan Services]
            PIPE[Pipeline Service]
            CORR[AI Correlation]
            ASSET[Asset Service]
            PLUGIN[Plugin Loader]
        end

        subgraph Engines
            N[Nmap Engine]
            H[HTTPX Engine]
            NUC[Nuclei Engine]
            K[Katana Engine]
            F[FFUF Engine]
        end
    end

    subgraph Database
        PG[(PostgreSQL)]
        RD[(Redis)]
    end

    subgraph Security Tools
        N[nmap]
        HX[httpx]
        NCL[nuclei]
        KTN[katana]
        FF[ffuf]
        dig[dig]
        WHOIS[whois]
    end

    NEXT --> FASTAPI
    API_CLIENT --> FASTAPI
    FASTAPI --> JWT
    ROUTER --> SCAN
    ROUTER --> PIPE
    ROUTER --> CORR
    ROUTER --> ASSET
    SCAN --> N
    PIPE --> N & HX & NCL
    NUC --> NCL
    K --> KTN
    F --> FF
    N --> dig
    N --> WHOIS
    SCAN --> PG
    PIPE --> PG
    CORR --> PG
    ASSET --> PG
    FASTAPI --> RD
```

---

## Technology Stack

| Layer | Technology |
|-------|-----------|
| **Backend** | Python 3.12+, FastAPI, Uvicorn |
| **Frontend** | Next.js 15, React 19, TypeScript, Tailwind CSS |
| **Database** | PostgreSQL 16, Redis 7 |
| **Auth** | JWT (HS256), bcrypt |
| **ORM** | SQLAlchemy 2.0 (async), Alembic |
| **AI** | Rules-based correlation engine (no external API required) |
| **Scan Tools** | Nmap, HTTPX, Nuclei, Katana, FFUF |
| **Container** | Docker, Docker Compose |
| **CI/CD** | GitHub Actions |
| **Code Quality** | Ruff, mypy, Prettier, ESLint |

---

## Quick Start

### Prerequisites

- Python 3.12+
- Node.js 22+
- Docker Engine 24+ with Compose V2
- PostgreSQL 16+
- Redis 7+
- Nmap, HTTPX, Nuclei (for scan features)

### Docker Installation (Recommended)

```bash
# Clone repository
git clone https://github.com/ANKIT48274/offensec-ai.git
cd offensec-ai

# Generate JWT secret
echo "JWT_SECRET=$(python3 -c 'import secrets; print(secrets.token_hex(32))')" > .env

# Start all services
docker compose up -d

# Apply database migrations
docker compose exec backend alembic upgrade head

# Access the platform
# Frontend: http://localhost:3000
# API:      http://localhost:8000
# Swagger:  http://localhost:8000/docs
```

### Manual Installation

```bash
# Backend
python3 -m venv .venv
source .venv/bin/activate
pip install -e backend -e ai -e plugins -e knowledge

# Database (ensure PostgreSQL and Redis are running)
alembic upgrade head

# Start backend
JWT_SECRET="your-secret-here" uvicorn backend.main:app --port 8000 --reload

# Frontend (separate terminal)
cd frontend
npm install
npm run dev

# Access the platform
# Frontend: http://localhost:3000
# API:      http://localhost:8000
```

### Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `JWT_SECRET` | **Yes** | — | HMAC signing key (min 32 chars) |
| `DATABASE_URL` | No | `postgresql+asyncpg://offensec:changeme@localhost:5432/offensec` | PostgreSQL connection string |
| `REDIS_URL` | No | `redis://localhost:6379/0` | Redis connection string |
| `CORS_ORIGINS` | No | `` | Comma-separated allowed origins |
| `LOG_LEVEL` | No | `INFO` | Log level (DEBUG, INFO, WARNING, ERROR) |
| `ENVIRONMENT` | No | `production` | Application environment |

---

## Screenshots

> Screenshots are generated from the running application.

| | |
|---|---|
| **Dashboard** | `docs/images/dashboard.png` |
| **Login** | `docs/images/login.png` |
| **Projects** | `docs/images/projects.png` |
| **Scan Pipeline** | `docs/images/pipeline.png` |
| **Nmap Results** | `docs/images/nmap-results.png` |
| **HTTPX Results** | `docs/images/httpx-results.png` |
| **Nuclei Results** | `docs/images/nuclei-results.png` |
| **AI Correlation** | `docs/images/ai-correlation.png` |
| **Risk Dashboard** | `docs/images/risk-dashboard.png` |
| **Swagger API** | `docs/images/swagger.png` |

---

## API Overview

The API exposes **39 endpoints** across 12 resource groups.

| Group | Prefix | Endpoints | Auth |
|-------|--------|-----------|------|
| Authentication | `/auth` | Register, Login, Me | No/Yes |
| Users | `/users` | Get, List | Yes |
| Projects | `/projects` | CRUD | Yes |
| Assessments | `/assessments` | CRUD + Start/Complete | Yes |
| Findings | `/findings` | CRUD | Yes |
| Reports | `/reports` | Generate | Yes |
| Scans | `/scans` | Run, List, Get | Yes |
| Pipeline | `/pipeline` | Start, Jobs, Get | Yes |
| Nuclei | `/nuclei` | Results, Stats | Yes |
| Assets | `/assets` | List, Get | Yes |
| Evidence | `/evidence` | List, Get | Yes |
| AI | `/ai` | Analyze, Report, Attack Paths | Yes |
| Dashboard | `/dashboard` | Overview, Trends, Graph | Yes |
| Plugins | `/plugins` | CRUD | Yes |

Full documentation available at `/docs` when the backend is running.

---

## Security Features

- **JWT Bearer authentication** on all endpoints (except register/login)
- **bcrypt password hashing** with 12 rounds
- **No hardcoded secrets** — all via environment variables
- **Subprocess input validation** — command injection prevention
- **SQLAlchemy ORM** — no raw SQL queries
- **CORS configuration** via environment
- **Graceful process termination** — SIGTERM before SIGKILL
- **Stderr output capped** at 64KB (OOM prevention)
- **Temp file cleanup** with try/finally on all paths

---

## Roadmap

### v1.0.0 (Current)
- ✅ Core CRUD operations
- ✅ Nmap, HTTPX, Nuclei scan engines
- ✅ Multi-tool pipeline
- ✅ Discovery tools (Katana, FFUF, DNS, WHOIS, TLS)
- ✅ Asset and evidence management
- ✅ AI correlation and risk scoring
- ✅ Professional reports (Executive, Technical, OWASP, PTES)
- ✅ Plugin system
- ✅ Dashboard and analytics
- ✅ 39 API endpoints, 179 tests

### v1.1.0 (Planned)
- [ ] Background task queue (Celery/Redis)
- [ ] WebSocket for live scan progress
- [ ] Report PDF generation (WeasyPrint)
- [ ] Light mode theme
- [ ] API rate limiting
- [ ] Rollback database migrations

### v2.0.0 (Future)
- [ ] Multi-tenant support (MSSP)
- [ ] Cloud security assessment (AWS, Azure, GCP)
- [ ] Mobile application assessment
- [ ] AI red teaming modules
- [ ] Continuous assessment mode
- [ ] Automated false positive reduction

---

## Project Structure

```
OffenSec-AI/
├── backend/                     # FastAPI application
│   ├── domain/                  # Business entities, value objects, events
│   ├── application/             # Services, use cases, DTOs
│   ├── infrastructure/          # DB, auth, scan engines, plugins, reporting
│   └── interfaces/              # REST API routes, WebSocket, CLI
├── frontend/                    # Next.js + TypeScript SPA
│   ├── app/                     # App router pages
│   ├── components/              # Shared UI components
│   ├── lib/                     # API client, hooks, stores
│   └── stores/                  # Zustand state management
├── ai/                          # AI agents, planner, analyst, writer
├── plugins/                     # Plugin SDK, registry, sandbox
├── knowledge/                   # Methodology playbooks, framework mappings
├── tests/                       # Unit, integration, security tests
├── docs/                        # Architecture, API, deployment, security guides
├── infra/                       # Docker, Kubernetes configurations
└── .github/                     # CI/CD workflows
```

---

## FAQ

**Q: Is OffenSec AI completely free?**  
A: Yes. MIT licensed, self-hosted, no paid tiers.

**Q: Does it require an internet connection?**  
A: No. Core functionality works fully offline. AI analysis is rules-based.

**Q: Can I use my own AI model?**  
A: The correlation engine is rules-based. Future releases will support local and cloud LLMs.

**Q: What targets can I scan?**  
A: Any network reachable target — IPs, hostnames, CIDR ranges.

**Q: Is it safe to run on production systems?**  
A: Yes. You control scope and exploitation. Passive scanning by default.

---

## Troubleshooting

**Backend won't start: "JWT_SECRET is not set"**  
→ Generate and set `JWT_SECRET` environment variable.

**Database connection error**  
→ Ensure PostgreSQL is running and `DATABASE_URL` is correct.

**Nmap not found**  
→ Install nmap: `sudo apt install nmap` (Linux) or `brew install nmap` (macOS).

**Frontend shows "Network error"**  
→ Ensure backend is running on port 8000. Check Next.js API proxy in `next.config.js`.

---

## Contributing

Contributions are welcome. See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'feat: add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

Please ensure tests pass and code is formatted with Ruff.

---

## License

MIT License. See [LICENSE](LICENSE) for full text.

---

<p align="center">Built with ❤️ for the security community</p>
