# Multi-stage Dockerfile for pyWATS
# Supports: API library, headless client, MCP server

# ============================================================================
# Stage 1: Base image with common dependencies
# ============================================================================
FROM python:3.11-slim AS base

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy package files
COPY pyproject.toml README.md LICENSE MANIFEST.in ./
COPY src/ ./src/
COPY converters/ ./converters/

# ============================================================================
# Stage 2: API library only (minimal)
# ============================================================================
FROM base AS api

# Install only the core API
RUN pip install --no-cache-dir -e .

# Create non-root user
RUN useradd -m -u 1000 pywats && chown -R pywats:pywats /app
USER pywats

# Health check (test import)
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s \
  CMD python -c "import pywats; print('pyWATS API OK')" || exit 1

CMD ["python"]

# ============================================================================
# Stage 3: Headless client (for servers, Raspberry Pi, etc.)
# ============================================================================
FROM base AS client-headless

# Install headless client dependencies
RUN pip install --no-cache-dir -e .[client-headless]

# Create directories for client data
RUN mkdir -p /app/data /app/logs /app/config && \
    useradd -m -u 1000 pywats && \
    chown -R pywats:pywats /app

USER pywats

# Environment variables for headless mode
ENV PYWATS_HEADLESS=1 \
    PYWATS_CONFIG_DIR=/app/config \
    PYWATS_DATA_DIR=/app/data \
    PYWATS_LOG_DIR=/app/logs

# Mount points for configuration and data
VOLUME ["/app/config", "/app/data", "/app/logs"]

# Health check
HEALTHCHECK --interval=60s --timeout=10s --start-period=30s \
  CMD python -c "from pywats_client.core import ServiceManager; print('Client OK')" || exit 1

# Run headless client
CMD ["python", "-m", "pywats_client", "--headless"]

# ============================================================================
# Stage 4: Development image (all dependencies)
# ============================================================================
FROM base AS dev

# Install all dependencies (api + client-headless + dev + docs)
RUN pip install --no-cache-dir -e .[client-headless,dev,docs]

# Create non-root user
RUN useradd -m -u 1000 pywats && chown -R pywats:pywats /app
USER pywats

CMD ["bash"]

# ============================================================================
# Default stage is headless client
# ============================================================================
FROM client-headless
