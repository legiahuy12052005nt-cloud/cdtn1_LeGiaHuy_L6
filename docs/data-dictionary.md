# DATA DICTIONARY – MEKONG MOBILE DATA WAREHOUSE

**Project:** Sales Data Warehouse and Revenue Analysis Dashboard for Mekong Mobile  
**Student:** Le Gia Huy  
**Student ID:** 2374802010175  
**Track:** DA – L6  
**Release:** v1.0  
**Repository:** https://github.com/legiahuy12052005nt-cloud/cdtn1_LeGiaHuy_L6

---

## 1. Introduction

### 1.1. Purpose

This document describes the data structure of the Mekong Mobile Sales Data Warehouse.

It provides the definitions, data types, constraints, valid values, nullability, sensitivity classification, and security handling of the analytical tables.

The Data Dictionary supports data consistency between the ETL pipeline, SQLite database, and Power BI Dashboard.

### 1.2. Data Warehouse Overview

The Data Warehouse follows a Star Schema with one Fact table and three Dimension tables.

| Table | Purpose | Number of Columns |
|---|---|---:|
| `fact_sales` | Stores sales details and reconciliation results | 12 |
| `dim_date` | Stores calendar information | 6 |
| `dim_product` | Stores product information | 5 |
| `dim_store` | Stores store information | 5 |
| **Total** | **4 analytical tables** | **28** |

The SQLite database is created at:

`data/warehouse/mekong_mobile.db`

The actual SQLite schema is defined in:

`src/warehouse/schema.sql`

### 1.3. Terminology

| Term | Meaning |
|---|---|
| Primary Key (PK) | Uniquely identifies each record in a table |
| Foreign Key (FK) | References a record in another table |
| UNIQUE | Prevents duplicate values in a defined column |
| NOT NULL | Requires a value to be present |
| CHECK | Validates values against a defined SQL condition |
| Surrogate Key | A technical identifier used in the Data Warehouse |
| Grain | The level of detail represented by one record |
| PII | Personally Identifiable Information |

### 1.4. Data Type Conventions

The implemented SQLite database mainly uses two data types:

- `INTEGER`: Used for numerical values, technical keys, quantities, and sales amounts.
- `TEXT`: Used for identifiers, descriptions, dates, and reconciliation statuses.

Earlier database design documents proposed types such as `BIGINT`, `VARCHAR`, and `DECIMAL`.

However, this document uses the actual data types implemented in SQLite release `v1.0`.

When pandas reads source CSV files, the inferred pandas data types may differ from SQLite storage types.

The implemented schema is the reference for database column definitions and constraints.

---

## 2. Fact_Sales Table

### 2.1. Purpose

The `fact_sales` table stores detailed sales transactions and supports revenue reconciliation.

Each row represents one product detail row from `order_items.csv`.

### 2.2. Grain and Source Data

**Grain:** One source order-item row.

The table is created using:

- `order_items.csv`
- `orders_2024_2026.csv`
- Product dimension keys
- Store dimension keys
- Date dimension keys

Each row is uniquely identified by `source_line_id`.

Fully duplicated source rows are preserved when no business rule confirms that they should be removed.

### 2.3. Column Definitions

| Column | SQLite Type | Description | Valid Values / Rules | Nullable | Classification | Security Handling |
|---|---|---|---|---|---|---|
| `sales_key` | INTEGER | Primary key of a sales record | Unique integer; PRIMARY KEY | No | Internal | Enforce primary key integrity |
| `source_line_id` | TEXT | Unique identifier of a source detail row | Non-empty, unique value | No | Internal | Restrict access to source-level identifiers |
| `order_id` | TEXT | Order identifier from source data | Non-empty text identifier | No | Internal | Do not publicly expose transaction identifiers |
| `date_key` | INTEGER | Foreign key to `dim_date` | Valid date key in YYYYMMDD format or NULL | Yes | Internal | Validate foreign key relationships |
| `product_key` | INTEGER | Foreign key to `dim_product` | Existing product key | No | Internal | Enforce foreign key integrity |
| `store_key` | INTEGER | Foreign key to `dim_store` | Existing store key | No | Internal | Enforce foreign key integrity |
| `quantity` | INTEGER | Quantity sold in the source detail row | Integer greater than 0 | No | Internal | Apply SQL CHECK constraint |
| `unit_price` | INTEGER | Unit selling price | Non-negative integer | No | Business-sensitive | Limit access to pricing data |
| `reported_sales_amount` | INTEGER | Sales amount reported by the source | Non-negative integer | No | Business-sensitive | Preserve original value and restrict access |
| `calculated_sales_amount` | INTEGER | Sales amount calculated by the ETL pipeline | `quantity * unit_price` | No | Business-sensitive | Verify calculation against source fields |
| `difference_amount` | INTEGER | Difference between reported and calculated amounts | Negative, zero, or positive integer | No | Business-sensitive | Preserve difference for reconciliation |
| `reconciliation_status` | TEXT | Result of sales amount reconciliation | `MATCH` or `MISMATCH` | No | Internal | Validate allowed status values |

