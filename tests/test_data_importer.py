from src.etl.extract import DataImporter


def main():

    importer = DataImporter()

    datasets = importer.load_data()

    print("\nDatasets loaded:")
    
    for name, df in datasets.items():

        print(
            f"{name} | "
            f"Rows: {df.shape[0]} | "
            f"Columns: {df.shape[1]}"
        )


if __name__ == "__main__":
    main()