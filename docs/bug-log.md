
# BUG LOG – MEKONG MOBILE

**Sinh viên:** Lê Gia Huy  
**MSSV:** 2374802010175  
**Track:** DA – Luồng L6  
**Phiên bản:** BT3 – Buổi 14

## BUG-01 – ETL bị dừng khi xuất thông báo tiếng Việt

- **Mức độ:** Major
- **Phát hiện bởi:** TC-11 – Kiểm thử tái lập ETL.
- **Hiện tượng:** ETL phát sinh UnicodeEncodeError khi in thông báo tiếng Việt trong môi trường sử dụng bảng mã cp1252.
- **Cách tái hiện:** Chạy ETL thông qua Python subprocess với PYTHONIOENCODING=cp1252.
- **Nguyên nhân:** Luồng stdout không hỗ trợ một số ký tự tiếng Việt, khiến lệnh print phát sinh ngoại lệ.
- **Cách sửa:** Cấu hình sys.stdout.reconfigure(errors="backslashreplace") trong hàm main() của run_etl.py để xử lý ký tự không được bảng mã hỗ trợ.
- **Kiểm thử lại:** Đã thực hiện kiểm thử sau sửa với môi trường cp1252; ghi nhận kết quả thành công theo lần kiểm thử.
- **Trạng thái:** Fixed.
- **Commit:** [d3fc130737072572ee2b11d46d03037ddc63570e](https://github.com/legiahuy12052005nt-cloud/cdtn1_LeGiaHuy_L6/commit/d3fc130737072572ee2b11d46d03037ddc63570e)
- **Ảnh trước sửa:** [BUG-01-before](screenshots/BUG-01-before.PNG)
- **Ảnh sau sửa:** [BUG-01-after](screenshots/BUG-01-after.PNG)

## BUG-02 – File CSV rỗng trả về lỗi kỹ thuật khó hiểu

- **Mức độ:** Minor
- **Phát hiện bởi:** Kiểm thử dữ liệu đầu vào rỗng.
- **Hiện tượng:** Khi đọc file CSV hoàn toàn rỗng, hệ thống phát sinh `EmptyDataError: No columns to parse from file`.
- **Cách tái hiện:** Tạo file `empty.csv` không có nội dung và truyền đường dẫn vào hàm `extract_csv()`.
- **Nguyên nhân:** Hàm `extract_csv()` sử dụng `pd.read_csv()` nhưng chưa xử lý riêng ngoại lệ `pandas.errors.EmptyDataError`.
- **Cách sửa:** Bắt ngoại lệ `EmptyDataError` và chuyển thành `ValueError` với thông báo rõ ràng, kèm đường dẫn file bị lỗi.
- **Kiểm thử lại:** Chạy lại với `empty.csv`; hệ thống trả về `ValueError` có chứa tên file và thông báo rõ ràng.
- **Trạng thái:** Fixed.
- **Commit:** [8041a8178264674e33ea6466498e15403afb9436](https://github.com/legiahuy12052005nt-cloud/cdtn1_LeGiaHuy_L6/commit/8041a8178264674e33ea6466498e15403afb9436)
- **Ảnh trước sửa:** [BUG-02-before](screenshots/BUG-02-before.PNG)
- **Ảnh sau sửa:** [BUG-02-after](screenshots/BUG-02-after.PNG)

## BUG-03 – Hệ thống chấp nhận mã ID chỉ chứa khoảng trắng

- **Mức độ:** Major
- **Phát hiện bởi:** Kiểm thử dữ liệu sai tại hàm `validate_order_items()`.
- **Hiện tượng:** Dòng dữ liệu có `order_id` hoặc `product_id` chỉ chứa khoảng trắng có thể được đưa vào `valid_df` thay vì `rejected_df`.
- **Cách tái hiện:** Tạo DataFrame có `order_id="   "`, các trường còn lại hợp lệ, sau đó gọi `validate_order_items()`. Trước khi sửa, dòng dữ liệu không bị Reject.
- **Nguyên nhân:** Hàm chỉ sử dụng `pd.isna()` để kiểm tra mã ID thiếu, không phát hiện chuỗi rỗng hoặc chỉ chứa khoảng trắng.
- **Cách sửa:** Bổ sung kiểm tra chuỗi bằng `strip()` cho cả `order_id` và `product_id`, kết hợp kiểm tra `None`/`NaN`.
- **Kiểm thử lại:** Dùng 4 dòng dữ liệu giả lập gồm 3 dòng lỗi và 1 dòng hợp lệ. Kết quả mong đợi và đã kiểm tra theo quy trình: 1 dòng hợp lệ, 3 dòng Reject có lý do.
- **Trạng thái:** Fixed (theo lần kiểm thử lại đã thực hiện).
- **Commit:** [28c6f87b46ccae09a233e4912f0524fb8fd18723](https://github.com/legiahuy12052005nt-cloud/cdtn1_LeGiaHuy_L6/commit/28c6f87b46ccae09a233e4912f0524fb8fd18723)
- **Ảnh trước sửa:** [BUG-03-before](screenshots/BUG-03-before.PNG)
- **Ảnh sau sửa:** [BUG-03-after](screenshots/BUG-03-after.PNG)

## Kết quả kiểm thử hồi quy sau khi sửa lỗi

Sau khi sửa BUG-01, BUG-02 và BUG-03, hệ thống đã được kiểm thử hồi quy trên dự án chính bằng lệnh:

```powershell
.\.venv\Scripts\python.exe -m pytest tests/ -q
```

Kết quả thực tế:
- Tổng số bài kiểm thử: 14.
- PASS: 14.
- FAIL: 0.
- Tỷ lệ PASS: 100%.
- Thời gian thực thi: 1.21 giây.

**Kết luận:** Bộ kiểm thử tự động hiện có PASS sau khi sửa ba lỗi.

**Minh chứng:** [Regression after fixes](screenshots/regression-after-fixes.PNG)


