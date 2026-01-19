"""
Local development settings.
"""
import os  # noqa: F401

from .base import *  # noqa: F403, F401

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

# Database for local development (can use SQLite or local PostgreSQL)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('POSTGRES_DB', 'license_plate_db'),
        'USER': os.environ.get('POSTGRES_USER', 'lpr_user'),
        'PASSWORD': os.environ.get('POSTGRES_PASSWORD', 'lpr_password'),
        'HOST': os.environ.get('POSTGRES_HOST', 'localhost'),
        'PORT': os.environ.get('POSTGRES_PORT', '5432'),
    }
}
