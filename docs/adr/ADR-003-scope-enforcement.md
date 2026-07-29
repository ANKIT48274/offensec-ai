# ADR-003: Scope Enforcement Architecture

**Status:** Accepted
**Date:** 2026-07-29
**Deciders:** Security Architecture Team

## Context

The platform must ensure that all assessment activities remain within authorized scope boundaries. Scope violations during penetration testing can have legal and contractual consequences.

## Decision

Scope enforcement is implemented at **four independent layers**:

1. **Planning Layer** — AI-generated plans are validated against scope before presentation to the user.
2. **Execution Layer** — Tool commands are checked against allowed targets and techniques before execution.
3. **Evidence Layer** — Ingested evidence is tagged with scope metadata; cross-scope evidence is flagged.
4. **Reporting Layer** — Report generation excludes findings outside authorized scope.

### Key Decisions

- **Scope is defined as a data structure**, not a UI constraint. Scope objects are validated at every layer.
- **Fail closed**: violations block the operation and raise a `ScopeViolationError` with full audit trail.
- **Scope includes**: targets, excluded targets, allowed techniques, allowed tools, rate limits, and intrusive testing flag.
- **Audit logging records all scope checks**, including passes and violations.

## Consequences

- **Positive**: Defense-in-depth for scope enforcement; clear audit trail for compliance.
- **Negative**: Additional validation overhead on every operation; scope propagation across distributed components requires careful design.
