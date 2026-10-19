
import pandas as pd


def build_dim_date(orders_df: pd.DataFrame) -> pd.DataFrame:
    """
    Xây dựng Dim_Date từ ngày đặt hàng.

    Mỗi ngày hợp lệ chỉ xuất hiện một lần.
    Không tự tạo ngày cho đơn hàng thiếu ngày.
    """

    if "ngay" not in orders_df.columns:
        raise ValueError("Thiếu cột ngay trong dữ liệu đơn hàng")

    # Chuyển ngày nguồn sang kiểu datetime
    
    dates = pd.to_datetime(
        orders_df["ngay"],
        format="mixed",
        dayfirst=True,
        errors="coerce"
    )


    # Giữ ngày hợp lệ, không lấy ngày bị thiếu
    valid_dates = (
        dates.dropna()
        .dt.normalize()
        .drop_duplicates()
        .sort_values()
        .reset_index(drop=True)
    )

    dim_date = pd.DataFrame({
        "full_date": valid_dates
    })

    # Khóa ngày dạng YYYYMMDD
    dim_date["date_key"] = (
        dim_date["full_date"].dt.strftime("%Y%m%d").astype(int)
    )

    dim_date["day"] = dim_date["full_date"].dt.day
    dim_date["month"] = dim_date["full_date"].dt.month
    dim_date["quarter"] = dim_date["full_date"].dt.quarter
    dim_date["year"] = dim_date["full_date"].dt.year

    return dim_date[
        ["date_key", "full_date", "day", "month", "quarter", "year"]
    ]
