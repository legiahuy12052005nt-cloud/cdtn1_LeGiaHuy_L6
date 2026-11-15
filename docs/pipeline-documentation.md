# ETL PIPELINE DOCUMENTATION – MEKONG MOBILE DATA WAREHOUSE

**Project:** Sales Data Warehouse and Revenue Analysis Dashboard for Mekong Mobile  
**Student:** Le Gia Huy  
**Student ID:** 2374802010175  
**Track:** DA – L6  
**Release:** v1.0  
**Repository:** https://github.com/legiahuy12052005nt-cloud/cdtn1_LeGiaHuy_L6

---

## 1. Pipeline Overview

The Mekong Mobile project uses an ETL (Extract, Transform, Load) pipeline to process sales data from CSV files and build a SQLite Data Warehouse.

The pipeline is developed using Python 3.10.11 and pandas.

Its main purposes are to clean and validate sales data, reconcile sales amounts, handle invalid records, and prepare Fact and Dimension tables for analysis.

### 1.1. Pipeline Architecture

The data processing flow is:

```text
Source CSV Files
       |
       v
Extract Data
       |
       v
Transform and Normalize Data
       |
       v
Data Quality Validation
       |
       +------> Rejected Records (CSV)
       |
       v
Sales Reconciliation
       |
       v
Processed Sales Data (CSV)
       |
       v
Build Fact and Dimension Tables
       |
       v
Export Warehouse CSV Files
       |
       v
Load SQLite Data Warehouse
       |
       v
Power BI Dashboard
```

The main execution file is `run_etl.py`.

Power BI uses the exported Warehouse CSV files. It runs separately from the Docker ETL container.

### 1.2. Pipeline Objectives

The ETL pipeline is designed to:

1. Read sales data from four CSV files.
2. Normalize column names and data formats.
3. Validate important business rules.
4. Separate invalid records and record rejection reasons.
5. Preserve original reported sales amounts.
6. Calculate sales amounts for reconciliation.
7. Build Fact and Dimension tables.
8. Export analytical data to CSV and SQLite.
9. Support reproducible execution using sample data.

---

## 2. Source Data

### 2.1. Input Files

The pipeline uses four main CSV files.

| Source File | Description |
|---|---|
| `orders_2024_2026.csv` | Order information, sales dates, and store references |
| `order_items.csv` | Product details, quantities, prices, and reported sales amounts |
| `products.csv` | Product information and categories |
| `stores.csv` | Store information and locations |

The default source data directory is:

`data/raw/`

For Docker deployment, the sample CSV files from `data/sample/` are copied into the container during the Docker Image build.

The file `customers_raw.csv` is not used in the current analytical ETL pipeline.

### 2.2. Business Rules

The project follows the business rules documented in `docs/srs.md`.

| Rule | Description |
|---|---|
| BR02 | `orders.ma_cua_hang` must reference `stores.store_code`. |
| BR03 | `order_items.product_id` must reference `products.product_id`. |
| BR04 | Missing sales dates must not be replaced with invented dates. |
| BR05 | Original reported sales amounts must be preserved for reconciliation. |
| BR06 | `ma_don` must not be treated as a unique order identifier. |
| BR07 | Each source detail row must have a stable identifier. |
| BR08 | The number of orders must be calculated using `COUNT(DISTINCT order_id)`. |
| BR09 | Sales amount differences must be marked for reconciliation. |

These rules help preserve source data and ensure consistent analytical results.

---

## 3. Target Data Warehouse

### 3.1. Star Schema

The Data Warehouse uses a Star Schema with one Fact table and three Dimension tables.

| Table | Grain | Purpose |
|---|---|---|
| `fact_sales` | One source order-item row | Stores sales transactions and reconciliation results |
| `dim_date` | One valid calendar date | Supports time-based analysis |
| `dim_product` | One unique product | Supports product and category analysis |
| `dim_store` | One unique store | Supports store and location analysis |

The `fact_sales` table contains a stable `source_line_id` and references the Dimension tables through foreign keys.

A missing source sales date is not replaced with an artificial date. The corresponding `date_key` may remain NULL.

### 3.2. Warehouse Structure

