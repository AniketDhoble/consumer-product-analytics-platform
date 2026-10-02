import pymysql


# ============================================================
# MYSQL DATABASE CONFIGURATION
# ============================================================

DB_HOST = "localhost"
DB_PORT = 3306
DB_USER = "root"
DB_PASSWORD = "aaibaba11"

DB_NAME = "consumer_product_analytics"

DB_CHARSET = "utf8mb4"
DB_CONNECT_TIMEOUT = 10


# ============================================================
# MYSQL CONNECTION
# ============================================================

def get_connection():

    connection = pymysql.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        charset=DB_CHARSET,
        connect_timeout=DB_CONNECT_TIMEOUT
    )

    return connection