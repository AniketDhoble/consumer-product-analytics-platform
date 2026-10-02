"""
Central validation manager.
"""

from src.core.validator.structural_validator import (
    StructuralValidator
)

from src.core.validator.consistency_validator import (
    ConsistencyValidator
)

from src.core.validator.business_validator import (
    BusinessValidator
)

from src.config.logging_config import get_logger


class ValidatorManager:

    def __init__(self, df, dataset_name):

        self.df = df
        self.dataset_name = dataset_name

        self.logger = get_logger(
            "ValidatorManager"
        )

        self.report = {}

    def run(self):

        self.logger.info(
            f"{self.dataset_name} | "
            "Validation started."
        )

        # ----------------------------------------------------
        # STRUCTURAL VALIDATION
        # ----------------------------------------------------

        structural_validator = StructuralValidator(
            self.df,
            self.dataset_name
        )

        self.report["StructuralValidator"] = (
            structural_validator.validate()
        )

        # ----------------------------------------------------
        # CONSISTENCY VALIDATION
        # ----------------------------------------------------

        consistency_validator = ConsistencyValidator(
            self.df,
            self.dataset_name
        )

        self.report["ConsistencyValidator"] = (
            consistency_validator.validate()
        )

        # ----------------------------------------------------
        # BUSINESS VALIDATION
        # ----------------------------------------------------

        business_validator = BusinessValidator(
            self.df,
            self.dataset_name
        )

        self.report["BusinessValidator"] = (
            business_validator.validate()
        )

        self.logger.info(
            f"{self.dataset_name} | "
            "Validation completed."
        )

        return self.report