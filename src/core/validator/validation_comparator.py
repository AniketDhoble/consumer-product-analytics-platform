
"""
Before vs After validation comparison.
"""

import numbers

import pandas as pd


class ValidationComparator:

    def __init__(
        self,
        before_report,
        after_report
    ):
        self.before_report = before_report
        self.after_report = after_report

    def compare(self):

        rows = []

        # ====================================================
        # STRUCTURAL VALIDATION
        # ====================================================

        self._compare_category(
            "StructuralValidator",
            rows
        )

        # ====================================================
        # CONSISTENCY VALIDATION
        # ====================================================

        self._compare_category(
            "ConsistencyValidator",
            rows
        )

        # ====================================================
        # BUSINESS VALIDATION
        # ====================================================

        self._compare_category(
            "BusinessValidator",
            rows
        )

        return pd.DataFrame(rows)

    def _compare_category(
        self,
        category,
        rows
    ):

        before = self.before_report.get(
            category,
            {}
        )

        after = self.after_report.get(
            category,
            {}
        )

        check_names = set(before) | set(after)

        for check_name in sorted(check_names):

            before_value = before.get(
                check_name,
                "N/A"
            )

            after_value = after.get(
                check_name,
                "N/A"
            )

            status = self._determine_status(
                check_name,
                before_value,
                after_value
            )

            rows.append(
                {
                    "Category": category,
                    "Check": check_name,
                    "Before": before_value,
                    "After": after_value,
                    "Status": status
                }
            )

    @staticmethod
    def _determine_status(
        check_name,
        before_value,
        after_value
    ):

        # ----------------------------------------------------
        # INFORMATIONAL STRUCTURAL COUNTS
        # ----------------------------------------------------

        if check_name in {
            "row_count",
            "column_count"
        }:
            return "INFO"

        # ----------------------------------------------------
        # VALIDATION CHECKS
        # ----------------------------------------------------

        if (
            isinstance(before_value, numbers.Integral)
            and isinstance(after_value, numbers.Integral)
        ):

            if after_value == 0:
                return "PASS"

            return "FAIL"

        # ----------------------------------------------------
        # NON-NUMERIC / UNEXPECTED VALUES
        # ----------------------------------------------------

        return "INFO"
