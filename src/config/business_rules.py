"""
Business rules for the Consumer & Product Analytics Platform.

These rules represent known business expectations discovered
during data profiling and will be reused during cleaning
and validation.
"""


# ============================================================
# DATA QUALITY RULES
# ============================================================

REQUIRE_NO_DUPLICATE_ROWS = True
REQUIRE_NO_BLANK_STRINGS = True
REQUIRE_NO_MISSING_VALUES = True


# ============================================================
# DATE RULES
# ============================================================

ORDER_DATE_COLUMN = "Order Date"
SHIP_DATE_COLUMN = "Ship Date"
SALES_DATE_COLUMN = "Sales Date"
DATE_OF_BIRTH_COLUMN = "Date of Birth"

REQUIRE_ORDER_DATE_BEFORE_SHIP_DATE = True


# ============================================================
# CUSTOMER RULES
# ============================================================

CUSTOMER_ID_COLUMN = "Customer ID"
CUSTOMER_NAME_COLUMN = "Customer Name"

REQUIRE_CUSTOMER_ID_UNIQUE = True
REQUIRE_CUSTOMER_ID_NAME_CONSISTENCY = True


# ============================================================
# PRODUCT RULES
# ============================================================

PRODUCT_ID_COLUMN = "Product ID"
PRODUCT_NAME_COLUMN = "Product Name"
SUBCATEGORY_COLUMN = "Sub-Category"

REQUIRE_PRODUCT_ID_UNIQUE = True
REQUIRE_PRODUCT_ID_NAME_CONSISTENCY = True
REQUIRE_PRODUCT_ID_SUBCATEGORY_CONSISTENCY = True


# ============================================================
# ORDER RULES
# ============================================================

ORDER_ID_COLUMN = "Order ID"

REQUIRE_ORDER_ID_UNIQUE = True


# ============================================================
# NUMERIC BUSINESS RULES
# ============================================================

SALES_COLUMN = "Sales"
QUANTITY_COLUMN = "Quantity"
DISCOUNT_COLUMN = "Discount"
PROFIT_COLUMN = "Profit"

MIN_SALES = 0
MIN_QUANTITY = 1
MIN_DISCOUNT = 0
MAX_DISCOUNT = 1
MIN_PROFIT = 0


# ============================================================
# YEAR RULE
# ============================================================

YEAR_COLUMN = "Year"

# Profiling showed that Year does not reliably correspond
# to Order Date, Ship Date, or Sales Date.
#
# Therefore we DO NOT use Year as the authoritative
# transaction year.

YEAR_REQUIRES_INVESTIGATION = True

AUTHORITATIVE_ORDER_YEAR_SOURCE = ORDER_DATE_COLUMN