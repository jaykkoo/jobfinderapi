import pytest
import os

# Import Django settings before ASGI/WSGI application
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

from config.asgi import application as asgi_app
from config.wsgi import application as wsgi_app

def test_asgi_application():
    """Test if ASGI application initializes without errors."""
    assert asgi_app is not None

def test_wsgi_application():
    """Test if WSGI application initializes without errors."""
    assert wsgi_app is not None