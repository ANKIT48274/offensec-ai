# Contributing to OffenSec AI

## Code of Conduct

All contributors must adhere to the code of conduct defined in `CODE_OF_CONDUCT.md`.

## Getting Started

1. Fork the repository.
2. Set up the development environment (see `development-setup.md`).
3. Create a feature branch from `develop`.
4. Make your changes.
5. Submit a pull request to `develop`.

## Pull Request Requirements

- Description of the change and its motivation.
- Link to related issue(s).
- All tests pass.
- New code includes tests.
- Code follows project style guidelines (ruff, mypy, prettier).
- Documentation updated if applicable.

## Code Standards

### Python

- Python 3.12+
- Type annotations required for all function signatures.
- Use `ruff` for formatting and linting.
- Use `mypy` in strict mode for type checking.
- Domain logic must not depend on framework code.
- Tests use `pytest` with `asyncio_mode = "auto"`.

### TypeScript/React

- TypeScript strict mode enabled.
- Use functional components with hooks.
- Props typed with TypeScript interfaces.
- State management via Zustand stores.

## Commit Naming Conventions

```
<type>(<scope>): <description>

Types: feat, fix, refactor, test, docs, chore, security
Scopes: backend, frontend, ai, plugins, knowledge, infra, ci

Example: feat(backend): add assessment state machine
```

## Security Considerations

- Never commit secrets, keys, or credentials.
- Validate and sanitize all user inputs.
- AI outputs must pass schema validation.
- Scope violations must be caught before execution.
- All actions must be auditable.
