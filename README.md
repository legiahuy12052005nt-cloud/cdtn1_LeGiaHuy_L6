# Kho dữ liệu bán hàng và báo cáo doanh thu

**Sinh viên:**
Lê Gia Huy - 2374802010175 - Lớp: 71K29CNTT02

**Học phần:**
Chuyên đề Tốt nghiệp 1 - Lớp HP: 261_71ITGR40203_02

**Luồng nghiệp vụ:**
L6 - (DA) Trích xuất, làm sạch dữ liệu và xây dựng báo cáo

## 1. Mục tiêu
Dự án tự động hóa quá trình trích xuất và làm sạch dữ liệu bán hàng từ các nguồn tài liệu thô (file Excel). Dữ liệu sau khi xử lý sẽ được lưu trữ tập trung để phục vụ việc xây dựng Dashboard trên Power BI, cung cấp báo cáo doanh thu trực quan giúp ban quản lý dễ dàng theo dõi và ra quyết định.

## 2. Yêu cầu môi trường
* Python 3.10+ 
* Power BI Desktop
* Các thư viện Python: xem file `requirements.txt` (pandas, openpyxl,...)

## 3. Hướng dẫn chạy
1. `git clone <link_repo>` và di chuyển vào thư mục dự án.
2. `pip install -r requirements.txt` để cài đặt các thư viện cần thiết.
3. `python src/etl/smoke_test.py` để chạy kịch bản ETL và kiểm tra luồng dữ liệu.
4. Mở file `.pbix` bằng phần mềm Power BI Desktop để xem Dashboard báo cáo.

## 4. Cấu trúc thư mục
* `data/`: Chứa các file dữ liệu đầu vào (Excel) và dữ liệu đầu ra sau khi đã làm sạch.
* `src/etl/`: Chứa các kịch bản (script) Python xử lý nghiệp vụ ETL (Trích xuất - Biến đổi - Tải dữ liệu).
* `dashboards/`: Nơi lưu trữ các tệp Power BI (`.pbix`) thiết kế báo cáo trực quan.
* `requirements.txt`: Danh sách các thư viện phụ thuộc của Python.

## 5. Kiểm thử
Chạy lệnh sau để thực hiện smoke test luồng ETL cơ bản:
`python src/etl/smoke_test.py` → Nếu terminal không báo lỗi và dữ liệu đầu ra được tạo thành công, test PASS.

## 6. Trạng thái hiện tại
- [x] Khởi tạo project, script smoke test chạy được (buổi 2)
- [ ] Module trích xuất và làm sạch dữ liệu (buổi 8–10)
- [ ] Xây dựng mô hình dữ liệu và Dashboard báo cáo (buổi 10–12)