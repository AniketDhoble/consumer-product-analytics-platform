"""
Numeric profiling.

Checks:
    - Numeric columns
    - Mean
    - Median
    - Mode
    - Minimum
    - Maximum
    - Standard deviation
    - Variance
    - Skewness
    - Kurtosis
    - Q1
    - Q3
    - IQR
    - Zero count
    - Negative count
"""

from .base_profiler import BaseProfiler


class NumericProfiler(BaseProfiler):

    def _numeric_df(self):
        return self.df.select_dtypes(
            include="number"
        )

    def numeric_columns(self):
        result = list(
            self._numeric_df().columns
        )

        self.log_check("numeric_columns")

        return result

    def mean(self):
        result = {
            column: float(value)
            for column, value
            in self._numeric_df()
            .mean()
            .items()
        }

        self.log_check("mean")

        return result

    def median(self):
        result = {
            column: float(value)
            for column, value
            in self._numeric_df()
            .median()
            .items()
        }

        self.log_check("median")

        return result

    def mode(self):
        result = {}

        numeric_df = self._numeric_df()

        for column in numeric_df.columns:

            mode_values = (
                numeric_df[column]
                .dropna()
                .mode()
            )

            result[column] = (
                float(mode_values.iloc[0])
                if not mode_values.empty
                else None
            )

        self.log_check("mode")

        return result

    def minimum_value(self):
        result = {
            column: float(value)
            for column, value
            in self._numeric_df()
            .min()
            .items()
        }

        self.log_check("minimum_value")

        return result

    def maximum_value(self):
        result = {
            column: float(value)
            for column, value
            in self._numeric_df()
            .max()
            .items()
        }

        self.log_check("maximum_value")

        return result

    def standard_deviation(self):
        result = {
            column: float(value)
            for column, value
            in self._numeric_df()
            .std()
            .items()
        }

        self.log_check("standard_deviation")

        return result

    def variance(self):
        result = {
            column: float(value)
            for column, value
            in self._numeric_df()
            .var()
            .items()
        }

        self.log_check("variance")

        return result

    def skewness(self):
        result = {
            column: float(value)
            for column, value
            in self._numeric_df()
            .skew()
            .items()
        }

        self.log_check("skewness")

        return result

    def kurtosis(self):
        result = {
            column: float(value)
            for column, value
            in self._numeric_df()
            .kurtosis()
            .items()
        }

        self.log_check("kurtosis")

        return result

    def q1(self):
        result = {
            column: float(value)
            for column, value
            in self._numeric_df()
            .quantile(0.25)
            .items()
        }

        self.log_check("q1")

        return result

    def q3(self):
        result = {
            column: float(value)
            for column, value
            in self._numeric_df()
            .quantile(0.75)
            .items()
        }

        self.log_check("q3")

        return result

    def iqr(self):
        numeric_df = self._numeric_df()

        result = {}

        for column in numeric_df.columns:

            q1 = numeric_df[column].quantile(0.25)
            q3 = numeric_df[column].quantile(0.75)

            result[column] = float(q3 - q1)

        self.log_check("iqr")

        return result

    def zero_count(self):
        result = {
            column: int(
                (self._numeric_df()[column] == 0)
                .sum()
            )
            for column
            in self._numeric_df().columns
        }

        self.log_check("zero_count")

        return result

    def negative_count(self):
        result = {
            column: int(
                (self._numeric_df()[column] < 0)
                .sum()
            )
            for column
            in self._numeric_df().columns
        }

        self.log_check("negative_count")

        return result

    def run(self):

        self.report = {
            "numeric_columns":
                self.numeric_columns(),

            "mean":
                self.mean(),

            "median":
                self.median(),

            "mode":
                self.mode(),

            "minimum":
                self.minimum_value(),

            "maximum":
                self.maximum_value(),

            "standard_deviation":
                self.standard_deviation(),

            "variance":
                self.variance(),

            "skewness":
                self.skewness(),

            "kurtosis":
                self.kurtosis(),

            "q1":
                self.q1(),

            "q3":
                self.q3(),

            "iqr":
                self.iqr(),

            "zero_count":
                self.zero_count(),

            "negative_count":
                self.negative_count()
        }

        return self.report