-- ============================================================
-- CONSUMER & PRODUCT ANALYTICS PLATFORM
-- ANALYTICAL VIEWS
-- ============================================================

USE consumer_product_analytics;


-- ============================================================
-- 1. SALES DETAIL VIEW
-- ============================================================

CREATE OR REPLACE VIEW vw_sales_detail AS
SELECT
    f.sales_key,
    f.order_id,

    c.customer_id,
    c.customer_name,
    c.segment,

    p.product_id,
    p.product_name,
    p.category_of_goods,
    p.sub_category,

    d.full_date AS order_date,
    d.year AS order_year,
    d.month AS order_month,
    d.month_name,
    d.quarter,

    l.country,
    l.region,
    l.state,
    l.city_type,
    l.outlet_type,
    l.postal_code,

    f.ship_mode,
    f.sales,
    f.quantity,
    f.discount,
    f.profit,
    f.profit_margin

FROM fact_sales f

LEFT JOIN dim_customer c
    ON f.customer_key = c.customer_key

LEFT JOIN dim_product p
    ON f.product_key = p.product_key

LEFT JOIN dim_date d
    ON f.order_date_key = d.date_key

LEFT JOIN dim_location l
    ON f.location_key = l.location_key;


-- ============================================================
-- 2. CUSTOMER PERFORMANCE VIEW
-- ============================================================

CREATE OR REPLACE VIEW vw_customer_performance AS
SELECT
    c.customer_id,
    c.customer_name,
    c.segment,

    COUNT(DISTINCT f.order_id) AS total_orders,
    SUM(f.sales) AS total_sales,
    SUM(f.quantity) AS total_quantity,
    SUM(f.profit) AS total_profit,

    SUM(f.profit) / NULLIF(SUM(f.sales), 0) AS profit_margin

FROM dim_customer c

LEFT JOIN fact_sales f
    ON c.customer_key = f.customer_key

GROUP BY
    c.customer_id,
    c.customer_name,
    c.segment;


-- ============================================================
-- 3. PRODUCT PERFORMANCE VIEW
-- ============================================================

CREATE OR REPLACE VIEW vw_product_performance AS
SELECT
    p.product_id,
    p.product_name,
    p.category_of_goods,
    p.sub_category,

    COUNT(DISTINCT f.order_id) AS total_orders,
    SUM(f.quantity) AS total_quantity,
    SUM(f.sales) AS total_sales,
    SUM(f.profit) AS total_profit,

    SUM(f.profit) / NULLIF(SUM(f.sales), 0) AS profit_margin

FROM dim_product p

LEFT JOIN fact_sales f
    ON p.product_key = f.product_key

GROUP BY
    p.product_id,
    p.product_name,
    p.category_of_goods,
    p.sub_category;


-- ============================================================
-- 4. MONTHLY SALES VIEW
-- ============================================================

CREATE OR REPLACE VIEW vw_monthly_sales AS
SELECT
    d.year,
    d.month,
    d.month_name,
    d.quarter,

    COUNT(DISTINCT f.order_id) AS total_orders,
    SUM(f.sales) AS total_sales,
    SUM(f.quantity) AS total_quantity,
    SUM(f.profit) AS total_profit,

    SUM(f.profit) / NULLIF(SUM(f.sales), 0) AS profit_margin

FROM fact_sales f

LEFT JOIN dim_date d
    ON f.order_date_key = d.date_key

GROUP BY
    d.year,
    d.month,
    d.month_name,
    d.quarter;


-- ============================================================
-- 5. REGIONAL PERFORMANCE VIEW
-- ============================================================

CREATE OR REPLACE VIEW vw_regional_performance AS
SELECT
    l.country,
    l.region,
    l.state,
    l.city_type,
    l.outlet_type,

    COUNT(DISTINCT f.order_id) AS total_orders,
    SUM(f.sales) AS total_sales,
    SUM(f.quantity) AS total_quantity,
    SUM(f.profit) AS total_profit,

    SUM(f.profit) / NULLIF(SUM(f.sales), 0) AS profit_margin

FROM fact_sales f

LEFT JOIN dim_location l
    ON f.location_key = l.location_key

GROUP BY
    l.country,
    l.region,
    l.state,
    l.city_type,
    l.outlet_type;