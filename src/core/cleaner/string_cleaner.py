"""
String cleaning module.
"""

import pandas as pd

from src.core.cleaner.base_cleaner import BaseCleaner


class StringCleaner(BaseCleaner):

    def clean_string_columns(self):

        string_columns = self.df.select_dtypes(
            include=["object", "string"]
        ).columns

        for column in string_columns:

            self.df[column] = (
                self.df[column]
                .astype("string")
                .str.strip()
            )

            self.log_change(
                f"Whitespace standardized: {column}"
            )

        return self.df