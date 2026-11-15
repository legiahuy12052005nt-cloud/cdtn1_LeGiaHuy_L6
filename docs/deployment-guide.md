# DEPLOYMENT GUIDE – MEKONG MOBILE DATA WAREHOUSE

**Project:** Sales Data Warehouse and Revenue Analysis Dashboard for Mekong Mobile  
**Student:** Le Gia Huy  
**Student ID:** 2374802010175  
**Track:** DA – L6  
**Release Version:** v1.0  
**Repository:** https://github.com/legiahuy12052005nt-cloud/cdtn1_LeGiaHuy_L6

---

## 1. Prerequisites

### 1.1. Required Software

The project uses Docker to build and run the ETL pipeline.

The following tools are required:

| Software | Purpose |
|---|---|
| Git | Download the project from GitHub |
| Docker Engine or Docker Desktop | Build and run the ETL container |
| Docker Compose V2 | Run the ETL service |
| Internet connection | Download the source code and Docker dependencies |

The Docker Image uses **Python 3.10.11**.

Python does not need to be installed on the host machine when running the project with Docker.

To check Docker:

`docker --version`

To check Docker Compose:

`docker compose version`

At least 2 GB of free disk space is recommended for the development environment.

### 1.2. Network Ports

The ETL pipeline runs as a batch-processing application.

It does not provide a web server or REST API. Therefore, no application HTTP port is required.

### 1.3. Tested Environment

Docker deployment has been successfully tested using **GitHub Actions on Ubuntu Linux**.

The following operations were verified:

- Docker Image build.
- ETL execution using sample CSV files.
- SQLite Data Warehouse creation.
- Database record count verification.
- ETL rerun without duplicated Fact records.
- Automated pytest execution inside Docker.

A separate GitHub Actions workflow also verified the clean clone of Git tag `v1.0` and Docker execution.

Docker Desktop execution on the local Windows development computer has not been verified successfully.

---

## 2. Installation and Deployment

### 2.1. Clone the Repository

The project is available in a public GitHub repository.

Clone the BT3 release:

`git clone --branch v1.0 https://github.com/legiahuy12052005nt-cloud/cdtn1_LeGiaHuy_L6.git`

Move to the project directory:

`cd cdtn1_LeGiaHuy_L6`

The `v1.0` tag refers to commit `61e34ba`.

Checking out a Git tag may display a detached HEAD message. This is normal and does not prevent the project from running.

### 2.2. Build and Run the ETL Pipeline

Run the following command from the project root directory:

`docker compose run --build --rm pipeline`

This command builds the Docker Image and executes the ETL pipeline.

The execution process includes:

1. Preparing the Python environment inside Docker.
2. Installing packages from `requirements.txt`.
3. Loading the included sample CSV files.
4. Extracting sales data.
5. Normalizing the input data.
6. Validating data quality rules.
7. Separating rejected records.
8. Reconciling reported and calculated sales amounts.
9. Creating Fact and Dimension tables.
10. Exporting Warehouse CSV files and creating the SQLite database.

The container exits after the ETL process finishes.

This is expected behavior because the project runs as a batch-processing application.

### 2.3. Deployment Files

| File | Description |
|---|---|
| `Dockerfile` | Defines the Python environment and application files |
| `docker-compose.yml` | Defines the ETL service and output volume mappings |
| `.dockerignore` | Excludes unnecessary files from the Docker build context |
| `.env.example` | Documents example configuration values |
| `requirements.txt` | Defines required Python packages |
| `run_etl.py` | Main entry point of the ETL pipeline |
| `src/` | Contains the Extract, Transform, Quality, and Load modules |
| `tests/` | Contains the automated pytest test suite |

The current Dockerfile includes the application source code, test suite, and sample data.

In particular, the test directory is included through:

`COPY tests/ ./tests/`

This allows pytest to run directly inside the Docker container.

---

## 3. Environment Variables and Configuration

### 3.1. Example Environment Variables

The repository contains an `.env.example` file describing the following variables:

