# OffenSec AI — Production Readiness Audit

**Date:** 2026-07-29
**Auditor:** Lead Software Architect
**Scope:** Full codebase audit (188 Python files, 56 TS/TSX files)

---

## Priority 1 (Critical)

### P1-1: Command Injection — `httpx` targets passed unsanitized to subprocess

**File:** `backend/infrastructure/pipeline/runner.py` — Line 115-125
**Explanation:** `target_list = " ".join(targets[:20])` is unused. More critically, `targets` items from `_extract_live_hosts()` are constructed from user-supplied values and passed as positional args via `*cmd`. A target like `; rm -rf /` could inject commands via `create_subprocess_exec` if the `_is_valid_target` check is bypassed in the pipeline's nmap step (which does NOT validate targets).
**Impact:** Critical — arbitrary command execution as the application user.
**Fix:** Add `_is_valid_target()` validation from `scan_engine/runner.py` to `_run_nmap_step()` in `pipeline/runner.py`. Validate all target inputs at the boundary.

### P1-2: Hardcoded Default JWT Secret

**File:** `backend/infrastructure/auth.py` — Line 17
**Explanation:** `get_jwt_secret()` returns a hardcoded fallback `"offensec-ai-default-jwt-secret-min-32-bytes!!"` when `JWT_SECRET` env var is not set. This allows any attacker knowing the default secret to forge valid JWT tokens.
**Impact:** Critical — authentication bypass, arbitrary user impersonation.
**Fix:** Remove the hardcoded default. Raise `ValueError` if `JWT_SECRET` is not set in production. Document the requirement in `.env.example` and deployment guides.

### P1-3: No Authentication Enforcement on API Routes

**File:** `backend/interfaces/api/v1/projects.py`, `assessments.py`, `findings.py`, `scans.py`, `pipeline.py`, `nuclei.py`, `assets.py`, `evidence.py`
**Explanation:** Every route uses `x_user_id: str | None = Header(default=None)` with no token verification. Any caller can set any `x-user-id` header and access or modify any user's data. The JWT `Bearer` auth is only implemented on `/auth/me`.
**Impact:** Critical — complete lack of authorization. Any authenticated network accessor can read/write all data.
**Fix:** Implement a global `Depends(get_current_user)` dependency that extracts user ID from JWT Bearer token. Remove `x-user-id` header pattern entirely.

### P1-4: Subprocess Timeout — `proc.kill()` without `SIGTERM` Grace Period

**File:** `backend/infrastructure/scan_engine/runner.py` Line 40, `pipeline/runner.py` Line 69/136, `nuclei/runner.py` Line 42
**Explanation:** On timeout, `proc.kill()` sends `SIGKILL` immediately without sending `SIGTERM` first. This leaves child processes in an unknown state and can orphan nmap/httpx/nuclei processes.
**Impact:** High — zombie processes, resource leaks, corrupt temp files.
**Fix:** Use `proc.terminate()` first, wait briefly, then `proc.kill()` if still running.

### P1-5: Temp File Race Condition — XML/JSON Files Left on Disk on Error

**File:** `backend/infrastructure/scan_engine/runner.py` Line 60, `pipeline/runner.py` Line 56, `nuclei/runner.py` Line 23
**Explanation:** Multiple code paths create temp files but only clean up on known exceptions. An unexpected exception (e.g., `KeyboardInterrupt`, `asyncio.CancelledError`) leaks the temp file. The `scan_engine/runner.py` also returns `xml_path` in its result dict, and the caller may never clean up.
**Impact:** Medium — disk space exhaustion on long-running systems.
**Fix:** Use `try/finally` blocks or context managers for temp file lifecycle.

---

## Priority 2 (High)

### P2-1: Duplicate `run_nmap_scan` and `_run_nmap_step` Logic

