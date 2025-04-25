# Base stage for building dependencies
FROM python:3.12-bookworm as base

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONFAULTHANDLER=1 \
    PIP_NO_CACHE_DIR=true \
    PIP_DEFAULT_TIMEOUT=100 \
    PIP_DISABLE_PIP_VERSION_CHECK=on

WORKDIR /myapp

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        gcc \
        libpq-dev && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Create and activate virtual environment
RUN python -m venv /.venv
ENV PATH="/.venv/bin:$PATH"

# Install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Final lightweight stage
FROM python:3.12-slim-bookworm as final

# Install runtime dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        libpq5 && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Copy virtual environment from base stage
COPY --from=base /.venv /.venv
ENV PATH="/.venv/bin:$PATH"

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONFAULTHANDLER=1

WORKDIR /myapp

# Create and switch to non-root user
RUN useradd -m myuser
USER myuser

# Copy application code
COPY --chown=myuser:myuser . .

# Expose port
EXPOSE 8000

# Entrypoint
ENTRYPOINT ["uvicorn", "app.main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]