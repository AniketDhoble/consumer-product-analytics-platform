-- ============================================================
-- CONSUMER & PRODUCT ANALYTICS PLATFORM
-- FOREIGN KEY CONSTRAINTS
-- ============================================================

USE consumer_product_analytics;


-- ============================================================
-- FACT → CUSTOMER
-- ============================================================

ALTER TABLE fact_sales
ADD CONSTRAINT fk_fact_customer
FOREIGN KEY (customer_key)
REFERENCES dim_customer(customer_key);


-- ============================================================
-- FACT → PRODUCT
-- ============================================================

ALTER TABLE fact_sales
ADD CONSTRAINT fk_fact_product
FOREIGN KEY (product_key)
REFERENCES dim_product(product_key);


-- ============================================================
-- FACT → ORDER DATE
-- ============================================================

ALTER TABLE fact_sales
ADD CONSTRAINT fk_fact_order_date
FOREIGN KEY (order_date_key)
REFERENCES dim_date(date_key);


-- ============================================================
-- FACT → SALES DATE
-- ============================================================

ALTER TABLE fact_sales
ADD CONSTRAINT fk_fact_sales_date
FOREIGN KEY (sales_date_key)
REFERENCES dim_date(date_key);


-- ============================================================
-- FACT → SHIP DATE
-- ============================================================

ALTER TABLE fact_sales
ADD CONSTRAINT fk_fact_ship_date
FOREIGN KEY (ship_date_key)
REFERENCES dim_date(date_key);


-- ============================================================
-- FACT → LOCATION
-- ============================================================

ALTER TABLE fact_sales
ADD CONSTRAINT fk_fact_location
FOREIGN KEY (location_key)
REFERENCES dim_location(location_key);