# Data Quality Report

## Dataset

Indian Store Dataset

## Status

Data profiling, cleaning, and validation have been completed.

---

## 1. Structural Checks

The dataset was checked for:

- Row count
- Column count
- Data types
- Duplicate records
- Column structure

The processed dataset was validated against the expected
analytical structure.

---

## 2. Missing Value Checks

Missing values were analyzed across the dataset.

Columns with missing values were identified and reviewed during
the data cleaning process.

---

## 3. Duplicate Checks

The dataset was checked for duplicate records.

Duplicate records were reviewed during the cleaning and validation
process.

---

## 4. Data Type Checks

Column data types were profiled and validated.

The dataset contains:

- Numeric fields
- Categorical fields
- Date fields
- Identifier fields

Data types were standardized where required during cleaning.

---

## 5. Unique Value Checks

Categorical and identifier columns were analyzed for:

- Unique value counts
- Cardinality
- Potential identifier columns
- Unexpected categorical values

---

## 6. Invalid Value Checks

The dataset was checked for invalid or inconsistent values.

Validation included:

- Invalid numeric values
- Invalid categorical values
- Blank values
- Date inconsistencies
- Business-rule violations

---

## 7. Date Validation

Date fields were checked for valid date values.

The relationship between order date and ship date was also
validated.

Order dates occurring after ship dates were treated as
inconsistent records.

---

## 8. Numeric Validation

Numeric fields were reviewed for valid business values.

Important fields include:

- Sales
- Quantity
- Discount
- Profit
- Profit Margin

Negative profit values were not treated as invalid because they
represent legitimate loss-making transactions.

---

## 9. Business Validation

Business-level consistency checks were performed for:

- Customer information
- Product information
- Order information
- Sales values
- Profit values
- Discount values
- Profit Margin
- Date relationships

---

## 10. Validation Reports

The project generates validation reports for the processed dataset.

The reports include:

- Structural validation results
- Consistency validation results
- Business validation results
- Before-versus-after validation comparison

---

## 11. Final Assessment

The dataset has been profiled, cleaned, and validated for use in
the Consumer & Product Analytics Platform.

The validated data is suitable for downstream MySQL loading and
business analytics.

Data quality checks and validation results are stored in the
project reports directory.