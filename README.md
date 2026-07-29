# OffenSec AI

AI-Powered Offensive Security Platform

## Overview

OffenSec AI is an open-source platform that applies structured AI reasoning to offensive security assessments. The platform automates reconnaissance planning, evidence correlation, vulnerability analysis, and report generation while keeping all exploitation decisions under human control.

## Architecture

This repository is a monorepo containing the following primary components:

| Component | Directory | Description |
|---|---|---|
| Backend API | `backend/` | FastAPI application with clean architecture (domain, application, infrastructure, interfaces) |
| Web Frontend | `frontend/` | Next.js + TypeScript application |
| AI Engine | `ai/` | Agent definitions, model abstraction layer, planning engine, reasoning pipeline |
| Plugin System | `plugins/` | Plugin SDK, registry, sandbox runtime, community module loader |
| Knowledge Base | `knowledge/` | Methodology playbooks, vulnerability data, framework mappings, evidence store schema |
| Infrastructure | `infra/` | Docker Compose configurations |
| Documentation | `docs/` | Architecture decisions (ADRs), API reference, developer guides |
| CI/CD | `.github/` | GitHub Actions workflows, release automation, quality gates |

## Repository Structure

```
OffenSec-AI/
├── backend/              # FastAPI application
│   ├── domain/           # Business entities and domain logic
│   ├── application/      # Use cases and orchestration
│   ├── infrastructure/   # External integrations and persistence
│   └── interfaces/       # API routes and middleware
├── frontend/             # Next.js + TypeScript SPA
│   ├── app/              # Next.js app router pages
│   ├── components/       # Shared UI components
│   ├── lib/              # Client-side utilities and API client
│   └── stores/           # State management
├── ai/                   # AI engine
│   ├── agents/           # Specialized AI agent implementations
│   ├── planner/          # Assessment planning engine
│   ├── analyst/          # Vulnerability analysis pipeline
│   ├── writer/           # Report generation engine
│   ├── teacher/          # Learning and explanation engine
│   ├── models/           # Model abstraction and routing layer
│   └── reasoning/        # Structured reasoning pipelines
├── plugins/              # Plugin infrastructure
│   ├── sdk/              # Plugin development kit
│   ├── registry/         # Plugin registry and metadata
│   ├── sandbox/          # Isolated plugin runtime
│   └── community/        # Community-contributed plugins
├── knowledge/            # Structured knowledge base
│   ├── methodologies/    # Assessment methodology playbooks
│   ├── frameworks/       # OWASP, MITRE ATT&CK, NIST mappings
│   ├── signatures/       # Vulnerability signatures and patterns
│   └── evidence/         # Evidence store schemas and migrations
├── tests/                # Cross-cutting test suites
│   ├── unit/             # Unit tests per component
│   ├── integration/      # Integration tests across boundaries
│   ├── e2e/              # End-to-end platform tests
│   ├── security/         # Security-focused test suite
│   └── fixtures/         # Shared test data and mocks
├── docs/                 # Documentation
│   ├── adr/              # Architecture Decision Records
│   ├── api/              # API reference documentation
│   └── guides/           # Setup and operations guides
├── infra/                # Infrastructure as code
│   └── docker/           # Dockerfiles
├── .github/              # GitHub configuration
│   ├── workflows/        # CI/CD pipeline definitions
│   ├── actions/          # Reusable composite actions
│   └── templates/        # Issue and PR templates
├── .env.example          # Environment variable reference
├── .gitignore            # Git exclusion rules
├── LICENSE               # MIT License
├── docker-compose.yml    # Production service definitions
├── docker-compose.dev.yml# Development service definitions
├── Makefile              # Top-level build and development commands
├── pyproject.toml        # Root Python project metadata
├── package.json          # Root workspace configuration
└── README.md             # This file
```

## Required Dependencies

- Python 3.12+
- Node.js 22+
- Docker Engine 24+ with Compose V2
- PostgreSQL 16+
- Redis 7+

## Quick Start

See `docs/guides/development-setup.md` for local environment setup instructions.

## Documentation

- `docs/adr/` — Architecture Decision Records
- `docs/api/v1/` — API reference documentation
- `docs/guides/development-setup.md` — Local setup guide
- `docs/guides/contributing.md` — Contribution guidelines

## License

MIT License. See `LICENSE` for details.
