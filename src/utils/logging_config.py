import logging
import sys
from pathlib import Path


def setup_logger(
    name: str = "twitch_analytics", level: int = logging.INFO
) -> logging.Logger:
    """Setup and configure logger for the application

    Args:
        name: Logger name
        level: Logging level

    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)

    # Avoid adding handlers multiple times
    if logger.handlers:
        return logger

    logger.setLevel(level)

    # Create console handler
    console_handler = logging.StreamHandler(sys.stderr)  # Use stderr instead of stdout
    console_handler.setLevel(level)

    # Create file handler (optional)
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    file_handler = logging.FileHandler(log_dir / "twitch_analytics.log")
    file_handler.setLevel(logging.DEBUG)

    # Create formatter
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    console_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)

    # Add handlers to logger
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger


# Create default logger instance
logger = setup_logger()
