# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2026-07-29

### Added
- Project foundation with monorepo structure.
- FastAPI backend with Clean Architecture (domain, application, infrastructure, interfaces).
- PostgreSQL ORM models with Alembic migrations.
- Redis caching and token blacklist infrastructure.
- JWT authentication with bcrypt password hashing.
- Project, Assessment, Finding, and Report management APIs.
- AI agent framework with 6 specialized agents (recon, enumeration, vuln_analysis, path_analysis, report_writer, teacher).
- AI model abstraction layer supporting local and cloud providers.
- Plugin system with SDK, registry, and sandbox runtime.
- Knowledge base with methodology playbooks (web, network, AD, API, cloud, mobile).
- OWASP Top 10 and MITRE ATT&CK framework mappings.
- WebSocket handler for real-time assessment updates.
- Docker Compose for all services (postgres, redis, backend, frontend, ai-runner, plugin-sandbox).
- GitHub Actions workflows for CI, release, security scanning, and Docker publishing.
- Frontend application with Next.js 15, React 19, and TypeScript.
- Component library (sidebar, forms, lists, detail views, analytics dashboard).
- API client and Zustand state management stores.
- Comprehensive test suite for domain entities, value objects, events, auth, and reporting.