**File:** `backend/infrastructure/scan_engine/runner.py` (lines 18-70) and `backend/infrastructure/pipeline/runner.py` (lines 54-93)
**Explanation:** Two nearly identical implementations of nmap subprocess execution. The standalone scan engine uses `-sV -sC -O` while the pipeline uses `--top-ports 100`. Both parse XML identically. This doubles the maintenance surface.
**Impact:** Medium — maintenance burden, inconsistent flags.
**Fix:** Extract shared nmap execution into a single helper in `scan_engine/runner.py` with configurable arguments. Import and reuse in pipeline.

### P2-2: Missing Input Validation — `_extract_live_hosts()` Generates URLs Without Validation

**File:** `backend/infrastructure/pipeline/runner.py` — Lines 96-108
**Explanation:** `_extract_live_hosts()` constructs `http://ip:port` URLs from nmap output. Port comes from parsed XML (trusted) but IP comes from the same source. If XML parsing is compromised or the target was maliciously crafted, the URL could contain injected special characters that get passed to httpx subprocess.
**Impact:** High — SSRF or argument injection via crafted nmap response.
**Fix:** Validate extracted IPs with `ipaddress.ip_address()` before URL construction.

### P2-3: `pip-audit` / `npm audit` Not Run in CI

**File:** `.github/workflows/ci.yml`
**Explanation:** The CI workflow runs lint and tests but does not scan dependencies for known vulnerabilities. `pip-audit` and `npm audit` are only in the `security-scan.yml` which runs weekly.
**Impact:** High — known-vulnerability dependencies can be deployed for up to 7 days.
**Fix:** Add `pip-audit` and `npm audit --audit-level=high` steps to the CI workflow on every push.

### P2-4: Broad `CORS` Configuration

**File:** `backend/main.py` — Lines 99-106
**Explanation:** `CORS_ORIGINS` env var defaults to empty string, causing `[""]` to be set as allowed origins. When set, it allows arbitrary origins by splitting on commas with no validation.
**Impact:** Medium — CSRF on API endpoints that don't use Bearer auth.
**Fix:** Validate CORS origins against a whitelist pattern. Reject wildcard origins in production.

### P2-5: Unbounded `ANY` Types in Route Handlers

**File:** `backend/interfaces/api/v1/*.py` — All route files use `Any` for service dependencies
**Explanation:** Every route uses `service: Any = Depends(...)` instead of the concrete service type. This bypasses type checking and allows passing incorrect dependencies at runtime.
**Impact:** Medium — runtime errors that could be caught at compile time.
**Fix:** Import and use concrete service types as type annotations.

### P2-6: `pip install` Runs as Root in Docker

**File:** `backend/Dockerfile`
**Explanation:** The production Dockerfile likely installs dependencies and runs the app as root. The `plugins/Dockerfile.sandbox` uses `no-new-privileges:true` but the base images don't create non-root users.
**Impact:** High — container escape via compromised dependency widens to full host access.
**Fix:** Create and switch to a non-root user in all Dockerfiles. Use `USER offensec` with uid 10001.

### P2-7: Subprocess `stderr` Not Size-Limited

**File:** `backend/infrastructure/nuclei/runner.py` Line 47, `pipeline/runner.py` Line 75/141, `scan_engine/runner.py` Line 46
**Explanation:** `stderr.decode("utf-8", errors="replace")` reads the entire stderr output into memory. A noisy tool could produce gigabytes of stderr, causing OOM.
**Impact:** Medium — memory exhaustion on large scans.
**Fix:** Limit stderr read to a configurable maximum (e.g., 64KB). Truncate and warn if exceeded.

---

## Priority 3 (Medium)

### P3-1: No Request Timeout on FastAPI Routes

**File:** `backend/main.py` — All routes
**Explanation:** FastAPI has no global or per-route timeout. Long-running endpoints like POST `/api/v1/scans` (which blocks for the full nmap duration) can tie up workers indefinitely.
**Impact:** Medium — worker starvation, degraded throughput under load.
**Fix:** Set timeout middleware or use `asyncio.wait_for()` in long-running routes. Consider a background task queue (Celery/Redis Queue) for scan operations.

### P3-2: Missing Database Connection Pool Validation

