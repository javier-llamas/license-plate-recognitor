# License Plate Recognition System

A complete license plate recognition system designed for Raspberry Pi 5 with Django web interface, HTMX frontend, and DBOS-based computer vision worker.

## Features

- **Test Shots**: Capture single test images on demand
- **Continuous Detection**: Start/stop continuous license plate detection with 2-second intervals
- **Training Mode**: Evaluate and correct detection results to build a training dataset
- **Real-time Updates**: HTMX-powered interface for seamless user experience
- **Workflow Management**: DBOS-based workflows for reliable computer vision processing

## Architecture

The system consists of three Docker containers:

1. **web**: Django application with django-ninja API and HTMX frontend
2. **cv**: DBOS worker for computer vision tasks with camera and detector access
3. **db**: PostgreSQL database for storing results

### Technology Stack

- **Backend**: Django 5.0 with django-ninja for REST API
- **Frontend**: HTMX for dynamic interactions
- **Computer Vision**: fast_alpr for license plate detection
- **Camera**: picamera2 (optimized for Raspberry Pi 5)
- **Workflow Engine**: DBOS for reliable async processing
- **Database**: PostgreSQL 15
- **Monitoring**: Logfire for observability

## Quick Start

### Docker Compose (Recommended)

1. Clone and navigate to the directory:
```bash
git clone <repository-url>
cd license-plate-recognitor
```

2. Start all services:
```bash
docker-compose up --build
```

3. Access the web interface at `http://localhost:8000`

### Local Development

1. Create virtual environment and install dependencies:
```bash
python -m venv .venv
source .venv/bin/activate
pip install uv
uv pip install -r pyproject.toml
```

2. Start PostgreSQL:
```bash
docker-compose up db -d
```

3. Run migrations:
```bash
python manage.py migrate
python manage.py createsuperuser
```

4. Run development server:
```bash
python manage.py runserver
```

## Usage

### Web Interface

- **Home (/)**: Control detection jobs and view recent results
- **Test Shot**: Capture single images for testing
- **Evaluate (/evaluate)**: Review and correct detection results

### API Documentation

Interactive API documentation available at `http://localhost:8000/api/docs`

## Configuration

### Environment Variables

Set in `docker-compose.yml` or `.env` file:

- `POSTGRES_DB`: Database name (default: license_plate_db)
- `POSTGRES_USER`: Database user (default: lpr_user)
- `POSTGRES_PASSWORD`: Database password
- `DJANGO_SECRET_KEY`: Django secret key
- `DJANGO_SETTINGS_MODULE`: Settings module (local/production)

### Camera Access

The CV container requires privileged mode for camera access on Raspberry Pi:
```yaml
privileged: true
devices:
  - /dev/video0:/dev/video0
```

## Development Notes

- **Mock Mode**: Automatically uses mock camera/detector when hardware is unavailable
- **Media Storage**: Images stored in `/app/media` shared volume
- **Workflows**: DBOS workflows ensure reliable async processing

## Troubleshooting

### Camera Issues
```bash
ls -la /dev/video*
docker-compose logs cv
```

### Database Issues
```bash
docker-compose ps db
docker-compose logs db
```

## License

MIT License
