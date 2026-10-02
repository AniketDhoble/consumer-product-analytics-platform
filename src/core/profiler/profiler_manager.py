"""
Profiler manager.

Runs all dataset profiling modules
and combines their results into one report.
"""

from src.config.logging_config import get_logger

from .overview_profiler import OverviewProfiler
from .schema_profiler import SchemaProfiler
from .missing_profiler import MissingProfiler
from .numeric_profiler import NumericProfiler
from .categorical_profiler import CategoricalProfiler
from .datetime_profiler import DatetimeProfiler
from .quality_profiler import QualityProfiler


class ProfilerManager:

    def __init__(self, df, dataset_name):

        self.df = df
        self.dataset_name = dataset_name

        self.logger = get_logger(
            "ProfilerManager"
        )

        self.report = {}

    def run(self):

        self.logger.info(
            f"{self.dataset_name} | "
            "Data profiling started."
        )

        profilers = [
            OverviewProfiler(
                self.df,
                self.dataset_name
            ),

            SchemaProfiler(
                self.df,
                self.dataset_name
            ),

            MissingProfiler(
                self.df,
                self.dataset_name
            ),

            NumericProfiler(
                self.df,
                self.dataset_name
            ),

            CategoricalProfiler(
                self.df,
                self.dataset_name
            ),

            DatetimeProfiler(
                self.df,
                self.dataset_name
            ),

            QualityProfiler(
                self.df,
                self.dataset_name
            )
        ]

        for profiler in profilers:

            profiler_name = (
                profiler.__class__.__name__
            )

            try:

                self.report[
                    profiler_name
                ] = profiler.run()

                self.logger.info(
                    f"{self.dataset_name} | "
                    f"{profiler_name} completed."
                )

            except Exception:

                self.logger.exception(
                    f"{self.dataset_name} | "
                    f"{profiler_name} failed."
                )

        self.logger.info(
            f"{self.dataset_name} | "
            "Data profiling completed."
        )

        return self.report