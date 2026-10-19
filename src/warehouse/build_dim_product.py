
import pandas as pd


def build_dim_product(products_df: pd.DataFrame) -> pd.DataFrame:
    """
    Xây dựng Dimension sản phẩm theo Star Schema BT1.

    Mỗi product_id tương ứng với một sản phẩm.
    product_key là khóa thay thế (surrogate key).
    """

    required_columns = [
        "product_id",
        "product_name",
        "thuong_hieu",
        "nhom_san_pham",
    ]

    missing_columns = [
        col for col in required_columns
        if col not in products_df.columns
    ]

    if missing_columns:
        raise ValueError(f"Thiếu cột bắt buộc: {missing_columns}")

    dim_product = products_df[required_columns].copy()

    dim_product = dim_product.rename(columns={
        "thuong_hieu": "brand",
        "nhom_san_pham": "category",
    })

    # Không tự động xóa sản phẩm trùng hoặc thiếu mã.
    if dim_product["product_id"].isna().any():
        raise ValueError("Phát hiện sản phẩm thiếu product_id")

    if dim_product["product_id"].duplicated().any():
        raise ValueError("Phát hiện product_id trùng lặp")

    # Sắp xếp để tạo surrogate key ổn định khi chạy lại.
    dim_product = (
        dim_product
        .sort_values("product_id")
        .reset_index(drop=True)
    )

    dim_product.insert(
        0,
        "product_key",
        range(1, len(dim_product) + 1)
    )

    return dim_product[
        [
            "product_key",
            "product_id",
            "product_name",
            "category",
            "brand",
        ]
    ]
