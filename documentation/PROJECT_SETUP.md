# Project Setup

## Project Name

Consumer & Product Analytics Platform

## Project Type

Consumer and Product Analytics

## Objective

Analyze retail sales, customers, products, regions, discounts,
and profitability to identify actionable business insights.

## Technology Stack

- Python
- Pandas
- NumPy
- MySQL
- SQL
- Git/GitHub

## Architecture

Raw Data
→ Data Understanding
→ Data Profiling
→ Data Cleaning
→ Data Validation
→ MySQL
→ SQL Analysis
→ Analytics Modules
→ Business Insights

## Data Storage

- `datasets/raw/` — Original source data
- `datasets/interim/` — Temporary processing data
- `datasets/processed/` — Final cleaned and processed data
- `reports/` — Profiling and validation reports

## Development Approach

The original dataset will never be modified directly.

All transformations will be performed through Python processing
workflows and saved to appropriate output locations.

The processed data is validated before being loaded into MySQL.

Business analysis is performed using SQL and Python analytics modules.