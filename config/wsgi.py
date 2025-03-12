"""
WSGI config for jobfinderapi project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/wsgi/
"""

import os
import sys

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

application = get_wsgi_application()

def application(environ, start_response):
    for key, value in environ.items():
        if isinstance(value, str):
            os.environ[key] = value
    return get_wsgi_application()(environ, start_response)