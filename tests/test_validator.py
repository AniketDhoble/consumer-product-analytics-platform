from src.etl.validate_data import (
    validate_data
)


def main():

    dataset_name = "store_sales_data (2)"

    print("\n")
    print("=" * 70)
    print("PROCESSED DATA VALIDATION TEST")
    print("=" * 70)

    # ==================================================
    # RUN VALIDATION
    # ==================================================

    df, validation_report = (
        validate_data(
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

    print(
        f"Processed data: {df.shape}"
    )

    # ==================================================
    # VALIDATION REPORT
    # ==================================================

    print("\n")
    print("=" * 70)
    print("VALIDATION RESULTS")
    print("=" * 70)

    for category, results in (
        validation_report.items()
    ):

        print(f"\n--- {category} ---")

        for check, result in results.items():

            print(
                f"{check}: {result}"
            )

    # ==================================================
    # PROFIT MARGIN CHECK
    # ==================================================

    assert "Profit Margin" in df.columns

    print("\n")
    print(
        "Profit Margin column : PASS"
    )

    # ==================================================
    # FINAL
    # ==================================================

    print("\n")
    print("=" * 70)
    print("PROCESSED DATA VALIDATION COMPLETED")
    print("=" * 70)


if __name__ == "__main__":
    main()