
#!/usr/bin/env python3
"""
BT3 - Đánh giá chất lượng dữ liệu Mekong Mobile

Chương trình kiểm tra ba chiều chất lượng dữ liệu:
1. Completeness: Tính đầy đủ của dữ liệu.
2. Validity: Tính hợp lệ của dữ liệu.
3. Consistency: Tính nhất quán của dữ liệu.

Cách chạy từ thư mục gốc của dự án:
    python scripts/check_data_quality_bt3.py

Lưu ý:
- Không chỉnh sửa hoặc ghi đè các file CSV nguồn.
- Không xuất tên khách hàng hoặc số điện thoại thực tế.
- Các ngưỡng đánh giá được đề xuất cho đồ án,
  không phải tiêu chuẩn chính thức của Mekong Mobile.
"""

import csv
import json
from collections import Counter
from datetime import datetime
from decimal import Decimal, InvalidOperation
from pathlib import Path


# ============================================================
# 1. CẤU HÌNH ĐƯỜNG DẪN VÀ DANH SÁCH CỘT
# ============================================================

# Thư mục chứa dữ liệu gốc và thư mục lưu minh chứng.
DATA_DIR = Path("data/raw")
OUTPUT_DIR = Path("docs/evidence")

# Danh sách bốn file CSV và các cột bắt buộc.
FILES = {
    "orders_2024_2026.csv": [
        "order_id",
        "ma_don",
        "ma_cua_hang",
        "ngay",
        "ten_khach",
        "so_dien_thoai",
        "thanh_tien",
        "nhan_vien",
        "ghi_chu",
    ],
    "order_items.csv": [
        "order_id",
        "product_id",
        "so_luong",
        "don_gia",
        "thanh_tien",
    ],
    "products.csv": [
        "product_id",
        "product_code",
        "product_name",
        "thuong_hieu",
        "nhom_san_pham",
        "gia_niem_yet",
        "warranty_months",
    ],
    "stores.csv": [
        "store_id",
        "store_code",
        "store_name",
        "thanh_pho",
        "quan_huyen",
        "ngay_khai_truong",
    ],
}

# Các định dạng ngày được chấp nhận trong dữ liệu nguồn.
DATE_FORMATS = (
    "%Y-%m-%d",
    "%d/%m/%Y",
    "%Y/%m/%d",
    "%d-%m-%y",
    "%d-%m-%Y",
    "%d/%m/%y",
    "%Y.%m.%d",
)


# ============================================================
# 2. CẤU HÌNH NGƯỠNG CHẤT LƯỢNG DỮ LIỆU
# ============================================================

# Ngưỡng mặc định cho ba chiều chất lượng.
# Đơn vị: phần trăm (%).
DEFAULT_COMPLETENESS = 99.0
DEFAULT_VALIDITY = 99.0
DEFAULT_CONSISTENCY = 99.0

# Ngưỡng Completeness riêng cho một số cột.
# Sử dụng cả tên file và tên cột để tránh nhầm lẫn
# giữa những cột trùng tên trong các bảng khác nhau.
COMPLETENESS_THRESHOLDS = {
    ("orders_2024_2026.csv", "ngay"): 99.0,
    ("orders_2024_2026.csv", "thanh_tien"): 98.0,
    ("orders_2024_2026.csv", "so_dien_thoai"): 90.0,
    ("orders_2024_2026.csv", "ghi_chu"): 0.0,
}

# Có thể khai báo ngưỡng Validity riêng cho từng cột.
# Nếu không khai báo, chương trình dùng ngưỡng mặc định.
VALIDITY_THRESHOLDS = {}

# Có thể khai báo ngưỡng Consistency riêng cho từng cột.
# Nếu không khai báo, chương trình dùng ngưỡng
# được quy định trong từng phép kiểm tra.
CONSISTENCY_THRESHOLDS = {}


# ============================================================
# 3. HÀM ĐỌC VÀ CHUẨN HÓA DỮ LIỆU
# ============================================================

def is_missing(value):
    """Kiểm tra giá trị bị thiếu hoặc chỉ chứa khoảng trắng."""
    return value is None or not str(value).strip()


def normalize(value):
    """Chuẩn hóa giá trị về chuỗi và loại bỏ khoảng trắng dư."""
    return "" if is_missing(value) else str(value).strip()


