"""
Datetime profiling.

Checks:
    - Existing datetime columns
    - Potential datetime columns
    - Minimum date
    - Maximum date
    - Date range
"""

import pandas as pd

from .base_profiler import BaseProfiler


class DatetimeProfiler(BaseProfiler):

    def _datetime_df(self):

        return self.df.select_dtypes(
            include=["datetime", "datetimetz"]
        )

    def datetime_columns(self):

        result = list(
            self._datetime_df().columns
        )

        self.log_check(
            "datetime_columns"
        )

        return result

    def potential_datetime_columns(self):

        candidates = []

        name_keywords = [
            "date",
            "time",
            "year",
            "month",
            "day"
        ]

        for column in self.df.columns:

            column_name = str(column).lower()

            if any(
                keyword in column_name
                for keyword in name_keywords
            ):

                if self.df[column].dtype == "object":

                    try:

                        parsed = pd.to_datetime(
                            self.df[column],
                            errors="coerce"
                        )

                        valid_ratio = (
                            parsed.notna().mean()
                        )

                        if valid_ratio >= 0.80:
                            candidates.append(
                                column
                            )

                    except Exception:
                        continue

        self.log_check(
            "potential_datetime_columns"
        )

        return candidates

    def minimum_date(self):

        result = {}

        for column in self._datetime_df().columns:

            value = self.df[column].min()

            result[column] = (
                value.isoformat()
                if pd.notna(value)
                else None
            )

        self.log_check(
            "minimum_date"
        )

        return result

    def maximum_date(self):

        result = {}

        for column in self._datetime_df().columns:

            value = self.df[column].max()

            result[column] = (
                value.isoformat()
                if pd.notna(value)
                else None
            )

        self.log_check(
            "maximum_date"
        )

        return result

    def date_range(self):

        result = {}

        for column in self._datetime_df().columns:

            series = self.df[column].dropna()

            if series.empty:
                result[column] = None
                continue

            minimum = series.min()
            maximum = series.max()

            result[column] = (
                maximum - minimum
            ).days

        self.log_check(
            "date_range"
        )

        return result

    def run(self):

        self.report = {
            "datetime_columns":
                self.datetime_columns(),

            "potential_datetime_columns":
                self.potential_datetime_columns(),

            "minimum_date":
                self.minimum_date(),

            "maximum_date":
                self.maximum_date(),

            "date_range_days":
                self.date_range()
        }

        return self.report