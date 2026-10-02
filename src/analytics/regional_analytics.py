"""
Regional Analytics

Provides reusable regional and location-level business analytics
from the MySQL fact_sales and dim_location tables.
"""

from src.config.logging_config import get_logger
from src.infrastructure.db_connection import get_connection


class RegionalAnalytics:

    def __init__(self):
        self.logger = get_logger("RegionalAnalytics")

    # ========================================================
    # 1. SALES AND PROFIT BY REGION
    # ========================================================

    def get_sales_by_region(self):

        query = """
            SELECT
                l.region,
                SUM(f.sales) AS total_sales,
                SUM(f.profit) AS total_profit,
                SUM(f.quantity) AS total_quantity,
                COUNT(DISTINCT f.order_id) AS total_orders,
                SUM(f.profit) / NULLIF(SUM(f.sales), 0)
                    AS profit_margin
            FROM fact_sales f
            JOIN dim_location l
                ON f.location_key = l.location_key
            GROUP BY l.region
            ORDER BY total_sales DESC;
        """

        return self._execute_query(query)

    # ========================================================
    # 2. SALES AND PROFIT BY STATE
    # ========================================================

    def get_sales_by_state(self):

        query = """
            SELECT
                l.state,
                SUM(f.sales) AS total_sales,
                SUM(f.profit) AS total_profit,
                COUNT(DISTINCT f.order_id) AS total_orders,
                SUM(f.profit) / NULLIF(SUM(f.sales), 0)
                    AS profit_margin
            FROM fact_sales f
            JOIN dim_location l
                ON f.location_key = l.location_key
            GROUP BY l.state
            ORDER BY total_sales DESC;
        """

        return self._execute_query(query)

    # ========================================================
    # 3. SALES BY OUTLET TYPE
    # ========================================================

    def get_sales_by_outlet_type(self):

        query = """
            SELECT
                l.outlet_type,
                SUM(f.sales) AS total_sales,
                SUM(f.profit) AS total_profit,
                SUM(f.quantity) AS total_quantity,
                SUM(f.profit) / NULLIF(SUM(f.sales), 0)
                    AS profit_margin
            FROM fact_sales f
            JOIN dim_location l
                ON f.location_key = l.location_key
            GROUP BY l.outlet_type
            ORDER BY total_sales DESC;
        """

        return self._execute_query(query)

    # ========================================================
    # 4. SALES BY CITY TYPE
    # ========================================================

    def get_sales_by_city_type(self):

        query = """
            SELECT
                l.city_type,
                SUM(f.sales) AS total_sales,
                SUM(f.profit) AS total_profit,
                COUNT(DISTINCT f.order_id) AS total_orders,
                SUM(f.profit) / NULLIF(SUM(f.sales), 0)
                    AS profit_margin
            FROM fact_sales f
            JOIN dim_location l
                ON f.location_key = l.location_key
            GROUP BY l.city_type
            ORDER BY total_sales DESC;
        """

        return self._execute_query(query)

    # ========================================================
    # 5. REGIONS WITH NEGATIVE PROFIT
    # ========================================================

    def get_negative_profit_regions(self):

        query = """
            SELECT
                l.region,
                SUM(f.sales) AS total_sales,
                SUM(f.profit) AS total_profit,
                COUNT(DISTINCT f.order_id) AS total_orders,
                SUM(f.profit) / NULLIF(SUM(f.sales), 0)
                    AS profit_margin
            FROM fact_sales f
            JOIN dim_location l
                ON f.location_key = l.location_key
            GROUP BY l.region
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
                "Executing regional analytics query."
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
                f"Regional analytics query completed. "
                f"Rows returned: {len(result)}"
            )

            return result

        except Exception as error:

            self.logger.exception(
                f"Regional analytics query failed: {error}"
            )

            raise

        finally:

            if cursor is not None:
                cursor.close()

            if connection is not None:
                connection.close()