"""
ETL Transformation Step

Reads the cleaned dataset from the interim directory,
applies analytical transformations, and saves the
processed dataset into the processed directory.
"""

import pandas as pd

from src.config.paths import (
    INTERIM_DATA_DIR,
    PROCESSED_DATA_DIR
)

from src.config.logging_config import (
    get_logger
)


class DataTransformer:

    def __init__(self, dataset_name):

        self.dataset_name = dataset_name

        self.logger = get_logger(
            "DataTransformer"
        )

        self.transformations = {}

        # ==================================================
        # INPUT FILE
        # ==================================================

        safe_dataset_name = (
            dataset_name
            .replace(" ", "_")
            .replace("/", "_")
            .replace("\\", "_")
        )

        self.input_file = (
            INTERIM_DATA_DIR
            / f"{safe_dataset_name}_cleaned.csv"
        )

        # ==================================================
        # OUTPUT FILE
        # ==================================================

        self.output_file = (
            PROCESSED_DATA_DIR
            / f"{safe_dataset_name}_processed.csv"
        )

    # ======================================================
    # LOAD CLEANED DATA
    # ======================================================

    def load_cleaned_data(self):

        if not self.input_file.exists():

            self.logger.error(
                f"Cleaned dataset not found: "
                f"{self.input_file}"
            )

            raise FileNotFoundError(
                f"Cleaned dataset not found: "
                f"{self.input_file}"
            )

        self.df = pd.read_csv(
            self.input_file
        )

        self.logger.info(
            f"{self.dataset_name} | "
            f"Cleaned dataset loaded | "
            f"Shape: {self.df.shape}"
        )

        return self.df

    # ======================================================
    # CREATE PROFIT MARGIN
    # ======================================================

    def create_profit_margin(self):

        required_columns = [
            "Sales",
            "Profit"
        ]

        for column in required_columns:

            if column not in self.df.columns:

                self.logger.error(
                    f"Required column missing: {column}"
                )

                raise KeyError(
                    f"Required column missing: {column}"
                )

        # Avoid division by zero
        self.df["Profit Margin"] = (
            self.df["Profit"]
            / self.df["Sales"]
        )

        self.transformations[
            "Profit Margin"
        ] = "Profit / Sales"

        self.logger.info(
            f"{self.dataset_name} | "
            "Profit Margin created."
        )

    # ======================================================
    # RUN TRANSFORMATION
    # ======================================================

    def run(self):

        self.logger.info(
            f"{self.dataset_name} | "
            "Data transformation started."
        )

        # Load cleaned dataset
        self.load_cleaned_data()

        # Create analytical columns
        self.create_profit_margin()

        # ==================================================
        # CREATE PROCESSED DIRECTORY
        # ==================================================

        PROCESSED_DATA_DIR.mkdir(
            parents=True,
            exist_ok=True
        )

        # ==================================================
        # SAVE PROCESSED DATA
        # ==================================================

        self.df.to_csv(
            self.output_file,
            index=False,
            encoding="utf-8"
        )

        self.logger.info(
            f"{self.dataset_name} | "
            f"Processed dataset saved: "
            f"{self.output_file}"
        )

        self.logger.info(
            f"{self.dataset_name} | "
            f"Processed dataset shape: "
            f"{self.df.shape}"
        )

        self.logger.info(
            f"{self.dataset_name} | "
            "Data transformation completed."
        )

        return (
            self.df,
            self.transformations,
            self.output_file
        )