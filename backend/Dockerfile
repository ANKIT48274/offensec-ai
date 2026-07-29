FROM python:3.12-slim

WORKDIR /app/backend

COPY backend/pyproject.toml backend/
RUN pip install --no-cache-dir backend/

COPY backend/ backend/

WORKDIR /app

ENV PYTHONPATH=/app

RUN addgroup --system --gid 1001 offensec && \
    adduser --system --uid 1001 --no-create-home offensec && \
    mkdir -p /var/log/offensec && \
    chown -R offensec:offensec /app /var/log/offensec

USER offensec

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=10s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')" || exit 1

CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4", "--timeout-keep-alive", "65"]
