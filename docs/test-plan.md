
# TEST PLAN – KIỂM THỬ HỆ THỐNG MEKONG MOBILE

**Học phần:** Chuyên đề Tốt nghiệp 1  
**Sinh viên:** Lê Gia Huy  
**MSSV:** 2374802010175  
**Track:** DA – Luồng L6  
**Đề tài:** Xây dựng kho dữ liệu bán hàng và Dashboard phân tích doanh thu cho Mekong Mobile  
**Phiên bản kiểm thử:** BT3 – Buổi 14

## 1. Phạm vi kiểm thử

### 1.1. Các chức năng được kiểm thử

- Đọc dữ liệu bán hàng từ các file CSV.
- Chuẩn hóa dữ liệu và kiểm tra các quy tắc nghiệp vụ.
- Phát hiện dữ liệu không hợp lệ và ghi nhận lý do Reject.
- Kiểm tra đối soát doanh thu.
- Xây dựng các bảng Fact_Sales, Dim_Date, Dim_Product và Dim_Store.
- Kiểm tra dữ liệu được lưu trong SQLite Data Warehouse.
- Kiểm tra tính tái lập khi chạy ETL nhiều lần trên cùng dữ liệu.
- Kiểm tra Dashboard Power BI với dữ liệu mẫu và các trạng thái Empty, Error.

### 1.2. Các nội dung chủ ý không kiểm thử

- Hiệu năng xử lý với dữ liệu lớn vượt bộ dữ liệu hiện có.
- Kiểm thử tải đồng thời nhiều người dùng.
- Kiểm thử phân quyền người dùng trên Power BI Service.
- Khả năng tương thích trên nhiều hệ điều hành ngoài Windows.
- Kiểm thử các API hoặc hệ thống thanh toán bên ngoài vì không thuộc phạm vi dự án.

## 2. Loại kiểm thử và số lượng test case

Dự kiến thực hiện 12 test case thuộc 5 nhóm:

| Nhóm kiểm thử | Số lượng | Mã test case |
|---|---:|---|
| Luồng đúng | 3 | TC-01, TC-02, TC-03 |
| Giá trị biên | 2 | TC-04, TC-05 |
| Dữ liệu sai | 3 | TC-06, TC-07, TC-08 |
| Bảo mật / Chất lượng dữ liệu | 2 | TC-09, TC-10 |
| Tái lập | 2 | TC-11, TC-12 |
| **Tổng cộng** | **12** | |

### Danh sách test case dự kiến

- TC-01: Chạy ETL thành công với 4 file CSV hợp lệ.
- TC-02: Kiểm tra các bảng Warehouse và số dòng dữ liệu Demo.
- TC-03: Kiểm tra Dashboard hiển thị KPI chính xác.
- TC-04: Kiểm tra số lượng sản phẩm bằng 0.
- TC-05: Kiểm tra số lượng sản phẩm tại ranh giới hợp lệ và không hợp lệ.
- TC-06: Kiểm tra số lượng sản phẩm âm.
- TC-07: Kiểm tra đơn giá âm.
- TC-08: Kiểm tra mã đơn hàng hoặc mã sản phẩm bị thiếu.
- TC-09: Kiểm tra phát hiện chênh lệch doanh thu.
- TC-10: Kiểm tra Reject có ghi nhận lý do lỗi, không đưa dữ liệu khách hàng thật lên GitHub.
- TC-11: Chạy ETL hai lần không tạo khóa Fact trùng.
- TC-12: Clone repository từ GitHub và chạy lại quy trình với dữ liệu Demo.

Kỹ thuật chọn dữ liệu kiểm thử:

- Phân vùng tương đương: dữ liệu hợp lệ và không hợp lệ.
- Giá trị biên: số lượng -1, 0, 1.
- Dữ liệu lỗi: thiếu ID, số lượng âm, đơn giá âm, doanh thu không hợp lệ.
- Kiểm thử tái lập: chạy lại ETL và đối chiếu số dòng, khóa dữ liệu.

## 3. Tiêu chí thành công

- Mỗi test case phải được chạy thực tế theo tiền điều kiện và các bước đã xác định.
- Kết quả thực tế phải được ghi cụ thể trong Test Report.
- PASS khi toàn bộ kết quả thực tế khớp kết quả mong đợi.
- FAIL khi có bất kỳ kết quả nào khác mong đợi; ghi nhận lỗi để phân tích và sửa.
- Mỗi test case có ảnh chụp kết quả trong `docs/screenshots/`, đặt tên `TC-01.png` đến `TC-12.png`.
- Bộ kiểm thử tự động hiện có phải chạy được bằng một lệnh `python -m pytest tests/ -q`.
- Dữ liệu Reject phải thể hiện được nguyên nhân vi phạm quy tắc chất lượng.
- Chạy ETL lại trên cùng dữ liệu không làm tăng số dòng Fact_Sales hoặc tạo khóa sales_key trùng.
- Sau khi sửa bug, chạy lại toàn bộ bộ kiểm thử tự động để kiểm tra hồi quy.

## 4. Môi trường và dữ liệu kiểm thử

### 4.1. Môi trường

- Hệ điều hành: Windows.
- Python: 3.10.11.
- Thư viện: pandas 2.3.3 và pytest 9.2.0.
- Công cụ: Visual Studio Code, PowerShell, Git và GitHub.
- Kho dữ liệu: SQLite và các bảng CSV Warehouse.
- Dashboard: Power BI Desktop.

### 4.2. Dữ liệu kiểm thử

- Sử dụng 4 file CSV Demo từ thư mục `data/sample/`.
- Sao chép dữ liệu Demo vào `data/raw/` trước khi chạy ETL.
- Sử dụng dữ liệu lỗi giả lập để kiểm tra Data Quality và Reject.
- Không sử dụng dữ liệu khách hàng thật trong các minh chứng công khai.

Kết quả tham chiếu với dữ liệu Demo:

| Chỉ tiêu | Giá trị |
|---|---:|
| Fact_Sales | 4 dòng |
| Dim_Date | 3 dòng |
| Dim_Product | 3 dòng |
| Dim_Store | 2 dòng |
| Tổng doanh thu | 23.500.000 VND |
| Tổng đơn hàng | 3 |
| Tổng số lượng sản phẩm bán | 5 |

### 4.3. Quản lý minh chứng

- Lưu ảnh chạy từng test case trong `docs/screenshots/`.
- Mỗi ảnh phải thể hiện lệnh hoặc thao tác và kết quả thực tế.
- Ghi kết quả PASS/FAIL vào `docs/test-report.md`.
- Nếu phát hiện lỗi, ghi vào `docs/bug-log.md`.
- Mỗi bug được sửa bằng commit riêng có liên kết GitHub.
