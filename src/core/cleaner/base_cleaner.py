"""
Base cleaner class.

Provides common functionality for all cleaning modules.
"""

from src.config.logging_config import get_logger


class BaseCleaner:

    def __init__(self, df, dataset_name):

        self.df = df.copy()
        self.dataset_name = dataset_name

        self.logger = get_logger(
            self.__class__.__name__
        )

        self.changes = {}

    def log_change(self, message):

        self.logger.info(
            f"{self.dataset_name} | {message}"
        )

    def record_change(self, check_name, value):

        self.changes[check_name] = value