| Variable | Description | Example Value | Required |
|---|---|---|---|
| `SOURCE_DIR` | Source data directory | `data/raw` | No |
| `OUTPUT_DIR` | Processed data directory | `data/processed` | No |
| `DWH_URL` | SQLite database location | `sqlite:///data/warehouse/mekong_mobile.db` | No |

### 3.2. Current Configuration Limitations

In release `v1.0`, the ETL pipeline uses relative paths defined in the source code.

The variables in `.env.example` are provided for documentation purposes.

Changing these variables does not currently update the ETL paths automatically.

Therefore, creating a `.env` file is not required to run the Docker sample deployment.

### 3.3. Configuration Security

Passwords, API keys, access tokens, and other confidential information must not be committed to the public repository.

The project uses Git and Docker exclusion rules to reduce the risk of exposing local configuration files.

The `.env` file is excluded from Git tracking through `.gitignore`.

These controls provide basic protection but do not replace a complete secret-scanning process.

---

## 4. Sample Data and Expected Output

### 4.1. Sample Input Files

The Docker deployment uses four sample CSV files located in:

`data/sample/`

The files are:

- `orders_2024_2026.csv`
- `order_items.csv`
- `products.csv`
- `stores.csv`

During the Docker Image build, these sample files are copied into `data/raw/` inside the container.

No manual CSV import is required.

The sample dataset is designed for deployment testing and does not represent the full sales dataset.

### 4.2. Generated Files

After a successful ETL execution, the system generates processed, rejected, and Warehouse data.

The main output paths are:

| Output | Location |
|---|---|
| Clean sales data | `data/processed/clean_order_items.csv` |
| Rejected sales records | `data/rejected/rejected_order_items.csv` |
| Date dimension | `data/warehouse/Dim_Date.csv` |
| Product dimension | `data/warehouse/Dim_Product.csv` |
| Store dimension | `data/warehouse/Dim_Store.csv` |
| Sales fact table | `data/warehouse/Fact_Sales.csv` |
| SQLite database | `data/warehouse/mekong_mobile.db` |

The output directories are mapped from the container to the host through Docker Compose.

### 4.3. Expected SQLite Record Counts

The expected results for the sample dataset are:

| SQLite Table | Expected Records |
|---|---:|
| `dim_date` | 3 |
| `dim_product` | 3 |
| `dim_store` | 2 |
| `fact_sales` | 4 |

These record counts apply only to the included sample dataset.

The full dataset is larger and is used separately for business analysis and data quality evaluation.

---

## 5. Deployment Verification

### 5.1. Verify ETL Completion

Run:

`docker compose run --build --rm pipeline`

A successful execution should finish without an unhandled error.

The ETL completion message is:

`=== HOAN THANH ETL ===`

The output database should be created at:

`data/warehouse/mekong_mobile.db`

### 5.2. Verify SQLite Data

Run the following command from the project root directory:

`docker compose run --rm pipeline python -c "import sqlite3; c=sqlite3.connect('data/warehouse/mekong_mobile.db'); print({t:c.execute('SELECT COUNT(*) FROM '+t).fetchone()[0] for t in ['dim_date','dim_product','dim_store','fact_sales']})"`

Expected output:

`{'dim_date': 3, 'dim_product': 3, 'dim_store': 2, 'fact_sales': 4}`

This command checks the record counts in the SQLite Data Warehouse.

### 5.3. Verify ETL Rerun

Run the pipeline again:

`docker compose run --rm pipeline`

After the second execution, verify the SQLite record counts again.

Expected behavior:

- The ETL process completes successfully.
- The SQLite database is generated correctly.
- The `fact_sales` table still contains 4 records.
- No duplicated sales records are introduced in the tested rerun scenario.

This verification confirms reproducible behavior for the sample dataset. It does not guarantee idempotency under every possible failure scenario.

### 5.4. Run Automated Tests Inside Docker

The automated tests are stored in the `tests/` directory.

The Docker Image includes this directory.

Run pytest inside Docker with:

`docker compose run --rm pipeline python -m pytest tests/ -v`

Expected behavior:

- Pytest discovers the available test cases.
- Test execution completes successfully.
- The test summary reports no failed tests.

The automated test suite covers data transformation, validation, reconciliation, and other implemented ETL rules.

