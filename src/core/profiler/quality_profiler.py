"""
Data-quality profiling.

Checks:
    - Constant columns
    - Mixed data types
    - Potential numeric-as-text columns
    - Potential identifier columns
    - Duplicate rows
    - Duplicate row percentage
    - Blank/whitespace-only values
"""

from .base_profiler import BaseProfiler


class QualityProfiler(BaseProfiler):

    def constant_columns(self):

        result = [
            column
            for column in self.df.columns
            if self.df[column]
            .nunique(dropna=False) == 1
        ]

        self.log_check(
            "constant_columns"
        )

        return result

    def mixed_data_type_columns(self):

        result = {}

        for column in self.df.columns:

            non_null = (
                self.df[column]
                .dropna()
            )

            if non_null.empty:
                continue

            type_count = (
                non_null
                .map(type)
                .nunique()
            )

            if type_count > 1:
                result[column] = int(
                    type_count
                )

        self.log_check(
            "mixed_data_type_columns"
        )

        return result

    def numeric_as_text_columns(
        self,
        threshold=0.95
    ):

        result = {}

        for column in self.df.select_dtypes(
            include=["object", "string"]
        ).columns:

            series = (
                self.df[column]
                .dropna()
            )

            if series.empty:
                continue

            converted = (
                series.astype(str)
                .str.replace(",", "", regex=False)
            )

            numeric_values = (
                converted
                .str.replace(
                    ".", "",
                    n=1,
                    regex=False
                )
                .str.replace(
                    "-", "",
                    n=1,
                    regex=False
                )
                .str.isnumeric()
            )

            ratio = numeric_values.mean()

            if ratio >= threshold:

                result[column] = round(
                    float(ratio * 100),
                    2
                )

        self.log_check(
            "numeric_as_text_columns"
        )

        return result

    def identifier_columns(
        self,
        threshold=0.90
    ):

        result = {}

        for column in self.df.columns:

            non_null_count = (
                self.df[column]
                .notna()
                .sum()
            )

            if non_null_count == 0:
                continue

            unique_count = (
                self.df[column]
                .nunique(dropna=True)
            )

            uniqueness_ratio = (
                unique_count
                / non_null_count
            )

            column_name = (
                str(column)
                .lower()
            )

            identifier_keyword = any(
                keyword in column_name
                for keyword in [
                    "id",
                    "code",
                    "key",
                    "number",
                    "no"
                ]
            )

            if (
                uniqueness_ratio >= threshold
                and identifier_keyword
            ):

                result[column] = round(
                    float(
                        uniqueness_ratio * 100
                    ),
                    2
                )

        self.log_check(
            "potential_identifier_columns"
        )

        return result

    def duplicate_row_count(self):

        result = int(
            self.df.duplicated()
            .sum()
        )

        self.log_check(
            "duplicate_row_count"
        )

        return result

    def duplicate_row_percentage(self):

        if len(self.df) == 0:
            result = 0.0
        else:
            result = round(
                float(
                    self.df.duplicated()
                    .mean()
                    * 100
                ),
                2
            )

        self.log_check(
            "duplicate_row_percentage"
        )

        return result

    def blank_string_count(self):

        result = {}

        for column in self.df.select_dtypes(
            include=["object", "string"]
        ).columns:

            count = (
                self.df[column]
                .fillna("")
                .astype(str)
                .str.strip()
                .eq("")
                .sum()
            )

            result[column] = int(count)

        self.log_check(
            "blank_string_count"
        )

        return result

    def run(self):

        self.report = {
            "constant_columns":
                self.constant_columns(),

            "mixed_data_type_columns":
                self.mixed_data_type_columns(),

            "numeric_as_text_columns":
                self.numeric_as_text_columns(),

            "potential_identifier_columns":
                self.identifier_columns(),

            "duplicate_row_count":
                self.duplicate_row_count(),

            "duplicate_row_percentage":
                self.duplicate_row_percentage(),

            "blank_string_count":
                self.blank_string_count()
        }

        return self.report