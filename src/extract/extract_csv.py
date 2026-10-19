
from pathlib import Path

import pandas as pd


def extract_csv(file_path: str | Path) -> pd.DataFrame:
    """
    Đọc file CSV và trả về dữ liệu dạng DataFrame.
    """
    file_path = Path(file_path)

    if not file_path.is_file():
        raise FileNotFoundError(f"Không tìm thấy file: {file_path}")

    df = pd.read_csv(file_path, low_memory=False)

    print(f"Đã đọc {file_path.name}: {len(df)} dòng")

    return df
