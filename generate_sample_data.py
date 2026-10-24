
import csv
from pathlib import Path

SAMPLE_DIR = Path("data/sample")
SAMPLE_DIR.mkdir(parents=True, exist_ok=True)


def write_csv(filename, columns, rows):
    file_path = SAMPLE_DIR / filename

    with file_path.open("w", newline="", encoding="utf-8-sig") as file:
        writer = csv.writer(file)
        writer.writerow(columns)
        writer.writerows(rows)

    print(f"Created: {file_path} ({len(rows)} rows)")


def main():
    write_csv(
        "stores.csv",
        [
            "store_id", "store_code", "store_name",
            "thanh_pho", "quan_huyen", "ngay_khai_truong"
        ],
        [
            ["ST001", "CH001", "Mekong Mobile Demo 1",
             "Can Tho", "Ninh Kieu", "2024-01-01"],
            ["ST002", "CH002", "Mekong Mobile Demo 2",
             "Ho Chi Minh", "Quan 1", "2024-02-01"],
        ],
    )

    write_csv(
        "products.csv",
        [
            "product_id", "product_code", "product_name",
            "thuong_hieu", "nhom_san_pham",
            "gia_niem_yet", "warranty_months"
        ],
        [
            ["P001", "SP001", "Dien thoai Demo A",
             "Brand A", "Dien thoai", 5000000, 12],
            ["P002", "SP002", "Tai nghe Demo B",
             "Brand B", "Phu kien", 500000, 6],
            ["P003", "SP003", "May tinh bang Demo C",
             "Brand C", "May tinh bang", 8000000, 12],
        ],
    )

    write_csv(
        "orders_2024_2026.csv",
        [
            "order_id", "ma_don", "ma_cua_hang", "ngay",
            "ten_khach", "so_dien_thoai", "thanh_tien",
            "nhan_vien", "ghi_chu"
        ],
        [
            ["O001", "DH001", "CH001", "2025-02-10",
             "Khach Demo 1", "0000000000", 5500000,
             "Nhan vien Demo", "Du lieu gia lap"],
            ["O002", "DH002", "CH002", "2025-03-15",
             "Khach Demo 2", "0000000000", 8000000,
             "Nhan vien Demo", "Du lieu gia lap"],
            ["O003", "DH003", "CH001", "2025-03-20",
             "Khach Demo 3", "0000000000", 10000000,
             "Nhan vien Demo", "Du lieu gia lap"],
        ],
    )

    write_csv(
        "order_items.csv",
        [
            "order_id", "product_id", "so_luong",
            "don_gia", "thanh_tien"
        ],
        [
            ["O001", "P001", 1, 5000000, 5000000],
            ["O001", "P002", 1, 500000, 500000],
            ["O002", "P003", 1, 8000000, 8000000],
            ["O003", "P001", 2, 5000000, 10000000],
        ],
    )

    print("\nSample data generated successfully!")


if __name__ == "__main__":
    main()
