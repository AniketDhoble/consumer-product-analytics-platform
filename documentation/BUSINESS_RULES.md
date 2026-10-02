
# Business Rules

## Purpose

This document defines the business rules used to calculate,
validate, and interpret analytical metrics in the
Consumer & Product Analytics Platform.

The rules are applied consistently across the data transformation,
MySQL analytical layer, and analytics modules.

---

## 1. Sales

Sales represents the monetary value of an order or sales transaction.

The `Sales` field from the source dataset is used as the primary
sales measure.

Sales is aggregated using:

```text
Total Sales = SUM(Sales)
```

---

## 2. Profit

Profit represents the amount earned or lost from a sales transaction.

The `Profit` field from the source dataset is used as the primary
profit measure.

Profit is aggregated using:

```text
Total Profit = SUM(Profit)
```

Negative profit values are valid business data and represent
loss-making transactions.

---

## 3. Profit Margin

Profit Margin shows how much profit is generated relative to sales.

Profit Margin is calculated using:

```text
Profit Margin = Total Profit / Total Sales
```

For aggregated data, the calculation is:

```text
Profit Margin = SUM(Profit) / SUM(Sales)
```

---

## 4. Customer Analysis

Customer analysis is based on the `Customer ID` field.

Customer performance is measured using:

- Total Orders
- Total Sales
- Total Quantity
- Total Profit
- Profit Margin
- Segment

Orders are counted using distinct `Order ID` values.

---

## 5. Product Analysis

Product analysis is based on the `Product ID` field.

Product performance is measured using:

- Total Orders
- Total Quantity
- Total Sales
- Total Profit
- Profit Margin
- Category
- Sub-Category
- Product Name

---

## 6. Regional Analysis

Regional analysis is based on the geographic fields available
in the dataset.

The main fields used are:

- Country
- Region
- State
- City Type
- Outlet Type
- Postal Code

Regional performance is measured using:

- Total Orders
- Total Sales
- Total Quantity
- Total Profit
- Profit Margin

---

## 7. Discount Analysis

Discount analysis is based on the `Discount` field.

The impact of discount is analyzed using:

- Sales
- Profit
- Profit Margin
- Loss-making transactions

High-discount transactions are analyzed separately to understand
their relationship with profitability.

---

## 8. Order Analysis

Order analysis is based on the `Order ID` field.

Order-level analysis includes:

- Sales
- Profit
- Quantity
- Discount
- Profit Margin
- Order Date
- Shipping information

Each order is identified using its `Order ID`.

---

## 9. Date Analysis

Date analysis is based on the order date.

The date dimension supports analysis by:

- Year
- Month
- Month Name
- Quarter
- Full Date

This allows sales and profitability to be analyzed over time.

---

## 10. Loss-Making Transactions

Transactions with negative profit are considered loss-making
transactions.

The rule is:

```text
Profit < 0 = Loss-making transaction
```

Negative-profit transactions are not removed during cleaning because
they represent valid business conditions.

They are analyzed separately to identify:

- Loss-making customers
- Loss-making products
- Loss-making regions
- High-discount loss-making orders

---

## 11. Data Validation

The dataset is validated before being loaded into the MySQL
analytical database.

Validation checks include:

- Row and column structure
- Missing values
- Duplicate records
- Date consistency
- Customer consistency
- Product consistency
- Numeric data quality
- Categorical data quality
- Business-rule consistency

---

## 12. Business Rule Governance

Business rules must be:

1. Documented
2. Reproducible
3. Consistent across the project
4. Based on verified dataset fields
5. Applied consistently in Python and SQL
6. Validated against the processed data