The exact number of passed tests should be taken from the execution log.

### 5.5. GitHub Actions Verification

The project includes the workflow:

`.github/workflows/docker-test.yml`

The workflow performs the following operations:

1. Builds and runs the ETL Docker container.
2. Verifies the SQLite Warehouse tables.
3. Runs the ETL pipeline again.
4. Checks that the rerun does not duplicate Fact records.
5. Executes pytest inside the Docker container.

The updated workflow successfully completed on GitHub Actions.

The repository also contains the previously captured evidence:

`docs/evidence/docker_pass_BT3.PNG`

This screenshot represents an earlier Docker verification run. Detailed pytest results should be supported by the log of the updated workflow.

A separate GitHub Actions workflow was used to verify Docker execution from a clean clone of tag `v1.0`.

### 5.6. Power BI Dashboard

The Power BI template is located at:

`powerbi/Mekong_Mobile_Dashboard_BT2_Final.pbit`

The dashboard runs separately through Power BI Desktop on Windows.

It uses the generated Warehouse CSV files as its data source.

Docker is used to deploy the ETL pipeline and SQLite Warehouse only.

The Power BI interface is not included in the Docker container.

---

## 6. Security Checklist

The project includes a basic security review for the prototype.

| Security Item | Status | Explanation |
|---|---|---|
| Secrets management | Basic | `.env` is excluded from Git tracking. Complete Git history secret scanning has not been verified. |
| Input validation | Implemented | The pipeline validates required IDs, quantity, unit price, and sales amounts. Invalid data can be recorded as rejected records. |
| Authorization | Not applicable | The ETL prototype does not provide user login or public API endpoints. |
| Password and encryption | Not implemented | The local SQLite database is not encrypted. No production password management system is deployed. |
| Safe error handling | Partially implemented | The pipeline handles some missing, empty, and invalid input scenarios. Not all possible errors have been tested. |
| Secure logging | Partially implemented | ETL execution information is recorded, but complete log auditing for personal information has not been performed. |
| Dependency security | Basic verification | `pip-audit` was executed and the captured result did not identify known vulnerabilities in the checked dependencies at that time. |

### 6.1. Personal Data Protection

The analytical SQLite Warehouse contains four tables:

- `fact_sales`
- `dim_date`
- `dim_product`
- `dim_store`

The analytical schema does not include the source customer fields `ten_khach` and `so_dien_thoai`.

The `customers_raw.csv` file is not included in the public analytical pipeline.

This design reduces the exposure of direct customer identifiers in the analytical Warehouse.

However, it does not mean that every source file has been anonymized or that the prototype is ready for production security requirements.

### 6.2. Security Limitations

The current prototype has not implemented:

- SQLite database encryption.
- A production authentication and authorization system.
- Automated secret scanning across the complete Git history.
- Comprehensive Docker Image security auditing.
- Centralized secure logging.
- Production-grade backup and recovery.

These items should be considered in future development.

---

## 7. Deployment Status and Known Limitations

### 7.1. Deployment Status

**Status: SUCCESSFULLY VERIFIED ON GITHUB ACTIONS.**

The Docker-based ETL deployment has been successfully tested on Ubuntu Linux.

The verification confirms that the system can:

- Build and run the ETL container.
- Load the included sample data.
- Create the SQLite Data Warehouse.
- Verify the expected record counts.
- Rerun the ETL pipeline.
- Run automated pytest tests inside Docker.

### 7.2. Current Limitations

The following features are not included in release `v1.0`:

- Web-based application deployment.
- Scheduled ETL execution.
- Incremental data loading.
- Power BI deployment inside Docker.
- Encrypted SQLite storage.
- Production monitoring and alerting.

Docker Desktop was not successfully verified on the local Windows development environment. Docker verification was completed through GitHub Actions instead.

### 7.3. Conclusion

The Mekong Mobile prototype provides a reproducible Docker-based ETL deployment using sample sales data.

The system creates a SQLite Data Warehouse and supports automated verification through GitHub Actions.

The deployment is suitable for prototype demonstration and academic testing, subject to the documented security and operational limitations.
