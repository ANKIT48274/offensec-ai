# Deployment Guide

## Prerequisites

- Docker Engine 24+ with Compose V2
- 4 GB RAM minimum (8 GB recommended)
- 10 GB free disk space
- PostgreSQL 16+ (for manual install)
- Redis 7+ (for manual install)

## Docker Deployment (Recommended)

### Production

```bash
# 1. Clone and enter
git clone https://github.com/ANKIT48274/offensec-ai.git
cd offensec-ai

# 2. Configure secrets
echo "JWT_SECRET=$(python3 -c 'import secrets; print(secrets.token_hex(32))')" >> .env

# 3. Start all services
docker compose up -d

# 4. Apply migrations
docker compose exec backend alembic upgrade head

# 5. Verify
curl http://localhost:8000/health
# Expected: {"status":"ok","version":"0.1.0"}
```

### Development

```bash
docker compose -f docker-compose.dev.yml up --build
```

## Manual Installation

### Backend

```bash
# System dependencies
sudo apt install nmap postgresql redis-server python3.12 python3.12-venv
# Or on macOS: brew install nmap postgresql redis python@3.12

# Python setup
python3.12 -m venv .venv
source .venv/bin/activate
pip install -e backend -e ai -e plugins -e knowledge

# Database setup
sudo systemctl start postgresql redis-server
createdb offensec

# Configure environment
export JWT_SECRET="your-32-char-secret"
export DATABASE_URL="postgresql+asyncpg://user:pass@localhost/offensec"

# Run migrations
alembic upgrade head

# Start
uvicorn backend.main:app --host 0.0.0.0 --port 8000 --workers 4
```

### Frontend

```bash
cd frontend
npm install
npm run build
npm start
```

## Environment Configuration

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `JWT_SECRET` | Yes | — | HMAC signing key (min 32 chars) |
| `DATABASE_URL` | No | `postgresql+asyncpg://offensec:changeme@localhost:5432/offensec` | PostgreSQL connection |
| `REDIS_URL` | No | `redis://localhost:6379/0` | Redis connection |
| `CORS_ORIGINS` | No | `` | Comma-separated allowed CORS origins |
| `LOG_LEVEL` | No | `INFO` | Logging level |
| `ENVIRONMENT` | No | `production` | `development` or `production` |

## Database Migrations

```bash
# Apply all pending migrations
alembic upgrade head

# Rollback last migration
alembic downgrade -1

# Check migration history
alembic history
```

## Monitoring

### Health Checks

```bash
# API health
curl http://localhost:8000/health

# Database health (Docker)
docker compose exec postgres pg_isready -U offensec

# Redis health (Docker)
docker compose exec redis redis-cli ping
```

### Logs

```bash
# All services
docker compose logs -f

# Specific service
docker compose logs -f backend
docker compose logs -f frontend
```

## Backup & Restore

### Database Backup

```bash
docker compose exec postgres pg_dump -U offensec > backup_$(date +%Y%m%d).sql
```

### Database Restore

```bash
docker compose exec -T postgres psql -U offensec < backup_20260730.sql
```

## Security Checklist

- [ ] `JWT_SECRET` set to secure random value
- [ ] `DATABASE_URL` uses strong password
- [ ] `CORS_ORIGINS` set to specific domains
- [ ] Docker containers not running as root
- [ ] Reverse proxy configured with TLS
- [ ] Database backup schedule configured
- [ ] Monitoring and alerting set up
