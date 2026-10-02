-- ============================================================
-- CONSUMER & PRODUCT ANALYTICS PLATFORM
-- BUSINESS QUERIES
-- ============================================================

USE consumer_product_analytics;


-- ============================================================
-- SECTION 1: SALES PERFORMANCE
-- ============================================================


-- ============================================================
-- 1. TOTAL SALES, PROFIT AND ORDERS
-- ============================================================

SELECT
    COUNT(DISTINCT order_id) AS total_orders,
    SUM(sales) AS total_sales,
    SUM(profit) AS total_profit,
    SUM(quantity) AS total_quantity
FROM fact_sales;


-- ============================================================
-- 2. SALES AND PROFIT BY YEAR
-- ============================================================

SELECT
    d.year,
    COUNT(DISTINCT f.order_id) AS total_orders,
    SUM(f.sales) AS total_sales,
    SUM(f.profit) AS total_profit,
    SUM(f.profit) / NULLIF(SUM(f.sales), 0) AS profit_margin
FROM fact_sales f
JOIN dim_date d
    ON f.order_date_key = d.date_key
GROUP BY d.year
ORDER BY d.year;


-- ============================================================
-- 3. MONTHLY SALES PERFORMANCE
-- ============================================================

SELECT
    d.year,
    d.month,
    d.month_name,
    SUM(f.sales) AS total_sales,
    SUM(f.profit) AS total_profit,
    SUM(f.profit) / NULLIF(SUM(f.sales), 0) AS profit_margin
FROM fact_sales f
JOIN dim_date d
    ON f.order_date_key = d.date_key
GROUP BY
    d.year,
    d.month,
    d.month_name
ORDER BY
    d.year,
    d.month;


-- ============================================================
-- 4. TOP 10 ORDERS BY SALES
-- ============================================================

SELECT
    order_id,
    sales,
    profit,
    quantity,
    discount,
    profit_margin
FROM fact_sales
ORDER BY sales DESC
LIMIT 10;


-- ============================================================
-- 5. TOP 10 ORDERS BY PROFIT
-- ============================================================

SELECT
    order_id,
    sales,
    profit,
    quantity,
    discount,
    profit_margin
FROM fact_sales
ORDER BY profit DESC
LIMIT 10;


-- ============================================================
-- SECTION 2: CUSTOMER ANALYSIS
-- ============================================================


-- ============================================================
-- 6. TOP 10 CUSTOMERS BY SALES
-- ============================================================

SELECT
    c.customer_id,
    c.customer_name,
    c.segment,
    SUM(f.sales) AS total_sales,
    SUM(f.profit) AS total_profit,
    COUNT(DISTINCT f.order_id) AS total_orders,
    SUM(f.profit) / NULLIF(SUM(f.sales), 0) AS profit_margin
FROM fact_sales f
JOIN dim_customer c
    ON f.customer_key = c.customer_key
GROUP BY
    c.customer_id,
    c.customer_name,
    c.segment
ORDER BY total_sales DESC
LIMIT 10;


-- ============================================================
-- 7. TOP 10 CUSTOMERS BY PROFIT
-- ============================================================

SELECT
    c.customer_id,
    c.customer_name,
    c.segment,
    SUM(f.profit) AS total_profit,
    SUM(f.sales) AS total_sales,
    COUNT(DISTINCT f.order_id) AS total_orders,
    SUM(f.profit) / NULLIF(SUM(f.sales), 0) AS profit_margin
FROM fact_sales f
JOIN dim_customer c
    ON f.customer_key = c.customer_key
GROUP BY
    c.customer_id,
    c.customer_name,
    c.segment
ORDER BY total_profit DESC
LIMIT 10;


-- ============================================================
-- 8. SALES AND PROFIT BY CUSTOMER SEGMENT
-- ============================================================

SELECT
    c.segment,
    COUNT(DISTINCT f.order_id) AS total_orders,
    SUM(f.sales) AS total_sales,
    SUM(f.profit) AS total_profit,
    SUM(f.quantity) AS total_quantity,
    SUM(f.profit) / NULLIF(SUM(f.sales), 0) AS profit_margin
FROM fact_sales f
JOIN dim_customer c
    ON f.customer_key = c.customer_key
