
import pandas as pd


def normalize_order_items(df: pd.DataFrame) -> pd.DataFrame:
    """
    Chuẩn hóa tên cột của dữ liệu chi tiết đơn hàng.
    Không xóa dòng hoặc thay đổi giá trị gốc.
    """

    df = df.copy()

    column_mapping = {
        "order_id": "order_id",
        "product_id": "product_id",
        "so_luong": "quantity",
        "don_gia": "unit_price",
        "thanh_tien": "reported_sales_amount",
    }

    df = df.rename(columns=column_mapping)

    return df

def reconcile_sales(df: pd.DataFrame) -> pd.DataFrame:
    """
    Đối soát doanh thu:
    - Giữ nguyên thành tiền từ nguồn.
    - Tính thành tiền theo số lượng và đơn giá.
    - Ghi nhận chênh lệch, không tự sửa dữ liệu nguồn.
    """
    result = df.copy()

    result["calculated_sales_amount"] = (
        result["quantity"] * result["unit_price"]
    )

    result["difference_amount"] = (
        result["reported_sales_amount"]
        - result["calculated_sales_amount"]
    )

    result["reconciliation_status"] = "MATCH"

    result.loc[
        result["difference_amount"] != 0,
        "reconciliation_status"
    ] = "MISMATCH"

    return result
