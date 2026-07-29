# Security Guide

## Authentication

OffenSec AI uses **JWT Bearer tokens** for all API authentication.

### Setup

1. Generate a secure JWT secret:
   ```bash
   python3 -c 'import secrets; print(secrets.token_hex(32))'
   ```

2. Set the `JWT_SECRET` environment variable before starting:
   ```bash
   export JWT_SECRET="<your-generated-secret>"
   ```

3. All API endpoints (except `/auth/register` and `/auth/login`) require:
   ```
   Authorization: Bearer <token>
   ```

### Token Lifetime

- Access tokens: 60 minutes
- Refresh tokens: 7 days

## Subprocess Security

All external tool execution (nmap, httpx, nuclei, katana, ffuf) uses `asyncio.create_subprocess_exec` with explicit argument arrays (no shell=True).

### Validation

- All target inputs are validated against `ipaddress.ip_address()` or hostname regex before execution.
- Extracted live hosts from nmap XML are re-validated before passing to httpx/nuclei.
- Output is capped at 64KB for stderr to prevent OOM.

### Process Termination

All subprocesses use a graceful two-phase termination:
1. `SIGTERM` is sent first
2. After 5-second timeout, `SIGKILL` is used as fallback

## Database Security

- All queries use SQLAlchemy ORM — no raw SQL.
- Database URL must be configured via `DATABASE_URL` environment variable.
- Default credentials are for development only.

## API Security

- CORS origins must be explicitly configured via `CORS_ORIGINS`.
- Rate limiting should be configured at the reverse proxy level.
- All input validation via Pydantic schemas.

## Deployment Checklist

- [ ] Set `JWT_SECRET` to a secure random value (min 32 chars)
- [ ] Set `DATABASE_URL` to production PostgreSQL with strong password
- [ ] Set `CORS_ORIGINS` to specific allowed origins
- [ ] Run `pip-audit` and `npm audit` to check for vulnerable dependencies
- [ ] Enable `SCOPE_ENFORCEMENT=true`
- [ ] Use non-root user in Docker containers
- [ ] Configure TLS/SSL for production
- [ ] Set up database backup schedule
- [ ] Monitor logs via structured JSON output
