# ĐẶC TẢ USE CASE NHÁP — L6

**UC04 — Nạp dữ liệu đã chuẩn hóa vào kho**  
**Actor chính:** Chuyên viên dữ liệu  
**Liên quan:** FR04, US04 (MUST)

**Tiền điều kiện:** Nguồn đã đọc và dữ liệu đã qua kiểm tra/chuẩn hóa, kho dữ liệu đích sẵn sàng.  
**Hậu điều kiện:** Dữ liệu đủ điều kiện được nạp Fact/Dimensions; kết quả và lỗi được ghi nhận.

## Luồng chính
1. Chuyên viên dữ liệu chọn thực thi nạp kho.
2. Hệ thống xác định các bản ghi hợp lệ từ staging.
3. Hệ thống cập nhật hoặc thêm các Dimension cần thiết.
4. Hệ thống ánh xạ từng dòng nguồn với các khóa Dimension.
5. Hệ thống kiểm tra định danh dòng nguồn chưa được nạp.
6. Hệ thống ghi các dòng hợp lệ vào Fact_Sales.
7. Hệ thống báo cáo số dòng đã nạp, bỏ qua và gặp lỗi.

## Luồng ngoại lệ
- **2a.** Dữ liệu nguồn không đạt validation → ghi log lỗi; không nạp dòng đó.
- **4a.** Không tìm được Product/Store/Date key → cách ly dòng và ghi rõ mã thiếu.
- **5a.** Định danh dòng đã tồn tại → không thêm dòng trùng; ghi số lượng bỏ qua.
- **6a.** Lỗi kết nối/khoá dữ liệu đích → rollback đơn vị giao dịch đã chọn và ghi lỗi.

