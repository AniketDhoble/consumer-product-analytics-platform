-- ============================================================
-- CONSUMER & PRODUCT ANALYTICS PLATFORM
-- INDEXES
-- ============================================================

USE consumer_product_analytics;


-- Customer lookup
CREATE INDEX idx_customer_id
ON dim_customer(customer_id);


-- Product lookup
CREATE INDEX idx_product_id
ON dim_product(product_id);


-- Date lookup
CREATE INDEX idx_full_date
ON dim_date(full_date);


-- Location lookup
CREATE INDEX idx_location_region
ON dim_location(region);


-- Fact table date filtering
CREATE INDEX idx_fact_order_date
ON fact_sales(order_date_key);


CREATE INDEX idx_fact_sales_date
ON fact_sales(sales_date_key);


CREATE INDEX idx_fact_ship_date
ON fact_sales(ship_date_key);


-- Fact table dimension joins
CREATE INDEX idx_fact_customer
ON fact_sales(customer_key);


CREATE INDEX idx_fact_product
ON fact_sales(product_key);


CREATE INDEX idx_fact_location
ON fact_sales(location_key);