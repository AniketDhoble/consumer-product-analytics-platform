"""
Profiling Report Exporter

Saves the complete profiling report as a JSON file.
"""

import json

from src.config.paths import REPORTS_DIR
from src.config.logging_config import get_logger


class ProfilingReportExporter:

    def __init__(self, report, dataset_name):

        self.report = report
        self.dataset_name = dataset_name

        self.logger = get_logger(
            "ProfilingReportExporter"
        )

        # ====================================================
        # REPORT OUTPUT DIRECTORY
        # ====================================================

        self.output_dir = (
            REPORTS_DIR / "profiling"
        )

        self.output_dir.mkdir(
            parents=True,
            exist_ok=True
        )

    # ========================================================
    # JSON SERIALIZATION
    # ========================================================

    def _make_json_serializable(self, value):

        # Dictionary
        if isinstance(value, dict):

            return {
                str(key): self._make_json_serializable(
                    item
                )
                for key, item in value.items()
            }

        # List / Tuple
        if isinstance(value, (list, tuple)):

            return [
                self._make_json_serializable(
                    item
                )
                for item in value
            ]

        # NumPy / Pandas scalar
        if hasattr(value, "item"):

            try:
                return value.item()

            except Exception:
                pass

        # Datetime / Timestamp
        if hasattr(value, "isoformat"):

            try:
                return value.isoformat()

            except Exception:
                pass

        return value

    # ========================================================
    # EXPORT REPORT
    # ========================================================

    def export(self):

        # Create safe filename
        safe_dataset_name = (
            self.dataset_name
            .replace(" ", "_")
            .replace("/", "_")
            .replace("\\", "_")
        )

        output_file = (
            self.output_dir
            / f"{safe_dataset_name}_profiling_report.json"
        )

        # Convert report to JSON-safe format
        serializable_report = (
            self._make_json_serializable(
                self.report
            )
        )

        # Save JSON
        with open(
            output_file,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                serializable_report,
                file,
                indent=4,
                ensure_ascii=False
            )

        self.logger.info(
            f"Profiling report saved successfully: "
            f"{output_file}"
        )

        return output_file