The four tables contain 28 columns in total.

| Table | Number of Columns |
|---|---:|
| `fact_sales` | 12 |
| `dim_date` | 6 |
| `dim_product` | 5 |
| `dim_store` | 5 |
| **Total** | **28** |

The SQLite schema is defined in:

`src/warehouse/schema.sql`

The detailed descriptions of all 28 columns are maintained separately in:

`docs/data-dictionary.md`

### 3.3. Output Locations

| Output | Location |
|---|---|
| Processed sales data | `data/processed/clean_order_items.csv` |
| Rejected records | `data/rejected/rejected_order_items.csv` |
| Warehouse CSV files | `data/warehouse/` |
| SQLite database | `data/warehouse/mekong_mobile.db` |

The SQLite Warehouse contains the analytical tables used for data verification.

The Power BI Dashboard reads the Warehouse CSV files rather than connecting directly to SQLite.

---

## 4. Data Transformation and Quality Rules

### 4.1. Transformation Process

The pipeline performs the following operations:

1. Extracts data from the four source CSV files.
2. Normalizes column names and data types.
3. Checks required identifiers and numeric values.
4. Separates rejected records from accepted records.
5. Calculates sales amounts for reconciliation.
6. Normalizes valid sales dates.
7. Creates Product, Store, and Date dimensions.
8. Creates the Sales Fact table.
9. Exports Warehouse CSV files.
10. Loads the SQLite Data Warehouse.

### 4.2. Main Validation and Transformation Rules

| Field or Condition | Rule | Handling |
|---|---|---|
| `order_id` | Must contain a valid order identifier | Apply input validation rules |
| `product_id` | Must contain a valid product identifier | Apply input validation rules |
| `quantity` | Must be a positive number | Invalid values are handled by the quality checks |
| `unit_price` | Must be non-negative | Invalid values are handled by the quality checks |
| `reported_sales_amount` | Must be non-negative | Preserve valid source values |
| `ngay` | Normalize the source sales date | Do not create a date when the source date is missing |
| `ma_don` | Does not need to be unique | Preserve repeated values according to BR06 |
| `source_line_id` | Identifies a source detail row | Supports row preservation and repeated execution |
| Sales amount mismatch | Compare reported and calculated amounts | Mark as `MISMATCH`; do not overwrite the original amount |
| Fully duplicated source rows | No confirmed business rule for automatic removal | Do not remove automatically |

Rejected records are stored in:

`data/rejected/rejected_order_items.csv`

The rejected data includes information about the validation reason.

A revenue mismatch is not automatically classified as a rejected record.

### 4.3. Full Dataset Profile

The main dataset contains:

| Metric | Value |
|---|---:|
| Source orders | 26,000 |
| Order-item rows | 35,697 |
| Products | 320 |
| Stores | 24 |
| Orders with missing dates | 114 |
| Sales rows with matching amounts | 35,177 |
| Sales rows with mismatched amounts | 520 |

The analytical `fact_sales` table contains 35,697 rows in the verified full-dataset result.

The number of rejected rows must be checked from the ETL log and rejected CSV file for the same execution.

The figures above describe the full sales dataset. They must not be confused with the smaller Docker sample dataset.

### 4.4. Sales Reconciliation

The pipeline calculates the expected sales amount:

`calculated_sales_amount = quantity * unit_price`

It then calculates the difference:

`difference_amount = reported_sales_amount - calculated_sales_amount`

The reconciliation status is assigned as follows:

- `MATCH`: The reported amount equals the calculated amount.
- `MISMATCH`: The reported amount differs from the calculated amount.

The original `reported_sales_amount` is preserved.

The pipeline does not automatically change the original sales value to match the calculated amount.

### 4.5. Verification of BR05 and BR09

The sales reconciliation logic was verified using all 35,697 source order-item rows.

| Verification Item | Result |
|---|---|
| Total order-item rows | 35,697 |
| `MATCH` rows | 35,177 |
| `MISMATCH` rows | 520 |
| Preserve reported sales amount | PASS |
| Calculate expected sales amount | PASS |
| Calculate difference amount | PASS |
| Assign reconciliation status | PASS |

