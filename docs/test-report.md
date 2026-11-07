
# TEST REPORT – KIỂM THỬ HỆ THỐNG MEKONG MOBILE

**Sinh viên:** Lê Gia Huy  
**MSSV:** 2374802010175  
**Track:** DA – Luồng L6  
**Đề tài:** Xây dựng kho dữ liệu bán hàng và Dashboard phân tích doanh thu cho Mekong Mobile  
**Phiên bản:** BT3 – Buổi 14  
**Ngày kiểm thử:** 07/11/2026

## 1. Thông tin kiểm thử

- Hệ thống: Kho dữ liệu bán hàng và Dashboard phân tích doanh thu Mekong Mobile.
- Phạm vi: ETL, Data Quality, Data Validation, Reject, SQLite Warehouse, Power BI Dashboard và khả năng tái lập.
- Công cụ: Python 3.10.11, pandas 2.3.3, pytest 9.2.0, SQLite, Power BI Desktop, VS Code và PowerShell.
- Môi trường: Windows.
- Bộ dữ liệu: CSV Demo trong `data/sample/`.
- Môi trường thực thi: Bản clone `mekong_mobile_v02_test` từ tag `v0.2`.
- Số test case: 12.
- Số nhóm kiểm thử: 5.
- Thư mục minh chứng: `docs/screenshots/`.

## 2. Bảng kết quả kiểm thử

| Mã TC | Nhóm / Ưu tiên | Tiền điều kiện | Bước thực hiện | Kết quả mong đợi | Kết quả thực tế | PASS/FAIL | Minh chứng |
|---|---|---|---|---|---|---|---|
| TC-01 | Luồng đúng / Cao | Có 4 file CSV Demo hợp lệ trong `data/raw/` | Chạy `python run_etl.py` | ETL chạy thành công và tạo dữ liệu Warehouse | ETL chạy thành công; tạo các bảng Warehouse và SQLite Database | PASS | [TC-01](screenshots/TC-01.PNG) |
| TC-02 | Luồng đúng / Cao | Đã chạy ETL với dữ liệu Demo | Truy vấn số dòng của 4 bảng trong SQLite | Fact_Sales=4, Dim_Date=3, Dim_Product=3, Dim_Store=2 | Fact_Sales=4, Dim_Date=3, Dim_Product=3, Dim_Store=2 | PASS | [TC-02](screenshots/TC-02.PNG) |
| TC-03 | Luồng đúng / Cao | Đã tạo dữ liệu Warehouse Demo | Mở Power BI Template, cấu hình `ProjectFolder`, kiểm tra KPI | Doanh thu=23.500.000 VND; đơn hàng=3; số lượng bán=5 | Dashboard tải dữ liệu thành công; doanh thu=23.500.000 VND; đơn hàng=3; số lượng bán=5; AOV≈7.833.333 VND | PASS | [TC-03](screenshots/TC-03.PNG) |
| TC-04 | Giá trị biên / Cao | Có DataFrame với `quantity=0` | Gọi hàm `check_quantity` với giá trị 0 | Giá trị không hợp lệ; error_count=1; error_rate=100% | Hàm kiểm tra phát hiện `quantity=0` là dữ liệu không hợp lệ | PASS | [TC-04](screenshots/TC-04.PNG) |
| TC-05 | Giá trị biên / Cao | Có DataFrame với `quantity=1` | Gọi hàm `check_quantity` với giá trị 1 | Giá trị hợp lệ; error_count=0; error_rate=0% | error_count=0; error_rate=0%; bài kiểm thử PASS | PASS | [TC-05](screenshots/TC-05.PNG) |
| TC-06 | Dữ liệu sai / Cao | Có DataFrame với `quantity=-1` | Gọi hàm `check_quantity` với giá trị -1 | Phát hiện số lượng âm; error_count=1; error_rate=100% | error_count=1; error_rate=100%; bài kiểm thử PASS | PASS | [TC-06](screenshots/TC-06.PNG) |
| TC-07 | Dữ liệu sai / Cao | Có DataFrame với `unit_price=-1` | Gọi hàm `check_unit_price` với giá trị -1 | Phát hiện đơn giá âm; error_count=1; error_rate=100% | error_count=1; error_rate=100%; bài kiểm thử PASS | PASS | [TC-07](screenshots/TC-07.PNG) |
| TC-08 | Dữ liệu sai / Cao | Có DataFrame với `order_id=None` | Gọi hàm `check_order_id` với giá trị None | Phát hiện mã đơn hàng thiếu; error_count=1; error_rate=100% | error_count=1; error_rate=100%; bài kiểm thử PASS | PASS | [TC-08](screenshots/TC-08.PNG) |
| TC-09 | Chất lượng dữ liệu / Cao | quantity=2; unit_price=10.000.000; reported_sales_amount=22.000.000 | Chạy `pytest tests/test_transform_sales.py::test_reconciliation_mismatch -v` | Doanh thu tính toán=20.000.000; trạng thái MISMATCH | Bài kiểm thử đối soát doanh thu chạy thành công; 1 passed | PASS | [TC-09](screenshots/TC-09.PNG) |
| TC-10 | Chất lượng dữ liệu / Cao | Có dữ liệu lỗi giả lập | Chạy `generate_reject_demo.py`, kiểm tra file Reject CSV | 3 dòng bị Reject và có lý do vi phạm | File Reject chứa 3 dòng dữ liệu lỗi và thông tin nguyên nhân | PASS | [TC-10](screenshots/TC-10.PNG) |
| TC-11 | Tái lập / Cao | Có 4 file CSV Demo hợp lệ | Chạy ETL 2 lần với `PYTHONIOENCODING=UTF-8`, truy vấn SQLite | Fact_Sales=4 sau mỗi lần; không trùng sales_key | Lần 1: Fact_Sales=4, trùng=0; lần 2: Fact_Sales=4, trùng=0 | PASS | [TC-11](screenshots/TC-11.PNG) |
| TC-12 | Tái lập / Cao | Có bản clone repository từ tag `v0.2` và môi trường Python | Chạy `python -m pytest tests/ -v` | Toàn bộ bài kiểm thử tự động PASS | 14 bài pytest PASS; không có FAILED hoặc ERROR | PASS | [TC-12](screenshots/TC-12.PNG) |

