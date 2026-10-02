-- ============================================================
-- CONSUMER & PRODUCT ANALYTICS PLATFORM
-- STAR SCHEMA - TABLE CREATION
-- ============================================================

USE consumer_product_analytics;


-- ============================================================
-- 1. DIMENSION: CUSTOMER
-- ============================================================

CREATE TABLE IF NOT EXISTS dim_customer (

    customer_key INT AUTO_INCREMENT,

    customer_id VARCHAR(50) NOT NULL,
    customer_name VARCHAR(150),
    last_name VARCHAR(100),
    date_of_birth DATE,
    segment VARCHAR(50),

    PRIMARY KEY (customer_key),
    UNIQUE KEY uq_customer_id (customer_id)

);


-- ============================================================
-- 2. DIMENSION: PRODUCT
-- ============================================================

CREATE TABLE IF NOT EXISTS dim_product (

    product_key INT AUTO_INCREMENT,

    product_id VARCHAR(50) NOT NULL,
    product_name VARCHAR(255),
    category_of_goods VARCHAR(100),
    sub_category VARCHAR(100),

    PRIMARY KEY (product_key),
    UNIQUE KEY uq_product_id (product_id)

);


-- ============================================================
-- 3. DIMENSION: DATE
-- ============================================================

CREATE TABLE IF NOT EXISTS dim_date (

    date_key INT,

    full_date DATE NOT NULL,
    year INT,
    month INT,
    month_name VARCHAR(20),
    quarter INT,
    day INT,
    day_name VARCHAR(20),

    PRIMARY KEY (date_key),
    UNIQUE KEY uq_full_date (full_date)

);


-- ============================================================
-- 4. DIMENSION: LOCATION
-- ============================================================

CREATE TABLE IF NOT EXISTS dim_location (

    location_key INT AUTO_INCREMENT,

    country VARCHAR(50),
    region VARCHAR(50),
    state VARCHAR(100),
    city_type VARCHAR(50),
    outlet_type VARCHAR(50),
    postal_code INT,

    PRIMARY KEY (location_key)

);


-- ============================================================
-- 5. FACT: SALES
-- ============================================================

CREATE TABLE IF NOT EXISTS fact_sales (

    sales_key BIGINT AUTO_INCREMENT,

    order_id VARCHAR(50) NOT NULL,

    customer_key INT NOT NULL,
    product_key INT NOT NULL,
    order_date_key INT NOT NULL,
    sales_date_key INT,
    ship_date_key INT,
    location_key INT NOT NULL,

    ship_mode VARCHAR(50),

    sales DECIMAL(12,2),
    quantity INT,
    discount DECIMAL(5,2),
    profit DECIMAL(12,2),
    profit_margin DECIMAL(10,6),

    PRIMARY KEY (sales_key),

    UNIQUE KEY uq_order_id (order_id)

);