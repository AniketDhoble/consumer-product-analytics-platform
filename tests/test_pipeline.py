"""
Test complete ETL pipeline.
"""

import sys
from pathlib import Path

# Add project root to Python path
PROJECT_ROOT = Path(__file__).resolve().parents[1]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.etl.pipeline import ETLPipeline


DATASET_NAME = "store_sales_data (2)"


def test_etl_pipeline():

    pipeline = ETLPipeline(dataset_name=DATASET_NAME)

    result = pipeline.run()

    assert result["status"] == "SUCCESS"

    assert result["rows_extracted"] == 100000
    assert result["rows_cleaned"] == 100000
    assert result["rows_processed"] == 100000
    assert result["rows_validated"] == 100000


if __name__ == "__main__":
    test_etl_pipeline()
    print("ETL pipeline test passed successfully.")