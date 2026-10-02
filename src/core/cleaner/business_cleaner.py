"""
Business-specific cleaning module.
"""

from src.core.cleaner.base_cleaner import BaseCleaner


class BusinessCleaner(BaseCleaner):

    def create_order_year(self):

        if "Order Date" not in self.df.columns:
            raise KeyError(
                "Order Date column is required."
            )

        self.df["Order Year"] = (
            self.df["Order Date"].dt.year
        )

        self.log_change(
            "Created Order Year from Order Date."
        )

        return self.df