**Total columns: 12.**

### 2.4. Implemented Constraints

The SQLite schema includes:

- `sales_key`: PRIMARY KEY.
- `source_line_id`: NOT NULL, UNIQUE.
- `order_id`: NOT NULL.
- `date_key`: Nullable FOREIGN KEY.
- `product_key`: NOT NULL, FOREIGN KEY.
- `store_key`: NOT NULL, FOREIGN KEY.
- `quantity`: NOT NULL, CHECK greater than 0.
- `unit_price`: NOT NULL, CHECK greater than or equal to 0.
- `reported_sales_amount`: NOT NULL, CHECK greater than or equal to 0.
- `calculated_sales_amount`: NOT NULL.
- `difference_amount`: NOT NULL.
- `reconciliation_status`: NOT NULL, CHECK allowing only MATCH or MISMATCH.

The financial formulas are ETL business rules. They are not all independently enforced by SQLite CHECK constraints.

### 2.5. Sales Reconciliation Rules

The pipeline preserves the original reported sales amount.

The calculated amount is:

`calculated_sales_amount = quantity * unit_price`

The difference is:

`difference_amount = reported_sales_amount - calculated_sales_amount`

Reconciliation status:

- `MATCH`: The reported amount equals the calculated amount.
- `MISMATCH`: The reported amount differs from the calculated amount.

The original sales amount is not automatically replaced when a mismatch is found.

### 2.6. Duplicate Source Records

The full source dataset contains 11 completely duplicated order-item rows.

These rows are preserved in the analytical Fact table because there is no confirmed business rule requiring their removal.

The `source_line_id` distinguishes individual source detail rows.

The system does not treat a repeated `ma_don` value as proof of a duplicated order, according to BR06.

### 2.7. Missing Sales Dates

Some source orders do not have a valid sales date.

The pipeline does not create an artificial date.

For these records:

`date_key = NULL`

The records are preserved in `fact_sales`.

They remain part of overall revenue calculations that do not require a date filter.

However, they cannot be assigned to a specific day, month, quarter, or year without additional source information.

---

## 3. Dim_Date Table

### 3.1. Purpose

The `dim_date` table supports time-based sales analysis.

It provides calendar attributes for valid sales dates.

### 3.2. Grain

**Grain:** One valid calendar date.

Each date appears once in the table.

### 3.3. Column Definitions

| Column | SQLite Type | Description | Valid Values / Rules | Nullable | Classification | Security Handling |
|---|---|---|---|---|---|---|
| `date_key` | INTEGER | Primary key representing a calendar date | Valid YYYYMMDD integer; unique | No | Internal | Enforce primary key integrity |
| `full_date` | TEXT | Full calendar date | Valid normalized date string | No | Internal | Validate date formatting |
| `day` | INTEGER | Day of the month | 1–31, consistent with the actual date | No | Internal | Validate date components |
| `month` | INTEGER | Month of the year | 1–12 | No | Internal | Validate value range |
| `quarter` | INTEGER | Calendar quarter | 1–4 | No | Internal | Check consistency with month |
| `year` | INTEGER | Calendar year | Year derived from the normalized source date | No | Internal | Check consistency with the full date |

**Total columns: 6.**

### 3.4. Source and Transformation Rules

The source date comes from the `ngay` column in `orders_2024_2026.csv`.

The ETL pipeline:

1. Reads the original sales date.
2. Normalizes supported date formats.
3. Converts valid dates into a consistent format.
4. Creates a numeric `date_key` using YYYYMMDD.
5. Extracts day, month, quarter, and year.
6. Creates one Dimension record for each valid date.

Missing or unparseable dates are not replaced with invented calendar values.

### 3.5. Implemented Constraints

- `date_key`: PRIMARY KEY.
- `full_date`: NOT NULL.
- `day`: NOT NULL.
- `month`: NOT NULL.
- `quarter`: NOT NULL.
- `year`: NOT NULL.

Detailed date-range checks are handled by ETL and data validation logic rather than independent SQL CHECK constraints for every date attribute.

---

## 4. Dim_Product Table

### 4.1. Purpose

The `dim_product` table stores information used to analyze revenue by product, brand, and product category.

