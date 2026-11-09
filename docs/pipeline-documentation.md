
# ETL Pipeline Documentation – Mekong Mobile

## 1. Pipeline Overview

The Mekong Mobile ETL pipeline processes sales data from CSV files and builds a SQLite Data Warehouse using a Star Schema.

The pipeline is implemented in Python 3.10.11 with pandas.

### Pipeline Flow

```text
CSV Source Files
       |
       v
Extract
       |
       v
Normalize and Transform
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
Processed Sales (CSV)
       |
       v
Build Dimensions and Fact
       |
       v
Warehouse CSV Files
       |
       v
SQLite Data Warehouse
       |
       v
Power BI Dashboard
```

The main entry point is `run_etl.py`.

## 2. Data Sources

The pipeline reads four primary CSV files.

| Source File | Description |
|---|---|
| `orders_2024_2026.csv` | Sales order information |
| `order_items.csv` | Sales order line items |
| `products.csv` | Product reference information |
| `stores.csv` | Store reference information |

The default input directory is `data/raw/`.

For Docker demonstration, the four sample files from `data/sample/` are copied into the container's `data/raw/` directory during image creation.

The `customers_raw.csv` dataset is not used by the current ETL pipeline.

## 3. Target Tables and Data Grain

The Data Warehouse follows a Star Schema with one Fact table and three Dimension tables.

| Target Table | Grain |
|---|---|
| `Fact_Sales` | One source sales order line item |
| `Dim_Date` | One valid calendar date |
| `Dim_Product` | One unique product |
| `Dim_Store` | One unique store |

The Fact table contains sales quantities, prices, calculated amounts, reported amounts, reconciliation differences, and Dimension keys.

The main output database is:

`data/warehouse/mekong_mobile.db`

CSV versions of the Warehouse tables are also generated in `data/warehouse/`.

Column definitions and constraints are documented in `docs/data-dictionary.md`.

## 4. Transformation and Data Quality

The pipeline performs the following operations:

1. Reads CSV files with pandas.
2. Normalizes sales order items.
3. Checks required identifiers and numeric fields.
4. Separates valid records from rejected records.
5. Calculates sales amounts and reconciliation differences.
6. Generates the Date, Product, and Store dimensions.
7. Builds the Fact table and links it to the dimensions.
8. Saves Warehouse CSV files.
9. Creates the SQLite database and checks foreign keys.

### Data Quality Rules

The pipeline checks:

- `order_id`
- `product_id`
- `quantity`
- `unit_price`
- `reported_sales_amount`

Invalid rows are written to:

`data/rejected/rejected_order_items.csv`

Valid processed rows are written to:

`data/processed/clean_order_items.csv`

Each rejected record includes a rejection reason.

The pipeline prints source, valid, and rejected row counts during execution.

### Reconciliation

The main formulas are:

- `calculated_sales_amount = quantity * unit_price`
- `difference_amount = reported_sales_amount - calculated_sales_amount`

Records are classified as `MATCH` or `MISMATCH`.

The original reported amount is preserved for auditability.

### Missing Dates and Duplicate Records

Records with missing dates may remain in Fact_Sales with a NULL date key according to the project's data rules.

Source rows are distinguished using `source_line_id`. Exact duplicate sales lines are not automatically discarded without an approved business rule.

## 5. Execution Schedule and Backfill

### Current Execution

The pipeline is currently a batch ETL process.

It is executed manually using Python or Docker Compose.

Docker execution command:

```bash
docker compose run --build --rm pipeline
```

No automated production scheduler is currently configured.

### Reprocessing and Backfill

When source CSV files are corrected or historical data needs to be reprocessed, the pipeline can be run again using the complete source dataset.

The current design uses full refresh rather than incremental loading.

Warehouse CSV files are regenerated, and the SQLite database is rebuilt from the processed Warehouse tables.

This approach avoids appending duplicate rows across repeated executions with unchanged input data.

The Docker demonstration uses bundled sample data. Processing a different dataset requires preparing the appropriate input files and deployment configuration.

## 6. Known Limitations

- The current pipeline uses local CSV files as data sources.
- The Warehouse is stored in SQLite rather than a server-based database.
- Incremental loading is not implemented.
- Automated scheduling and monitoring are not implemented.
- Slowly Changing Dimensions are not supported.
- SQLite does not provide built-in file encryption in this implementation.
- The Power BI dashboard runs separately from the Docker container.
- Docker container execution has not yet been verified in the current development environment.

## 7. Verification

The ETL pipeline should print:

```text
=== HOAN THANH ETL ===
```

The expected SQLite tables are:

- `dim_date`
- `dim_product`
- `dim_store`
- `fact_sales`

For the bundled sample data, expected table counts are:

| Table | Expected Rows |
|---|---:|
| dim_date | 3 |
| dim_product | 3 |
| dim_store | 2 |
| fact_sales | 4 |

The existing automated regression test suite contains 14 tests, which passed during BT3 preparation.

The Docker deployment remains pending real execution verification before the final release.
