"""
Categorical profiling.

Checks:
    - Categorical columns
    - Unique value count
    - Cardinality
    - Most frequent value
    - Most frequent count
    - Least frequent value
    - Top 10 value counts
"""

from .base_profiler import BaseProfiler


class CategoricalProfiler(BaseProfiler):

    def _categorical_df(self):

        return self.df.select_dtypes(
            include=["object", "string", "category"]
        )

    def categorical_columns(self):

        result = list(
            self._categorical_df().columns
        )

        self.log_check(
            "categorical_columns"
        )

        return result

    def unique_value_count(self):

        result = {
            column: int(
                self._categorical_df()[column]
                .nunique(dropna=True)
            )
            for column
            in self._categorical_df().columns
        }

        self.log_check(
            "unique_value_count"
        )

        return result

    def cardinality(self):

        result = {}

        for column in self._categorical_df().columns:

            non_null_count = (
                self._categorical_df()[column]
                .notna()
                .sum()
            )

            unique_count = (
                self._categorical_df()[column]
                .nunique(dropna=True)
            )

            if non_null_count == 0:
                result[column] = 0.0
            else:
                result[column] = round(
                    float(
                        unique_count
                        / non_null_count
                        * 100
                    ),
                    2
                )

        self.log_check("cardinality")

        return result

    def most_frequent_value(self):

        result = {}

        for column in self._categorical_df().columns:

            series = (
                self._categorical_df()[column]
                .dropna()
            )

            if series.empty:
                result[column] = None
            else:
                result[column] = str(
                    series.value_counts()
                    .index[0]
                )

        self.log_check(
            "most_frequent_value"
        )

        return result

    def most_frequent_count(self):

        result = {}

        for column in self._categorical_df().columns:

            series = (
                self._categorical_df()[column]
                .dropna()
            )

            if series.empty:
                result[column] = 0
            else:
                result[column] = int(
                    series.value_counts()
                    .iloc[0]
                )

        self.log_check(
            "most_frequent_count"
        )

        return result

    def least_frequent_value(self):

        result = {}

        for column in self._categorical_df().columns:

            series = (
                self._categorical_df()[column]
                .dropna()
            )

            if series.empty:
                result[column] = None
            else:
                result[column] = str(
                    series.value_counts()
                    .index[-1]
                )

        self.log_check(
            "least_frequent_value"
        )

        return result

    def top_10_value_counts(self):

        result = {}

        for column in self._categorical_df().columns:

            counts = (
                self._categorical_df()[column]
                .dropna()
                .value_counts()
                .head(10)
            )

            result[column] = {
                str(key): int(value)
                for key, value
                in counts.items()
            }

        self.log_check(
            "top_10_value_counts"
        )

        return result

    def run(self):

        self.report = {
            "categorical_columns":
                self.categorical_columns(),

            "unique_value_count":
                self.unique_value_count(),

            "cardinality":
                self.cardinality(),

            "most_frequent_value":
                self.most_frequent_value(),

            "most_frequent_count":
                self.most_frequent_count(),

            "least_frequent_value":
                self.least_frequent_value(),

            "top_10_value_counts":
                self.top_10_value_counts()
        }

        return self.report