# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

A license plate recognition system for Raspberry Pi 5 with Django web interface, HTMX frontend, and DBOS-based computer vision worker. The system runs in a containerized environment with three main services: web (Django), cv (computer vision worker), and db (PostgreSQL).

## Development Commands

### Local Development Setup

```bash
# Install dependencies using uv
pip install uv

# Install all dependencies for full local development (core + web + cv + dev)
# picamera2 is automatically skipped on macOS/Windows via platform marker
uv sync --all-groups

# Or for specific groups only
uv sync --group web --group dev  # Web development
uv sync --group cv --group dev   # CV development

# Start PostgreSQL in Docker
docker-compose up db -d

# Run migrations
python manage.py migrate

# Create superuser (optional)
python manage.py createsuperuser

# Run Django development server (uses local settings by default)
python manage.py runserver
```

### Docker Development

```bash
# Start all services
docker-compose up --build

# Start specific services
docker-compose up web db

# View logs
docker-compose logs -f cv
docker-compose logs -f web

# Stop all services
docker-compose down
```

### Database Operations

```bash
# Create new migration after model changes
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Access Django shell
python manage.py shell

# Access PostgreSQL directly
docker-compose exec db psql -U lpr_user -d license_plate_db
```

## Architecture

### Three-Service Architecture

1. **web**: Django 5.0 application
   - Django Ninja REST API (`/api/`)
   - HTMX-powered frontend
   - Serves static files and media
   - Uses DBOS client to start/cancel workflows

2. **cv**: Computer vision worker (Pure DBOS Python application)
   - No HTTP server - pure DBOS workflow executor
   - Manages camera and detector instances
   - Executes DBOS workflows for reliable async processing
   - Requires Django for ORM access (imports Django models)

3. **db**: PostgreSQL 15
   - Two databases:
     - `license_plate_db`: Django app data (DetectionResult, TestShot, TrainingShot)
     - `dbos_system`: DBOS workflow state (managed by DBOS)
   - Shared by both web and cv containers

### Code Organization

```
apps/
├── core/          # Database models (shared by web and cv)
├── api/           # Django Ninja API endpoints
└── web/           # HTMX views and templates

cv_worker/         # Computer vision worker
├── main.py        # Pure DBOS app entry point (no HTTP server)
├── camera.py      # Camera abstraction (picamera2 + mock)
├── detector.py    # License plate detector (fast_alpr + mock)
└── workflows/     # DBOS workflow definitions

config/
└── settings/      # Django settings (base, local, production)
```

### Key Architectural Patterns

**DBOS Workflows**: The cv worker uses DBOS workflows for reliable async processing. Workflows are durable and can be cancelled by workflow_id. See `cv_worker/workflows/detection_job.py` for the continuous detection loop pattern.

**Mock Mode**: Both camera and detector automatically fall back to mock implementations when hardware is unavailable (development on non-Raspberry Pi systems). This allows full-stack development without physical hardware.

**Django-DBOS Integration**: The cv worker imports Django (`django.setup()`) to access ORM models. It uses the production settings module. Both containers share two PostgreSQL databases: the Django app database and the DBOS system database.

**Shared Media Volume**: Images captured by the cv worker are saved to `/app/media` which is shared between cv and web containers via Docker volume.

## Django Settings

The project uses a split settings pattern:

- `config.settings.base`: Shared settings
- `config.settings.local`: Development (default for `manage.py`)
- `config.settings.production`: Production (used in Docker containers)

Override with: `DJANGO_SETTINGS_MODULE=config.settings.production`

## API Structure

Django Ninja API is mounted at `/api/` with automatic OpenAPI docs at `/api/docs`.

Three main endpoint groups:
- `/api/test-shots/`: Manual test image capture
- `/api/detection/`: Start/stop continuous detection jobs
- `/api/training-shots/`: Evaluate and correct detection results

API endpoints use DBOS client to start/cancel workflows directly (no HTTP calls to cv worker)

## Database Models

All models are in `apps/core/models.py`:

- **TestShot**: Manual test captures
- **DetectionResult**: Individual detections (indexed by workflow_id)
- **TrainingShot**: Images for evaluation with user corrections

Note: DBOS manages workflow state in its own system tables (`dbos_system` database)

## Computer Vision Components

**Camera** (`cv_worker/camera.py`):
- Singleton pattern via `get_camera()`
- Captures images as numpy arrays
- Saves to media directory with timestamps
- Auto-detects picamera2 availability

**Detector** (`cv_worker/detector.py`):
- Singleton pattern via `get_detector()`
- Uses fast_alpr with yolo-v9-s detector and cct-xs OCR model
- Returns (plate_text, confidence) tuples
- Mock mode generates random plates for testing

## DBOS Workflows

Workflows are defined in `cv_worker/workflows/`:

- **test_shot**: Single image capture workflow
- **detection_job**: Continuous detection with 2-second intervals

Workflows use `@DBOS.workflow()` and `@DBOS.step()` decorators. Steps are transactional and workflows are durable. The detection loop checks job status on each iteration to support graceful cancellation.

## Environment Variables

Required for both web and cv containers:

- `POSTGRES_DB`, `POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_HOST`, `POSTGRES_PORT`: Django database
- `DJANGO_SETTINGS_MODULE`: Settings module to use
- `DJANGO_SECRET_KEY`: Django secret key (web only)
- `DBOS_DATABASE_URL`: DBOS system database connection (both containers)
- `DATABASE_URL`: Django database connection (both containers)
- `DBOS_POSTGRES_*`: Individual DBOS database parameters (cv worker)

## Hardware Requirements

**Raspberry Pi Camera**: The cv container requires privileged mode and `/dev/video0` device access. Without camera hardware, the system automatically uses mock camera.

**ALPR Models**: fast_alpr downloads ONNX models on first run. These are cached in the container.

## Dependency Management

Dependencies are organized in `pyproject.toml` using dependency groups (PEP 735):

1. **Core dependencies**: Django, DBOS, PostgreSQL driver, Pillow, httpx, logfire
2. **Web dependency group**: Django Ninja, Gunicorn
3. **CV dependency group**: fast-alpr, opencv-python, picamera2 (Linux only via platform marker)
4. **Dev dependency group**: Testing tools, formatters (black, isort, ruff), notebooks

Dockerfiles use `uv sync` for fast dependency installation:
- Web: `uv sync --no-dev --group web`
- CV: `uv sync --no-dev --group cv`

**Note**: `picamera2` uses a platform marker (`sys_platform == 'linux'`) so it's only installed on Linux systems (Raspberry Pi). On macOS/Windows development, it's automatically skipped and the mock camera is used.

## Testing Notes

When testing locally without Raspberry Pi hardware:
- Camera and detector automatically use mock implementations
- Mock camera generates simple test patterns
- Mock detector returns random license plates with 70% success rate
- Full application flow can be tested without physical hardware
