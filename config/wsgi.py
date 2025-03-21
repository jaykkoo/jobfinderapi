"""
WSGI config for jobfinderapi project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/wsgi/
"""

import os
import sys

from django.core.wsgi import get_wsgi_application


application = get_wsgi_application()

if __name__ == '__main__':
    # Default to development if DJANGO_SETTINGS_MODULE isn't set
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.dev')
    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)