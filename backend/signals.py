import os

from backend import settings


def on_application_started():
    settings.MEDIA_PATH.mkdir(exist_ok=True)
