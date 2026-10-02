"""
ETL Validation Step

Reads the processed dataset and validates
its structural, consistency, and business rules.
"""

import pandas as pd

from src.config.paths import PROCESSED_DATA_DIR

from src.config.logging_config import get_logger

from src.core.validator.validator_manager import (
    ValidatorManager
)


def validate_data(dataset_name):

    logger = get_logger(
        "ETLValidateData"
    )

    # ==================================================
    # START
    # ==================================================

    logger.info(
        f"{dataset_name} | "
        "Processed data validation started."
    )

    # ==================================================
    # CREATE SAFE FILE NAME
    # ==================================================

    safe_dataset_name = (
        dataset_name
        .replace(" ", "_")
        .replace("/", "_")
        .replace("\\", "_")
    )

    input_file = (
        PROCESSED_DATA_DIR
        / f"{safe_dataset_name}_processed.csv"
    )

    # ==================================================
    # CHECK FILE
    # ==================================================

    if not input_file.exists():

        logger.error(
            f"Processed dataset not found: "
            f"{input_file}"
        )

        raise FileNotFoundError(
            f"Processed dataset not found: "
            f"{input_file}"
        )

    # ==================================================
    # LOAD PROCESSED DATA
    # ==================================================

    df = pd.read_csv(
        input_file
    )

    logger.info(
        f"{dataset_name} | "
        f"Processed dataset loaded | "
        f"Shape: {df.shape}"
    )

    # ==================================================
    # RUN VALIDATION
    # ==================================================

    validator = ValidatorManager(
        df=df,
        dataset_name=dataset_name
    )

    validation_report = validator.run()

    # ==================================================
    # FINAL STATUS
    # ==================================================

    logger.info(
        f"{dataset_name} | "
        "Processed data validation completed."
    )

    return (
        df,
        validation_report
    )