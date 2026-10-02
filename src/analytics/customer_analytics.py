"""
Customer Analytics

Provides reusable customer-level business analytics
from the MySQL fact_sales and dim_customer tables.
"""

from src.config.logging_config import get_logger
from src.infrastructure.db_connection import get_connection


class CustomerAnalytics:

    def __init__(self):
        self.logger = get_logger("CustomerAnalytics")

    # ========================================================
    # 1. TOP 10 CUSTOMERS BY SALES
    # ========================================================

    def get_top_customers_by_sales(self):

        query = """
            SELECT
                c.customer_id,
                c.customer_name,
                c.segment,
                SUM(f.sales) AS total_sales,
                SUM(f.profit) AS total_profit,
                COUNT(DISTINCT f.order_id) AS total_orders,
                SUM(f.profit) / NULLIF(SUM(f.sales), 0)
                    AS profit_margin
            FROM fact_sales f
            JOIN dim_customer c
                ON f.customer_key = c.customer_key
            GROUP BY
                c.customer_id,
                c.customer_name,
                c.segment
            ORDER BY total_sales DESC
            LIMIT 10;
        """

        return self._execute_query(query)

    # ========================================================
    # 2. TOP 10 CUSTOMERS BY PROFIT
    # ========================================================

    def get_top_customers_by_profit(self):

        query = """
            SELECT
                c.customer_id,
                c.customer_name,
                c.segment,
                SUM(f.profit) AS total_profit,
                SUM(f.sales) AS total_sales,
                COUNT(DISTINCT f.order_id) AS total_orders,
                SUM(f.profit) / NULLIF(SUM(f.sales), 0)
                    AS profit_margin
            FROM fact_sales f
            JOIN dim_customer c
                ON f.customer_key = c.customer_key
            GROUP BY
                c.customer_id,
                c.customer_name,
                c.segment
            ORDER BY total_profit DESC
            LIMIT 10;
        """

        return self._execute_query(query)

    # ========================================================
    # 3. SALES AND PROFIT BY CUSTOMER SEGMENT
    # ========================================================

    def get_sales_by_segment(self):

        query = """
            SELECT
                c.segment,
                COUNT(DISTINCT f.order_id) AS total_orders,
                SUM(f.sales) AS total_sales,
                SUM(f.profit) AS total_profit,
                SUM(f.quantity) AS total_quantity,
                SUM(f.profit) / NULLIF(SUM(f.sales), 0)
                    AS profit_margin
            FROM fact_sales f
            JOIN dim_customer c
                ON f.customer_key = c.customer_key
            GROUP BY c.segment
            ORDER BY total_sales DESC;
        """

        return self._execute_query(query)

    # ========================================================
    # 4. CUSTOMERS WITH NEGATIVE PROFIT
    # ========================================================

    def get_negative_profit_customers(self):

        query = """
            SELECT
                c.customer_id,
                c.customer_name,
                c.segment,
                SUM(f.sales) AS total_sales,
                SUM(f.profit) AS total_profit,
                SUM(f.profit) / NULLIF(SUM(f.sales), 0)
                    AS profit_margin
            FROM fact_sales f
            JOIN dim_customer c
                ON f.customer_key = c.customer_key
            GROUP BY
                c.customer_id,
                c.customer_name,
                c.segment
            HAVING SUM(f.profit) < 0
            ORDER BY total_profit ASC;
        """

        return self._execute_query(query)

    # ========================================================
    # 5. HIGH SALES BUT LOW PROFIT CUSTOMERS
    # ========================================================

    def get_high_sales_low_profit_customers(self):

        query = """
            SELECT
                c.customer_id,
                c.customer_name,
                c.segment,
                SUM(f.sales) AS total_sales,
                SUM(f.profit) AS total_profit,
                SUM(f.profit) / NULLIF(SUM(f.sales), 0)
                    AS profit_margin
            FROM fact_sales f
            JOIN dim_customer c
                ON f.customer_key = c.customer_key
            GROUP BY
                c.customer_id,
                c.customer_name,
                c.segment
            HAVING
                SUM(f.sales) > 100000
                AND SUM(f.profit) < 10000
            ORDER BY total_sales DESC;
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
                "Executing customer analytics query."
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
                f"Customer analytics query completed. "
                f"Rows returned: {len(result)}"
            )

            return result

        except Exception as error:

            self.logger.exception(
                f"Customer analytics query failed: {error}"
            )

            raise

        finally:

            if cursor is not None:
                cursor.close()

            if connection is not None:
                connection.close()