"""
Central cleaning manager.
"""

from src.core.cleaner.datetime_cleaner import (
    DatetimeCleaner
)

from src.core.cleaner.string_cleaner import (
    StringCleaner
)

from src.core.cleaner.numeric_cleaner import (
    NumericCleaner
)

from src.core.cleaner.business_cleaner import (
    BusinessCleaner
)

from src.config.logging_config import get_logger


class CleanerManager:

    def __init__(self, df, dataset_name):

        self.df = df.copy()
        self.dataset_name = dataset_name

        self.logger = get_logger(
            "CleanerManager"
        )

        self.report = {}

    def run(self):

        self.logger.info(
            f"{self.dataset_name} | "
            "Data cleaning started."
        )

        # ----------------------------------------------------
        # STRING CLEANING
        # ----------------------------------------------------

        string_cleaner = StringCleaner(
            self.df,
            self.dataset_name
        )

        self.df = (
            string_cleaner
            .clean_string_columns()
        )

        self.report["StringCleaner"] = (
            string_cleaner.changes
        )

        # ----------------------------------------------------
        # DATETIME CLEANING
        # ----------------------------------------------------

        datetime_cleaner = DatetimeCleaner(
            self.df,
            self.dataset_name
        )

        self.df = (
            datetime_cleaner
            .convert_date_columns()
        )

        self.report["DatetimeCleaner"] = (
            datetime_cleaner.changes
        )

        # ----------------------------------------------------
        # NUMERIC CLEANING
        # ----------------------------------------------------

        numeric_cleaner = NumericCleaner(
            self.df,
            self.dataset_name
        )

        self.df = (
            numeric_cleaner
            .standardize_numeric_columns()
        )

        self.report["NumericCleaner"] = (
            numeric_cleaner.changes
        )

        # ----------------------------------------------------
        # BUSINESS CLEANING
        # ----------------------------------------------------

        business_cleaner = BusinessCleaner(
            self.df,
            self.dataset_name
        )

        self.df = (
            business_cleaner
            .create_order_year()
        )

        self.report["BusinessCleaner"] = (
            business_cleaner.changes
        )

        self.logger.info(
            f"{self.dataset_name} | "
            "Data cleaning completed."
        )

        return self.df, self.report