### 4.2. Grain

**Grain:** One unique product.

The source is:

`products.csv`

### 4.3. Column Definitions

| Column | SQLite Type | Description | Valid Values / Rules | Nullable | Classification | Security Handling |
|---|---|---|---|---|---|---|
| `product_key` | INTEGER | Surrogate primary key of a product | Unique integer; PRIMARY KEY | No | Internal | Enforce primary key integrity |
| `product_id` | TEXT | Product identifier from source data | Non-empty, unique text identifier | No | Internal | Apply UNIQUE constraint |
| `product_name` | TEXT | Product name | Text value or NULL | Yes | Internal | Use only for authorized analysis |
| `category` | TEXT | Product category | Text value or NULL | Yes | Internal | Control access to product data |
| `brand` | TEXT | Product brand | Text value or NULL | Yes | Internal | Control access to product data |

**Total columns: 5.**

### 4.4. Transformation Rules

The pipeline:

1. Reads product data from `products.csv`.
2. Normalizes the source column names.
3. Maintains one Dimension record for each product identifier.
4. Sorts product identifiers using the implemented ETL logic.
5. Generates `product_key` values as surrogate keys.

For the same source dataset and the same transformation rules, the generated keys are expected to remain consistent across repeated full-refresh executions.

### 4.5. Implemented Constraints

- `product_key`: PRIMARY KEY.
- `product_id`: NOT NULL, UNIQUE.
- `product_name`: Nullable.
- `category`: Nullable.
- `brand`: Nullable.

The SQLite schema does not enforce a fixed list of allowed product brands or categories.

---

## 5. Dim_Store Table

### 5.1. Purpose

The `dim_store` table stores store information used for sales analysis by store, city, and district.

### 5.2. Grain

**Grain:** One unique store.

The source is:

`stores.csv`

### 5.3. Column Definitions

| Column | SQLite Type | Description | Valid Values / Rules | Nullable | Classification | Security Handling |
|---|---|---|---|---|---|---|
| `store_key` | INTEGER | Surrogate primary key of a store | Unique integer; PRIMARY KEY | No | Internal | Enforce primary key integrity |
| `store_code` | TEXT | Store code from source data | Non-empty, unique text identifier | No | Internal | Apply UNIQUE constraint |
| `store_name` | TEXT | Store name | Text value or NULL | Yes | Internal | Limit access to business information |
| `city` | TEXT | City where the store operates | Text value or NULL | Yes | Internal | Use for authorized regional analysis |
| `district` | TEXT | District where the store operates | Text value or NULL | Yes | Internal | Use for authorized regional analysis |

**Total columns: 5.**

### 5.4. Transformation Rules

The pipeline:

1. Reads store data from `stores.csv`.
2. Normalizes source column names.
3. Maintains one Dimension record for each store code.
4. Sorts store codes according to the implemented ETL logic.
5. Generates `store_key` values.

For unchanged source data and transformation rules, the generated keys are expected to remain consistent during reruns.

### 5.5. Implemented Constraints

- `store_key`: PRIMARY KEY.
- `store_code`: NOT NULL, UNIQUE.
- `store_name`: Nullable.
- `city`: Nullable.
- `district`: Nullable.

---

## 6. Relationships Between Tables

The Data Warehouse uses a Star Schema.

The central `fact_sales` table references three Dimension tables.

| Fact Table | Foreign Key | Dimension Table | Primary Key | Relationship |
|---|---|---|---|---|
| `fact_sales` | `date_key` | `dim_date` | `date_key` | Many-to-one |
| `fact_sales` | `product_key` | `dim_product` | `product_key` | Many-to-one |
| `fact_sales` | `store_key` | `dim_store` | `store_key` | Many-to-one |

### 6.1. Relationship Rules

- Each sales detail row must reference an existing product.
- Each sales detail row must reference an existing store.
- Sales records with a valid date reference an existing Date Dimension row.
- Sales records with a missing date may keep `date_key = NULL`.

### 6.2. Foreign Key Verification

The SQLite database-building program uses:

`PRAGMA foreign_keys = ON`

The pipeline also uses:

`PRAGMA foreign_key_check`

These operations support foreign key enforcement and verification during SQLite processing.

The foreign key constraints are defined in `src/warehouse/schema.sql`.

### 6.3. Time-Based Analysis

Rows with a NULL `date_key` are not assigned to a calendar period.

They may still be included in overall revenue measures without time-based filtering.

This rule preserves original sales information without inventing missing dates.

---

## 7. ETL Verification Results

### 7.1. Full Dataset Record Counts

The following results were recorded for the full dataset.

