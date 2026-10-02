import pymysql

from src.config.database_config import (
    DB_HOST,
    DB_PORT,
    DB_USER,
    DB_PASSWORD
)


connection = pymysql.connect(
    host=DB_HOST,
    port=DB_PORT,
    user=DB_USER,
    password=DB_PASSWORD
)

cursor = connection.cursor()

cursor.execute(
    """
    CREATE DATABASE IF NOT EXISTS consumer_product_analytics
    """
)

print("MySQL connection successful!")
print("Database created/verified successfully!")

cursor.close()
connection.close()