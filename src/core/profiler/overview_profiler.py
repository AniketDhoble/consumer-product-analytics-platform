"""
Overview profiling.

Checks:
    - Dataset name
    - Row count
    - Column count
    - Memory usage
"""

from .base_profiler import BaseProfiler


class OverviewProfiler(BaseProfiler):

    def dataset_name_check(self):
        result = self.dataset_name

        self.log_check("dataset_name")

        return result

    def row_count(self):
        result = len(self.df)

        self.log_check("row_count")

        return result

    def column_count(self):
        result = len(self.df.columns)

        self.log_check("column_count")

        return result

    def memory_usage(self):
        result = int(
            self.df.memory_usage(
                deep=True
            ).sum()
        )

        self.log_check("memory_usage")

        return result

    def run(self):

        self.report = {
            "dataset_name": self.dataset_name_check(),
            "row_count": self.row_count(),
            "column_count": self.column_count(),
            "memory_usage_bytes": self.memory_usage()
        }

        return self.report