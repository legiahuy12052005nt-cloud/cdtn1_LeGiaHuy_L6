# ĐẶC TẢ YÊU CẦU DỮ LIỆU — TRACK DA, L6 (BT1)

**Sinh viên:** Lê Gia Huy — 2374802010175  


## 1. Câu hỏi phân tích và truy vết
| Câu hỏi | Nguồn báo cáo | User Story |
|---|---|---|
| AQ01: Giá trị bán hàng/số đơn/số lượng theo tháng, quý, năm? | Fact_Sales, Dim_Date | US05 |
| AQ02: Top sản phẩm và danh mục theo giá trị bán hàng? | Fact_Sales, Dim_Product | US07 |
| AQ03: Cửa hàng, thành phố nào có giá trị bán hàng cao/thấp? | Fact_Sales, Dim_Store | US06 |
| AQ04: Có bao nhiêu dòng `thanh_tien` chênh `so_luong × don_gia`? | Staging / Data Quality report | US03 |

**Ngoài phạm vi:** Phân tích khách có thông tin/vãng lai từ `customers_raw.csv` chưa có Dimension khách hàng trong Star Schema 3 chiều.

## 2. Dữ liệu nguồn
| File | Vai trò | Số dòng quan sát | Khóa / liên kết | Tần suất |
|---|---|---:|---|---|
| `orders_2024_2026.csv` | Hóa đơn | 26.000 | `order_id`, `ma_cua_hang` | TODO: xác nhận |
| `order_items.csv` | Dòng chi tiết bán hàng | 35.697 | `order_id`, `product_id` | TODO: xác nhận |
| `products.csv` | Danh mục sản phẩm | 320 | `product_id` | TODO: xác nhận |
| `stores.csv` | Danh mục cửa hàng | 24 | `store_code` | TODO: xác nhận |
| `customers_raw.csv` | Tham khảo ngoài phạm vi | 67.037 | `record_id`; thiếu liên kết chắc chắn với Fact | Không dùng trong prototype |

**Nguồn thực tế:** CSV được cung cấp trong bộ dữ liệu môn học. Không sử dụng tên giả định `Sales_Data.xlsx`.

## 3. GRAIN và mô hình kho
**GRAIN đề xuất:** Mỗi dòng `Fact_Sales` đại diện cho **một dòng chi tiết sản phẩm xuất hiện trong hóa đơn nguồn**, không gộp các dòng chỉ vì cùng `order_id` và `product_id`.

**Star Schema (1 Fact + 3 Dim):**
- `Fact_Sales`: `sales_key` (PK), `source_file_id`, `source_row_number`, `order_id`, `date_key`, `product_key`, `store_key`, `quantity`, `unit_price`, `reported_sales_amount`, `calculated_sales_amount`, `difference_amount`, `reconciliation_flag`.
- `Dim_Date`: `date_key` (PK), `full_date`, `day`, `month`, `quarter`, `year`.
- `Dim_Product`: `product_key` (PK), `product_id` (unique nguồn), `product_name`, `brand`, `category`.
- `Dim_Store`: `store_key` (PK), `store_code` (unique nguồn), `store_name`, `city`, `district`.

**Chống trùng giữa lần chạy:** TODO: quyết định cách định danh phiên bản file. Nếu sử dụng hash của file + số dòng, chỉ bảo đảm chống nạp trùng đối với bản file không đổi; khi dữ liệu được sắp xếp lại cần chiến lược khác. Không tự động xóa 11 dòng trùng toàn bộ giá trị nguồn.

## 4. Data Dictionary nguồn (các trường sử dụng)
| File | Trường | Kiểu đọc CSV | Chuẩn hóa / Vai trò |
|---|---|---|---|
| Orders | `order_id` | String | Integer, liên kết chi tiết |
| Orders | `ma_cua_hang` | String | Join `stores.store_code` |
| Orders | `ngay` | String | Parse DATE; có nhiều định dạng |
| Orders | `thanh_tien` | String | Giá trị cấp hóa đơn để đối chiếu riêng (có thể thiếu) |
| Order Items | `order_id` | String | Integer |
| Order Items | `product_id` | String | Integer, join Products |
| Order Items | `so_luong` | String | Integer |
| Order Items | `don_gia` | String | Decimal |
| Order Items | `thanh_tien` | String | Decimal, `reported_sales_amount` |
| Products | `product_id` | String | Integer |
| Products | `product_name`, `nhom_san_pham`, `thuong_hieu` | String | Tên, nhóm, thương hiệu sản phẩm |
| Stores | `store_code`, `store_name`, `thanh_pho`, `quan_huyen` | String | Mã, tên và địa điểm cửa hàng |

