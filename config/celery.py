from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# Set default Django settings module for Celery
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'jobfinderapi.settings')

# Create the Celery application instance
app = Celery('jobfinderapi')

# Load custom settings from Django settings
app.config_from_object('django.conf:settings', namespace='CELERY')

# Discover tasks from all installed Django apps
app.autodiscover_tasks()
