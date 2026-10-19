
import pandas as pd


def build_fact_sales(
    sales_df: pd.DataFrame,
    orders_df: pd.DataFrame,
    dim_date: pd.DataFrame,
    dim_product: pd.DataFrame,
    dim_store: pd.DataFrame,
) -> pd.DataFrame:
    """
    Xây dựng Fact_Sales theo grain:
    1 dòng Fact = 1 dòng chi tiết đơn hàng nguồn.

    Không xóa dòng trùng và không tự sửa giá trị tiền.
    """

    fact = sales_df.copy().reset_index(drop=True)
    source_count = len(fact)

    # Định danh mỗi dòng theo vị trí trong file nguồn.
    # Cần giữ nguyên thứ tự nguồn giữa các lần ETL.
    fact.insert(
        0,
        "source_line_id",
        [
            f"order_items.csv:{i}"
            for i in range(1, source_count + 1)
        ],
    )

    # Khóa riêng cho từng dòng Fact
    fact.insert(
        0,
        "sales_key",
        range(1, source_count + 1)
    )

    # Chuẩn bị đơn hàng và chuẩn hóa ngày
    orders = orders_df[
        ["order_id", "ma_cua_hang", "ngay"]
    ].copy()

    orders["full_date"] = pd.to_datetime(
        orders["ngay"],
        format="mixed",
        dayfirst=True,
        errors="coerce"
    ).dt.normalize()

    # Nối với đơn hàng
    fact = fact.merge(
        orders[["order_id", "ma_cua_hang", "full_date"]],
        on="order_id",
        how="left",
        validate="many_to_one",
        sort=False,
    )

    # Nối Dim_Product
    fact = fact.merge(
        dim_product[["product_id", "product_key"]],
        on="product_id",
        how="left",
        validate="many_to_one",
        sort=False,
    )

    # Nối Dim_Store
    fact = fact.merge(
        dim_store[["store_code", "store_key"]],
        left_on="ma_cua_hang",
        right_on="store_code",
        how="left",
        validate="many_to_one",
        sort=False,
    )

    # Nối Dim_Date
    fact = fact.merge(
        dim_date[["full_date", "date_key"]],
        on="full_date",
        how="left",
        validate="many_to_one",
        sort=False,
    )

    # Kiểm soát grain: không mất hoặc nhân đôi dòng
    if len(fact) != source_count:
        raise ValueError(
            "Số dòng Fact_Sales không khớp dữ liệu nguồn"
        )

    if fact["source_line_id"].duplicated().any():
        raise ValueError("source_line_id bị trùng")

    # Những khóa này phải liên kết thành công
    if fact["product_key"].isna().any():
        raise ValueError("Có dòng không tìm thấy sản phẩm")

    if fact["store_key"].isna().any():
        raise ValueError("Có dòng không tìm thấy cửa hàng")

    # Cho phép date_key trống với đơn thiếu ngày
    fact["date_key"] = fact["date_key"].astype("Int64")

    return fact[
        [
            "sales_key",
            "date_key",
            "product_key",
            "store_key",
            "order_id",
            "source_line_id",
            "quantity",
            "unit_price",
            "reported_sales_amount",
            "calculated_sales_amount",
            "difference_amount",
            "reconciliation_status",
        ]
    ]