GROUP BY c.segment
ORDER BY total_sales DESC;


-- ============================================================
-- 9. CUSTOMERS WITH NEGATIVE PROFIT
-- ============================================================

SELECT
    c.customer_id,
    c.customer_name,
    c.segment,
    SUM(f.sales) AS total_sales,
    SUM(f.profit) AS total_profit,
    SUM(f.profit) / NULLIF(SUM(f.sales), 0) AS profit_margin
FROM fact_sales f
JOIN dim_customer c
    ON f.customer_key = c.customer_key
GROUP BY
    c.customer_id,
    c.customer_name,
    c.segment
HAVING SUM(f.profit) < 0
ORDER BY total_profit ASC;


-- ============================================================
-- 10. CUSTOMERS WITH HIGH SALES BUT LOW PROFIT
-- ============================================================

SELECT
    c.customer_id,
    c.customer_name,
    c.segment,
    SUM(f.sales) AS total_sales,
    SUM(f.profit) AS total_profit,
    SUM(f.profit) / NULLIF(SUM(f.sales), 0) AS profit_margin
FROM fact_sales f
JOIN dim_customer c
    ON f.customer_key = c.customer_key
GROUP BY
    c.customer_id,
    c.customer_name,
    c.segment
HAVING
    SUM(f.sales) > 100000
    AND SUM(f.profit) < 10000
ORDER BY total_sales DESC;


-- ============================================================
-- SECTION 3: PRODUCT ANALYSIS
-- ============================================================


-- ============================================================
-- 11. TOP 10 PRODUCTS BY SALES
-- ============================================================

SELECT
    p.product_id,
    p.product_name,
    p.category_of_goods,
    p.sub_category,
    SUM(f.sales) AS total_sales,
    SUM(f.profit) AS total_profit,
    SUM(f.quantity) AS total_quantity,
    SUM(f.profit) / NULLIF(SUM(f.sales), 0) AS profit_margin
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


-- ============================================================
-- 12. TOP 10 PRODUCTS BY PROFIT
-- ============================================================

SELECT
    p.product_id,
    p.product_name,
    p.category_of_goods,
    p.sub_category,
    SUM(f.profit) AS total_profit,
    SUM(f.sales) AS total_sales,
    SUM(f.quantity) AS total_quantity,
    SUM(f.profit) / NULLIF(SUM(f.sales), 0) AS profit_margin
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


-- ============================================================
-- 13. SALES AND PROFIT BY CATEGORY
-- ============================================================

SELECT
    p.category_of_goods,
    SUM(f.sales) AS total_sales,
    SUM(f.profit) AS total_profit,
    SUM(f.quantity) AS total_quantity,
    COUNT(DISTINCT f.order_id) AS total_orders,
    SUM(f.profit) / NULLIF(SUM(f.sales), 0) AS profit_margin
FROM fact_sales f
JOIN dim_product p
    ON f.product_key = p.product_key
GROUP BY p.category_of_goods
ORDER BY total_sales DESC;


-- ============================================================
-- 14. SALES AND PROFIT BY SUB-CATEGORY
-- ============================================================

SELECT
    p.category_of_goods,
    p.sub_category,
    SUM(f.sales) AS total_sales,
    SUM(f.profit) AS total_profit,
    SUM(f.quantity) AS total_quantity,
    COUNT(DISTINCT f.order_id) AS total_orders,
    SUM(f.profit) / NULLIF(SUM(f.sales), 0) AS profit_margin
FROM fact_sales f
JOIN dim_product p
    ON f.product_key = p.product_key
GROUP BY
    p.category_of_goods,
    p.sub_category
ORDER BY total_sales DESC;


-- ============================================================
-- 15. PRODUCTS WITH NEGATIVE PROFIT
-- ============================================================

SELECT
    p.product_id,
    p.product_name,
    p.category_of_goods,
    p.sub_category,
    SUM(f.sales) AS total_sales,
    SUM(f.profit) AS total_profit,
    SUM(f.profit) / NULLIF(SUM(f.sales), 0) AS profit_margin
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


-- ============================================================
-- SECTION 4: REGIONAL ANALYSIS
-- ============================================================


-- ============================================================
-- 16. SALES AND PROFIT BY REGION
-- ============================================================

