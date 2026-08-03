FROM python:3.12-slim

WORKDIR /app

# Install build deps + security scan tools
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    nmap \
    whois \
    dnsutils \
    curl \
    unzip \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Install ProjectDiscovery tools (httpx, nuclei, katana) from prebuilt binaries
# Pinned versions for deterministic builds. Asset format: <name>_<ver>_<os>_<arch>.zip
ARG TARGETARCH=amd64
RUN set -eux; \
    if [ "$TARGETARCH" = "arm64" ]; then pd_arch=arm64; else pd_arch=amd64; fi; \
    \
    curl -fL --retry 5 --retry-delay 3 --retry-all-errors -o /tmp/httpx.zip "https://github.com/projectdiscovery/httpx/releases/download/v1.10.0/httpx_1.10.0_linux_${pd_arch}.zip"; \
    curl -fL --retry 5 --retry-delay 3 --retry-all-errors -o /tmp/nuclei.zip "https://github.com/projectdiscovery/nuclei/releases/download/v3.11.0/nuclei_3.11.0_linux_${pd_arch}.zip"; \
    curl -fL --retry 5 --retry-delay 3 --retry-all-errors -o /tmp/katana.zip "https://github.com/projectdiscovery/katana/releases/download/v1.6.1/katana_1.6.1_linux_${pd_arch}.zip"; \
    \
    mkdir -p /tmp/pd && unzip -o /tmp/httpx.zip -d /tmp/pd/httpx && cp /tmp/pd/httpx/httpx /tmp/pd/httpx.bin; \
    unzip -o /tmp/nuclei.zip -d /tmp/nuclei && cp /tmp/nuclei/nuclei /usr/local/bin/nuclei; \
    unzip -o /tmp/katana.zip -d /tmp/katana && cp /tmp/katana/katana /usr/local/bin/katana; \
    \
    chmod +x /tmp/pd/httpx.bin /usr/local/bin/nuclei /usr/local/bin/katana; \
    rm -rf /tmp/httpx* /tmp/nuclei* /tmp/katana*

# Install ffuf from tar.gz (ffuf ships tarballs for linux, not zips)
RUN set -eux; \
    if [ "$TARGETARCH" = "arm64" ]; then ffuf_arch=arm64; else ffuf_arch=amd64; fi; \
    curl -fL --retry 5 --retry-delay 3 --retry-all-errors -o /tmp/ffuf.tar.gz "https://github.com/ffuf/ffuf/releases/download/v2.2.1/ffuf_2.2.1_linux_${ffuf_arch}.tar.gz"; \
    mkdir -p /tmp/ffuf && tar -xzf /tmp/ffuf.tar.gz -C /tmp/ffuf; \
    cp /tmp/ffuf/ffuf /usr/local/bin/ffuf; \
    chmod +x /usr/local/bin/ffuf; \
    rm -rf /tmp/ffuf*

COPY backend /app/backend/

# Install Python deps FIRST, then re-install the ProjectDiscovery httpx binary.
# `pip install httpx` (the Python HTTP client) installs a CLI entrypoint at
# /usr/local/bin/httpx that would shadow the ProjectDiscovery scanner — so we
# re-copy the scanner binary after pip to guarantee it wins on PATH.
RUN pip install --no-cache-dir fastapi uvicorn[standard] sqlalchemy[asyncio] asyncpg alembic redis[hiredis] httpx python-multipart websockets cryptography orjson structlog tenacity pyjwt bcrypt \
    && cp /tmp/pd/httpx.bin /usr/local/bin/httpx \
    && chmod +x /usr/local/bin/httpx \
    && rm -rf /tmp/pd

ENV PYTHONPATH=/app \
    HOME=/home/offensec \
    NUCLEI_CONFIG_DIR=/home/offensec/.config/nuclei

RUN addgroup --system --gid 1001 offensec && \
    adduser --system --uid 1001 --no-create-home offensec && \
    mkdir -p /var/log/offensec /home/offensec/.config /home/offensec/.cache && \
    chown -R offensec:offensec /app /var/log/offensec /home/offensec

USER offensec

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=10s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')" || exit 1

CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4", "--timeout-keep-alive", "65"]
