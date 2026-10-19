
from src.extract.extract_csv import extract_csv
from src.transform.transform_sales import (
    normalize_order_items,
    reconcile_sales,
)
from src.quality.validate_sales import validate_order_items
from src.quality.reject_logger import save_rejected_rows
from src.load.load_sales import load_clean_sales
from src.load.load_warehouse import save_warehouse_table

from src.warehouse.build_dim_date import build_dim_date
from src.warehouse.build_dim_product import build_dim_product
from src.warehouse.build_dim_store import build_dim_store
from src.warehouse.build_fact_sales import build_fact_sales


def main():
    print("=== BAT DAU QUY TRINH ETL ===")

    # BUOC 1: EXTRACT
    items = extract_csv("data/raw/order_items.csv")
    orders = extract_csv("data/raw/orders_2024_2026.csv")
    products = extract_csv("data/raw/products.csv")
    stores = extract_csv("data/raw/stores.csv")

    # BUOC 2: TRANSFORM
    normalized = normalize_order_items(items)

    # BUOC 3: QUALITY
    valid, rejected = validate_order_items(normalized)

    # BUOC 4: GHI ERROR LOG
    save_rejected_rows(rejected)

    # BUOC 5: DOI SOAT DOANH THU
    sales = reconcile_sales(valid)

    # BUOC 6: LUU DU LIEU TRUNG GIAN
    load_clean_sales(sales)

    # BUOC 7: XAY DUNG DIMENSION
    dim_date = build_dim_date(orders)
    dim_product = build_dim_product(products)
    dim_store = build_dim_store(stores)

    # BUOC 8: XAY DUNG FACT
    fact_sales = build_fact_sales(
        sales,
        orders,
        dim_date,
        dim_product,
        dim_store,
    )

    # BUOC 9: LUU STAR SCHEMA
    save_warehouse_table(dim_date, "Dim_Date")
    save_warehouse_table(dim_product, "Dim_Product")
    save_warehouse_table(dim_store, "Dim_Store")
    save_warehouse_table(fact_sales, "Fact_Sales")

    # BUOC 10: THONG KE KET QUA
    match_count = (
        fact_sales["reconciliation_status"] == "MATCH"
    ).sum()

    mismatch_count = (
        fact_sales["reconciliation_status"] == "MISMATCH"
    ).sum()

    print("\n=== KET QUA DATA WAREHOUSE ===")
    print(f"Tong dong nguon: {len(items)}")
    print(f"Dong hop le: {len(valid)}")
    print(f"Dong bi tu choi: {len(rejected)}")
    print(f"Dim_Date: {len(dim_date)}")
    print(f"Dim_Product: {len(dim_product)}")
    print(f"Dim_Store: {len(dim_store)}")
    print(f"Fact_Sales: {len(fact_sales)}")
    print(f"MATCH: {match_count}")
    print(f"MISMATCH: {mismatch_count}")
    print(
        "Fact thieu date_key:",
        fact_sales["date_key"].isna().sum(),
    )
    print("=== HOAN THANH ETL ===")


if __name__ == "__main__":
    main()
