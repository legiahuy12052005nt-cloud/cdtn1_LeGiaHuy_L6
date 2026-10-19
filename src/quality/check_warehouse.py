
import pandas as pd
from pathlib import Path

WAREHOUSE_DIR = Path("data/warehouse")

fact = pd.read_csv(WAREHOUSE_DIR / "fact_sales.csv")
dim_date = pd.read_csv(WAREHOUSE_DIR / "dim_date.csv")
dim_product = pd.read_csv(WAREHOUSE_DIR / "dim_product.csv")
dim_store = pd.read_csv(WAREHOUSE_DIR / "dim_store.csv")

print("=== 1. KIỂM TRA KHÓA CHÍNH (PK) ===")

tables = [
    ("Fact_Sales", fact, "sales_key"),
    ("Dim_Date", dim_date, "date_key"),
    ("Dim_Product", dim_product, "product_key"),
    ("Dim_Store", dim_store, "store_key"),
]

for table_name, df, key in tables:
    print(
        f"{table_name}: "
        f"PK trùng = {df[key].duplicated().sum()}, "
        f"PK NULL = {df[key].isna().sum()}"
    )

print("\n=== 2. KIỂM TRA KHÓA NGOẠI (FK) ===")

relationships = [
    ("date_key", dim_date, True),
    ("product_key", dim_product, False),
    ("store_key", dim_store, False),
]

for key, dimension, allow_null in relationships:
    missing = fact[key].isna().sum()
    invalid = (
        fact[key].notna()
        & ~fact[key].isin(dimension[key])
    ).sum()

    print(
        f"{key}: "
        f"NULL = {missing}, "
        f"FK không tồn tại = {invalid}, "
        f"Cho phép NULL = {allow_null}"
    )

print("\n=== 3. KIỂM TRA MÃ DÒNG NGUỒN ===")

print("source_line_id trùng =", fact["source_line_id"].duplicated().sum())
print("source_line_id NULL =", fact["source_line_id"].isna().sum())

print("\n=== 4. KIỂM TRA TRẠNG THÁI ĐỐI SOÁT ===")

print(fact["reconciliation_status"].value_counts(dropna=False))

print("\n=== HOÀN THÀNH KIỂM TRA ===")
