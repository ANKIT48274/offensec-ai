# ADR-002: AI Model Abstraction Layer

**Status:** Accepted
**Date:** 2026-07-29
**Deciders:** Architecture Team

## Context

The platform must support multiple AI model providers (local, OpenAI, Anthropic, Ollama) without coupling assessment logic to any specific provider.

## Decision

Introduce a **Model Abstraction Layer** with the following components:

1. **Abstract Base Client** — Defines the contract for all AI operations (plan, analyze, report, explain).
2. **Provider Implementations** — One per provider (Local, OpenAI, Anthropic), implementing the abstract interface.
3. **Factory Function** — Creates the appropriate client based on environment configuration.
4. **Model Router** — Selects providers per task type based on capability requirements.
5. **Model Cache** — Caches responses to avoid redundant API calls.

### Key Decisions

- **Provider is selected at startup** via `AI_MODEL_PROVIDER` environment variable.
- **Local inference runs in a separate container** (ai-runner) to allow GPU isolation.
- **All AI outputs must pass through a validation gate** before reaching the user.
- **No user assessment data is used for model training** — enforced at the client layer.

## Consequences

- **Positive**: Provider agnosticism; ability to run fully offline; easy to add new providers.
- **Negative**: Additional latency for structured output validation; limited to lowest-common-denominator capabilities across providers.
