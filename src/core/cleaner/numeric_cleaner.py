"""
Numeric cleaning module.
"""

import pandas as pd

from src.core.cleaner.base_cleaner import BaseCleaner


class NumericCleaner(BaseCleaner):

    NUMERIC_COLUMNS = [
        "Sales",
        "Year",
        "Postal Code",
        "Quantity",
        "Discount",
        "Profit"
    ]

    def standardize_numeric_columns(self):

        for column in self.NUMERIC_COLUMNS:

            if column not in self.df.columns:
                self.logger.warning(
                    f"Numeric column not found: {column}"
                )
                continue

            self.df[column] = pd.to_numeric(
                self.df[column],
                errors="coerce"
            )

            self.log_change(
                f"Numeric type standardized: {column}"
            )

        return self.df