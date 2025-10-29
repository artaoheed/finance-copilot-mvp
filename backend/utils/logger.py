import logging
from datetime import datetime

def setup_logger(name="finance_copilot", log_file="app.log", level=logging.INFO):
    """Basic rotating logger setup."""
    formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s')
    handler = logging.FileHandler(log_file)
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)
    return logger

logger = setup_logger()
