"""
Data consistency validation checks.
"""

import pandas as pd

from src.core.validator.base_validator import (
    BaseValidator
)


class ConsistencyValidator(BaseValidator):

    def validate(self):

        # ----------------------------------------------------
        # DATE CONSISTENCY
        # ----------------------------------------------------

        order_date = pd.to_datetime(
            self.df["Order Date"],
            errors="coerce"
        )

        ship_date = pd.to_datetime(
            self.df["Ship Date"],
            errors="coerce"
        )

        invalid_date_order = int(
            (order_date > ship_date).sum()
        )

        self.record_result(
            "order_date_after_ship_date",
            invalid_date_order
        )

        # ----------------------------------------------------
        # CUSTOMER ID → CUSTOMER NAME
        # ----------------------------------------------------

        customer_check = (
            self.df
            .groupby("Customer ID")["Customer Name"]
            .nunique()
        )

        customer_inconsistencies = int(
            (customer_check > 1).sum()
        )

        self.record_result(
            "customer_id_name_inconsistencies",
            customer_inconsistencies
        )

        # ----------------------------------------------------
        # PRODUCT ID → PRODUCT NAME
        # ----------------------------------------------------

        product_name_check = (
            self.df
            .groupby("Product ID")["Product Name"]
            .nunique()
        )

        product_name_inconsistencies = int(
            (product_name_check > 1).sum()
        )

        self.record_result(
            "product_id_name_inconsistencies",
            product_name_inconsistencies
        )

        # ----------------------------------------------------
        # PRODUCT ID → SUB-CATEGORY
        # ----------------------------------------------------

        product_category_check = (
            self.df
            .groupby("Product ID")["Sub-Category"]
            .nunique()
        )

        product_category_inconsistencies = int(
            (product_category_check > 1).sum()
        )

        self.record_result(
            "product_id_subcategory_inconsistencies",
            product_category_inconsistencies
        )

        return self.results