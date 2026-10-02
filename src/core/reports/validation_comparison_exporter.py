"""
Validation Comparison Report Exporter

Saves the Before vs After validation comparison
as a CSV file.
"""

from src.config.paths import REPORTS_DIR
from src.config.logging_config import get_logger


class ValidationComparisonExporter:

    def __init__(
        self,
        comparison_df,
        dataset_name
    ):

        self.comparison_df = comparison_df
        self.dataset_name = dataset_name

        self.logger = get_logger(
            "ValidationComparisonExporter"
        )

        # ====================================================
        # OUTPUT DIRECTORY
        # ====================================================

        self.output_dir = (
            REPORTS_DIR / "comparison"
        )

        self.output_dir.mkdir(
            parents=True,
            exist_ok=True
        )

    # ========================================================
    # EXPORT
    # ========================================================

    def export(self):

        safe_dataset_name = (
            self.dataset_name
            .replace(" ", "_")
            .replace("/", "_")
            .replace("\\", "_")
        )

        output_file = (
            self.output_dir
            / f"{safe_dataset_name}_validation_comparison.csv"
        )

        self.comparison_df.to_csv(
            output_file,
            index=False,
            encoding="utf-8"
        )

        self.logger.info(
            f"Validation comparison saved successfully: "
            f"{output_file}"
        )

        return output_file