| Metric | Result |
|---|---:|
| `fact_sales` rows | 35,697 |
| `dim_date` rows | 792 |
| `dim_product` rows | 320 |
| `dim_store` rows | 24 |
| `MATCH` rows | 35,177 |
| `MISMATCH` rows | 520 |
| Source orders with missing dates | 114 |
| Fact rows with NULL `date_key` | 154 |
| Fact rows with NULL `product_key` | 0 |
| Fact rows with NULL `store_key` | 0 |
| Completely duplicated source detail rows | 11 |

### 7.2. Source Data Preservation

The recorded verification results are:

| Verification Metric | Result |
|---|---:|
| Source order-item rows | 35,697 |
| Fact rows after ETL | 35,697 |
| Row count difference | 0 |
| Source reported sales amount | 415,773,438,750 VND |
| Fact reported sales amount | 415,773,438,750 VND |
| Reported revenue difference | 0 VND |

These results show that the recorded ETL execution preserved the source row count and total reported revenue.

They do not prove that every source field is correct.

### 7.3. Data Integrity Verification

| Verification Item | Recorded Result | Status |
|---|---|---|
| `fact_sales` primary key | 0 duplicates, 0 NULL | PASS |
| `dim_date` primary key | 0 duplicates, 0 NULL | PASS |
| `dim_product` primary key | 0 duplicates, 0 NULL | PASS |
| `dim_store` primary key | 0 duplicates, 0 NULL | PASS |
| `product_key` foreign key | 0 NULL, 0 invalid references | PASS |
| `store_key` foreign key | 0 NULL, 0 invalid references | PASS |
| `date_key` foreign key | 154 allowed NULL, 0 invalid references | PASS |
| `source_line_id` | 0 duplicates, 0 NULL | PASS |
| Sales reconciliation processing | 35,177 MATCH, 520 MISMATCH | PASS |

A PASS result means that the checked data meets the defined integrity or reconciliation rule.

For sales reconciliation, PASS means that the system correctly preserves and classifies the differences. It does not mean that all source sales amounts match calculated values.

### 7.4. Data Integrity Evidence

The repository contains data integrity verification logic at:

`src/quality/check_warehouse.py`

The previously captured evidence is located at:

`docs/evidence/warehouse_integrity_check.PNG`

The verification results originally recorded for the Warehouse CSV outputs are retained as development evidence.

SQLite constraints provide additional structural verification in BT3.

---

## 8. Data Quality Assessment

### 8.1. Three Quality Dimensions

BT3 includes a separate data quality assessment over 27 source columns.

The assessment program is:

`scripts/check_data_quality_bt3.py`

| Quality Dimension | PASS | FAIL | N/A |
|---|---:|---:|---:|
| Completeness | 26 | 1 | 0 |
| Validity | 27 | 0 | 0 |
| Consistency | 8 | 1 | 18 |

Detailed reports:

- `docs/evidence/data_quality_bt3.json`
- `docs/evidence/data_quality_bt3.csv`

### 8.2. Identified Issues

**Issue DQ-01: Employee Information Completeness**

- File: `orders_2024_2026.csv`
- Column: `nhan_vien`
- Completeness: 96.11%
- Threshold: 99%
- Result: FAIL

**Issue DQ-02: Sales Amount Consistency**

- File: `order_items.csv`
- Column: `thanh_tien`
- Consistency: 98.54%
- Threshold: 99%
- Matching rows: 35,177
- Mismatched rows: 520
- Result: FAIL

These issues are documented without automatically modifying the original source values.

### 8.3. Assessment Limitations

The quality assessment uses defined project-level thresholds.

Validity results are limited to the implemented rules.

For some text fields, validity checking focuses on non-empty values rather than complete business validation.

Columns without applicable consistency rules are marked `N/A`.

Therefore, the quality results describe the current scope of checking and should not be interpreted as proof of complete data accuracy.

---

## 9. Data Classification and Security

### 9.1. Classification Policy

The analytical data is classified into two main groups:

- **Internal:** Technical keys, product information, store information, and non-public transaction identifiers.
- **Business-sensitive:** Unit prices, reported sales amounts, calculated sales amounts, and reconciliation differences.

These classifications describe the intended handling of data.

They do not mean that SQLite currently provides column-level access control.

### 9.2. Personal Information

The source file `orders_2024_2026.csv` contains customer-related fields such as:

- `ten_khach`
- `so_dien_thoai`

These two fields are not included in the 28 columns of the analytical Star Schema.

The analytical Warehouse is designed to avoid directly exporting these customer identifiers.

However, the source CSV files may still contain personal information.

They require appropriate storage and access restrictions.

