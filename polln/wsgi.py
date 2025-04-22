"""
WSGI config for polln project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

# Settings module should be:
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'polln.settings.prod_settings') # for production
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'polln.settings.dev_settings') # for development

os.environ.setdefault("DJANGO_SETTINGS_MODULE", os.getenv("DJANGO_SETTINGS_MODULE", "polln.settings.dev_settings"))

application = get_wsgi_application()
