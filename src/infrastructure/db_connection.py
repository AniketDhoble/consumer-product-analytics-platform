"""
MySQL Database Connection
"""

from src.config.database_config import get_connection


def test_connection():

    connection = None

    try:
        connection = get_connection()

        print("MySQL connection successful.")

        return True

    except Exception as error:

        print(
            f"MySQL connection failed: {error}"
        )

        return False

    finally:

        if connection:
            connection.close()