"""
DBOS Computer Vision Worker - Main Entry Point

This is a pure DBOS Python application (no FastAPI).
Django sends workflow start signals via DBOS client.
DBOS manages its own system tables for workflow state.
"""

import os
import sys

import django

# Add project root to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Setup Django for ORM access
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.production")
django.setup()

import logfire  # noqa: E402
from dbos import DBOS, DBOSConfig  # noqa: E402

# Configure logfire for monitoring
logfire.configure()

# Initialize DBOS with configuration
# DBOS will read from dbos-config.yaml for database URLs
config = DBOSConfig(
    name="lpr-cv-worker",
    system_database_url=os.environ.get("DBOS_DATABASE_URL"),
    application_database_url=os.environ.get("DATABASE_URL"),
    log_level="INFO",
)

# Create DBOS instance
app = DBOS(config=config)

# Import workflows to register them with DBOS

# DBOS will run as a background service
# Workflows are triggered via DBOS client from Django API
if __name__ == "__main__":
    # Start DBOS runtime (keeps process alive)
    app.launch()
