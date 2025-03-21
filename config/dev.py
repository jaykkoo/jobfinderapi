from .base import *

ALLOWED_HOSTS = ['localhost', '127.0.0.1', '*'] 

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'jobfinderdb',
        'USER': 'postgres',
        'PASSWORD': 'postgres', 
        'HOST': 'localhost',
        'PORT': '5432',
    },
}

# CORS settings
CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",  # Your frontend origin
]


# Celery

# CELERY_BROKER_URL = 'amqp://guest:guest@localhost:5672//'  # Using RabbitMQ in Docker
# CELERY_RESULT_BACKEND = 'rpc://'
# CELERY_ACCEPT_CONTENT = ['json']
# CELERY_TASK_SERIALIZER = 'json'
# CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers.DatabaseScheduler'