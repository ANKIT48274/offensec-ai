FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    curl \
    && rm -rf /var/lib/apt/lists/*

RUN adduser --system --no-create-home offensec

COPY pyproject.toml .
RUN pip install --no-cache-dir .

COPY . .

USER offensec

EXPOSE 8002

HEALTHCHECK --interval=30s --timeout=10s --retries=3 \
    CMD curl -sf http://localhost:8002/health || exit 1

CMD ["uvicorn", "offensec.plugins.sandbox.server:app", "--host", "0.0.0.0", "--port", "8002"]
