"""
Base profiler class.

Provides common functionality for all profiler modules.
"""

from src.config.logging_config import get_logger


class BaseProfiler:
    """
    Base class for dataset profiling.
    """

    def __init__(self, df, dataset_name):
        self.df = df
        self.dataset_name = dataset_name
        self.report = {}

        self.logger = get_logger(
            self.__class__.__name__
        )

    def log_check(self, check_name):
        """
        Log successful profiling check.
        """

        self.logger.info(
            f"{self.dataset_name} | "
            f"Profiling check completed: {check_name}"
        )

    def log_error(self, check_name):
        """
        Log profiling check failure.
        """

        self.logger.exception(
            f"{self.dataset_name} | "
            f"Profiling check failed: {check_name}"
        )