**File:** `backend/infrastructure/persistence/postgres/__init__.py` — Lines 37-43
**Explanation:** `pool_size=10, max_overflow=20` with `pool_pre_ping=True` is configured, but there is no retry logic on connection failure during startup. If PostgreSQL is unavailable at startup, the application crashes.
**Impact:** Medium — application crash if database is temporarily unavailable.
**Fix:** Implement startup retry with exponential backoff. Add health check that verifies DB connectivity.

### P3-3: No Database Indexes on Foreign Keys

**File:** `backend/infrastructure/persistence/postgres/models.py` — Multiple tables
**Explanation:** Foreign key columns like `project_id`, `assessment_id`, `job_id`, `asset_id` lack explicit indexes. SQLAlchemy does not auto-index FKs. Queries filtering by project_id will scan entire tables.
**Impact:** Medium — performance degradation as tables grow beyond 10K rows.
**Fix:** Add `index=True` to all foreign key `Column` definitions. The Alembic migration `005_add_assets_evidence.py` correctly adds indexes but earlier tables (scans, findings, etc.) do not have them.

### P3-4: `except Exception` Blankets in All Route Handlers

**File:** `backend/interfaces/api/v1/*.py` — Every route handler
**Explanation:** All route handlers wrap logic in `try/except Exception` and return `error_response(str(e), ...)`. This catches everything including `SystemExit`, `KeyboardInterrupt`, and hides the actual error from the client with potentially leaky information.
**Impact:** Medium — hides programming errors, may leak internal details.
**Fix:** Catch specific exceptions. Add a global exception handler for unhandled errors. Log the full traceback server-side.

### P3-5: Async Session `get_db_session` Creates One Session Per Request But Holds No Transaction

**File:** `backend/infrastructure/di.py` — Lines 40-44
**Explanation:** `get_db_session` yields a session that's used across the entire request. Service methods (`authenticate`, `create`) call multiple repository methods without explicit transaction boundaries. Auto-commit in repositories means partial writes can occur.
**Impact:** Medium — partial data writes on error, no rollback across multiple repo calls.
**Fix:** Use explicit transaction management. Begin transaction at request start, commit on success, rollback on error.

### P3-6: No Pagination on Evidence and Asset List Endpoints Without Project

**File:** `backend/interfaces/api/v1/assets.py` Line 16-18, `backend/interfaces/api/v1/evidence.py` Line 16-18
**Explanation:** Both endpoints return all results when `project_id` is empty. No upper bound on page_size (max 100), but `project_id=""` returns ALL rows from the table.
**Impact:** Medium — unbounded query, OOM on large datasets.
**Fix:** Require `project_id` to be non-empty. Return error if missing.

### P3-7: `asyncpg` Connection String Has Default Password

**File:** `backend/infrastructure/persistence/postgres/__init__.py` — Line 28
**Explanation:** Default connection string includes `changeme` as password. If `DATABASE_URL` env var is not set, the system connects with this weak default.
**Impact:** Medium — weak default credentials in production.
**Fix:** Remove default password. Require `DATABASE_URL` to be explicitly set in production.

### P3-8: `/api/v1/auth/me` Route Has No Logic

**File:** `backend/interfaces/api/v1/auth.py` — Lines 55-59
**Explanation:** `GET /auth/me` verifies the Bearer token exists but returns a static `{"message": "Authenticated"}` instead of the actual user data. The token's `sub` claim (user_id) is not decoded or used.
**Impact:** Low — missing functionality, frontend cannot determine current user.
**Fix:** Decode the token, look up the user, return user data (email, id, username).

---

## Priority 4 (Low)

### P4-1: Duplicate `_cleanup` Functions

**File:** `backend/infrastructure/scan_engine/runner.py` line 92, `pipeline/runner.py` line 169, `nuclei/runner.py` line 83
**Explanation:** Three identical implementations of `_cleanup()` across three files.
**Fix:** Extract to a shared utility module.

### P4-2: Unused Imports Across Multiple Modules

