# ADR-001: Project Structure and Architecture

**Status:** Accepted
**Date:** 2026-07-29
**Deciders:** Architecture Team

## Context

The OffenSec AI platform requires a modular, scalable architecture that supports multiple integration patterns (REST API, WebSocket, CLI, plugins) while maintaining clean separation of concerns.

## Decision

We adopt a **Clean Architecture** with four layers:

1. **Domain Layer** — Core business entities, value objects, events, and exceptions. No external dependencies.
2. **Application Layer** — Use cases, services, DTOs, and port interfaces (driven ports). Depends only on domain.
3. **Infrastructure Layer** — Persistence (PostgreSQL, Redis, file), external integrations (AI providers, security tools), logging, and authentication. Implements application ports.
4. **Interfaces Layer** — API routes, CLI commands, webhooks, and middleware. Translates external requests into application calls.

### Key Decisions

- **Monorepo layout** with separate `pyproject.toml` per component for independent versioning and dependency management.
- **Interface-based dependency injection** via protocol classes in the application layer.
- **Domain events** for cross-module communication, published asynchronously through an event bus.
- **CQRS-lite**: Queries go through repositories directly; commands go through service/use-case layer.

## Consequences

- **Positive**: Independent deployability of components; clear test boundaries; domain logic remains framework-agnostic.
- **Negative**: More files and boilerplate for simple CRUD operations.
- **Mitigation**: Repository implementations provide helper methods; DTOs generated from Pydantic models.
