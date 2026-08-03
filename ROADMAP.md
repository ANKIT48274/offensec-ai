# Roadmap

## v1.0.0 (Current Release) — Foundation

Completed features:
- ✅ Core CRUD (Users, Projects, Assessments, Findings, Reports)
- ✅ JWT Authentication with bcrypt password hashing
- ✅ Nmap scan engine with XML parsing
- ✅ HTTPX web probing with technology detection
- ✅ Nuclei template-based vulnerability scanning
- ✅ Multi-tool scan pipeline (Nmap → HTTPX → Nuclei)
- ✅ Asset management with automatic deduplication
- ✅ Evidence storage with source tracking
- ✅ AI correlation engine with risk scoring (0–100)
- ✅ Attack path detection and mapping
- ✅ Professional reports (Executive, Technical, OWASP, PTES, CSV, JSON)
- ✅ Discovery tools (Katana, FFUF, DNS, WHOIS, TLS, Subdomain)
- ✅ Plugin system with SDK and loader
- ✅ Dashboard API with overview statistics
- ✅ Production Docker Compose with health checks
- ✅ Database indexing (20+ indexes across all tables)
- ✅ GitHub Actions CI/CD with security scanning
- ✅ 39 API endpoints, 179 passing tests

## v1.1.0 — Performance & UX

- [ ] Background task queue (Celery/Redis) for non-blocking scans
- [ ] WebSocket-based live scan progress in frontend
- [ ] PDF report generation (WeasyPrint integration)
- [ ] Light mode / dark mode theme toggle
- [ ] Global error boundary in frontend
- [x] API rate limiting middleware (Redis-backed, auth endpoints stricter)
- [x] Refresh token blacklist (Redis-based revocation + logout endpoint)
- [ ] Rollback database migrations to any revision
- [x] Frontend/API E2E test suite (full user journey against running stack)
- [ ] Performance benchmark suite
- [x] Password hash never exposed via API (register/me/users)
- [x] Scan tools bundled in Docker image (nmap, httpx, nuclei, katana, ffuf)
- [x] Frontend health endpoint for container healthchecks

## v1.2.0 — Intelligence

- [ ] AWS S3/GCS for evidence storage
- [ ] LLM integration for natural language report generation
- [ ] Advanced attack path graphing (visual graph UI)
- [ ] Automated false positive reduction with ML heuristics
- [ ] Scheduled recurring assessments
- [ ] Email notification for assessment completion
- [ ] Custom methodology playbooks
- [ ] Findings deduplication across assessments
- [ ] Timeline view for asset changes

## v2.0.0 — Scale

- [ ] Multi-tenant architecture (MSSP mode)
- [ ] Cloud security assessment (AWS, Azure, GCP modules)
- [ ] Mobile application assessment (Android, iOS)
- [ ] Active Directory attack path analysis
- [ ] Compliance reporting (PCI DSS, SOC 2, HIPAA, ISO 27001)
- [ ] API security testing module
- [ ] Red team exercise planner with OPSEC awareness
- [ ] Community plugin registry
- [ ] Real-time collaborative assessments

## Long Term

- Continuous assessment mode with drift detection
- AI-driven penetration testing agent framework
- Integration with SIEM and SOAR platforms
- Bug bounty program integration
- Managed cloud offering
- Industry certification for AI-augmented pentesting methodology

---

## Release Cadence

| Version | Timeline | Focus |
|---------|----------|-------|
| v1.0.x | Now | Stability and bug fixes |
| v1.1.x | Q3 2026 | Performance and UX |
| v1.2.x | Q4 2026 | Intelligence and automation |
| v2.0.x | 2027 | Scale and enterprise |
