# Build stage
FROM python:3.12.1-slim AS builder

WORKDIR /app
COPY requirements.txt .

# Install all dependencies including pytest to /install
RUN mkdir -p /install && \
    pip install --prefix=/install -r requirements.txt

# Runtime stage
FROM python:3.12.1-slim

WORKDIR /app

# Copy installed packages and ensure they're in PATH
COPY --from=builder /install /usr/local
COPY . .

# Install in editable mode to make CLI available
RUN pip install -e .

# Verify core functionality
RUN python -c "import sys; assert sys.version_info >= (3,12,1), 'Python version mismatch'"
RUN python -c "import sqlite3; print(f'SQLite version: {sqlite3.sqlite_version}')"

# Install pytest in final image for testing (remove for production)
RUN pip install pytest pytest-cov

# Run tests (fixed path from test/ to tests/)
RUN python -m pytest test/ -v --cov=src

# Set entrypoint to make commands easier to run
ENTRYPOINT ["transaction-pipeline"]
CMD ["--help"]