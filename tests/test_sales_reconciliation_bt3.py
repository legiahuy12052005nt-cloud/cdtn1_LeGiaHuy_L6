
import pandas as pd
from src.transform.transform_sales import (
    normalize_order_items,
    reconcile_sales,
)


def test_br05_br09_sales_reconciliation():
    """
    Kiểm tra BR05 và BR09:
    - Không thay đổi doanh thu nguồn.
    - Tính đúng doanh thu theo số lượng và đơn giá.
    - Đánh dấu MATCH nếu doanh thu khớp.
    - Đánh dấu MISMATCH nếu doanh thu chênh lệch.
    """

    # Tạo dữ liệu kiểm thử có cả dòng đúng và dòng lệch.
    source = pd.DataFrame({
        "order_id": [1, 2, 3],
        "product_id": [101, 102, 103],
        "so_luong": [2, 1, 3],
        "don_gia": [100000, 200000, 50000],
        "thanh_tien": [200000, 220000, 135000],
    })

    # Chuẩn hóa tên cột rồi thực hiện đối soát.
    normalized = normalize_order_items(source)
    result = reconcile_sales(normalized)

    # Số dòng phải được giữ nguyên.
    assert len(result) == 3

    # Thành tiền nguồn không được tự động chỉnh sửa.
    assert result["reported_sales_amount"].tolist() == [
        200000, 220000, 135000
    ]

    # Doanh thu tính toán phải chính xác.
    assert result["calculated_sales_amount"].tolist() == [
        200000, 200000, 150000
    ]

    # Giá trị chênh lệch phải chính xác.
    assert result["difference_amount"].tolist() == [
        0, 20000, -15000
    ]

    # Đánh dấu đúng trạng thái đối soát.
    assert result["reconciliation_status"].tolist() == [
        "MATCH", "MISMATCH", "MISMATCH"
    ]

    # Dữ liệu đầu vào phải được giữ nguyên.
    assert source["thanh_tien"].tolist() == [
        200000, 220000, 135000
    ]