## 5. Data Profiling đã kiểm tra trên file nguồn
| Phát hiện | Số lượng | Ý nghĩa |
|---|---:|---|
| Orders thiếu `ngay` | 114 / 26.000 | Không ánh xạ ngày được nếu chưa xử lý |
| Orders thiếu `thanh_tien` | 279 / 26.000 | Cần quyết định cách đối chiếu tổng hóa đơn |
| Orders thiếu `so_dien_thoai` | 1.488 / 26.000 | Ngoài phạm vi phân tích khách hàng |
| Order Items: thành tiền khác `so_luong × don_gia` | 520 / 35.697 | 269 dòng +10%, 251 dòng −10% |
| Dòng Order Items trùng hoàn toàn giá trị | 11 dòng vượt các bản ghi duy nhất | Không mặc định là bản ghi lỗi |

**Số liệu tổng nguồn (chưa làm sạch):** `SUM(so_luong × don_gia) = 415.700.622.000`, `SUM(thanh_tien) = 415.773.438.750`, chênh lệch ròng `+72.816.750` VND. **Không trình bày các tổng này là doanh thu sạch/chính thức.**

**Nguyên nhân 520 dòng:** Các dòng chênh lệch rơi đúng vào 269 dòng +10% và 251 dòng −10%; CSV không có trường mã chiết khấu/thuế ở mức dòng để quy kết nguyên nhân. VAT, giảm giá hoặc sai lệch mô phỏng chỉ là giả thuyết. Dữ liệu không chứng minh giá trị nào là doanh thu kế toán chính thức.

## 6. Data Quality Rules đề xuất
| Mã | Quy tắc | Hành vi khi vi phạm | Liên kết |
|---|---|---|---|
| DQ01 | Có đủ 4 file và cột bắt buộc | Dừng Extract, ghi file/cột thiếu | FR01 |
| DQ02 | `ngay` parse được từ định dạng công bố | Cách ly hóa đơn/chi tiết phụ thuộc, giữ chuỗi nguồn | FR02 |
| DQ03 | `order_id`, `product_id`, `ma_cua_hang` ánh xạ được | Cách ly dòng liên quan, ghi khóa không tìm thấy | FR02 |
| DQ04 | `so_luong`, `don_gia`, `thanh_tien` đọc được và thỏa điều kiện đã chốt | Cách ly và ghi mã lỗi | FR02 |
| DQ05 | So sánh `thanh_tien` với `so_luong × don_gia` | Gắn cờ, KHÔNG xóa/sửa dòng chỉ vì chênh ±10% | FR03 |
| DQ06 | Không tăng Fact khi nạp lại cùng định danh nguồn | Ngăn insert trùng hoặc báo lỗi rõ ràng | FR04 |

**Ngưỡng chất lượng:** NFR02 yêu cầu 100% dòng thất bại validation có log; tỷ lệ bản ghi được chấp nhận tối thiểu là **TODO: chọn ngưỡng có cơ sở** (không tự đặt theo cảm tính).

## 7. Luồng xử lý đề xuất (Data Flow)
1. Đọc 4 CSV, ghi `source_file_id` và số dòng nguồn.
2. Lưu Staging, giữ nguyên chuỗi dữ liệu gốc.
3. Validation và chuẩn hóa ngày, tiền, khóa tham chiếu.
4. Tính giá trị báo cáo và giá trị đối soát; gắn cờ chênh ±10%.
5. Nạp Dim_Date, Dim_Product, Dim_Store.
6. Nạp Fact_Sales; không trùng theo định danh dòng đã quyết định.
7. Power BI truy vấn bảng Fact + Dimension, hiển thị ghi chú về định nghĩa chỉ số tiền.

## 8. Dữ liệu thiếu và cách kiểm tra
- Không tự thay ngày thiếu bằng ngày chạy ETL hoặc một ngày tùy ý.
- Dùng `order_id` để nối hóa đơn–chi tiết, và `store_code` / `product_id` cho Dimension.
- Ghi nhận tệp, dòng, trường và mã lỗi cho bản ghi cách ly.
- Đối với các dòng thành tiền ±10%, bảo toàn cả giá trị gốc và tính toán; ghi trạng thái chờ xác nhận.