def read_csv(path):
    """Đọc file CSV bằng UTF-8 và trả về tên cột, dữ liệu."""
    with path.open(
        "r", encoding="utf-8-sig", newline=""
    ) as file:
        reader = csv.DictReader(file)

        if reader.fieldnames is None:
            raise ValueError(f"File CSV thiếu dòng tiêu đề: {path}")

        return reader.fieldnames, list(reader)


def parse_decimal(value):
    """
    Chuyển giá trị thành số Decimal.

    Trả về None nếu dữ liệu không phải số hợp lệ.
    Decimal được dùng để tránh sai số số thực
    khi đối soát doanh thu.
    """
    try:
        number = Decimal(normalize(value))

        if not number.is_finite():
            return None

        return number
    except (InvalidOperation, ValueError):
        return None


# ============================================================
# 4. KIỂM TRA TÍNH HỢP LỆ - VALIDITY
# ============================================================

def is_nonnegative_number(value):
    """Kiểm tra giá trị là số lớn hơn hoặc bằng 0."""
    number = parse_decimal(value)
    return number is not None and number >= 0


def is_positive_integer(value):
    """Kiểm tra giá trị là số nguyên lớn hơn 0."""
    number = parse_decimal(value)

    return (
        number is not None
        and number > 0
        and number == number.to_integral_value()
    )


def is_nonnegative_integer(value):
    """Kiểm tra giá trị là số nguyên lớn hơn hoặc bằng 0."""
    number = parse_decimal(value)

    return (
        number is not None
        and number >= 0
        and number == number.to_integral_value()
    )


def is_valid_date(value):
    """
    Kiểm tra ngày theo các định dạng được hỗ trợ.

    Không chỉ kiểm tra cấu trúc chuỗi mà còn
    xác nhận ngày có tồn tại trên lịch hay không.
    """
    if is_missing(value):
        return False

    for date_format in DATE_FORMATS:
        try:
            datetime.strptime(
                normalize(value), date_format
            )
            return True
        except ValueError:
            continue

    return False


def validate_value(filename, column, value):
    """
    Kiểm tra tính hợp lệ của dữ liệu theo từng cột.

    - Số lượng phải là số nguyên dương.
    - Thời gian bảo hành phải là số nguyên không âm.
    - Giá và thành tiền phải là số không âm.
    - Ngày phải thuộc định dạng được hỗ trợ.
    - Các cột văn bản chỉ kiểm tra không rỗng.

    Chưa kiểm tra các quy tắc nghiệp vụ chuyên sâu
    cho những cột chưa có đặc tả tương ứng.
    """
    if is_missing(value):
        return False

    if column == "so_luong":
        return is_positive_integer(value)

    if column == "warranty_months":
        return is_nonnegative_integer(value)

    if column in (
        "don_gia",
        "thanh_tien",
        "gia_niem_yet",
    ):
        return is_nonnegative_number(value)

    if column in ("ngay", "ngay_khai_truong"):
        return is_valid_date(value)

    return True


# ============================================================
# 5. HÀM TÍNH TỶ LỆ VÀ ĐÁNH GIÁ PASS/FAIL
# ============================================================

def percentage(numerator, denominator):
    """
    Tính tỷ lệ phần trăm và làm tròn hai chữ số.

    Trả về None nếu không có dữ liệu để tính.
    """
    if denominator == 0:
        return None

    return round(numerator / denominator * 100, 2)


def status_for(rate, threshold):
    """
    Đánh giá kết quả so với ngưỡng.

    PASS: Đạt hoặc vượt ngưỡng.
    FAIL: Thấp hơn ngưỡng.
    N/A: Không có dữ liệu để đánh giá.
    """
    if rate is None:
        return "N/A"

    return "PASS" if rate >= threshold else "FAIL"


# ============================================================
# 6. KIỂM TRA TÍNH NHẤT QUÁN - CONSISTENCY
# ============================================================

def make_consistency_result(
    rule, checked, matched, threshold=DEFAULT_CONSISTENCY
):
    """Tạo kết quả chung cho một quy tắc Consistency."""
    rate = percentage(matched, checked)

    return {
        "rule": rule,
        "checked_rows": checked,
        "matched_rows": matched,
        "failed_rows": checked - matched,
        "rate_pct": rate,
        "threshold_pct": threshold,
        "status": status_for(rate, threshold),
    }


