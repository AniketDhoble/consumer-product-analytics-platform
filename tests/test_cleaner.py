from src.etl.extract import DataImporter

from src.etl.clean_data import (
    clean_data
)


def main():

    importer = DataImporter()

    datasets = importer.load_data()

    for dataset_name, df in datasets.items():

        print("\n")
        print("=" * 70)
        print("CLEAN DATA ETL TEST")
        print("=" * 70)

        # ==================================================
        # RUN CLEANING
        # ==================================================

        cleaned_df, cleaning_report, output_file = (
            clean_data(
                df=df,
                dataset_name=dataset_name
            )
        )

        # ==================================================
        # DATASET SHAPE
        # ==================================================

        print("\n")
        print("=" * 70)
        print("DATASET SHAPE")
        print("=" * 70)

        print(f"Before: {df.shape}")
        print(f"After : {cleaned_df.shape}")

        # ==================================================
        # CHECK ORDER YEAR
        # ==================================================

        print("\n")
        print("=" * 70)
        print("CLEANING CHECK")
        print("=" * 70)

        if "Order Year" in cleaned_df.columns:
            print("Order Year: PASS")
        else:
            print("Order Year: FAIL")

        # ==================================================
        # CHECK SAVED FILE
        # ==================================================

        print("\n")
        print("=" * 70)
        print("CLEANED DATASET")
        print("=" * 70)

        print(
            f"Saved to: {output_file}"
        )

        # ==================================================
        # CLEANING REPORT
        # ==================================================

        print("\n")
        print("=" * 70)
        print("CLEANING REPORT")
        print("=" * 70)

        for cleaner, changes in cleaning_report.items():

            print(f"\n--- {cleaner} ---")

            for check, result in changes.items():

                print(
                    f"{check}: {result}"
                )


if __name__ == "__main__":
    main()