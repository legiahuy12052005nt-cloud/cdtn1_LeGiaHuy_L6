# ĐẶC TẢ YÊU CẦU RÚT GỌN (SRS)
**Dự án:** Kho dữ liệu bán hàng và báo cáo doanh thu (Luồng 6)

## 1. Phạm vi dự án
Hệ thống tự động trích xuất dữ liệu đơn hàng từ các cửa hàng, tiến hành làm sạch các lỗi chất lượng và nạp vào kho dữ liệu tập trung, kết thúc bằng việc xây dựng dashboard báo cáo doanh thu nhiều chiều phục vụ Ban giám đốc.

## 2. Danh sách User Story (US)
* **US1:** Là Chuyên viên dữ liệu, tôi muốn nhập trực tiếp dữ liệu thô từ các file Excel vào hệ thống để có nguồn thông tin đầu vào cho quá trình phân tích.
* **US2:** Là Chuyên viên dữ liệu, tôi muốn hệ thống tự động nhận diện và làm sạch các lỗi dữ liệu (như thiếu cột, sai định dạng) để đảm bảo số liệu lên báo cáo không bị sai lệch.
* **US3:** Là Chuyên viên dữ liệu, tôi muốn thiết lập luồng ETL tự động chạy theo lịch hẹn để dữ liệu mới nhất luôn được nạp lên kho mà không cần phải thao tác thủ công mỗi ngày.
* **US4:** Là Chuyên viên dữ liệu, tôi muốn xây dựng và tinh chỉnh mô hình dữ liệu để tổ chức các bảng thông tin gọn gàng, giúp Dashboard tải số liệu nhanh và mượt hơn.
* **US5:** Là Ban giám đốc, tôi muốn xem ngay Dashboard tổng quan về doanh thu nhiều chiều để nắm bắt tình hình kinh doanh tức thời mà không phải chờ đợi nhân viên tổng hợp báo cáo.
* **US6:** Là Quản lý cửa hàng, tôi muốn lọc số liệu trên báo cáo theo từng mốc thời gian hoặc khu vực để dễ dàng so sánh hiệu quả bán hàng của riêng chi nhánh mình.
* **US7:** Là Quản lý cửa hàng, tôi muốn xuất nhanh báo cáo ra file định dạng PDF hoặc Excel để tiện mang đi họp hoặc gửi email báo cáo cho cấp trên.

## 3. Bảng truy vết yêu cầu (Traceability Matrix)

| Mã FR | Yêu cầu chức năng (Functional Requirement) | User Story | Use Case | Test Case ID |
| :--- | :--- | :--- | :--- | :--- |
| FR01 | Hệ thống cho phép nhập file Excel (Sales, Product). | US1 | UC1 | TC_01 |
| FR02 | Hệ thống tự động báo lỗi nếu file thiếu cột bắt buộc. | US2 | UC2 | TC_02 |
| FR03 | Hệ thống chạy tiến trình ETL tự động theo lịch (hàng ngày). | US3 | UC3 | TC_03 |
| FR04 | Hệ thống cho phép cập nhật định nghĩa các chiều (Dimension). | US4 | UC4 | TC_04 |
| FR05 | Dashboard hiển thị tổng doanh thu, số lượng đơn hàng. | US5 | UC5 | TC_05 |
| FR06 | Dashboard cho phép lọc theo bộ lọc thời gian, khu vực. | US6 | UC6 | TC_06 |
| FR07 | Hệ thống cho phép xuất Dashboard ra file PDF/Excel. | US7 | UC7 | TC_07 |