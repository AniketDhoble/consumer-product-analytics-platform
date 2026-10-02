"""
Sales Analytics

Provides reusable business-level sales analytics
from the MySQL fact_sales and dim_date tables.
"""

from src.config.logging_config import get_logger
from src.infrastructure.db_connection import get_connection


class SalesAnalytics:

    def __init__(self):
        self.logger = get_logger("SalesAnalytics")

    # ========================================================
    # 1. OVERALL SALES PERFORMANCE
    # ========================================================

    def get_overall_sales(self):

        query = """
            SELECT
                COUNT(DISTINCT order_id) AS total_orders,
                SUM(sales) AS total_sales,
                SUM(profit) AS total_profit,
                SUM(quantity) AS total_quantity,
                SUM(profit) / NULLIF(SUM(sales), 0)
                    AS profit_margin
            FROM fact_sales;
        """

        return self._execute_query(query)

    # ========================================================
    # 2. SALES BY YEAR
    # ========================================================

    def get_sales_by_year(self):

        query = """
            SELECT
                d.year,
                COUNT(DISTINCT f.order_id) AS total_orders,
                SUM(f.sales) AS total_sales,
                SUM(f.profit) AS total_profit,
                SUM(f.profit) / NULLIF(SUM(f.sales), 0)
                    AS profit_margin
            FROM fact_sales f
            JOIN dim_date d
                ON f.order_date_key = d.date_key
            GROUP BY d.year
            ORDER BY d.year;
        """

        return self._execute_query(query)

    # ========================================================
    # 3. MONTHLY SALES PERFORMANCE
    # ========================================================

    def get_monthly_sales(self):

        query = """
            SELECT
                d.year,
                d.month,
                d.month_name,
                COUNT(DISTINCT f.order_id) AS total_orders,
                SUM(f.sales) AS total_sales,
                SUM(f.profit) AS total_profit,
                SUM(f.profit) / NULLIF(SUM(f.sales), 0)
                    AS profit_margin
            FROM fact_sales f
            JOIN dim_date d
                ON f.order_date_key = d.date_key
            GROUP BY
                d.year,
                d.month,
                d.month_name
            ORDER BY
                d.year,
                d.month;
        """

        return self._execute_query(query)

    # ========================================================
    # 4. TOP 10 ORDERS BY SALES
    # ========================================================

    def get_top_orders_by_sales(self):

        query = """
            SELECT
                order_id,
                sales,
                profit,
                quantity,
                discount,
                profit_margin
            FROM fact_sales
            ORDER BY sales DESC
            LIMIT 10;
        """

        return self._execute_query(query)

    # ========================================================
    # 5. TOP 10 ORDERS BY PROFIT
    # ========================================================

    def get_top_orders_by_profit(self):

        query = """
            SELECT
                order_id,
                sales,
                profit,
                quantity,
                discount,
                profit_margin
            FROM fact_sales
            ORDER BY profit DESC
            LIMIT 10;
        """

        return self._execute_query(query)

    # ========================================================
    # INTERNAL QUERY EXECUTOR
    # ========================================================

    def _execute_query(self, query):

        connection = None
        cursor = None

        try:

            self.logger.info(
                "Executing sales analytics query."
            )

            connection = get_connection()

            cursor = connection.cursor()

            cursor.execute(query)

            rows = cursor.fetchall()

            columns = [
                column[0]
                for column in cursor.description
            ]

            result = [
                dict(zip(columns, row))
                for row in rows
            ]

            self.logger.info(
                f"Sales analytics query completed. "
                f"Rows returned: {len(result)}"
            )

            return result

        except Exception as error:

            self.logger.exception(
                f"Sales analytics query failed: {error}"
            )

            raise

        finally:

            if cursor is not None:
                cursor.close()

            if connection is not None:
                connection.close()