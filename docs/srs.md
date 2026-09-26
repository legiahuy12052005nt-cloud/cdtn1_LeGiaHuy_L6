# ĐẶC TẢ YÊU CẦU RÚT GỌN (SRS)
**Dự án:** Kho dữ liệu bán hàng và báo cáo doanh thu (Luồng L6)

## 1. Phạm vi dự án
Hệ thống tự động trích xuất dữ liệu đơn hàng từ các cửa hàng, tiến hành làm sạch các lỗi chất lượng và nạp vào kho dữ liệu tập trung, kết thúc bằng việc xây dựng dashboard báo cáo doanh thu nhiều chiều phục vụ Ban giám đốc.

## 2. Danh sách User Story (US)
* **US1:** Là Ban giám đốc, tôi muốn xem dashboard doanh thu tổng thể nhiều chiều để giải quyết triệt để tình trạng thiếu báo cáo và phải chờ đợi lâu.
* **US2:** Là Ban giám đốc, tôi muốn phân tích doanh thu theo chiều thời gian (ngày, tháng, năm) và theo nhóm khách hàng để nhận diện các xu hướng mua sắm.
* **US3:** Là Quản lý cửa hàng, tôi muốn xem báo cáo doanh thu chi tiết và so sánh hiệu quả của riêng chi nhánh mình để có chiến lược kinh doanh cục bộ.
* **US4:** Là Quản lý cửa hàng, tôi muốn thống kê chi tiết các mặt hàng/linh kiện bán chạy nhất để tối ưu hóa quy trình nhập hàng và quản lý tồn kho.
* **US5:** Là Chuyên viên dữ liệu, tôi muốn thiết lập luồng tự động (ETL) xử lý các lỗi chất lượng từ dữ liệu thô để đưa dữ liệu chuẩn vào bảng tạm (stg_order) trước khi nạp lên bảng sự kiện chính (fact_sales).