"""
Advanced Analytics

Provides advanced business analytics using
fact_sales and dim_product tables.
"""

from src.config.logging_config import get_logger
from src.infrastructure.db_connection import get_connection


class AdvancedAnalytics:

    def __init__(self):
        self.logger = get_logger("AdvancedAnalytics")

    # ========================================================
    # 1. CATEGORY WITH HIGHEST PROFIT
    # ========================================================

    def get_category_with_highest_profit(self):

        query = """
            SELECT
                p.category_of_goods,
                SUM(f.sales) AS total_sales,
                SUM(f.profit) AS total_profit,
                SUM(f.profit) / NULLIF(SUM(f.sales), 0)
                    AS profit_margin
            FROM fact_sales f
            JOIN dim_product p
                ON f.product_key = p.product_key
            GROUP BY p.category_of_goods
            ORDER BY total_profit DESC
            LIMIT 1;
        """

        return self._execute_query(query)

    # ========================================================
    # 2. SUB-CATEGORY WITH HIGHEST PROFIT
    # ========================================================

    def get_subcategory_with_highest_profit(self):

        query = """
            SELECT
                p.category_of_goods,
                p.sub_category,
                SUM(f.sales) AS total_sales,
                SUM(f.profit) AS total_profit,
                SUM(f.profit) / NULLIF(SUM(f.sales), 0)
                    AS profit_margin
            FROM fact_sales f
            JOIN dim_product p
                ON f.product_key = p.product_key
            GROUP BY
                p.category_of_goods,
                p.sub_category
            ORDER BY total_profit DESC
            LIMIT 1;
        """

        return self._execute_query(query)

    # ========================================================
    # 3. SALES ABOVE OVERALL AVERAGE
    # ========================================================

    def get_sales_above_average(self):

        query = """
            SELECT
                order_id,
                sales,
                profit,
                quantity,
                discount
            FROM fact_sales
            WHERE sales > (
                SELECT AVG(sales)
                FROM fact_sales
            )
            ORDER BY sales DESC;
        """

        return self._execute_query(query)

    # ========================================================
    # 4. PROFIT ABOVE OVERALL AVERAGE
    # ========================================================

    def get_profit_above_average(self):

        query = """
            SELECT
                order_id,
                sales,
                profit,
                profit_margin
            FROM fact_sales
            WHERE profit > (
                SELECT AVG(profit)
                FROM fact_sales
            )
            ORDER BY profit DESC;
        """

        return self._execute_query(query)

    # ========================================================
    # 5. PRODUCTS ABOVE AVERAGE PRODUCT SALES
    # ========================================================

    def get_products_above_average_sales(self):

        query = """
            SELECT
                p.product_id,
                p.product_name,
                SUM(f.sales) AS total_sales
            FROM fact_sales f
            JOIN dim_product p
                ON f.product_key = p.product_key
            GROUP BY
                p.product_id,
                p.product_name
            HAVING SUM(f.sales) > (
                SELECT AVG(product_sales)
                FROM (
                    SELECT
                        product_key,
                        SUM(sales) AS product_sales
                    FROM fact_sales
                    GROUP BY product_key
                ) AS product_summary
            )
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
                "Executing advanced analytics query."
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
                f"Advanced analytics query completed. "
                f"Rows returned: {len(result)}"
            )

            return result

        except Exception as error:

            self.logger.exception(
                f"Advanced analytics query failed: {error}"
            )

            raise

        finally:

            if cursor is not None:
                cursor.close()

            if connection is not None:
                connection.close()