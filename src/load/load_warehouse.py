
from pathlib import Path

import pandas as pd


def save_warehouse_table(
    df: pd.DataFrame,
    table_name: str,
    output_dir: str = "data/warehouse"
) -> Path:
    """
    Lưu bảng Dimension hoặc Fact thành CSV.

    Khi chạy lại, file cũ được thay thế bằng kết quả mới,
    không nối thêm dữ liệu gây trùng dòng.
    """

    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    file_path = output_path / f"{table_name}.csv"

    df.to_csv(
        file_path,
        index=False,
        encoding="utf-8-sig"
    )

    print(
        f"Đã lưu bảng {table_name}: "
        f"{len(df)} dòng -> {file_path}"
    )

    return file_path
