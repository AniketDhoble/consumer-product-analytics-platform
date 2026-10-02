"""
Test MySQL data loader.
"""

import pymysql

from src.etl.load_mysql import MySQLLoader
from src.config.database_config import (
    DB_HOST,
    DB_PORT,
    DB_NAME,
    DB_USER,
    DB_PASSWORD,
    DB_CHARSET,
    DB_CONNECT_TIMEOUT
)


DATASET_NAME = "store_sales_data (2)"


def get_connection():

    return pymysql.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        charset=DB_CHARSET,
        connect_timeout=DB_CONNECT_TIMEOUT
    )


def clear_tables(connection):

    with connection.cursor() as cursor:

        cursor.execute(
            "SET FOREIGN_KEY_CHECKS = 0"
        )

        cursor.execute(
            "TRUNCATE TABLE fact_sales"
        )

        cursor.execute(
            "TRUNCATE TABLE dim_location"
        )

        cursor.execute(
            "TRUNCATE TABLE dim_date"
        )

        cursor.execute(
            "TRUNCATE TABLE dim_product"
        )

        cursor.execute(
            "TRUNCATE TABLE dim_customer"
        )

        cursor.execute(
            "SET FOREIGN_KEY_CHECKS = 1"
        )

    connection.commit()


def test_mysql_loader():

    # --------------------------------------------------------
    # Connect to database
    # --------------------------------------------------------

    connection = get_connection()

    try:

        # ----------------------------------------------------
        # Start with clean tables
        # ----------------------------------------------------

        clear_tables(connection)

    finally:

        connection.close()

    # --------------------------------------------------------
    # Run loader
    # --------------------------------------------------------

    loader = MySQLLoader(
        dataset_name=DATASET_NAME
    )

    loader.run()

    # --------------------------------------------------------
    # Verify database
    # --------------------------------------------------------

    connection = get_connection()

    try:

        with connection.cursor() as cursor:

            # --------------------------------------------
            # Customer count
            # --------------------------------------------

            cursor.execute(
                "SELECT COUNT(*) FROM dim_customer"
            )

            customer_count = cursor.fetchone()[0]

            assert customer_count == 100000

            # --------------------------------------------
            # Product count
            # --------------------------------------------

            cursor.execute(
                "SELECT COUNT(*) FROM dim_product"
            )

            product_count = cursor.fetchone()[0]

            assert product_count == 100000

            # --------------------------------------------
            # Date count
            # --------------------------------------------

            cursor.execute(
                "SELECT COUNT(*) FROM dim_date"
            )

            date_count = cursor.fetchone()[0]

            assert date_count == 1833

            # --------------------------------------------
            # Location count
            # --------------------------------------------

            cursor.execute(
                "SELECT COUNT(*) FROM dim_location"
            )

            location_count = cursor.fetchone()[0]

            assert location_count == 360

            # --------------------------------------------
            # Fact count
            # --------------------------------------------

            cursor.execute(
                "SELECT COUNT(*) FROM fact_sales"
            )

            fact_count = cursor.fetchone()[0]

            assert fact_count == 100000

    finally:

        connection.close()