"""
Product Analytics

Provides reusable product-level business analytics
from the MySQL fact_sales and dim_product tables.
"""

from src.config.logging_config import get_logger
from src.infrastructure.db_connection import get_connection


class ProductAnalytics:

    def __init__(self):
        self.logger = get_logger("ProductAnalytics")

    # ========================================================
    # 1. TOP 10 PRODUCTS BY SALES
    # ========================================================

    def get_top_products_by_sales(self):

        query = """
            SELECT
                p.product_id,
                p.product_name,
                p.category_of_goods,
                p.sub_category,
                SUM(f.sales) AS total_sales,
                SUM(f.profit) AS total_profit,
                SUM(f.quantity) AS total_quantity,
                SUM(f.profit) / NULLIF(SUM(f.sales), 0)
                    AS profit_margin
            FROM fact_sales f
            JOIN dim_product p
                ON f.product_key = p.product_key
            GROUP BY
                p.product_id,
                p.product_name,
                p.category_of_goods,
                p.sub_category
            ORDER BY total_sales DESC
            LIMIT 10;
        """

        return self._execute_query(query)

    # ========================================================
    # 2. TOP 10 PRODUCTS BY PROFIT
    # ========================================================

    def get_top_products_by_profit(self):

        query = """
            SELECT
                p.product_id,
                p.product_name,
                p.category_of_goods,
                p.sub_category,
                SUM(f.profit) AS total_profit,
                SUM(f.sales) AS total_sales,
                SUM(f.quantity) AS total_quantity,
                SUM(f.profit) / NULLIF(SUM(f.sales), 0)
                    AS profit_margin
            FROM fact_sales f
            JOIN dim_product p
                ON f.product_key = p.product_key
            GROUP BY
                p.product_id,
                p.product_name,
                p.category_of_goods,
                p.sub_category
            ORDER BY total_profit DESC
            LIMIT 10;
        """

        return self._execute_query(query)

    # ========================================================
    # 3. SALES AND PROFIT BY CATEGORY
    # ========================================================

    def get_sales_by_category(self):

        query = """
            SELECT
                p.category_of_goods,
                SUM(f.sales) AS total_sales,
                SUM(f.profit) AS total_profit,
                SUM(f.quantity) AS total_quantity,
                COUNT(DISTINCT f.order_id) AS total_orders,
                SUM(f.profit) / NULLIF(SUM(f.sales), 0)
                    AS profit_margin
            FROM fact_sales f
            JOIN dim_product p
                ON f.product_key = p.product_key
            GROUP BY p.category_of_goods
            ORDER BY total_sales DESC;
        """

        return self._execute_query(query)

    # ========================================================
    # 4. SALES AND PROFIT BY SUB-CATEGORY
    # ========================================================

    def get_sales_by_subcategory(self):

        query = """
            SELECT
                p.category_of_goods,
                p.sub_category,
                SUM(f.sales) AS total_sales,
                SUM(f.profit) AS total_profit,
                SUM(f.quantity) AS total_quantity,
                COUNT(DISTINCT f.order_id) AS total_orders,
                SUM(f.profit) / NULLIF(SUM(f.sales), 0)
                    AS profit_margin
            FROM fact_sales f
            JOIN dim_product p
                ON f.product_key = p.product_key
            GROUP BY
                p.category_of_goods,
                p.sub_category
            ORDER BY total_sales DESC;
        """

        return self._execute_query(query)

    # ========================================================
    # 5. PRODUCTS WITH NEGATIVE PROFIT
    # ========================================================

    def get_negative_profit_products(self):

        query = """
            SELECT
                p.product_id,
                p.product_name,
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
                p.product_id,
                p.product_name,
                p.category_of_goods,
                p.sub_category
            HAVING SUM(f.profit) < 0
            ORDER BY total_profit ASC;
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
                "Executing product analytics query."
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
                f"Product analytics query completed. "
                f"Rows returned: {len(result)}"
            )

            return result

        except Exception as error:

            self.logger.exception(
                f"Product analytics query failed: {error}"
            )

            raise

        finally:

            if cursor is not None:
                cursor.close()

            if connection is not None:
                connection.close()