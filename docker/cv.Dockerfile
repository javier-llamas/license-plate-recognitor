FROM python:3.13-slim

WORKDIR /app

# Install system dependencies for picamera2, OpenCV, and fast_alpr
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    g++ \
    libcamera-dev \
    libopencv-dev \
    libcap-dev \
    python3-opencv \
    git \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Install uv for faster dependency installation
RUN pip install uv

# Copy dependency files
COPY pyproject.toml uv.lock* ./

# Install core dependencies + cv group using uv sync
# --no-dev excludes dev dependencies, --group cv includes the cv dependency group
# picamera2 will be installed automatically on Linux via platform marker
# RUN uv sync --no-dev --group cv
COPY README.md .
RUN uv sync --all-groups

# Copy application code
COPY . .

# Create media directories
RUN mkdir -p /app/media/test_shots /app/media/detections /app/media/training

# Set Python path to include the project root
ENV PYTHONPATH=/app:$PYTHONPATH

# No exposed port - DBOS worker communicates via database, not HTTP
CMD ["python", "cv_worker/main.py"]
