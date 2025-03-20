from .base import *
import os

ALLOWED_HOSTS = ['35.180.198.48']

AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID', '')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY', '')
AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME', '')


STORAGES = {
    "default": {
        "BACKEND": "storages.backends.s3boto3.S3Boto3Storage",
    },
    "staticfiles": {
        "BACKEND": "storages.backends.s3boto3.S3Boto3Storage",
    },
}
AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'

# AWS_S3_FILE_OVERWRITE = False

ADMIN_MEDIA_PREFIX = '/static/admin/'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME'),
        'USER': os.environ.get('DB_USER'),
        'PASSWORD': os.environ.get('DB_PASSWORD'), 
        'HOST': os.environ.get('DB_HOST'),
        'PORT': '5432',
         'TEST': {
            'NAME': 'jobfindertest',  # Default to 'test_db' if not set
            'USER': 'postgres',
            'PASSWORD': 'postgreS',
            'HOST':'database-test-2.cdy0g4auei8z.eu-west-3.rds.amazonaws.com',
        },
    },
}
STATIC_URL = f"https://{AWS_S3_CUSTOM_DOMAIN}/static/"

CORS_ALLOWED_ORIGINS = [
    "http://35.180.198.48",  # Your frontend origin
]

CORS_ALLOW_CREDENTIALS = True  # Allow sending cookies with requests
CSRF_COOKIE_SECURE = True  # Ensure CSRF cookie is sent over HTTPS
CSRF_COOKIE_SAMESITE = 'None'  # Allow CSRF cookies to be sent cross-site
CSRF_TRUSTED_ORIGINS = [
    'http://35.180.198.48',  # Trust your frontend domain
]