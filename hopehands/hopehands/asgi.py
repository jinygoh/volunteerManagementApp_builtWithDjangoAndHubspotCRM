"""
ASGI config for the HopeHands project.

This file provides the entry-point for ASGI-compatible web servers to serve the
HopeHands application. Asynchronous Server Gateway Interface (ASGI) is a standard
for Python asynchronous web apps and servers.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hopehands.settings")

application = get_asgi_application()
