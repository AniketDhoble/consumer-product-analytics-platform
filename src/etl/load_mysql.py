"""
MySQL Loading Step

Loads the processed dataset into the MySQL star schema.

Load order:
    1. dim_customer
    2. dim_product
    3. dim_date
    4. dim_location
    5. fact_sales

Before loading:
    - Existing analytical data is cleared.
    - Tables are reloaded from the processed dataset.

This makes the ETL pipeline re-runnable.
"""

import pandas as pd
import pymysql

from src.config.paths import PROCESSED_DATA_DIR
from src.config.database_config import (
    DB_HOST,
    DB_PORT,
    DB_NAME,
    DB_USER,
    DB_PASSWORD,
    DB_CHARSET,
    DB_CONNECT_TIMEOUT
)
from src.config.logging_config import get_logger


class MySQLLoader:

    def __init__(self, dataset_name):

        self.dataset_name = dataset_name

        self.logger = get_logger(
            "MySQLLoader"
        )

        safe_dataset_name = (
            dataset_name
            .replace(" ", "_")
            .replace("/", "_")
            .replace("\\", "_")
        )

        self.input_file = (
            PROCESSED_DATA_DIR
            / f"{safe_dataset_name}_processed.csv"
        )

        self.connection = None

    # ========================================================
    # DATABASE CONNECTION
    # ========================================================

    def connect(self):

        self.logger.info(
            "Connecting to MySQL database."
        )

        self.connection = pymysql.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME,
            charset=DB_CHARSET,
            connect_timeout=DB_CONNECT_TIMEOUT
        )

        self.logger.info(
            "MySQL connection established."
        )

    # ========================================================
    # CLEAR EXISTING DATA
    # ========================================================

    def clear_tables(self):

        self.logger.info(
            "Clearing existing MySQL tables before reload."
        )

        statements = [
            "SET FOREIGN_KEY_CHECKS = 0",
            "TRUNCATE TABLE fact_sales",
            "TRUNCATE TABLE dim_customer",
            "TRUNCATE TABLE dim_product",
            "TRUNCATE TABLE dim_date",
            "TRUNCATE TABLE dim_location",
            "SET FOREIGN_KEY_CHECKS = 1"
        ]

        with self.connection.cursor() as cursor:

            for statement in statements:
                cursor.execute(statement)

        self.logger.info(
            "Existing MySQL data cleared successfully."
        )

    # ========================================================
    # LOAD PROCESSED DATA
    # ========================================================

    def load_data(self):

        if not self.input_file.exists():

            self.logger.error(
                f"Processed dataset not found: "
                f"{self.input_file}"
            )

            raise FileNotFoundError(
                f"Processed dataset not found: "
                f"{self.input_file}"
            )

        self.logger.info(
            f"Loading processed dataset: "
            f"{self.input_file}"
        )

        df = pd.read_csv(
            self.input_file
        )

        self.logger.info(
            f"Processed dataset loaded | "
            f"Rows: {len(df)} | "
            f"Columns: {len(df.columns)}"
        )

        return df

    # ========================================================
    # LOAD CUSTOMER DIMENSION
    # ========================================================

    def load_customers(self, df):

        self.logger.info(
            "Loading dim_customer."
        )

        customer_df = (
            df[
                [
                    "Customer ID",
                    "Customer Name",
                    "Last Name",
                    "Date of Birth",
                    "Segment"
                ]
            ]
            .drop_duplicates(
                subset=["Customer ID"]
            )
        )

        query = """
            INSERT INTO dim_customer
            (
                customer_id,
                customer_name,
                last_name,
                date_of_birth,
                segment
            )
            VALUES (%s, %s, %s, %s, %s)
        """

        data = list(
            customer_df.itertuples(
                index=False,
                name=None
            )
        )

        with self.connection.cursor() as cursor:

            cursor.executemany(
                query,
                data
            )

        self.logger.info(
            f"dim_customer loaded | "
            f"Rows: {len(data)}"
        )

    # ========================================================
    # LOAD PRODUCT DIMENSION
    # ========================================================

    def load_products(self, df):

        self.logger.info(
            "Loading dim_product."
        )

        product_df = (
            df[
                [
                    "Product ID",
                    "Product Name",
                    "Category of Goods",
                    "Sub-Category"
                ]
            ]
            .drop_duplicates(
                subset=["Product ID"]
            )
        )

        query = """
            INSERT INTO dim_product
            (
                product_id,
                product_name,
                category_of_goods,
                sub_category
            )
            VALUES (%s, %s, %s, %s)
        """

        data = list(
            product_df.itertuples(
                index=False,
                name=None
            )
        )

        with self.connection.cursor() as cursor:

            cursor.executemany(
                query,
                data
            )

        self.logger.info(
            f"dim_product loaded | "
            f"Rows: {len(data)}"
        )

    # ========================================================
    # LOAD DATE DIMENSION
    # ========================================================

    def load_dates(self, df):

        self.logger.info(
            "Loading dim_date."
        )

        date_columns = [
            "Order Date",
            "Sales Date",
            "Ship Date"
        ]

        dates = (
            pd.concat(
                [
                    pd.to_datetime(
                        df[column],
                        errors="coerce"
                    )
                    for column in date_columns
                ]
            )
            .dropna()
            .drop_duplicates()
            .sort_values()
        )

        query = """
            INSERT INTO dim_date
            (
                date_key,
                full_date,
                year,
                month,
                month_name,
                quarter,
                day,
                day_name
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """

        data = [
            (
                int(date_value.strftime("%Y%m%d")),
                date_value.date(),
                int(date_value.year),
                int(date_value.month),
                date_value.strftime("%B"),
                int(date_value.quarter),
                int(date_value.day),
                date_value.strftime("%A")
            )
            for date_value in dates
        ]

        with self.connection.cursor() as cursor:

            cursor.executemany(
                query,
                data
            )

        self.logger.info(
            f"dim_date loaded | "
            f"Rows: {len(data)}"
        )

    # ========================================================
    # LOAD LOCATION DIMENSION
    # ========================================================

    def load_locations(self, df):

        self.logger.info(
            "Loading dim_location."
        )

        location_columns = [
            "Country",
            "Region",
            "State",
            "City Type",
            "Outlet Type",
            "Postal Code"
        ]

        location_df = (
            df[
                location_columns
            ]
            .drop_duplicates()
        )

        query = """
            INSERT INTO dim_location
            (
                country,
                region,
                state,
                city_type,
                outlet_type,
                postal_code
            )
            VALUES (%s, %s, %s, %s, %s, %s)
        """

        data = list(
            location_df.itertuples(
                index=False,
                name=None
            )
        )

        with self.connection.cursor() as cursor:

            cursor.executemany(
                query,
                data
            )

        self.logger.info(
            f"dim_location loaded | "
            f"Rows: {len(data)}"
        )

    # ========================================================
    # LOAD FACT TABLE
    # ========================================================

    def load_fact_sales(self, df):

        self.logger.info(
            "Preparing fact_sales."
        )

        # ----------------------------------------------------
        # Retrieve dimension keys
        # ----------------------------------------------------

        with self.connection.cursor() as cursor:

            cursor.execute(
                """
                SELECT
                    customer_key,
                    customer_id
                FROM dim_customer
                """
            )

            customer_rows = cursor.fetchall()

            cursor.execute(
                """
                SELECT
                    product_key,
                    product_id
                FROM dim_product
                """
            )

            product_rows = cursor.fetchall()

            cursor.execute(
                """
                SELECT
                    date_key,
                    full_date
                FROM dim_date
                """
            )

            date_rows = cursor.fetchall()

            cursor.execute(
                """
                SELECT
                    location_key,
                    country,
                    region,
                    state,
                    city_type,
                    outlet_type,
                    postal_code
                FROM dim_location
                """
            )

            location_rows = cursor.fetchall()

        customer_map = {
            row[1]: row[0]
            for row in customer_rows
        }

        product_map = {
            row[1]: row[0]
            for row in product_rows
        }

        date_map = {
            pd.Timestamp(row[1]).date(): row[0]
            for row in date_rows
        }

        location_map = {
            (
                row[1],
                row[2],
                row[3],
                row[4],
                row[5],
                row[6]
            ): row[0]
            for row in location_rows
        }

        self.logger.info(
            "Dimension key mappings created."
        )

        # ----------------------------------------------------
        # Prepare date columns once
        # ----------------------------------------------------

        df = df.copy()

        df["Order Date"] = pd.to_datetime(
            df["Order Date"]
        ).dt.date

        df["Sales Date"] = pd.to_datetime(
            df["Sales Date"]
        ).dt.date

        df["Ship Date"] = pd.to_datetime(
            df["Ship Date"]
        ).dt.date

        # ----------------------------------------------------
        # Prepare fact data
        # ----------------------------------------------------

        fact_columns = [
            "Order ID",
            "Customer ID",
            "Product ID",
            "Order Date",
            "Sales Date",
            "Ship Date",
            "Country",
            "Region",
            "State",
            "City Type",
            "Outlet Type",
            "Postal Code",
            "Ship Mode",
            "Sales",
            "Quantity",
            "Discount",
            "Profit",
            "Profit Margin"
        ]

        fact_df = df[fact_columns].copy()

        # ----------------------------------------------------
        # Map dimension keys
        # ----------------------------------------------------

        fact_df["customer_key"] = (
            fact_df["Customer ID"]
            .map(customer_map)
        )

        fact_df["product_key"] = (
            fact_df["Product ID"]
            .map(product_map)
        )

        fact_df["order_date_key"] = (
            fact_df["Order Date"]
            .map(date_map)
        )

        fact_df["sales_date_key"] = (
            fact_df["Sales Date"]
            .map(date_map)
        )

        fact_df["ship_date_key"] = (
            fact_df["Ship Date"]
            .map(date_map)
        )

        location_keys = (
            fact_df[
                [
                    "Country",
                    "Region",
                    "State",
                    "City Type",
                    "Outlet Type",
                    "Postal Code"
                ]
            ]
            .apply(
                tuple,
                axis=1
            )
            .map(location_map)
        )

        fact_df["location_key"] = location_keys

        # ----------------------------------------------------
        # Validate dimension mappings
        # ----------------------------------------------------

        mapping_columns = [
            "customer_key",
            "product_key",
            "order_date_key",
            "sales_date_key",
            "ship_date_key",
            "location_key"
        ]

        missing_mappings = (
            fact_df[mapping_columns]
            .isna()
            .sum()
            .sum()
        )

        if missing_mappings > 0:

            raise ValueError(
                "Dimension mapping failed. "
                f"Missing mappings: {missing_mappings}"
            )

        # ----------------------------------------------------
        # Build tuples for MySQL
        # ----------------------------------------------------

        fact_data = list(
            fact_df[
                [
                    "Order ID",
                    "customer_key",
                    "product_key",
                    "order_date_key",
                    "sales_date_key",
                    "ship_date_key",
                    "location_key",
                    "Ship Mode",
                    "Sales",
                    "Quantity",
                    "Discount",
                    "Profit",
                    "Profit Margin"
                ]
            ]
            .itertuples(
                index=False,
                name=None
            )
        )

        # ----------------------------------------------------
        # Insert fact rows
        # ----------------------------------------------------

        query = """
            INSERT INTO fact_sales
            (
                order_id,
                customer_key,
                product_key,
                order_date_key,
                sales_date_key,
                ship_date_key,
                location_key,
                ship_mode,
                sales,
                quantity,
                discount,
                profit,
                profit_margin
            )
            VALUES
            (
                %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s,
                %s, %s, %s
            )
        """

        with self.connection.cursor() as cursor:

            cursor.executemany(
                query,
                fact_data
            )

        self.logger.info(
            f"fact_sales loaded | "
            f"Rows: {len(fact_data)}"
        )

    # ========================================================
    # RUN LOADER
    # ========================================================

    def run(self):

        self.logger.info(
            f"{self.dataset_name} | "
            "MySQL loading started."
        )

        try:

            self.connect()

            # Clear existing data so the loader
            # can safely run multiple times.
            self.clear_tables()

            df = self.load_data()

            self.load_customers(df)

            self.load_products(df)

            self.load_dates(df)

            self.load_locations(df)

            self.load_fact_sales(df)

            self.connection.commit()

            self.logger.info(
                f"{self.dataset_name} | "
                "MySQL loading completed successfully."
            )

        except Exception as error:

            if self.connection:

                self.connection.rollback()

            self.logger.exception(
                f"{self.dataset_name} | "
                f"MySQL loading failed: {error}"
            )

            raise

        finally:

            if self.connection:

                self.connection.close()

                self.logger.info(
                    "MySQL connection closed."
                )