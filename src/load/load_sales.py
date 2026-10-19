
from pathlib import Path

import pandas as pd


def load_clean_sales(
    df: pd.DataFrame,
    output_path: str = "data/processed/clean_order_items.csv"
) -> Path:
    """
    Lưu dữ liệu chi tiết đơn hàng hợp lệ
    sau bước Transform và Quality.
    """

    path = Path(output_path)

    # Tạo thư mục đầu ra nếu chưa tồn tại
    path.parent.mkdir(parents=True, exist_ok=True)

    # Xuất dữ liệu ra CSV
    df.to_csv(
        path,
        index=False,
        encoding="utf-8-sig"
    )

    print(f"Đã lưu {len(df)} dòng dữ liệu hợp lệ vào: {path}")

    return path
