
from pathlib import Path

import pandas as pd


def extract_csv(file_path: str | Path) -> pd.DataFrame:
    """
    Đọc file CSV và trả về dữ liệu dạng DataFrame.

    Nếu file không tồn tại hoặc không có cột dữ liệu,
    trả về thông báo lỗi rõ ràng cho người sử dụng.
    """
    file_path = Path(file_path)

    if not file_path.is_file():
        raise FileNotFoundError(f"Không tìm thấy file: {file_path}")

    try:
        df = pd.read_csv(file_path, low_memory=False)
    except pd.errors.EmptyDataError as exc:
        raise ValueError(
            f"File CSV rỗng hoặc không có cột dữ liệu: {file_path}"
        ) from exc

    print(f"Đã đọc {file_path.name}: {len(df)} dòng")

    return df
