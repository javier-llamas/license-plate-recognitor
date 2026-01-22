FROM python:3.13-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libpq-dev \
    postgresql-client \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Install uv for faster dependency installation
RUN pip install uv

# Copy dependency files
COPY pyproject.toml uv.lock* ./

# Install core dependencies + web group using uv sync
# --no-dev excludes dev dependencies, --group web includes the web dependency group
COPY README.md .
RUN uv sync --no-dev --group web

# Copy application code
COPY . .

# Make scripts executable
RUN chmod +x /app/scripts/init-databases.sh

# Create media directories
RUN mkdir -p /app/media/test_shots /app/media/detections /app/media/training

# Collect static files
RUN python manage.py collectstatic --noinput || true

EXPOSE 8000

CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "2"]
