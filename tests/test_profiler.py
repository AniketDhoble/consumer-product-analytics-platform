from src.etl.extract import DataImporter

from src.core.profiler.profiler_manager import (
    ProfilerManager
)

from src.core.reports.profiling_report_exporter import (
    ProfilingReportExporter
)


def main():

    # ---------------------------------------------------------
    # LOAD DATA
    # ---------------------------------------------------------

    importer = DataImporter()

    datasets = importer.load_data()

    # ---------------------------------------------------------
    # RUN PROFILER
    # ---------------------------------------------------------

    for dataset_name, df in datasets.items():

        profiler = ProfilerManager(
            df=df,
            dataset_name=dataset_name
        )

        report = profiler.run()

        # -----------------------------------------------------
        # SAVE PROFILING REPORT
        # -----------------------------------------------------

        exporter = ProfilingReportExporter(
            report=report,
            dataset_name=dataset_name
        )

        output_file = exporter.export()

        # -----------------------------------------------------
        # PRINT PROFILING REPORT
        # -----------------------------------------------------

        print("\n")
        print("=" * 70)
        print(f"DATASET: {dataset_name}")
        print("=" * 70)

        for profiler_name, profiler_report in report.items():

            print(f"\n--- {profiler_name} ---")

            for check, result in profiler_report.items():

                print(
                    f"{check}: {result}"
                )

        # -----------------------------------------------------
        # PRINT SAVED FILE LOCATION
        # -----------------------------------------------------

        print("\n")
        print("=" * 70)
        print("PROFILING REPORT SAVED")
        print("=" * 70)

        print(output_file)


if __name__ == "__main__":
    main()