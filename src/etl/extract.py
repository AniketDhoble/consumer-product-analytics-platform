"""
Data extraction module.

Responsible for:
    - Validating the raw data folder
    - Finding CSV files
    - Loading CSV files into pandas DataFrames
    - Logging successful operations
    - Logging errors
"""

from pathlib import Path

import pandas as pd

from src.config.paths import RAW_DATA_DIR
from src.config.logging_config import get_logger


class DataImporter:
    """
    Import CSV datasets from the raw data folder.
    """

    def __init__(self, folder_path=None):
        """
        Initialize the DataImporter.

        Parameters
        ----------
        folder_path : Path, optional
            Path to the raw dataset folder.
            Defaults to datasets/raw/.
        """

        self.folder_path = Path(
            folder_path or RAW_DATA_DIR
        )

        self.datasets = {}

        # Create project logger
        self.logger = get_logger(
            "DataImporter"
        )

    # ========================================================
    # FOLDER VALIDATION
    # ========================================================

    def validate_folder(self):
        """
        Validate that the dataset folder exists.
        """

        if not self.folder_path.exists():

            self.logger.error(
                f"Dataset folder not found: "
                f"{self.folder_path}"
            )

            raise FileNotFoundError(
                f"Dataset folder not found: "
                f"{self.folder_path}"
            )

        if not self.folder_path.is_dir():

            self.logger.error(
                f"Dataset path is not a directory: "
                f"{self.folder_path}"
            )

            raise NotADirectoryError(
                f"Dataset path is not a directory: "
                f"{self.folder_path}"
            )

        self.logger.info(
            f"Dataset folder validated successfully: "
            f"{self.folder_path}"
        )

        return True

    # ========================================================
    # FIND CSV FILES
    # ========================================================

    def get_csv_files(self):
        """
        Return all CSV files from the raw data folder.
        """

        self.validate_folder()

        csv_files = sorted(
            self.folder_path.glob("*.csv")
        )

        if not csv_files:

            self.logger.error(
                "No CSV files found in the raw data folder."
            )

            raise FileNotFoundError(
                "No CSV files found in the raw data folder."
            )

        self.logger.info(
            f"{len(csv_files)} CSV file(s) found."
        )

        for file in csv_files:

            self.logger.info(
                f"CSV file detected: {file.name}"
            )

        return csv_files

    # ========================================================
    # LOAD DATA
    # ========================================================

    def load_data(self):
        """
        Load all CSV files into pandas DataFrames.

        Returns
        -------
        dict
            Dictionary containing dataset names and DataFrames.
        """

        self.logger.info(
            "Data loading process started."
        )

        csv_files = self.get_csv_files()

        for file_path in csv_files:

            try:

                df = pd.read_csv(
                    file_path
                )

                dataset_name = file_path.stem

                self.datasets[dataset_name] = df

                self.logger.info(
                    f"{file_path.name} loaded successfully | "
                    f"Rows: {df.shape[0]} | "
                    f"Columns: {df.shape[1]}"
                )

                self.logger.info(
                    f"Dataset stored as: {dataset_name}"
                )

            except Exception:

                self.logger.exception(
                    f"Failed to load dataset: "
                    f"{file_path.name}"
                )

        if not self.datasets:

            self.logger.error(
                "No datasets were loaded successfully."
            )

            raise RuntimeError(
                "No datasets were loaded successfully."
            )

        self.logger.info(
            f"Data loading process completed | "
            f"Datasets loaded: {len(self.datasets)}"
        )

        return self.datasets

    # ========================================================
    # GET DATASET
    # ========================================================

    def get_dataset(self, name):
        """
        Return a dataset by its name.
        """

        if name not in self.datasets:

            self.logger.error(
                f"Dataset not found: {name}"
            )

            raise KeyError(
                f"Dataset '{name}' not found."
            )

        self.logger.info(
            f"Dataset retrieved successfully: {name}"
        )

        return self.datasets[name]