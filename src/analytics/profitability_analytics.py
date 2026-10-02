"""
Profitability Analytics

Provides reusable profitability and discount analytics
from the MySQL fact_sales and dim_product tables.
"""

from src.config.logging_config import get_logger
from src.infrastructure.db_connection import get_connection


class ProfitabilityAnalytics:

    def __init__(self):
        self.logger = get_logger("ProfitabilityAnalytics")

    # ========================================================
    # 1. PROFIT MARGIN BY DISCOUNT LEVEL
    # ========================================================

    def get_profit_margin_by_discount(self):

        query = """
            SELECT
                CASE
                    WHEN discount = 0 THEN 'No Discount'
                    WHEN discount <= 0.10 THEN 'Low Discount'
                    WHEN discount <= 0.30 THEN 'Medium Discount'
                    ELSE 'High Discount'
                END AS discount_level,

                COUNT(DISTINCT order_id) AS total_orders,
                SUM(sales) AS total_sales,
                SUM(profit) AS total_profit,

                SUM(profit) / NULLIF(SUM(sales), 0)
                    AS profit_margin

            FROM fact_sales

            GROUP BY
                CASE
                    WHEN discount = 0 THEN 'No Discount'
                    WHEN discount <= 0.10 THEN 'Low Discount'
                    WHEN discount <= 0.30 THEN 'Medium Discount'
                    ELSE 'High Discount'
                END

            ORDER BY total_sales DESC;
        """

        return self._execute_query(query)

    # ========================================================
    # 2. HIGH DISCOUNT ORDERS
    # ========================================================

    def get_high_discount_orders(self):

        query = """
            SELECT
                order_id,
                sales,
                discount,
                profit,
                profit_margin
            FROM fact_sales
            WHERE discount >= 0.30
            ORDER BY
                discount DESC,
                profit ASC
            LIMIT 20;
        """

        return self._execute_query(query)

    # ========================================================
    # 3. HIGH DISCOUNT + NEGATIVE PROFIT
    # ========================================================

    def get_high_discount_negative_profit_orders(self):

        query = """
            SELECT
                order_id,
                sales,
                discount,
                profit,
                profit_margin
            FROM fact_sales
            WHERE discount >= 0.30
              AND profit < 0
            ORDER BY profit ASC;
        """

        return self._execute_query(query)

    # ========================================================
    # 4. MOST PROFITABLE PRODUCTS BY PROFIT MARGIN
    # ========================================================

    def get_high_margin_products(self):

        query = """
            SELECT
                p.product_id,
                p.product_name,
                p.category_of_goods,
                p.sub_category,

                SUM(f.profit) / NULLIF(SUM(f.sales), 0)
                    AS profit_margin,

                SUM(f.sales) AS total_sales,
                SUM(f.profit) AS total_profit

            FROM fact_sales f

            JOIN dim_product p
                ON f.product_key = p.product_key

            GROUP BY
                p.product_id,
                p.product_name,
                p.category_of_goods,
                p.sub_category

            HAVING SUM(f.sales) > 10000

            ORDER BY profit_margin DESC

            LIMIT 10;
        """

        return self._execute_query(query)

    # ========================================================
    # 5. LOW PROFIT MARGIN PRODUCTS
    # ========================================================

    def get_low_margin_products(self):

        query = """
            SELECT
                p.product_id,
                p.product_name,
                p.category_of_goods,
                p.sub_category,

                SUM(f.profit) / NULLIF(SUM(f.sales), 0)
                    AS profit_margin,

                SUM(f.sales) AS total_sales,
                SUM(f.profit) AS total_profit

            FROM fact_sales f

            JOIN dim_product p
                ON f.product_key = p.product_key

            GROUP BY
                p.product_id,
                p.product_name,
                p.category_of_goods,
                p.sub_category

            HAVING SUM(f.sales) > 10000

            ORDER BY profit_margin ASC

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
                "Executing profitability analytics query."
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
                f"Profitability analytics query completed. "
                f"Rows returned: {len(result)}"
            )

            return result

        except Exception as error:

            self.logger.exception(
                f"Profitability analytics query failed: {error}"
            )

            raise

        finally:

            if cursor is not None:
                cursor.close()

            if connection is not None:
                connection.close()