import logging

from backend import settings

common_logger = logging.getLogger()
common_logger.setLevel(settings.LOGGING_LEVEL)
