"""
Settings specific to local development.
Inherits from base settings.
"""
from .base_settings import *

DEBUG = True

# Define base url (points to localhost in development)
BASE_URL = "http://127.0.0.1:8000"

ALLOWED_HOSTS = []
CSRF_TRUSTED_ORIGINS = []

INSTALLED_APPS += ["django_browser_reload"]
MIDDLEWARE += ["django_browser_reload.middleware.BrowserReloadMiddleware"]

STATIC_ROOT = BASE_DIR / "static_root"
STATICFILES_DIRS = [ BASE_DIR / "static", ]