def check_unique(rows, column):
    """
    Kiểm tra tính duy nhất của mã định danh.

    Mỗi giá trị không rỗng phải xuất hiện đúng một lần.
    Các giá trị rỗng được đánh giá ở Completeness.
    """
    values = [
        normalize(row.get(column))
        for row in rows
        if not is_missing(row.get(column))
    ]

    counts = Counter(values)

    matched = sum(
        counts[value] == 1 for value in values
    )

    return make_consistency_result(
        f"{column} phải có giá trị duy nhất",
        len(values),
        matched,
        100.0,
    )


def check_foreign_key(
    child_rows,
    child_column,
    parent_rows,
    parent_column,
):
    """
    Kiểm tra khóa ngoại giữa hai bảng.

    Mỗi giá trị khóa ngoại không rỗng trong bảng con
    phải tồn tại ở cột khóa chính của bảng cha.
    """
    parent_values = {
        normalize(row.get(parent_column))
        for row in parent_rows
        if not is_missing(row.get(parent_column))
    }

    values = [
        normalize(row.get(child_column))
        for row in child_rows
        if not is_missing(row.get(child_column))
    ]

    matched = sum(
        value in parent_values for value in values
    )

    return make_consistency_result(
        f"{child_column} tham chiếu {parent_column}",
        len(values),
        matched,
    )


def check_sales_reconciliation(rows):
    """
    Đối soát doanh thu của từng dòng chi tiết bán hàng.

    Quy tắc:
        thanh_tien = so_luong * don_gia

    Phân loại:
    - Khớp: Thành tiền đúng với phép tính.
    - Chênh lệch: Thành tiền khác kết quả tính.
    - Không hợp lệ: Không thể tính do dữ liệu số sai.
    """
    matched = 0
    mismatched = 0
    invalid = 0

    for row in rows:
        quantity = parse_decimal(row.get("so_luong"))
        price = parse_decimal(row.get("don_gia"))
        amount = parse_decimal(row.get("thanh_tien"))

        if (
            quantity is None
            or price is None
            or amount is None
        ):
            invalid += 1
            continue

        if (
            not is_positive_integer(row.get("so_luong"))
            or price < 0
            or amount < 0
        ):
            invalid += 1
            continue

        if quantity * price == amount:
            matched += 1
        else:
            mismatched += 1

    result = make_consistency_result(
        "thanh_tien = so_luong * don_gia",
        len(rows),
        matched,
    )

    result["mismatched_amount_rows"] = mismatched
    result["invalid_numeric_rows"] = invalid

    return result


def build_consistency_checks(data):
    """
    Xây dựng các phép kiểm tra nhất quán.

    Kiểm tra mã định danh, khóa ngoại và doanh thu
    dựa trên những quan hệ đã xác định được.

    Chưa kiểm tra ma_cua_hang vì cần xác nhận
    cột này liên kết với store_id hay store_code.
    """
    orders = data["orders_2024_2026.csv"]
    items = data["order_items.csv"]
    products = data["products.csv"]
    stores = data["stores.csv"]

    checks = {}

    def add(filename, column, result):
        """Lưu kết quả theo tên file và tên cột."""
        checks[(filename, column)] = result

    # Kiểm tra tính duy nhất của mã đơn hàng.
    add(
        "orders_2024_2026.csv",
        "order_id",
        check_unique(orders, "order_id"),
    )


    # BR02: Mã cửa hàng trong đơn hàng phải tồn tại
    # trong danh mục cửa hàng theo cột store_code.
    add(
        "orders_2024_2026.csv",
        "ma_cua_hang",
        check_foreign_key(
            orders,
            "ma_cua_hang",
            stores,
            "store_code",
        ),
    )

    # Kiểm tra khóa liên kết của bảng chi tiết đơn hàng.
    add(
        "order_items.csv",
        "order_id",
        check_foreign_key(
            items, "order_id", orders, "order_id"
        ),
    )

    add(
        "order_items.csv",
        "product_id",
        check_foreign_key(
            items, "product_id", products, "product_id"
        ),
    )

    # Kiểm tra đối soát doanh thu.
    add(
        "order_items.csv",
        "thanh_tien",
        check_sales_reconciliation(items),
    )

    # Kiểm tra tính duy nhất của mã sản phẩm.
    add(
        "products.csv",
        "product_id",
        check_unique(products, "product_id"),
    )

    add(
        "products.csv",
        "product_code",
        check_unique(products, "product_code"),
    )

    # Kiểm tra tính duy nhất của mã cửa hàng.
    add(
        "stores.csv",
        "store_id",
        check_unique(stores, "store_id"),
    )

    add(
        "stores.csv",
        "store_code",
        check_unique(stores, "store_code"),
    )

    return checks


