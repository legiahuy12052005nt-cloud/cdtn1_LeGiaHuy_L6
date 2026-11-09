
# Deployment Guide – Mekong Mobile Data Warehouse

## 1. Prerequisites

The following tools are required:

- Git
- Docker Desktop with Docker Compose
- A Windows, Linux, or macOS computer that supports Docker

Python does not need to be installed on the host computer because the ETL pipeline runs inside a Docker container.

## 2. Configuration

The project uses Python 3.10.11 and SQLite.

The main configuration files are:

- `Dockerfile`: Builds the Python ETL environment.
- `docker-compose.yml`: Defines the ETL service and output volumes.
- `.dockerignore`: Excludes unnecessary and sensitive files.
- `.env.example`: Documents the project's data paths.

The current ETL version uses fixed relative paths. Values in `.env.example` are for reference and do not change the ETL behavior.

The Docker image includes sample CSV files for demonstration.

## 3. Installation

Clone the public GitHub repository and enter the project folder:

```bash
git clone https://github.com/legiahuy12052005nt-cloud/cdtn1_LeGiaHuy_L6.git
cd cdtn1_LeGiaHuy_L6
```

Build the Docker image:

```bash
docker compose build
```

## 4. Run the ETL Pipeline

Run the pipeline:

```bash
docker compose run --rm pipeline
```

The pipeline performs the following operations:

1. Extracts CSV source data.
2. Normalizes sales records.
3. Validates data quality.
4. Saves rejected records.
5. Reconciles sales amounts.
6. Builds Dimension and Fact tables.
7. Creates the SQLite Data Warehouse.

Generated files are stored in:

- `data/processed/`
- `data/rejected/`
- `data/warehouse/`

The ETL pipeline can be executed again using the same command. Output files are regenerated rather than appended.

## 5. Verify the Deployment

After running the ETL pipeline, verify that the following files exist:

- `data/processed/clean_order_items.csv`
- `data/rejected/rejected_order_items.csv`
- `data/warehouse/Dim_Date.csv`
- `data/warehouse/Dim_Product.csv`
- `data/warehouse/Dim_Store.csv`
- `data/warehouse/Fact_Sales.csv`
- `data/warehouse/mekong_mobile.db`

The pipeline should finish with:

```text
=== HOAN THANH ETL ===
```

Check the terminal output for source rows, valid rows, rejected rows, and Warehouse table counts.

For the supplied sample dataset, the expected Warehouse row counts are:

| Table | Expected Rows |
|---|---:|
| Dim_Date | 3 |
| Dim_Product | 3 |
| Dim_Store | 2 |
| Fact_Sales | 4 |

The Power BI dashboard template is available at:

`powerbi/Mekong_Mobile_Dashboard_BT2_Final.pbit`

Power BI Desktop runs separately on Windows. It is not included in the Docker container.

**Deployment status: VERIFIED**

The ETL pipeline was successfully built and executed using Docker Compose on a clean Linux environment provided by GitHub Actions.

The following checks passed:

- Docker image build and ETL execution.
- SQLite Data Warehouse generation.
- Verification of all four Warehouse tables.
- ETL rerun with the same sample dataset.
- Verification that rerunning the pipeline does not duplicate sales records.

**Evidence:** `docs/evidence/docker_pass_BT3.PNG`

**CI workflow:** `.github/workflows/docker-test.yml`

This verification was performed on GitHub Actions. Docker Desktop execution on the local Windows development machine was not tested.
