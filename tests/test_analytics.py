"""
Analytics Layer Tests
"""

from src.analytics.sales_analytics import SalesAnalytics
from src.analytics.customer_analytics import CustomerAnalytics
from src.analytics.product_analytics import ProductAnalytics
from src.analytics.profitability_analytics import ProfitabilityAnalytics
from src.analytics.regional_analytics import RegionalAnalytics
from src.analytics.advanced_analytics import AdvancedAnalytics


# ============================================================
# SALES ANALYTICS
# ============================================================

def test_sales_analytics():

    analytics = SalesAnalytics()

    overall = analytics.get_overall_sales()
    yearly = analytics.get_sales_by_year()
    monthly = analytics.get_monthly_sales()
    top_sales = analytics.get_top_orders_by_sales()
    top_profit = analytics.get_top_orders_by_profit()

    assert len(overall) == 1
    assert len(yearly) > 0
    assert len(monthly) > 0
    assert len(top_sales) <= 10
    assert len(top_profit) <= 10


# ============================================================
# CUSTOMER ANALYTICS
# ============================================================

def test_customer_analytics():

    analytics = CustomerAnalytics()

    top_sales = analytics.get_top_customers_by_sales()
    top_profit = analytics.get_top_customers_by_profit()
    segment = analytics.get_sales_by_segment()
    negative = analytics.get_negative_profit_customers()
    high_sales_low_profit = (
        analytics.get_high_sales_low_profit_customers()
    )

    assert len(top_sales) > 0
    assert len(top_profit) > 0
    assert len(segment) > 0

    # These can legitimately return zero rows
    assert isinstance(negative, list)
    assert isinstance(high_sales_low_profit, list)


# ============================================================
# PRODUCT ANALYTICS
# ============================================================

def test_product_analytics():

    analytics = ProductAnalytics()

    top_sales = analytics.get_top_products_by_sales()
    top_profit = analytics.get_top_products_by_profit()
    category = analytics.get_sales_by_category()
    subcategory = analytics.get_sales_by_subcategory()
    negative = analytics.get_negative_profit_products()

    assert len(top_sales) > 0
    assert len(top_profit) > 0
    assert len(category) > 0
    assert len(subcategory) > 0

    assert isinstance(negative, list)


# ============================================================
# PROFITABILITY ANALYTICS
# ============================================================

def test_profitability_analytics():

    analytics = ProfitabilityAnalytics()

    discount_margin = (
        analytics.get_profit_margin_by_discount()
    )

    high_discount = (
        analytics.get_high_discount_orders()
    )

    high_discount_negative = (
        analytics.get_high_discount_negative_profit_orders()
    )

    high_margin = (
        analytics.get_high_margin_products()
    )

    low_margin = (
        analytics.get_low_margin_products()
    )

    assert len(discount_margin) > 0
    assert isinstance(high_discount, list)
    assert isinstance(high_discount_negative, list)
    assert isinstance(high_margin, list)
    assert isinstance(low_margin, list)


# ============================================================
# REGIONAL ANALYTICS
# ============================================================

def test_regional_analytics():

    analytics = RegionalAnalytics()

    region = analytics.get_sales_by_region()
    state = analytics.get_sales_by_state()
    outlet = analytics.get_sales_by_outlet_type()
    city = analytics.get_sales_by_city_type()
    negative = analytics.get_negative_profit_regions()

    assert len(region) > 0
    assert len(state) > 0
    assert len(outlet) > 0
    assert len(city) > 0

    assert isinstance(negative, list)


# ============================================================
# ADVANCED ANALYTICS
# ============================================================

def test_advanced_analytics():

    analytics = AdvancedAnalytics()

    category = (
        analytics.get_category_with_highest_profit()
    )

    subcategory = (
        analytics.get_subcategory_with_highest_profit()
    )

    sales_above_average = (
        analytics.get_sales_above_average()
    )

    profit_above_average = (
        analytics.get_profit_above_average()
    )

    products_above_average = (
        analytics.get_products_above_average_sales()
    )

    # Queries 26 and 27 use LIMIT 1
    assert len(category) == 1
    assert len(subcategory) == 1

    # Queries 28-30 should return lists
    assert isinstance(sales_above_average, list)
    assert isinstance(profit_above_average, list)
    assert isinstance(products_above_average, list)