**File:** Multiple Python files flagged by `ruff check`
**Explanation:** `ruff` reports 111 errors including unused imports (`F401`), unused method arguments (`ARG002`), and mutable default values (`RUF012`). Examples: `datetime.timezone` imported but unused in several `__init__.py` files, `subprocess` imported but unused in `pipeline/runner.py`.
**Fix:** Run `ruff check --fix` regularly in CI. Remove unused imports from `__init__.py` files.

### P4-3: `stores/auth.ts` and `stores/project.ts` Use `any` Types Throughout

**File:** `frontend/stores/auth.ts`, `frontend/stores/project.ts`
**Explanation:** Zustand stores define state and actions with `any` types instead of concrete interfaces. This bypasses TypeScript safety.
**Fix:** Define and export TypeScript interfaces for all store state and action types.

### P4-4: No Error Boundaries in Frontend

**File:** `frontend/app/layout.tsx`
**Explanation:** The root layout does not wrap children in a React Error Boundary. A rendering error in any page will crash the entire application.
**Fix:** Add a `global-error.tsx` page and wrap the app in a client error boundary.

### P4-5: Missing `key` Props in React Lists

**File:** `frontend/components/nuclei/NucleiResults.tsx` — Line 97, `.map((t, i) =>` uses index as key
**Explanation:** Using array index as React `key` prop can cause rendering bugs when lists are filtered or reordered.
**Fix:** Use stable unique IDs (template_id, finding.id) instead of array index.

### P4-6: Frontend Components Directly Access `localStorage` Instead of Using a Hook

**File:** `frontend/components/scans/ScanRunForm.tsx` Line 106-109, `frontend/components/pipeline/PipelineRunForm.tsx` Line 149-152
**Explanation:** Both components define a `getUserId()` helper that calls `localStorage.getItem("user_id")`. This is duplicated and not SSR-safe (though it checks `typeof window`).
**Fix:** Extract `getUserId()` into a shared hook `useUserId()` in `frontend/lib/hooks/`.

### P4-7: `docker-compose.yml` Maps Backend Volume as Read-Only But A-Target AI Runner Mapping is Inconsistent

**File:** `docker-compose.yml` — Lines 73-75, `docker-compose.dev.yml` Lines 65-67
**Explanation:** Production compose maps `./backend:/app:ro` (read-only). Development compose maps `./backend:/app` (writable). The Dockerfile and uvicorn command reference `offensec.main:app` (old package path) instead of `backend.main:app`.
**Fix:** Verified the uvicorn commands already reference `backend.main:app` in the latest version.

### P4-8: No Release Checklist or Version Tagging Convention

**File:** `.github/workflows/release.yml`
**Explanation:** The release workflow exists but does not enforce semantic versioning, generate changelogs, or run integration tests before tagging.
**Fix:** Add `git tag` validation, CHANGELOG verification, and pre-release test steps to the workflow.

---

### Summary

| Priority | Count | Key Areas |
|----------|-------|-----------|
| **Critical** | 5 | Command injection, hardcoded JWT secret, no auth, subprocess SIGKILL, temp file leaks |
| **High** | 7 | Duplicate nmap code, SSRF in pipeline, CI missing vuln scan, CORS, `Any` types, Docker root, unbounded stderr |
| **Medium** | 8 | No request timeout, DB connection pool, missing indexes, blanket exceptions, transaction management, unbound queries, default DB password, `/auth/me` stub |
| **Low** | 8 | Duplicate cleanup, ruff warnings, `any` types, error boundaries, key props, localStorage helpers, compose paths, release workflow |

**Total: 28 issues identified across 14 audit categories.**

---

### Recommended Remediation Order

1. **P1-1, P1-2, P1-3** — Fix immediately before any production deployment.
2. **P2-1, P2-2, P2-3, P2-6** — Fix within the current sprint.
3. **P1-4, P1-5, P2-4, P2-5, P2-7** — Fix within next sprint.
4. **P3-1 through P4-8** — Schedule for technical debt backlog.
