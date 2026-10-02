"""
Business rule validation checks.
"""

from src.core.validator.base_validator import (
    BaseValidator
)


class BusinessValidator(BaseValidator):

    def validate(self):

        # ----------------------------------------------------
        # SALES
        # ----------------------------------------------------

        sales_invalid = int(
            (self.df["Sales"] <= 0).sum()
        )

        self.record_result(
            "sales_less_than_or_equal_zero",
            sales_invalid
        )

        # ----------------------------------------------------
        # QUANTITY
        # ----------------------------------------------------

        quantity_invalid = int(
            (self.df["Quantity"] <= 0).sum()
        )

        self.record_result(
            "quantity_less_than_or_equal_zero",
            quantity_invalid
        )

        # ----------------------------------------------------
        # DISCOUNT
        # ----------------------------------------------------

        discount_invalid = int(
            (
                (self.df["Discount"] < 0)
                |
                (self.df["Discount"] > 1)
            ).sum()
        )

        self.record_result(
            "discount_outside_valid_range",
            discount_invalid
        )

        # ----------------------------------------------------
        # PROFIT
        # ----------------------------------------------------

        # ----------------------------------------------------
        # PROFIT
        # ----------------------------------------------------

        negative_profit_count = int(
            (self.df["Profit"] < 0).sum()
        )

        self.record_result(
            "negative_profit",
            negative_profit_count
        )