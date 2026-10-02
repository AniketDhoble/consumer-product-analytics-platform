from src.etl.transform_data import (
    DataTransformer
)

from src.etl.extract import DataImporter


def main():

    importer = DataImporter()

    datasets = importer.load_data()

    for dataset_name in datasets:

        print("\n")
        print("=" * 70)
        print("TRANSFORMER TEST")
        print("=" * 70)

        transformer = DataTransformer(
            dataset_name=dataset_name
        )

        transformed_df, transformation_report, output_file = (
            transformer.run()
        )

        # ==================================================
        # SHAPE
        # ==================================================

        print("\n")
        print("=" * 70)
        print("DATASET SHAPE")
        print("=" * 70)

        print(
            f"Processed: {transformed_df.shape}"
        )

        # ==================================================
        # CHECK PROFIT MARGIN
        # ==================================================

        print("\n")
        print("=" * 70)
        print("TRANSFORMATION CHECK")
        print("=" * 70)

        assert "Profit Margin" in transformed_df.columns

        print(
            "Profit Margin column : PASS"
        )

        # ==================================================
        # CHECK VALUES
        # ==================================================

        assert (
            transformed_df["Profit Margin"]
            .notna()
            .all()
        )

        print(
            "Profit Margin values : PASS"
        )

        # ==================================================
        # TRANSFORMATION REPORT
        # ==================================================

        print("\n")
        print("=" * 70)
        print("TRANSFORMATION REPORT")
        print("=" * 70)

        for name, description in (
            transformation_report.items()
        ):

            print(
                f"{name}: {description}"
            )

        # ==================================================
        # OUTPUT FILE
        # ==================================================

        print("\n")
        print("=" * 70)
        print("PROCESSED DATASET SAVED")
        print("=" * 70)

        print(output_file)

        # ==================================================
        # FINAL
        # ==================================================

        print("\n")
        print("=" * 70)
        print("ALL TRANSFORMER TESTS PASSED")
        print("=" * 70)


if __name__ == "__main__":
    main()