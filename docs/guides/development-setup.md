# Development Setup

## Prerequisites

- Python 3.12+
- Node.js 22+
- Docker Engine 24+ with Compose V2
- PostgreSQL 16+
- Redis 7+

## Local Setup

### 1. Clone the Repository

```bash
git clone <repository-url> offensec-ai
cd offensec-ai
```

### 2. Backend Setup

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

### 3. Frontend Setup

```bash
cd frontend
npm install
```

### 4. Environment Variables

```bash
cp .env.example .env
# Edit .env with your configuration
```

### 5. Database Setup

```bash
# Start dependencies
docker compose up -d postgres redis

# Run migrations
alembic -c backend/alembic.ini upgrade head
```

### 6. Start Development Servers

```bash
# Terminal 1: Backend
cd backend && uvicorn offensec.main:app --reload --port 8000

# Terminal 2: Frontend
cd frontend && npm run dev
```

### 7. Verify Setup

```bash
curl http://localhost:8000/health
```

## Docker Development

```bash
docker compose -f docker-compose.dev.yml up --build
```

## Running Tests

```bash
# All tests
make test

# Specific suites
make test-unit
make test-integration
make test-e2e
```

## Code Quality

```bash
# Format code
make format

# Run linters
make lint
```
