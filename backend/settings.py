import os

from pathlib import Path


_PROJECT_ROOT = Path('.').resolve()

# Common application configurations
MEDIA_PATH = _PROJECT_ROOT / 'media'
MONGO_CONNECTION_STRING = os.environ['MONGO_CONN_STRING']
LOGGING_LEVEL = os.getenv('LOGGING_LEVEL', 'INFO')

# Celery worker configuration
CELERY_BROKER_URL = os.environ['CELERY_BROKER_URL']
CELERY_RESULT_BACKEND_URL = os.environ['CELERY_RESULT_BACKEND_URL']
