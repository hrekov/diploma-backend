import os

from pathlib import Path


_PROJECT_ROOT = Path('.').resolve()

# Common application configurations
MEDIA_PATH = _PROJECT_ROOT / 'media'
LOGGING_LEVEL = os.getenv('LOGGING_LEVEL', 'INFO')
RESOURCES_FOLDER = _PROJECT_ROOT / 'resources'

# Celery worker configuration
CELERY_BROKER_URL = os.environ['CELERY_BROKER_URL']
CELERY_RESULT_BACKEND_URL = os.environ['CELERY_RESULT_BACKEND_URL']
