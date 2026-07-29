# Security

## Authentication

OffenSec AI uses **JWT Bearer tokens** for API authentication. All endpoints except `/auth/register` and `/auth/login` require a valid Bearer token in the `Authorization` header.

### Token Format

```
Authorization: Bearer <jwt_token>
```

### Token Lifetime

| Token | Lifetime |
|-------|----------|
| Access Token | 60 minutes |
| Refresh Token | 7 days |

### Setup

Generate a secure JWT secret:

```bash
python3 -c 'import secrets; print(secrets.token_hex(32))'
```

Set the `JWT_SECRET` environment variable:

```bash
export JWT_SECRET="<your-generated-secret>"
```

**Note:** The application will refuse to start without `JWT_SECRET` set.

## Password Storage

Passwords are hashed using **bcrypt** with 12 salt rounds.

## Subprocess Security

All external tool execution uses `asyncio.create_subprocess_exec` with literal command arrays — no shell execution, no string interpolation into shell commands.

### Input Validation

- All target inputs are validated with `ipaddress.ip_address()` or strict hostname regex
- Extracted live hosts from Nmap XML are re-validated before passing to HTTPX/Nuclei
- Process stderr output is capped at 64KB to prevent memory exhaustion

### Process Termination

Two-phase graceful termination:
1. `SIGTERM` sent first
2. `SIGKILL` sent after 5-second timeout

## Database

- All queries use SQLAlchemy ORM (no raw SQL)
- Connection pooling with `pool_pre_ping=True`
- Credentials configured via `DATABASE_URL` environment variable

## API Security

| Measure | Status |
|---------|--------|
| Authentication | JWT Bearer required |
| Input Validation | Pydantic schemas on all endpoints |
| CORS | Configurable via `CORS_ORIGINS` env var |
| Rate Limiting | Configured at reverse proxy level |
| Error Handling | Structured error responses, no stack traces exposed |

## Production Checklist

- [ ] Generate and set `JWT_SECRET` (min 32 random characters)
- [ ] Configure `DATABASE_URL` with strong password
- [ ] Set `CORS_ORIGINS` to specific allowed origins
- [ ] Run `pip-audit` to check Python dependencies
- [ ] Run `npm audit` to check frontend dependencies
- [ ] Use non-root user in Docker containers
- [ ] Configure TLS/SSL at reverse proxy
- [ ] Set up database backups
- [ ] Monitor structured JSON logs

## Reporting Vulnerabilities

Please report security issues to the GitHub Issues tracker with the label `security`.