### 9.3. Security Handling

The recommended controls include:

1. Restrict access to real sales data.
2. Avoid publishing source CSV files containing customer information.
3. Preserve data integrity using defined SQL constraints.
4. Validate important numeric and identifier fields.
5. Protect business-sensitive sales amounts.
6. Exclude secret configuration files from version control.
7. Review security requirements before production deployment.

The current prototype has not implemented complete database encryption or production-grade role-based access control.

### 9.4. Implemented and Recommended Controls

| Control | Current Status |
|---|---|
| Primary key constraints | Implemented in SQLite |
| Foreign key constraints | Defined and checked in SQLite processing |
| UNIQUE constraints | Implemented for selected identifiers |
| NOT NULL constraints | Implemented for required columns |
| CHECK constraints | Implemented for selected values |
| Removal of direct customer identifiers from analytical schema | Implemented for `ten_khach` and `so_dien_thoai` |
| SQLite file encryption | Not implemented |
| Column-level user authorization | Not implemented |
| Production database access management | Not implemented |

---

## 10. SQLite Implementation and Verification

### 10.1. Database Implementation

The SQLite Data Warehouse is created by:

`src/warehouse/build_sqlite_dwh.py`

The table definitions are provided in:

`src/warehouse/schema.sql`

The database output is:

`data/warehouse/mekong_mobile.db`

The system uses PRIMARY KEY, FOREIGN KEY, UNIQUE, NOT NULL, and selected CHECK constraints.

### 10.2. Implemented Data Types

The actual SQLite schema uses:

| Data Category | SQLite Storage Type |
|---|---|
| Primary and foreign keys | INTEGER or TEXT, depending on the column |
| Product and store descriptions | TEXT |
| Date descriptions | TEXT |
| Quantities | INTEGER |
| Sales amounts | INTEGER |
| Reconciliation status | TEXT |

The original design proposed some different SQL types, including `DECIMAL(18,2)` and `VARCHAR`.

Those were design suggestions and are not the implemented SQLite column declarations.

### 10.3. Sample Dataset Verification

The Docker deployment uses a small sample dataset.

Expected output:

| SQLite Table | Expected Rows |
|---|---:|
| `dim_date` | 3 |
| `dim_product` | 3 |
| `dim_store` | 2 |
| `fact_sales` | 4 |

These counts are separate from the full-dataset results in Section 7.

### 10.4. Docker Verification

The ETL application was successfully executed using Docker on GitHub Actions Ubuntu Linux.

The verification included:

- Building the Docker Image.
- Running the ETL pipeline.
- Creating SQLite tables.
- Checking expected record counts.
- Running the pipeline again.
- Running pytest inside Docker.

A separate workflow also verified a clean clone of Git tag `v1.0`.

Docker Desktop execution on the local Windows computer was not successfully verified.

---

## 11. Current Limitations and Future Improvements

### 11.1. Current Limitations

The current implementation has the following limitations:

- SQLite is a file-based database rather than a database server.
- The ETL pipeline uses batch processing.
- Incremental Loading is not implemented.
- Slowly Changing Dimensions are not implemented.
- Production scheduling is not available.
- SQLite file encryption is not implemented.
- Complete user authorization and access control are not implemented.
- Some source data quality issues remain unresolved.
- Power BI runs outside the Docker ETL container.

### 11.2. Future Improvements

Future development may include:

1. Support for Incremental Loading.
2. Automated ETL scheduling.
3. Improved data quality monitoring.
4. More detailed sales mismatch investigation.
5. Database security and access management.
6. Historical tracking for changing Dimension attributes.
7. Deployment to a server-based data platform when required.

These items are future development options and are not presented as completed features.

---

## 12. Conclusion

The Mekong Mobile Data Warehouse contains four analytical tables with 28 columns.

The Data Dictionary describes each column using its implemented SQLite type, meaning, valid values, nullability, sensitivity classification, and security handling.

The full dataset verification recorded 35,697 Fact rows, including 35,177 matching sales amounts and 520 mismatched amounts.

The system preserves source sales amounts, supports data integrity checking, and avoids exporting the direct customer fields `ten_khach` and `so_dien_thoai` into the analytical Star Schema.

Docker execution has been successfully verified using GitHub Actions.

The current prototype is suitable for academic demonstration and further improvement, subject to the documented data quality, security, and deployment limitations.

**Related Documents**

- `docs/srs.md`
- `docs/pipeline-documentation.md`
- `docs/deployment-guide.md`
- `docs/security-checklist.md`
- `docs/evidence/data_quality_bt3.json`
- `src/warehouse/schema.sql`
