
from pathlib import Path
import sqlite3

import pandas as pd


WAREHOUSE_DIR = Path("data/warehouse")
DATABASE_PATH = WAREHOUSE_DIR / "mekong_mobile.db"
SCHEMA_PATH = Path("src/warehouse/schema.sql")

TABLES = [
    ("dim_date", "dim_date.csv"),
    ("dim_product", "dim_product.csv"),
    ("dim_store", "dim_store.csv"),
    ("fact_sales", "fact_sales.csv"),
]


def build_sqlite_dwh():
    # Kiểm tra đầy đủ file đầu vào trước khi tạo database
    required_files = [SCHEMA_PATH] + [
        WAREHOUSE_DIR / filename for _, filename in TABLES
    ]

    for path in required_files:
        if not path.is_file():
            raise FileNotFoundError(f"Không tìm thấy file: {path}")

    WAREHOUSE_DIR.mkdir(parents=True, exist_ok=True)

    # Đọc dữ liệu trước khi thay đổi database
    data = {}

    for table_name, filename in TABLES:
        df = pd.read_csv(WAREHOUSE_DIR / filename)

        # Chuyển các giá trị NaN thành None để SQLite lưu thành NULL
        df = df.astype(object).where(pd.notna(df), None)

        # Đảm bảo khóa liên kết ngày là số nguyên hoặc NULL
        if table_name == "fact_sales":
            df["date_key"] = df["date_key"].apply(
                lambda value: int(value) if value is not None else None
            )

        # Mã nguồn trong SQLite được lưu dạng TEXT
        if table_name == "dim_product":
            df["product_id"] = df["product_id"].map(
                lambda value: str(value) if value is not None else None
            )

        if table_name == "fact_sales":
            df["order_id"] = df["order_id"].map(
                lambda value: str(value) if value is not None else None
            )

        data[table_name] = df

    # Tạo database tạm để tránh làm hỏng database đang có
    temporary_path = DATABASE_PATH.with_suffix(".tmp.db")

    if temporary_path.exists():
        temporary_path.unlink()

    connection = sqlite3.connect(temporary_path)

    try:
        # Bật kiểm tra khóa ngoại
        connection.execute("PRAGMA foreign_keys = ON")

        # Tạo 4 bảng theo cấu trúc SQL đã thiết kế
        schema_sql = SCHEMA_PATH.read_text(encoding="utf-8")
        connection.executescript(schema_sql)

        # Nạp các bảng Dimension trước, Fact sau
        for table_name, _ in TABLES:
            df = data[table_name]

            df.to_sql(
                name=table_name,
                con=connection,
                if_exists="append",
                index=False,
            )

            print(f"{table_name}: {len(df):,} dòng")

        # Kiểm tra các liên kết khóa ngoại
        fk_errors = connection.execute(
            "PRAGMA foreign_key_check"
        ).fetchall()

        if fk_errors:
            raise ValueError(
                f"Phát hiện lỗi khóa ngoại: {fk_errors[:5]}"
            )

        connection.commit()
        connection.close()

        # Chỉ thay thế database cũ sau khi tạo thành công
        temporary_path.replace(DATABASE_PATH)

        print("\nKiểm tra khóa ngoại: PASS")
        print(f"SQLite DWH: {DATABASE_PATH}")
        print("Hoàn thành tạo Data Warehouse!")

    except Exception:
        connection.close()

        if temporary_path.exists():
            temporary_path.unlink()

        raise


if __name__ == "__main__":
    build_sqlite_dwh()
