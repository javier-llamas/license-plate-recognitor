"""
Production settings for Raspberry Pi deployment.
"""
from .base import *  # noqa: F403, F401

DEBUG = False

ALLOWED_HOSTS = ['*']  # Local WiFi network, no authentication required

# Security settings for production
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = 'DENY'
SECURE_CONTENT_TYPE_NOSNIFF = True
