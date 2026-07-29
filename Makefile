.PHONY: help build test lint dev clean db init db-migrate db-reset format security-check

.DEFAULT_GOAL := help

SHELL := /bin/bash

# ──────────────────────────────────────────────
# Help
# ──────────────────────────────────────────────

help: ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-25s\033[0m %s\n", $$1, $$2}'

# ──────────────────────────────────────────────
# Build
# ──────────────────────────────────────────────

build: ## Build all containers
	docker compose build --no-cache

# ──────────────────────────────────────────────
# Development
# ──────────────────────────────────────────────

dev: ## Start development environment
	docker compose -f docker-compose.dev.yml up --build

# ──────────────────────────────────────────────
# Testing
# ──────────────────────────────────────────────

test: ## Run all test suites
	python -m pytest tests/ -v --tb=short --strict-markers
	cd frontend && npm run test

test-unit: ## Run unit tests only
	python -m pytest tests/unit/ -v --tb=short

test-integration: ## Run integration tests only
	python -m pytest tests/integration/ -v --tb=short

test-e2e: ## Run end-to-end tests only
	python -m pytest tests/e2e/ -v --tb=short

test-security: ## Run security-focused test suite
	python -m pytest tests/security/ -v --tb=short

# ──────────────────────────────────────────────
# Code Quality
# ──────────────────────────────────────────────

lint: ## Run linters on Python and TypeScript
	cd backend && ruff check . && ruff format --check . && mypy .
	cd frontend && npx eslint . && npx prettier --check .

format: ## Auto-format Python and TypeScript code
	cd backend && ruff format .
	cd frontend && npx prettier --write . && npx eslint --fix .

# ──────────────────────────────────────────────
# Database
# ──────────────────────────────────────────────

db: ## Connect to PostgreSQL database
	docker compose exec postgres psql -U ${POSTGRES_USER:-offensec} -d offensec

init: ## Run database initialisation scripts
	docker compose exec postgres psql -U ${POSTGRES_USER:-offensec} -d offensec -f /docker-entrypoint-initdb.d/01_init.sql

migrate: ## Apply pending database migrations
	python -m alembic -c backend/alembic.ini upgrade head

migrate-down: ## Rollback last migration
	python -m alembic -c backend/alembic.ini downgrade -1

migrate-history: ## Show migration history
	python -m alembic -c backend/alembic.ini history

# ──────────────────────────────────────────────
# Infrastructure
# ──────────────────────────────────────────────

down: ## Stop all services
	docker compose down

down-volumes: ## Stop services and remove volumes
	docker compose down -v

restart: ## Restart all services
	docker compose restart

logs: ## Tail container logs
	docker compose logs -f --tail=100

# ──────────────────────────────────────────────
# Security
# ──────────────────────────────────────────────

security-check: ## Run dependency vulnerability scans
	cd backend && pip-audit
	cd frontend && npm audit --audit-level=high

# ──────────────────────────────────────────────
# Cleanup
# ──────────────────────────────────────────────

clean: ## Remove build artifacts, caches, and temporary files
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	find . -type d -name .pytest_cache -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name .mypy_cache -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name .ruff_cache -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name .next -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name dist -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name node_modules -exec rm -rf {} + 2>/dev/null || true