SELECT
    l.region,
    SUM(f.sales) AS total_sales,
    SUM(f.profit) AS total_profit,
    SUM(f.quantity) AS total_quantity,
    COUNT(DISTINCT f.order_id) AS total_orders,
    SUM(f.profit) / NULLIF(SUM(f.sales), 0) AS profit_margin
FROM fact_sales f
JOIN dim_location l
    ON f.location_key = l.location_key
GROUP BY l.region
ORDER BY total_sales DESC;


-- ============================================================
-- 17. SALES AND PROFIT BY STATE
-- ============================================================

SELECT
    l.state,
    SUM(f.sales) AS total_sales,
    SUM(f.profit) AS total_profit,
    COUNT(DISTINCT f.order_id) AS total_orders,
    SUM(f.profit) / NULLIF(SUM(f.sales), 0) AS profit_margin
FROM fact_sales f
JOIN dim_location l
    ON f.location_key = l.location_key
GROUP BY l.state
ORDER BY total_sales DESC;


-- ============================================================
-- 18. SALES BY OUTLET TYPE
-- ============================================================

SELECT
    l.outlet_type,
    SUM(f.sales) AS total_sales,
    SUM(f.profit) AS total_profit,
    SUM(f.quantity) AS total_quantity,
    SUM(f.profit) / NULLIF(SUM(f.sales), 0) AS profit_margin
FROM fact_sales f
JOIN dim_location l
    ON f.location_key = l.location_key
GROUP BY l.outlet_type
ORDER BY total_sales DESC;


-- ============================================================
-- 19. SALES BY CITY TYPE
-- ============================================================

SELECT
    l.city_type,
    SUM(f.sales) AS total_sales,
    SUM(f.profit) AS total_profit,
    COUNT(DISTINCT f.order_id) AS total_orders,
    SUM(f.profit) / NULLIF(SUM(f.sales), 0) AS profit_margin
FROM fact_sales f
JOIN dim_location l
    ON f.location_key = l.location_key
GROUP BY l.city_type
ORDER BY total_sales DESC;


-- ============================================================
-- 20. REGIONS WITH NEGATIVE PROFIT
-- ============================================================

SELECT
    l.region,
    SUM(f.sales) AS total_sales,
    SUM(f.profit) AS total_profit,
    COUNT(DISTINCT f.order_id) AS total_orders,
    SUM(f.profit) / NULLIF(SUM(f.sales), 0) AS profit_margin
FROM fact_sales f
JOIN dim_location l
    ON f.location_key = l.location_key
GROUP BY l.region
HAVING SUM(f.profit) < 0
ORDER BY total_profit ASC;


-- ============================================================
-- SECTION 5: DISCOUNT & PROFITABILITY ANALYSIS
-- ============================================================


-- ============================================================
-- 21. PROFIT MARGIN BY DISCOUNT LEVEL
-- ============================================================

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


-- ============================================================
-- 22. ORDERS WITH HIGH DISCOUNT
-- ============================================================

SELECT
    order_id,
    sales,
    discount,
    profit,
    profit_margin
FROM fact_sales
WHERE discount >= 0.30
ORDER BY discount DESC, profit ASC
LIMIT 20;


-- ============================================================
-- 23. HIGH DISCOUNT + NEGATIVE PROFIT
-- ============================================================

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


-- ============================================================
-- 24. MOST PROFITABLE PRODUCTS BY PROFIT MARGIN
-- ============================================================

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


-- ============================================================
-- 25. LOW PROFIT MARGIN PRODUCTS
-- ============================================================

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


-- ============================================================
-- SECTION 6: ADVANCED BUSINESS ANALYSIS
-- ============================================================


-- ============================================================
-- 26. CATEGORY WITH HIGHEST PROFIT
-- ============================================================

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


-- ============================================================
-- 27. SUB-CATEGORY WITH HIGHEST PROFIT
-- ============================================================

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


-- ============================================================
-- 28. SALES ABOVE OVERALL AVERAGE
-- ============================================================

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


-- ============================================================
-- 29. PROFIT ABOVE OVERALL AVERAGE
-- ============================================================

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


-- ============================================================
-- 30. PRODUCTS ABOVE AVERAGE PRODUCT SALES
-- ============================================================

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