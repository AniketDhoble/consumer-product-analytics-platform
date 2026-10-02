"""
Structural validation checks.
"""

from src.core.validator.base_validator import (
    BaseValidator
)


class StructuralValidator(BaseValidator):

    def validate(self):

        # ----------------------------------------------------
        # ROW COUNT
        # ----------------------------------------------------

        self.record_result(
            "row_count",
            len(self.df)
        )

        # ----------------------------------------------------
        # COLUMN COUNT
        # ----------------------------------------------------

        self.record_result(
            "column_count",
            len(self.df.columns)
        )

        # ----------------------------------------------------
        # MISSING VALUES
        # ----------------------------------------------------

        missing_values = int(
            self.df.isna().sum().sum()
        )

        self.record_result(
            "total_missing_values",
            missing_values
        )

        # ----------------------------------------------------
        # DUPLICATE ROWS
        # ----------------------------------------------------

        duplicate_rows = int(
            self.df.duplicated().sum()
        )

        self.record_result(
            "duplicate_rows",
            duplicate_rows
        )

        # ----------------------------------------------------
        # BLANK STRINGS
        # ----------------------------------------------------

        blank_strings = 0

        string_columns = (
            self.df
            .select_dtypes(
                include=["object", "string"]
            )
            .columns
        )

        for column in string_columns:

            blank_strings += int(
                self.df[column]
                .fillna("")
                .astype(str)
                .str.strip()
                .eq("")
                .sum()
            )

        self.record_result(
            "blank_strings",
            blank_strings
        )

        return self.results