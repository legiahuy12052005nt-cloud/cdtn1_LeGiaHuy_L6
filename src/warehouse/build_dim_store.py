
import pandas as pd


def build_dim_store(stores_df: pd.DataFrame) -> pd.DataFrame:
    """
    Xây dựng Dimension cửa hàng theo Star Schema BT1.

    Mỗi store_code tương ứng với một cửa hàng.
    store_key là khóa thay thế (surrogate key).
    """

    required_columns = [
        "store_code",
        "store_name",
        "thanh_pho",
        "quan_huyen",
    ]

    missing_columns = [
        col for col in required_columns
        if col not in stores_df.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Thiếu cột bắt buộc: {missing_columns}"
        )

    dim_store = stores_df[required_columns].copy()

    # Chuẩn hóa tên cột theo Star Schema
    dim_store = dim_store.rename(columns={
        "thanh_pho": "city",
        "quan_huyen": "district",
    })

    # Kiểm tra khóa nghiệp vụ
    if dim_store["store_code"].isna().any():
        raise ValueError("Phát hiện cửa hàng thiếu store_code")

    if dim_store["store_code"].duplicated().any():
        raise ValueError("Phát hiện store_code trùng lặp")

    # Sắp xếp để tạo surrogate key ổn định
    dim_store = (
        dim_store
        .sort_values("store_code")
        .reset_index(drop=True)
    )

    # Tạo khóa thay thế
    dim_store.insert(
        0,
        "store_key",
        range(1, len(dim_store) + 1)
    )

    return dim_store[
        [
            "store_key",
            "store_code",
            "store_name",
            "city",
            "district",
        ]
    ]
