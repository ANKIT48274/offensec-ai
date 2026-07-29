# Troubleshooting Guide

## Backend

### Backend fails to start: "JWT_SECRET is not set"
**Cause:** The `JWT_SECRET` environment variable is required for security reasons.

**Fix:**
```bash
export JWT_SECRET=$(python3 -c 'import secrets; print(secrets.token_hex(32))')
```

### Backend fails to start: "Could not parse SQLAlchemy URL"
**Cause:** `DATABASE_URL` not set or invalid format.

**Fix:** Ensure PostgreSQL is running and set `DATABASE_URL`:
```bash
export DATABASE_URL="postgresql+asyncpg://user:password@localhost:5432/offensec"
```

### "Permission denied" when running Nmap/HTTPX/Nuclei
**Cause:** Security tools not installed or not in PATH.

**Fix:**
```bash
# Debian/Ubuntu/Kali
sudo apt install nmap

# macOS
brew install nmap

# Nuclei
go install github.com/projectdiscovery/nuclei/v3/cmd/nuclei@latest

# HTTPX
go install github.com/projectdiscovery/httpx/cmd/httpx@latest
```

## Frontend

### "Network error" when making API calls
**Cause:** Frontend cannot reach the backend API.

**Fix:**
1. Ensure backend is running: `curl http://localhost:8000/health`
2. Check Next.js API proxy in `frontend/next.config.js` — the `rewrites` section should point to the backend URL
3. If using a custom backend port, update the rewrite destination

### White screen or blank page
**Cause:** JavaScript error during rendering.

**Fix:**
1. Open browser developer console (F12) for error details
2. Ensure `npm run build` completed without errors
3. Clear browser cache and reload

## Database

### Migration fails: "relation already exists"
**Cause:** Migrations partially applied or database already has tables.

**Fix:**
```bash
# Force stamp the current migration
alembic stamp head
```

### "Could not connect to PostgreSQL server"
**Cause:** PostgreSQL not running or connection string incorrect.

**Fix:**
```bash
# Check PostgreSQL status
sudo systemctl status postgresql

# Verify connection
psql -U offensec -d offensec -c "SELECT 1"
```

## Docker

### Port already in use
**Cause:** Another service is using port 8000, 3000, 5432, or 6379.

**Fix:**
```bash
# Find and stop the conflicting process
lsof -ti:8000 | xargs kill

# Or use a different port
BACKEND_HOST_PORT=8001 docker compose up -d
```

### Container exits immediately
**Cause:** Missing environment variables or configuration.

**Fix:** Check container logs:
```bash
docker compose logs backend
docker compose logs frontend
```

## Scans

### Nmap scan returns no results
**Cause:** Target unreachable, blocked by firewall, or host is down.

**Fix:**
1. Verify target is reachable: `ping <target>`
2. Check if Nmap flags are appropriate for the target
3. Check Nmap is installed: `nmap --version`

### Nuclei returns no findings
**Cause:** Nuclei templates not installed or target has no known vulnerabilities.

**Fix:**
```bash
# Update Nuclei templates
nuclei -update-templates

# Verify templates are installed
ls ~/.nuclei-templates/
```

### Pipeline job stuck in "running" state
**Cause:** Subprocess timed out or crashed without proper cleanup.

**Fix:** The pipeline timeout will eventually trigger. Check job database for stuck entries:
```bash
docker compose exec postgres psql -U offensec -d offensec -c "UPDATE scan_jobs SET status='failed' WHERE status='running' AND created_at < NOW() - INTERVAL '1 hour';"
```