# ============================================================
# 7. CHƯƠNG TRÌNH CHÍNH - ĐÁNH GIÁ CHẤT LƯỢNG DỮ LIỆU
# ============================================================

def main():
    data = {}
    results = []

    # Bước 1: Đọc và kiểm tra cấu trúc bốn file CSV.
    for filename, expected_columns in FILES.items():
        path = DATA_DIR / filename

        if not path.is_file():
            raise FileNotFoundError(
                f"Không tìm thấy file dữ liệu: {path}"
            )

        actual_columns, rows = read_csv(path)

        if not rows:
            raise ValueError(
                f"File CSV không có dữ liệu: {filename}"
            )

        missing_columns = [
            column
            for column in expected_columns
            if column not in actual_columns
        ]

        if missing_columns:
            raise ValueError(
                f"{filename} thiếu các cột: {missing_columns}"
            )

        data[filename] = rows

    # Bước 2: Tính các phép kiểm tra Consistency.
    # Chỉ kiểm tra các cột có quy tắc đối chiếu rõ ràng.
    consistency_checks = build_consistency_checks(data)

    # Bước 3: Kiểm tra Completeness và Validity cho 27 cột.
    for filename, columns in FILES.items():
        rows = data[filename]
        total = len(rows)

        for column in columns:
            values = [
                row.get(column)
                for row in rows
            ]

            # Lọc những giá trị không bị thiếu.
            present_values = [
                value
                for value in values
                if not is_missing(value)
            ]

            present = len(present_values)
            missing = total - present

            # Đếm số giá trị hợp lệ và không hợp lệ.
            valid = sum(
                validate_value(filename, column, value)
                for value in present_values
            )

            invalid = present - valid

            # Tính tỷ lệ dữ liệu đầy đủ và hợp lệ.
            completeness = percentage(present, total)
            validity = percentage(valid, present)

            key = (filename, column)

            # Lấy ngưỡng Completeness của từng cột.
            c_threshold = COMPLETENESS_THRESHOLDS.get(
                key, DEFAULT_COMPLETENESS
            )

            # Lấy ngưỡng Validity của từng cột.
            v_threshold = VALIDITY_THRESHOLDS.get(
                key, DEFAULT_VALIDITY
            )

            # Lấy kết quả Consistency nếu có quy tắc.
            consistency = consistency_checks.get(key)

            if consistency:
                consistency_rate = consistency["rate_pct"]
                consistency_rule = consistency["rule"]
                consistency_checked = consistency["checked_rows"]
                consistency_failed = consistency["failed_rows"]

                s_threshold = CONSISTENCY_THRESHOLDS.get(
                    key, consistency["threshold_pct"]
                )

                consistency_status = status_for(
                    consistency_rate, s_threshold
                )
            else:
                # N/A nghĩa là chưa có quy tắc kiểm tra phù hợp.
                # Không được xem N/A là PASS.
                consistency_rate = None
                consistency_rule = (
                    "N/A - Chưa xác định quy tắc đối chiếu"
                )
                consistency_checked = 0
                consistency_failed = 0
                s_threshold = None
                consistency_status = "N/A"

            # Lưu kết quả đánh giá của từng cột.
            results.append({
                "file": filename,
                "column": column,
                "total_rows": total,
                "present_rows": present,
                "missing_rows": missing,
                "completeness_pct": completeness,
                "completeness_threshold_pct": c_threshold,
                "completeness_status": status_for(
                    completeness, c_threshold
                ),
                "valid_rows": valid,
                "invalid_rows": invalid,
                "validity_pct": validity,
                "validity_threshold_pct": v_threshold,
                "validity_status": status_for(
                    validity, v_threshold
                ),
                "consistency_rule": consistency_rule,
                "consistency_checked_rows": consistency_checked,
                "consistency_failed_rows": consistency_failed,
                "consistency_pct": consistency_rate,
                "consistency_threshold_pct": s_threshold,
                "consistency_status": consistency_status,
            })

    # Bước 4: Tổng hợp chi tiết các phép kiểm tra nhất quán.
    # Chỉ lưu số liệu thống kê, không lưu dữ liệu cá nhân.
    consistency_details = []

    for (filename, column), check in consistency_checks.items():
        consistency_details.append({
            "file": filename,
            "column": column,
            **check,
        })

    # Bước 5: Thống kê số lượng PASS, FAIL và N/A.
    summary = {
        "files_checked": len(FILES),
        "columns_checked": len(results),
        "completeness": dict(
            Counter(
                row["completeness_status"]
                for row in results
            )
        ),
        "validity": dict(
            Counter(
                row["validity_status"]
                for row in results
            )
        ),
        "consistency": dict(
            Counter(
                row["consistency_status"]
                for row in results
            )
        ),
    }

    # Bước 6: Tạo nội dung báo cáo chất lượng dữ liệu.
    report = {
        "project": "Mekong Mobile",
        "assignment": "BT3",
        "track": "DA",
        "source": "Các file CSV nguồn tại data/raw",
        "threshold_note": (
            "Ngưỡng đánh giá đề xuất cho đồ án sinh viên, "
            "không phải tiêu chuẩn chính thức của doanh nghiệp."
        ),
        "validity_note": (
            "Validity được tính trên các giá trị không rỗng. "
            "Các cột văn bản chưa có quy tắc chuyên biệt "
            "chỉ được kiểm tra ở mức không rỗng."
        ),
        "consistency_note": (
            "Consistency chỉ được đo tại các cột có quan hệ "
            "đối chiếu đã xác định. N/A không được tính là PASS."
        ),
        "summary": summary,
        "column_quality": results,
        "consistency_checks": consistency_details,
    }

    # Bước 7: Tạo thư mục lưu minh chứng nếu chưa tồn tại.
    OUTPUT_DIR.mkdir(
        parents=True, exist_ok=True
    )

    json_path = OUTPUT_DIR / "data_quality_bt3.json"
    csv_path = OUTPUT_DIR / "data_quality_bt3.csv"

    # Bước 8: Xuất báo cáo chi tiết dưới dạng JSON.
    json_path.write_text(
        json.dumps(
            report,
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )

    # Bước 9: Xuất bảng tổng hợp 27 cột dưới dạng CSV.
    # UTF-8 BOM giúp Excel hiển thị tiếng Việt tốt hơn.
    with csv_path.open(
        "w", encoding="utf-8-sig", newline=""
    ) as file:
        writer = csv.DictWriter(
            file,
            fieldnames=list(results[0].keys()),
        )
        writer.writeheader()
        writer.writerows(results)

    # Bước 10: Hiển thị kết quả tổng hợp trên Terminal.
    print("=== KIỂM TRA CHẤT LƯỢNG DỮ LIỆU BT3 ===")
    print(f"Số file đã kiểm tra: {summary['files_checked']}")
    print(f"Số cột đã kiểm tra: {summary['columns_checked']}")

    print("\n=== TỔNG HỢP CHẤT LƯỢNG ===")

    for dimension in (
        "completeness",
        "validity",
        "consistency",
    ):
        print(
            f"{dimension}: {summary[dimension]}"
        )

    print("\n=== KIỂM TRA TÍNH NHẤT QUÁN ===")

    for item in consistency_details:
        print(
            f"{item['file']} | {item['column']} | "
            f"{item['rule']} | "
            f"{item['rate_pct']}% | "
            f"{item['status']} | "
            f"Số dòng lỗi: {item['failed_rows']}"
        )

    print("\n=== CÁC PHÉP KIỂM TRA KHÔNG ĐẠT ===")

    failures = 0

    for row in results:
        for dimension in (
            "completeness",
            "validity",
            "consistency",
        ):
            if row[f"{dimension}_status"] == "FAIL":
                failures += 1

                print(
                    f"{row['file']} | "
                    f"{row['column']} | "
                    f"{dimension.upper()} | "
                    f"{row[f'{dimension}_pct']}%"
                )

    if failures == 0:
        print("Không có phép kiểm tra nào bị FAIL.")

    print("\n=== FILE MINH CHỨNG ĐÃ XUẤT ===")
    print(json_path)
    print(csv_path)

    # Kết quả chất lượng dữ liệu có FAIL không đồng nghĩa
    # với việc chương trình Python chạy thất bại.
    # Các kết quả FAIL được giữ lại để báo cáo trung thực.


if __name__ == "__main__":
    main()
