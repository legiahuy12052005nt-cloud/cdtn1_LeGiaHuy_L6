
import pandas as pd

from src.transform.transform_sales import (
    normalize_order_items,
    reconcile_sales,
)
from src.quality.validate_sales import validate_order_items


# TEST 01: Kiểm tra chuẩn hóa tên cột dữ liệu
def test_normalize_order_items():
    df = pd.DataFrame({
        "so_luong": [2],
        "don_gia": [10000000],
        "thanh_tien": [20000000],
    })

    result = normalize_order_items(df)

    assert "quantity" in result.columns
    assert "unit_price" in result.columns
    assert "reported_sales_amount" in result.columns

    assert result.loc[0, "quantity"] == 2
    assert result.loc[0, "unit_price"] == 10000000


# TEST 02: Kiểm tra công thức tính doanh thu
def test_calculated_sales_amount():
    df = pd.DataFrame({
        "quantity": [2],
        "unit_price": [15000000],
        "reported_sales_amount": [30000000],
    })

    result = reconcile_sales(df)

    assert result.loc[0, "calculated_sales_amount"] == 30000000


# TEST 03: Kiểm tra trạng thái MATCH
def test_reconciliation_match():
    df = pd.DataFrame({
        "quantity": [3],
        "unit_price": [5000000],
        "reported_sales_amount": [15000000],
    })

    result = reconcile_sales(df)

    assert result.loc[0, "reconciliation_status"] == "MATCH"
    assert result.loc[0, "difference_amount"] == 0


# TEST 04: Kiểm tra trạng thái MISMATCH
def test_reconciliation_mismatch():
    df = pd.DataFrame({
        "quantity": [2],
        "unit_price": [10000000],
        "reported_sales_amount": [22000000],
    })

    result = reconcile_sales(df)

    assert result.loc[0, "calculated_sales_amount"] == 20000000
    assert result.loc[0, "difference_amount"] == 2000000
    assert result.loc[0, "reconciliation_status"] == "MISMATCH"

    # Phải giữ nguyên doanh thu từ dữ liệu nguồn
    assert result.loc[0, "reported_sales_amount"] == 22000000


# TEST 05: Kiểm tra giá trị biên - số lượng bằng 0
def test_quantity_zero_is_rejected():
    df = pd.DataFrame({
        "order_id": [1001],
        "product_id": [101],
        "quantity": [0],
        "unit_price": [1000000],
        "reported_sales_amount": [0],
    })

    valid, rejected = validate_order_items(df)

    assert len(valid) == 0
    assert len(rejected) == 1


# TEST 06: Kiểm tra ngoại lệ - số lượng âm
def test_negative_quantity_is_rejected():
    df = pd.DataFrame({
        "order_id": [1002],
        "product_id": [102],
        "quantity": [-2],
        "unit_price": [5000000],
        "reported_sales_amount": [10000000],
    })

    valid, rejected = validate_order_items(df)

    assert len(valid) == 0
    assert len(rejected) == 1
