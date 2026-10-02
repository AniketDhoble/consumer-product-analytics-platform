"""
Missing-value profiling.

Checks:
    - Total missing values
    - Missing count
    - Missing percentage
    - Empty columns
    - Rows containing missing values
    - High-missing columns
    - Missing patterns
"""

from .base_profiler import BaseProfiler


class MissingProfiler(BaseProfiler):

    def total_missing_values(self):
        result = int(
            self.df.isna().sum().sum()
        )

        self.log_check("total_missing_values")

        return result

    def null_count(self):
        result = {
            column: int(count)
            for column, count
            in self.df.isna().sum().items()
        }

        self.log_check("null_count")

        return result

    def null_percentage(self):
        if len(self.df) == 0:
            result = {
                column: 0.0
                for column in self.df.columns
            }
        else:
            result = {
                column: round(
                    float(
                        self.df[column].isna().mean()
                        * 100
                    ),
                    2
                )
                for column in self.df.columns
            }

        self.log_check("null_percentage")

        return result

    def empty_columns(self):
        result = [
            column
            for column in self.df.columns
            if self.df[column].isna().all()
        ]

        self.log_check("empty_columns")

        return result

    def missing_row_count(self):
        result = int(
            self.df.isna()
            .any(axis=1)
            .sum()
        )

        self.log_check("missing_row_count")

        return result

    def missing_row_percentage(self):
        if len(self.df) == 0:
            result = 0.0
        else:
            result = round(
                float(
                    self.missing_row_count()
                    / len(self.df)
                    * 100
                ),
                2
            )

        self.log_check("missing_row_percentage")

        return result

    def high_missing_columns(
        self,
        threshold=50
    ):
        percentages = self.df.isna().mean() * 100

        result = {
            column: round(float(value), 2)
            for column, value
            in percentages.items()
            if value >= threshold
        }

        self.log_check(
            "high_missing_columns"
        )

        return result

    def missing_pattern(self, top_n=10):
        if self.df.empty:
            return {}

        patterns = (
            self.df.isna()
            .astype(int)
            .value_counts()
            .head(top_n)
        )

        result = {}

        for pattern, count in patterns.items():

            pattern_key = ",".join(
                map(str, pattern)
            )

            result[pattern_key] = int(count)

        self.log_check("missing_pattern")

        return result

    def run(self):

        self.report = {
            "total_missing_values":
                self.total_missing_values(),

            "null_count":
                self.null_count(),

            "null_percentage":
                self.null_percentage(),

            "empty_columns":
                self.empty_columns(),

            "missing_row_count":
                self.missing_row_count(),

            "missing_row_percentage":
                self.missing_row_percentage(),

            "high_missing_columns":
                self.high_missing_columns(),

            "missing_pattern":
                self.missing_pattern()
        }

        return self.report