
# Database Schema

## Database


consumer_product_analytics


## Tables


dim_customer
dim_product
dim_date
dim_location
fact_sales


## Relationships


dim_customer
     |
     v
fact_sales
     ^
     |
dim_product

dim_date
     |
     v
fact_sales

dim_location
     |
     v
fact_sales


## Views


vw_sales_detail
vw_customer_performance
vw_product_performance
vw_monthly_sales
vw_regional_performance


T