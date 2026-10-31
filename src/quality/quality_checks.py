
import pandas as pd


def build_quality_result(df, mask):
    """Trả về số dòng lỗi và tỷ lệ lỗi (%)."""
    total_rows = len(df)
    error_count = int(mask.fillna(True).sum())

    error_rate = (
        round(error_count / total_rows * 100, 2)
        if total_rows > 0 else 0.0
    )

    return {
        "error_count": error_count,
        "error_rate": error_rate,
    }


def check_order_id(df):
    """Kiểm tra mã đơn hàng bị thiếu."""
    mask = df["order_id"].isna() | (
        df["order_id"].astype("string").str.strip() == ""
    )
    return build_quality_result(df, mask)


def check_product_id(df):
    """Kiểm tra mã sản phẩm bị thiếu."""
    mask = df["product_id"].isna() | (
        df["product_id"].astype("string").str.strip() == ""
    )
    return build_quality_result(df, mask)


def check_quantity(df):
    """Kiểm tra số lượng không hợp lệ."""
    quantity = pd.to_numeric(df["quantity"], errors="coerce")
    mask = quantity.isna() | (quantity <= 0)
    return build_quality_result(df, mask)


def check_unit_price(df):
    """Kiểm tra đơn giá không hợp lệ."""
    unit_price = pd.to_numeric(df["unit_price"], errors="coerce")
    mask = unit_price.isna() | (unit_price < 0)
    return build_quality_result(df, mask)


def check_reported_sales_amount(df):
    """Kiểm tra doanh thu báo cáo không hợp lệ."""
    amount = pd.to_numeric(
        df["reported_sales_amount"],
        errors="coerce"
    )
    mask = amount.isna() | (amount < 0)
    return build_quality_result(df, mask)
