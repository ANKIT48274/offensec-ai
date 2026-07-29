# Contributing

## Code of Conduct

This project follows an open, inclusive, and respectful community standard. Be respectful, assume good faith, and focus on constructive technical discussion.

## Getting Started

1. Fork the repository
2. Clone your fork
3. Set up the development environment (see [README](README.md#quick-start))
4. Create a feature branch

## Development Setup

```bash
# Backend
python3 -m venv .venv
source .venv/bin/activate
pip install -e backend -e ai -e plugins -e knowledge
pip install ruff mypy pytest pytest-asyncio

# Frontend
cd frontend
npm install
```

## Coding Standards

### Python
- Follow PEP 8 (enforced by Ruff)
- Use type hints for all function signatures
- Use `async def` for I/O-bound functions
- Write Pydantic models for all API input/output
- Maximum line length: 100 characters

### TypeScript / React
- Use TypeScript strict mode
- Prefer functional components with hooks
- Use Zustand for global state
- Use Tailwind CSS for styling

## Testing

All new features must include tests.

```bash
# Run all backend tests
PYTHONPATH=. pytest tests/unit/backend/ -v

# Run specific test file
PYTHONPATH=. pytest tests/unit/backend/infrastructure/test_nmap_parser.py -v
```

### Test Coverage Requirements

| Module | Minimum Coverage |
|--------|-----------------|
| Domain entities | 90% |
| Infrastructure | 80% |
| API routes | 75% |
| Frontend components | 70% |

## Pull Request Process

1. Ensure all tests pass
2. Run `ruff check .` and `ruff format --check .`
3. Update documentation if adding new features
4. Add changelog entry
5. Submit PR with clear description of changes

### PR Title Convention

```
feat: add X
fix: resolve X
docs: update X
refactor: simplify X
test: add tests for X
chore: update dependencies
```

## Code Review

All PRs require at least one approval from a maintainer. Reviewers will check:

- Correctness
- Test coverage
- Security (input validation, auth, injection prevention)
- Performance (pagination, async, DB queries)
- Code style and consistency
- Documentation

## Architecture Decisions

Significant architectural changes should follow an Architecture Decision Record (ADR) format in `docs/adr/`.

## Questions?

Open a GitHub Discussion or issue.
