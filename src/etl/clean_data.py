"""
ETL Cleaning Step

Cleans the raw dataset and saves the cleaned
dataset into the interim data directory.
"""

from src.core.cleaner.cleaner_manager import (
    CleanerManager
)

from src.config.paths import (
    INTERIM_DATA_DIR
)

from src.config.logging_config import (
    get_logger
)


def clean_data(df, dataset_name):

    logger = get_logger(
        "ETLCleanData"
    )

    # ==================================================
    # RUN CLEANING
    # ==================================================

    logger.info(
        f"{dataset_name} | "
        "ETL cleaning started."
    )

    cleaner = CleanerManager(
        df=df,
        dataset_name=dataset_name
    )

    cleaned_df, cleaning_report = (
        cleaner.run()
    )

    # ==================================================
    # CREATE INTERIM DIRECTORY
    # ==================================================

    INTERIM_DATA_DIR.mkdir(
        parents=True,
        exist_ok=True
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

    output_file = (
        INTERIM_DATA_DIR
        / f"{safe_dataset_name}_cleaned.csv"
    )

    # ==================================================
    # SAVE CLEANED DATA
    # ==================================================

    cleaned_df.to_csv(
        output_file,
        index=False,
        encoding="utf-8"
    )

    logger.info(
        f"{dataset_name} | "
        f"Cleaned dataset saved: {output_file}"
    )

    logger.info(
        f"{dataset_name} | "
        f"Cleaned dataset shape: {cleaned_df.shape}"
    )

    # ==================================================
    # RETURN RESULTS
    # ==================================================

    return (
        cleaned_df,
        cleaning_report,
        output_file
    )