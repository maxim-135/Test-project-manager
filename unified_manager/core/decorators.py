import logging
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)


def log_entry_exit(func):
    """Decorator to log function entry and exit."""
    def wrapper(*args, **kwargs):
        logger.debug(f"Entering {func.__name__}")
        try:
            result = func(*args, **kwargs)
            logger.debug(f"Exiting {func.__name__}")
            return result
        except Exception as e:
            logger.error(f"Error in {func.__name__}: {e}")
            raise
    return wrapper


def retry(max_attempts: int = 3, delay: float = 1.0):
    """Decorator to retry a function on failure."""
    def decorator(func):
        def wrapper(*args, **kwargs):
            import time
            last_exception = None
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    logger.warning(f"Attempt {attempt + 1} failed: {e}")
                    if attempt < max_attempts - 1:
                        time.sleep(delay)
            raise last_exception
        return wrapper
    return decorator
