
from pathlib import Path
import pandas as pd


def save_rejected_rows(
    rejected_df: pd.DataFrame,
    output_path: str = "data/rejected/rejected_order_items.csv"
) -> Path:
    """
    Lưu các dòng dữ liệu không hợp lệ ra file CSV,
    kèm theo lý do lỗi (reject_reason).
    """

    path = Path(output_path)

    # Tự động tạo thư mục nếu chưa tồn tại
    path.parent.mkdir(parents=True, exist_ok=True)

    if "reject_reason" not in rejected_df.columns:
        raise ValueError("Thiếu cột reject_reason")

    # Lưu CSV để phục vụ kiểm tra và truy vết
    rejected_df.to_csv(
        path,
        index=False,
        encoding="utf-8-sig"
    )

    print(f"Đã lưu {len(rejected_df)} dòng lỗi vào: {path}")

    return path
