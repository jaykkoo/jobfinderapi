"""
Django settings for jobfinderapi project.

Generated by 'django-admin startproject' using Django 5.1.1.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

import os


from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-t%%32jr=%g-*&23^3!wq4^78f9hty8ecpi6&z#f-x8rg#wc)$y"


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework_simplejwt',
    'rest_framework_simplejwt.token_blacklist',
    'offers',
    'accounts',
    'rest_framework',
    'celery',
    'django_celery_beat',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': os.getenv('DATABASE_DEFAULT_NAME', default='jobfinder'),
#         'USER': os.getenv('DATABASE_DEFAULT_USER', default='your-db-user'),
#         'PASSWORD': os.getenv('DATABASE_DEFAULT_PASSWORD', default='your-db-password'),
#         'HOST': os.getenv('DATABASE_DEFAULT_URL', default='localhost'),
#         'PORT': os.getenv('DATABASE_DEFAULT_PORT', default='5432'),  # Set default port
#     },
# }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': "jobfinderdb",
        'USER': "postgres",
        'PASSWORD': "postgres",
        'HOST': "database-jobfinder.c3as2gamozkl.eu-west-3.rds.amazonaws.com",
        'PORT': 5432,  # Set default port
    },
}

# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ),
}

# Simple JWT settings
from datetime import timedelta

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=5),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,  # Enable token blacklisting
}

# Sentry settings
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration 
sentry_sdk.init(
    dsn="https://260e1d1b1606aee340cc32e90e773090@o1009241.ingest.us.sentry.io/4508128253378560",
    integrations=[DjangoIntegration()], 
    send_default_pii= True , 
    traces_sample_rate= 1.0
)

# Celery

CELERY_BROKER_URL = 'amqp://guest:guest@localhost:5672//'  # Using RabbitMQ in Docker
CELERY_RESULT_BACKEND = 'rpc://'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers.DatabaseScheduler'

# Mail settings

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'  # Correct SMTP server for Gmail
EMAIL_PORT = 587  # Port 587 is used for TLS
EMAIL_USE_TLS = True  # Use TLS encryption
EMAIL_HOST_USER = 'apptestbis@gmail.com'  # Your Gmail address
EMAIL_HOST_PASSWORD = 'ryql ofzd juaz vrdm'  # Your Gmail password or app password
DEFAULT_FROM_EMAIL = 'apptestbis@gmail.com'