**Result: BR05 and BR09 functional verification passed.**

This result means that the reconciliation logic worked as expected.

It does not mean that every reported source sales amount was correct.

The 520 mismatched rows remain available for further business investigation.

### 4.6. Three Data Quality Dimensions

BT3 includes an additional data quality assessment program:

`scripts/check_data_quality_bt3.py`

This program evaluates 27 columns from the four source CSV files.

Three data quality dimensions are measured:

- **Completeness:** Checks whether required data values are present.
- **Validity:** Checks whether non-missing values meet the implemented validation rules.
- **Consistency:** Checks supported uniqueness rules, source relationships, and sales reconciliation.

The assessment results are:

| Data Quality Dimension | PASS | FAIL | N/A |
|---|---:|---:|---:|
| Completeness | 26 | 1 | 0 |
| Validity | 27 | 0 | 0 |
| Consistency | 8 | 1 | 18 |

`N/A` means that no applicable consistency rule was defined for that column. It must not be counted as PASS.

The thresholds are project-level assessment thresholds, not official quality standards issued by Mekong Mobile.

Detailed results are stored in:

- `docs/evidence/data_quality_bt3.json`
- `docs/evidence/data_quality_bt3.csv`

### 4.7. Identified Data Quality Issues

#### DQ-01: Missing Employee Information

| Attribute | Result |
|---|---|
| Source file | `orders_2024_2026.csv` |
| Column | `nhan_vien` |
| Completeness | 96.11% |
| Required threshold | 99% |
| Status | FAIL |

Some orders do not contain employee information.

This may affect reports that analyze sales performance by employee.

The missing values are reported rather than silently replaced.

#### DQ-02: Sales Amount Mismatch

| Attribute | Result |
|---|---|
| Source file | `order_items.csv` |
| Column | `thanh_tien` |
| Consistency | 98.54% |
| Required threshold | 99% |
| Matching rows | 35,177 |
| Mismatched rows | 520 |
| Status | FAIL |

The reported sales amounts do not match the calculated amounts in 520 rows.

The pipeline preserves the original amounts and records the differences.

The cause of these differences has not been confirmed.

They must not automatically be classified as discounts, taxes, or input errors without further evidence.

### 4.8. Data Quality Limitations

Validity checks are based on the rules implemented in the assessment script.

For text fields without specific format rules, validity is mainly evaluated using non-empty values.

Therefore, 27 PASS results for Validity do not prove that every field is fully correct in all business situations.

Columns without applicable Consistency rules are reported as `N/A`, not automatically treated as valid.

---

## 5. Data Protection and PII Handling

The source file `orders_2024_2026.csv` contains customer-related fields such as:

- `ten_khach`
- `so_dien_thoai`

These fields are not included in the 28-column analytical SQLite Star Schema.

The Warehouse stores the information needed for sales analysis without directly exporting these two customer identifiers.

The file `customers_raw.csv` is not part of the current analytical ETL pipeline.

This reduces the exposure of personal information in analytical outputs.

However, the source CSV files may still contain personal information and must be stored and shared carefully.

The current prototype does not provide complete data anonymization, database encryption, or production-grade access control.

### 5.1. Data Protection Verification

The analytical tables are:

- `fact_sales`
- `dim_date`
- `dim_product`
- `dim_store`

Their structures can be inspected using SQLite:

`PRAGMA table_info(fact_sales);`

The same check can be performed for each Dimension table.

The verification confirms that `ten_khach` and `so_dien_thoai` are not present in the analytical table definitions.

It does not prove that all source data has been anonymized.

---

## 6. Scheduling, Rerun, and Historical Data

### 6.1. Current Execution Model

The ETL pipeline uses batch processing.

It can be executed manually through Python or Docker Compose.

Docker execution command:

`docker compose run --build --rm pipeline`

An automated production schedule has not been implemented.

### 6.2. Full Refresh

The current pipeline uses a Full Refresh approach.

When the source dataset changes, the pipeline processes the available input files again and rebuilds the analytical outputs.

The project does not currently support Incremental Loading.

### 6.3. Rerun Verification

The ETL pipeline was tested by running the same sample dataset more than once.

