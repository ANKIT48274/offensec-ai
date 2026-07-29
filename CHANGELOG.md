# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] — 2026-07-30

### Added
- Full authentication system with JWT Bearer tokens (register, login, token verification)
- bcrypt password hashing with 12 rounds
- Project CRUD with owner authorization
- Assessment lifecycle (draft → in_progress → completed)
- Finding management with severity/confidence scoring and CWE/CVSS mapping
- Report generation: Executive, Technical, OWASP, PTES, CSV, JSON
- Nmap scan engine with XML parsing (ports, services, OS, scripts)
- HTTPX web probing with technology detection, TLS grab, favicon hash
- Nuclei vulnerability scanning with CVE/CWE mapping
- Multi-tool pipeline (Nmap → HTTPX → Nuclei) with progress tracking
- Katana web endpoint crawling
- FFUF directory fuzzing
- DNS enumeration (A, AAAA, MX, NS, TXT, CNAME)
- WHOIS domain lookup
- DNS-based subdomain enumeration
- TLS certificate analysis
- Asset management with automatic deduplication
- Evidence storage with source tracking
- AI correlation engine with risk scoring (0–100)
- Attack path detection and mapping
- Dashboard API with overview statistics
- Plugin system with SDK and filesystem loader
- Database indexing (20+ indexes across all tables)
- PostgreSQL, Redis, and Backend health checks
- GitHub Actions CI/CD (lint, test, security scan, Docker build)
- Production and development Docker Compose configurations
- Structured JSON logging

### Changed
- Authentication moved from `x-user-id` header to JWT Bearer tokens
- Subprocess termination: SIGTERM before SIGKILL
- Temp file cleanup with try/finally on all paths
- Stderr output capped at 64KB
- All list endpoints paginated
- All route files updated for security hardening

### Removed
- Hardcoded JWT secret default (must now be set via environment)
- Unused `x-user-id` header pattern

### Security
- Command injection blocked via `create_subprocess_exec` with validated inputs
- SQL injection blocked via SQLAlchemy ORM
- No hardcoded secrets — all via environment
- CORS configurable via `CORS_ORIGINS`
- Graceful subprocess termination

## [0.2.0] — 2026-07-29

### Added
- Nmap scan runner with XML parsing
- HTTPX JSONL parser
- Pipeline engine: Nmap → HTTPX → Store
- Job management API
- Progress indicators in frontend
- 107 passing tests

## [0.1.0] — 2026-07-29

### Added
- Project foundation with monorepo structure
- FastAPI backend with Clean Architecture
- PostgreSQL ORM models with Alembic migrations
- Redis caching infrastructure
- JWT authentication with bcrypt
- CRUD for Projects, Assessments, Findings, Reports
- AI agent framework with 6 specialized agents
- Plugin system with SDK and sandbox
- Knowledge base with methodology playbooks
- OWASP and MITRE ATT&CK framework mappings
- WebSocket handler
- Docker Compose for all services
- GitHub Actions workflows
- Frontend with Next.js 15 and TypeScript
- 80 passing tests
