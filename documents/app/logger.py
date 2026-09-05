import logging

logger = logging.getLogger("uvicorn.error")


def log_exception(message: str, error: Exception) -> None:
    logger.error("%s: %s", message, error, exc_info=error)