## 3. Tổng hợp kết quả

| Chỉ tiêu | Kết quả |
|---|---:|
| Tổng số test case | 12 |
| Test case đã thực hiện | 12 |
| PASS | 12 |
| FAIL | 0 |
| Chưa chạy | 0 |
| Tỷ lệ PASS | 100% |
| Nhóm kiểm thử được bao phủ | 5/5 |
| Bài kiểm thử pytest trong TC-12 | 14 PASS |

### Phân loại kiểm thử

| Nhóm kiểm thử | Mã test case | Số lượng |
|---|---|---:|
| Luồng đúng | TC-01, TC-02, TC-03 | 3 |
| Giá trị biên | TC-04, TC-05 | 2 |
| Dữ liệu sai | TC-06, TC-07, TC-08 | 3 |
| Bảo mật / Chất lượng dữ liệu | TC-09, TC-10 | 2 |
| Tái lập | TC-11, TC-12 | 2 |
| **Tổng cộng** | **TC-01 đến TC-12** | **12** |

## 4. Nhận xét kết quả kiểm thử

### 4.1. Luồng xử lý dữ liệu

Quy trình ETL được kiểm thử với bộ dữ liệu Demo gồm 4 file CSV. Hệ thống có thể đọc dữ liệu, xử lý và tạo các bảng Warehouse.

Kết quả đối chiếu SQLite với dữ liệu Demo:
- Fact_Sales: 4 dòng.
- Dim_Date: 3 dòng.
- Dim_Product: 3 dòng.
- Dim_Store: 2 dòng.

### 4.2. Dashboard Power BI

Dashboard được kiểm tra với dữ liệu Demo và hiển thị các chỉ số:
- Tổng doanh thu: 23.500.000 VND.
- Tổng đơn hàng: 3.
- Tổng số lượng bán: 5.
- Giá trị đơn hàng trung bình: khoảng 7.833.333 VND.

### 4.3. Chất lượng dữ liệu

Các trường hợp kiểm tra bao gồm:
- Số lượng bằng 0.
- Số lượng bằng 1.
- Số lượng âm.
- Đơn giá âm.
- Thiếu mã đơn hàng.
- Doanh thu báo cáo không khớp với doanh thu tính toán.
- Dữ liệu lỗi được chuyển vào danh sách Reject kèm nguyên nhân.

### 4.4. Khả năng tái lập

Kiểm thử chạy ETL hai lần cho kết quả số dòng Fact_Sales không thay đổi và không phát sinh khóa sales_key trùng.

Bộ kiểm thử tự động trên bản clone của tag `v0.2` được thực hiện bằng lệnh:

```powershell
python -m pytest tests/ -v
```

Kết quả ghi nhận: 14 bài kiểm thử PASS.

### 4.5. Lỗi trong quá trình thực hiện

Trong quá trình thực hiện TC-11, chương trình từng gặp lỗi `UnicodeEncodeError` khi chạy ETL từ Python subprocess do cấu hình mã hóa đầu ra không hỗ trợ ký tự tiếng Việt.

Sau khi bổ sung cấu hình môi trường `PYTHONIOENCODING=UTF-8` cho lệnh kiểm thử, quy trình có thể tiếp tục thực hiện.

Vấn đề này cần được đánh giá trong Bug Log nếu xác định là lỗi thực tế cần sửa trong source code hoặc cấu hình triển khai. Việc thay đổi môi trường thực thi chưa được xem là một commit sửa bug của dự án.

## 5. Quản lý minh chứng

Các ảnh kiểm thử được lưu tại:

`docs/screenshots/`

Quy ước:
- TC-01.PNG: Chạy ETL thành công.
- TC-02.png: Đối chiếu số dòng SQLite.
- TC-03.png: Kiểm tra KPI Power BI.
- TC-04.png: Kiểm thử quantity=0.
- TC-05.png: Kiểm thử quantity=1.
- TC-06.png: Kiểm thử quantity=-1.
- TC-07.png: Kiểm thử unit_price=-1.
- TC-08.png: Kiểm thử order_id=None.
- TC-09.png: Kiểm thử doanh thu MISMATCH.
- TC-10.png: Kiểm tra file Reject.
- TC-11.png: Kiểm thử ETL chạy hai lần.
- TC-12.png: Chạy toàn bộ pytest trên bản clone.

## 6. Kết luận

Theo kết quả kiểm thử đã ghi nhận, cả 12 test case thuộc 5 nhóm kiểm thử đều đạt trạng thái PASS. Bộ kiểm thử tự động gồm 14 bài pytest cũng PASS trên môi trường kiểm thử.

Các kết quả trên cho thấy những chức năng được kiểm thử của hệ thống Mekong Mobile đáp ứng các kết quả mong đợi với dữ liệu Demo.

Phạm vi kết luận giới hạn ở bộ dữ liệu, môi trường và các kịch bản đã thực hiện; không khẳng định hệ thống không còn lỗi ngoài phạm vi kiểm thử.

Kết quả Test Report sẽ được sử dụng làm minh chứng cho Workshop Buổi 14 và làm cơ sở tiếp tục hoàn thiện Bug Log, sửa lỗi, kiểm thử hồi quy và chuẩn bị bài nộp BT3 chính thức.

