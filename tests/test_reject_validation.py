
import pandas as pd

from src.quality.validate_sales import validate_order_items


def test_reject_invalid_data():
    """Kiểm tra dữ liệu sai được đưa vào Reject kèm lý do."""

    sample_data = pd.DataFrame(
        {
            "order_id": ["O001", "O002", "O003", "O004"],
            "product_id": ["P001", "P002", "P003", "P004"],
            "quantity": [2, 0, -1, 3],
            "unit_price": [100000, 200000, 150000, -50000],
            "reported_sales_amount": [
                200000,
                0,
                -150000,
                300000,
            ],
        }
    )

    valid_df, rejected_df = validate_order_items(sample_data)

    # Chỉ dòng O001 là hợp lệ
    assert len(valid_df) == 1

    # Ba dòng còn lại phải bị từ chối
    assert len(rejected_df) == 3

    # Mỗi dòng bị từ chối phải có lý do
    assert rejected_df["reject_reason"].notna().all()
    assert (rejected_df["reject_reason"] != "").all()

    # Kiểm tra lý do lỗi cụ thể
    assert "Số lượng không hợp lệ" in rejected_df.iloc[0]["reject_reason"]
    assert "Số lượng không hợp lệ" in rejected_df.iloc[1]["reject_reason"]
    assert "Đơn giá không hợp lệ" in rejected_df.iloc[2]["reject_reason"]
    
from src.quality.reject_logger import save_rejected_rows


def test_save_rejected_rows_to_csv(tmp_path):
    """Kiểm tra dữ liệu lỗi được lưu ra CSV kèm lý do."""

    sample_data = pd.DataFrame(
        {
            "order_id": ["O001", "O002", "O003"],
            "product_id": ["P001", "P002", "P003"],
            "quantity": [2, 0, -1],
            "unit_price": [100000, 200000, 150000],
            "reported_sales_amount": [200000, 0, -150000],
        }
    )

    valid_df, rejected_df = validate_order_items(sample_data)

    output_path = tmp_path / "rejected_order_items.csv"

    saved_path = save_rejected_rows(
        rejected_df,
        output_path=str(output_path),
    )

    # File phải được tạo thành công
    assert saved_path.exists()

    # Đọc lại CSV để kiểm tra dữ liệu thực tế trên đĩa
    saved_df = pd.read_csv(saved_path)

    assert len(valid_df) == 1
    assert len(saved_df) == 2

    # File phải chứa lý do lỗi
    assert "reject_reason" in saved_df.columns
    assert saved_df["reject_reason"].notna().all()

    # Kiểm tra lý do lỗi cụ thể
    assert saved_df["reject_reason"].str.contains(
        "Số lượng không hợp lệ"
    ).all()

    # Chạy lại lần hai không được nhân đôi dữ liệu
    save_rejected_rows(
        rejected_df,
        output_path=str(output_path),
    )

    saved_again = pd.read_csv(output_path)

    assert len(saved_again) == 2

