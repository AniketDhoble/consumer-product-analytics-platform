"""
Centralized logging configuration.

Log files:
    logs/pipeline.log
        INFO and WARNING messages

    logs/errors.log
        ERROR and CRITICAL messages

Console:
    INFO, WARNING, ERROR and CRITICAL messages
"""

import logging
from pathlib import Path

from src.config.paths import LOGS_DIR


# ============================================================
# LOG DIRECTORY
# ============================================================

LOGS_DIR.mkdir(
    parents=True,
    exist_ok=True
)


# ============================================================
# LOG FILES
# ============================================================

PIPELINE_LOG_FILE = LOGS_DIR / "pipeline.log"

ERROR_LOG_FILE = LOGS_DIR / "errors.log"


# ============================================================
# LOG FORMAT
# ============================================================

LOG_FORMAT = (
    "%(asctime)s | "
    "%(levelname)s | "
    "%(name)s | "
    "%(message)s"
)

DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


# ============================================================
# CUSTOM FILTER
# ============================================================

class MaxLevelFilter(logging.Filter):
    """
    Allows log records only up to a specified level.

    Used so pipeline.log receives:
        INFO
        WARNING

    but does not receive:
        ERROR
        CRITICAL
    """

    def __init__(self, max_level):
        super().__init__()
        self.max_level = max_level

    def filter(self, record):
        return record.levelno <= self.max_level


# ============================================================
# LOGGING SETUP
# ============================================================

def setup_logging():
    """
    Configure application-wide logging.
    """

    root_logger = logging.getLogger()

    # --------------------------------------------------------
    # Prevent duplicate handlers
    # --------------------------------------------------------

    if root_logger.handlers:
        return

    root_logger.setLevel(logging.INFO)

    # ========================================================
    # FORMATTER
    # ========================================================

    formatter = logging.Formatter(
        fmt=LOG_FORMAT,
        datefmt=DATE_FORMAT
    )

    # ========================================================
    # PIPELINE FILE HANDLER
    # INFO + WARNING
    # ========================================================

    pipeline_handler = logging.FileHandler(
        PIPELINE_LOG_FILE,
        encoding="utf-8"
    )

    pipeline_handler.setLevel(logging.INFO)

    pipeline_handler.addFilter(
        MaxLevelFilter(logging.WARNING)
    )

    pipeline_handler.setFormatter(formatter)

    # ========================================================
    # ERROR FILE HANDLER
    # ERROR + CRITICAL
    # ========================================================

    error_handler = logging.FileHandler(
        ERROR_LOG_FILE,
        encoding="utf-8"
    )

    error_handler.setLevel(logging.ERROR)

    error_handler.setFormatter(formatter)

    # ========================================================
    # CONSOLE HANDLER
    # INFO+
    # ========================================================

    console_handler = logging.StreamHandler()

    console_handler.setLevel(logging.INFO)

    console_handler.setFormatter(formatter)

    # ========================================================
    # ADD HANDLERS
    # ========================================================

    root_logger.addHandler(
        pipeline_handler
    )

    root_logger.addHandler(
        error_handler
    )

    root_logger.addHandler(
        console_handler
    )


# ============================================================
# GET LOGGER
# ============================================================

def get_logger(name):
    """
    Return a logger for a specific module.
    """

    setup_logging()

    return logging.getLogger(name)