import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("TestLogger")


def error_logger(message):
    """Log errors."""
    logger.error(message)
