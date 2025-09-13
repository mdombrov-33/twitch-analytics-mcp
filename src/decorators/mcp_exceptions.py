import functools
from ..utils.exceptions import (
    AuthenticationError,
    ServiceUnavailableError,
    ResourceNotFoundError,
)
from ..utils.logging_config import logger


def handle_mcp_exceptions(func):
    """Decorator to handle common MCP tool exceptions"""

    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except AuthenticationError as e:
            logger.error(f"Authentication error in {func.__name__}: {e}")
            return [{"error": f"Authentication failed: {e}"}]
        except ServiceUnavailableError as e:
            logger.error(f"Service unavailable in {func.__name__}: {e}")
            return [{"error": f"Service temporarily unavailable: {e}"}]
        except ResourceNotFoundError as e:
            logger.warning(f"No resources found in {func.__name__}: {e}")
            return [{"message": str(e)}]
        except Exception as e:
            logger.error(f"Unexpected error in {func.__name__}: {e}")
            return [{"error": f"An unexpected error occurred: {e}"}]

    return wrapper
