# DATA PROFILING – L6 (kết quả có thể tái lập)

## Nguồn và cách kiểm chứng
Các thống kê từ 5 CSV người học cung cấp, được tính bằng `python scripts/profile_sales.py --data-dir data/raw` (không ghi đè dữ liệu nguồn).

| Tập dữ liệu | Dòng | Ghi chú |
|---|---:|---|
| `orders_2024_2026.csv` | 26.000 | 114 thiếu ngày, 279 thiếu thành tiền hóa đơn |
| `order_items.csv` | 35.697 | 520 dòng có chênh tiền |
| `products.csv` | 320 | Bảng danh mục |
| `stores.csv` | 24 | Bảng danh mục |
| `customers_raw.csv` | 67.037 | Tham khảo, ngoài phạm vi Star Schema hiện tại |

## Đối soát giá trị dòng chi tiết

| Phân nhóm | Dòng |
|---|---:|
| Khớp `so_luong × don_gia` | 35.177 |
| Cao hơn đúng 10% | 269 |
| Thấp hơn đúng 10% | 251 |
| Tổng dòng khác nhau | 520 |

