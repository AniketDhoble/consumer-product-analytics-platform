"""
Datetime cleaning module.
"""

import pandas as pd

from src.core.cleaner.base_cleaner import BaseCleaner


class DatetimeCleaner(BaseCleaner):

    DATE_COLUMNS = [
        "Date of Birth",
        "Sales Date",
        "Order Date",
        "Ship Date"
    ]

    def convert_date_columns(self):

        for column in self.DATE_COLUMNS:

            if column not in self.df.columns:
                self.logger.warning(
                    f"Date column not found: {column}"
                )
                continue

            original_invalid = (
                self.df[column].isna().sum()
            )

            self.df[column] = pd.to_datetime(
                self.df[column],
                errors="coerce"
            )

            new_invalid = (
                self.df[column].isna().sum()
            )

            self.record_change(
                f"{column}_conversion",
                {
                    "original_missing": int(
                        original_invalid
                    ),
                    "new_invalid": int(
                        new_invalid
                    )
                }
            )

            self.log_change(
                f"{column} converted to datetime."
            )

        return self.df