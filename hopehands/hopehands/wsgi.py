"""
WSGI config for the HopeHands project.

This file provides the entry-point for WSGI-compatible web servers to serve the
HopeHands application. Web Server Gateway Interface (WSGI) is the standard for
Python synchronous web apps and servers.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hopehands.settings")

application = get_wsgi_application()