The following behavior was verified:

- The ETL pipeline completed successfully.
- SQLite Warehouse tables were created.
- The second run did not increase the number of Fact rows.
- The sample `fact_sales` table still contained four rows.

**Result: PASS for the tested rerun scenario.**

This result does not guarantee correct behavior under every possible failure or recovery scenario.

### 6.4. Docker Sample Dataset

The Docker deployment uses the files in:

`data/sample/`

Expected SQLite results:

| Table | Expected Records |
|---|---:|
| `dim_date` | 3 |
| `dim_product` | 3 |
| `dim_store` | 2 |
| `fact_sales` | 4 |

The sample dataset is included for deployment verification.

It is separate from the full dataset used for Data Quality analysis.

### 6.5. Data Freshness

The project does not support real-time processing.

The Warehouse is updated only when the batch ETL pipeline runs.

There is no guaranteed production refresh schedule in the current prototype.

---

## 7. Deployment Verification, Risks, and Limitations

### 7.1. Deployment Verification

Docker execution was tested using GitHub Actions on Ubuntu Linux.

The verification covered:

1. Docker Image build.
2. ETL execution.
3. SQLite Warehouse creation.
4. Record counts of the four analytical tables.
5. ETL rerun without duplicated Fact rows.
6. Automated pytest execution inside Docker.

A separate GitHub Actions workflow also verified deployment from a clean clone of Git tag `v1.0`.

The Docker-based execution was successful in the tested GitHub Actions environment.

The latest detailed pytest count should be taken from the corresponding workflow log.

### 7.2. Automated Tests

The project includes a pytest suite in:

`tests/`

The current Dockerfile includes the test directory.

Run the tests inside Docker using:

`docker compose run --rm pipeline python -m pytest tests/ -v`

An earlier regression run recorded 14 passing tests.

Additional BT3 tests were later introduced, so the earlier count must not be presented as the result of the latest Docker run.

### 7.3. Current Risks and Limitations

| Limitation | Impact |
|---|---|
| Source data is stored in local CSV files | No automatic integration with external sales systems |
| SQLite is a file-based database | Limited suitability for large-scale concurrent production workloads |
| Full Refresh only | All available data is processed again during each ETL run |
| No production scheduler | Warehouse data does not refresh automatically |
| No Incremental Loading | New data cannot be loaded incrementally through the current implementation |
| No Slowly Changing Dimensions | Historical product and store attribute changes are not tracked through an SCD mechanism |
| No SQLite encryption | Database files require appropriate external protection |
| Power BI runs outside Docker | The dashboard is not automatically launched by the ETL container |
| 520 sales amount mismatches | Further business reconciliation may be required |
| Missing employee information | Employee-based analysis may be incomplete |
| Docker Desktop not verified on Windows | Docker evidence currently comes from GitHub Actions on Ubuntu Linux |

### 7.4. Evidence and Supporting Files

| Evidence | Repository Path |
|---|---|
| Docker verification screenshot | `docs/evidence/docker_pass_BT3.PNG` |
| Docker testing workflow | `.github/workflows/docker-test.yml` |
| Three-dimension quality results (JSON) | `docs/evidence/data_quality_bt3.json` |
| Three-dimension quality results (CSV) | `docs/evidence/data_quality_bt3.csv` |
| Data quality assessment script | `scripts/check_data_quality_bt3.py` |
| Sales reconciliation logic | `src/transform/transform_sales.py` |
| SQLite schema | `src/warehouse/schema.sql` |
| Data Dictionary | `docs/data-dictionary.md` |
| Business requirements | `docs/srs.md` |
| Deployment Guide | `docs/deployment-guide.md` |

### 7.5. Conclusion

The Mekong Mobile ETL pipeline processes sales data from CSV files and generates analytical tables in CSV and SQLite formats.

The project includes data validation, rejected-record handling, sales reconciliation, and a three-dimension Data Quality assessment.

Docker deployment and automated testing have been successfully verified through GitHub Actions.

Two source data quality issues remain below their defined thresholds. These issues are documented instead of being hidden or automatically corrected.

The prototype is suitable for academic demonstration and further development, subject to the limitations described above.
