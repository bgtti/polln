"""
Settings specific to production environment.
Inherits from base settings.
"""
from .base_settings import *
import mysql.connector

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# Define base url (points to localhost in development)
BASE_URL = os.getenv("BASE_URL")

ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '').split(',') 
CSRF_TRUSTED_ORIGINS = os.environ.get('CSRF_TRUSTED_ORIGINS', '').split(',')

STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
STATICFILES_DIRS = [ os.path.join(BASE_DIR / "static"), ]