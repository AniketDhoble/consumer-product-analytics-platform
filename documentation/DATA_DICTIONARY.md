# Data Dictionary

## Purpose

This document describes the columns used in the processed retail
dataset and explains their technical and business meaning.

---

## 1. Order Information

| Column Name | Data Type | Description | Business Meaning | Nullable | Example |
|---|---|---|---|---|---|
| Order ID | String | Unique identifier for an order | Identifies a customer order | No | ORD-10001 |
| Order Date | Date | Date when the order was placed | Used for time-based sales analysis | No | 2024-01-15 |
| Ship Date | Date | Date when the order was shipped | Used to analyze shipping activity | No | 2024-01-18 |
| Ship Mode | String | Shipping method used for the order | Used to analyze shipping patterns | No | Standard |

---

## 2. Customer Information

| Column Name | Data Type | Description | Business Meaning | Nullable | Example |
|---|---|---|---|---|---|
| Customer ID | String | Unique customer identifier | Identifies individual customers | No | CUST-1001 |
| Customer Name | String | Name of the customer | Used for customer-level analysis | No | Rahul Sharma |
| Segment | String | Customer segment | Used to compare customer groups | No | Consumer |

---

## 3. Product Information

| Column Name | Data Type | Description | Business Meaning | Nullable | Example |
|---|---|---|---|---|---|
| Product ID | String | Unique product identifier | Identifies individual products | No | PROD-1001 |
| Product Name | String | Name of the product | Used for product-level analysis | No | Office Chair |
| Category of Goods | String | Main product category | Used to analyze category performance | No | Furniture |
| Sub-Category | String | Product sub-category | Used for detailed product analysis | No | Chairs |

---

## 4. Sales and Profitability

| Column Name | Data Type | Description | Business Meaning | Nullable | Example |
|---|---|---|---|---|---|
| Sales | Numeric | Sales value of the transaction | Measures revenue generated | No | 1250.50 |
| Quantity | Integer | Number of units sold | Measures sales volume | No | 5 |
| Discount | Numeric | Discount applied to the transaction | Used to analyze discount impact | No | 0.20 |
| Profit | Numeric | Profit or loss from the transaction | Measures profitability | No | 250.75 |
| Profit Margin | Numeric | Profit relative to sales | Measures profitability efficiency | No | 0.20 |

---

## 5. Geographic Information

| Column Name | Data Type | Description | Business Meaning | Nullable | Example |
|---|---|---|---|---|---|
| Country | String | Country associated with the transaction | Used for geographic analysis | No | India |
| Region | String | Business region | Used to compare regional performance | No | West |
| State | String | State associated with the transaction | Used for state-level analysis | No | Maharashtra |
| City Type | String | Classification of the city | Used to compare city-level business performance | No | Metro |
| Outlet Type | String | Type of outlet | Used to compare outlet performance | No | Supermarket |
| Postal Code | String/Integer | Postal code associated with the location | Used for geographic identification | Yes | 400001 |

---

## 6. Date and Analytical Fields

| Column Name | Data Type | Description | Business Meaning | Nullable | Example |
|---|---|---|---|---|---|
| Order Year | Integer | Year extracted from Order Date | Used for yearly analysis | No | 2024 |
| Order Month | Integer | Month extracted from Order Date | Used for monthly analysis | No | 1 |
| Order Month Name | String | Name of the order month | Used for readable monthly analysis | No | January |
| Order Quarter | String | Quarter extracted from Order Date | Used for quarterly analysis | No | Q1 |

---

## Notes

The data dictionary is based on the verified dataset structure used
in the Consumer & Product Analytics Platform.

Data types and nullable status represent the analytical dataset after
data cleaning and validation.

Business meanings are aligned with the project's business rules and
analytical requirements.

`Profit Margin` is derived from Profit and Sales and is calculated
using:

```text
Profit Margin = SUM(Profit) / SUM(Sales)