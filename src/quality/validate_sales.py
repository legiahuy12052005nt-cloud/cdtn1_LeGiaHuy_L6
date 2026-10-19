
import pandas as pd


def validate_order_items(df: pd.DataFrame):
    """
    Kiểm tra chất lượng dữ liệu chi tiết đơn hàng.

    Trả về:
    - valid_df: Các dòng hợp lệ
    - rejected_df: Các dòng không hợp lệ và lý do lỗi
    """

    data = df.copy()

    required_columns = [
        "order_id",
        "product_id",
        "quantity",
        "unit_price",
        "reported_sales_amount",
    ]

    missing_columns = [
        col for col in required_columns if col not in data.columns
    ]

    if missing_columns:
        raise ValueError(f"Thiếu cột bắt buộc: {missing_columns}")

    # Kiểm tra giá trị số, không làm thay đổi dữ liệu gốc
    numeric_columns = [
        "quantity",
        "unit_price",
        "reported_sales_amount",
    ]

    numeric_values = {
        col: pd.to_numeric(data[col], errors="coerce")
        for col in numeric_columns
    }

    # Ghi lý do lỗi cho từng dòng
    reasons = [[] for _ in range(len(data))]

    for position in range(len(data)):
        row = data.iloc[position]

        if pd.isna(row["order_id"]):
            reasons[position].append("Thiếu order_id")

        if pd.isna(row["product_id"]):
            reasons[position].append("Thiếu product_id")

        quantity = numeric_values["quantity"].iloc[position]
        unit_price = numeric_values["unit_price"].iloc[position]
        reported_amount = numeric_values["reported_sales_amount"].iloc[position]

        if pd.isna(quantity) or quantity <= 0:
            reasons[position].append("Số lượng không hợp lệ")

        if pd.isna(unit_price) or unit_price < 0:
            reasons[position].append("Đơn giá không hợp lệ")

        if pd.isna(reported_amount) or reported_amount < 0:
            reasons[position].append("Thành tiền không hợp lệ")

    data["reject_reason"] = [
        "; ".join(item) for item in reasons
    ]

    rejected_mask = data["reject_reason"] != ""

    valid_df = data.loc[~rejected_mask].drop(
        columns=["reject_reason"]
    ).copy()

    rejected_df = data.loc[rejected_mask].copy()

    return valid_df, rejected_df
