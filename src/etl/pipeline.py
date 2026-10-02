"""
Main ETL Pipeline

Pipeline flow:

1. Extract raw CSV data
2. Clean data
3. Transform data
4. Validate processed data
5. Load data into MySQL
"""

from src.config.logging_config import get_logger

from src.etl.extract import DataImporter
from src.etl.clean_data import clean_data
from src.etl.transform_data import DataTransformer
from src.etl.validate_data import validate_data
from src.etl.load_mysql import MySQLLoader


class ETLPipeline:

    def __init__(self, dataset_name):

        self.dataset_name = dataset_name

        self.logger = get_logger(
            "ETLPipeline"
        )

    # ========================================================
    # RUN PIPELINE
    # ========================================================

    def run(self):

        self.logger.info(
            "=" * 70
        )

        self.logger.info(
            f"{self.dataset_name} | "
            "ETL pipeline started."
        )

        self.logger.info(
            "=" * 70
        )

        try:

            # =================================================
            # STEP 1 — EXTRACT
            # =================================================

            self.logger.info(
                f"{self.dataset_name} | "
                "STEP 1/5 | Extraction started."
            )

            importer = DataImporter()

            datasets = importer.load_data()

            if self.dataset_name not in datasets:

                raise KeyError(
                    f"Dataset '{self.dataset_name}' "
                    "was not found in extracted datasets."
                )

            df = importer.get_dataset(
                self.dataset_name
            )

            self.logger.info(
                f"{self.dataset_name} | "
                "STEP 1/5 | Extraction completed."
            )

            # =================================================
            # STEP 2 — CLEAN
            # =================================================

            self.logger.info(
                f"{self.dataset_name} | "
                "STEP 2/5 | Cleaning started."
            )

            cleaned_df, cleaning_report, cleaned_file = (
                clean_data(
                    df=df,
                    dataset_name=self.dataset_name
                )
            )

            self.logger.info(
                f"{self.dataset_name} | "
                "STEP 2/5 | Cleaning completed."
            )

            # =================================================
            # STEP 3 — TRANSFORM
            # =================================================

            self.logger.info(
                f"{self.dataset_name} | "
                "STEP 3/5 | Transformation started."
            )

            transformer = DataTransformer(
                dataset_name=self.dataset_name
            )

            processed_df, transformations, processed_file = (
                transformer.run()
            )

            self.logger.info(
                f"{self.dataset_name} | "
                "STEP 3/5 | Transformation completed."
            )

            # =================================================
            # STEP 4 — VALIDATE
            # =================================================

            self.logger.info(
                f"{self.dataset_name} | "
                "STEP 4/5 | Processed data validation started."
            )

            validated_df, validation_report = (
                validate_data(
                    dataset_name=self.dataset_name
                )
            )

            self.logger.info(
                f"{self.dataset_name} | "
                "STEP 4/5 | Processed data validation completed."
            )

            # =================================================
            # STEP 5 — LOAD MYSQL
            # =================================================

            self.logger.info(
                f"{self.dataset_name} | "
                "STEP 5/5 | MySQL loading started."
            )

            loader = MySQLLoader(
                dataset_name=self.dataset_name
            )

            loader.run()

            self.logger.info(
                f"{self.dataset_name} | "
                "STEP 5/5 | MySQL loading completed."
            )

            # =================================================
            # PIPELINE SUCCESS
            # =================================================

            self.logger.info(
                "=" * 70
            )

            self.logger.info(
                f"{self.dataset_name} | "
                "ETL pipeline completed successfully."
            )

            self.logger.info(
                "=" * 70
            )

            return {
                "dataset_name": self.dataset_name,
                "status": "SUCCESS",
                "rows_extracted": len(df),
                "rows_cleaned": len(cleaned_df),
                "rows_processed": len(processed_df),
                "rows_validated": len(validated_df),
                "cleaned_file": str(cleaned_file),
                "processed_file": str(processed_file),
                "cleaning_report": cleaning_report,
                "transformations": transformations,
                "validation_report": validation_report
            }

        except Exception as error:

            self.logger.exception(
                f"{self.dataset_name} | "
                f"ETL pipeline failed: {error}"
            )

            raise