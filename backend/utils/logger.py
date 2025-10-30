# backend/utils/logger.py
import logging
from logging.handlers import RotatingFileHandler
import os

# Create logs directory if not exists
LOG_DIR = os.path.join(os.path.dirname(__file__), "..", "logs")
os.makedirs(LOG_DIR, exist_ok=True)

LOG_FILE = os.path.join(LOG_DIR, "app.log")

def setup_logger(name="finance_copilot", log_file=LOG_FILE, level=logging.INFO):
    """Set up a rotating file logger."""
    logger = logging.getLogger(name)

    # Prevent duplicate handlers if reloaded
    if logger.hasHandlers():
        return logger

    logger.setLevel(level)

    # Rotating handler: 5MB per file, keep last 5 logs
    handler = RotatingFileHandler(log_file, maxBytes=5_000_000, backupCount=5)
    formatter = logging.Formatter(
        "%(asctime)s [%(levelname)s] %(filename)s:%(lineno)d - %(message)s"
    )
    handler.setFormatter(formatter)

    # Optional: also log to console during dev
    console = logging.StreamHandler()
    console.setFormatter(formatter)

    logger.addHandler(handler)
    logger.addHandler(console)

    return logger


# Initialize global logger instance
logger = setup_logger()

