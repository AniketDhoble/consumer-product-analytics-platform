"""
Base validator class.
"""

from src.config.logging_config import get_logger


class BaseValidator:

    def __init__(self, df, dataset_name):

        self.df = df
        self.dataset_name = dataset_name

        self.logger = get_logger(
            self.__class__.__name__
        )

        self.results = {}

    def record_result(self, check_name, result):

        self.results[check_name] = result

        self.logger.info(
            f"{self.dataset_name} | "
            f"Validation completed: {check_name}"
        )