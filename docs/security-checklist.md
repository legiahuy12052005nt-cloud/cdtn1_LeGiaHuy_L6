
# Security Checklist – Mekong Mobile Data Warehouse

**Dự án:** Xây dựng kho dữ liệu bán hàng và Dashboard phân tích doanh thu cho Mekong Mobile

**Track:** Data Analytics (DA)

**Phiên bản:** BT3 – Chuẩn bị triển khai

## 1. Quản lý thông tin bí mật (Secrets Management)

**Trạng thái:** ĐÃ LÀM (kiểm tra cơ bản)

- Sử dụng `.gitignore` và `.dockerignore` để loại trừ file `.env` khỏi các thao tác đóng gói thông thường.
- Sử dụng `.env.example` để mô tả cấu hình mà không chứa mật khẩu.
- Hệ thống sử dụng SQLite cục bộ, chưa cần tài khoản hoặc mật khẩu kết nối database.
- Chưa thực hiện kiểm tra toàn bộ lịch sử Git để xác nhận không có secrets từng được commit.

**Minh chứng:** `.gitignore`, `.dockerignore`, `.env.example`.
### Kết quả kiểm tra thực tế

- Đã xác nhận `.gitignore` loại trừ `.env`, `.venv/`, `data/raw/`, `data/private/` và các thư mục dữ liệu phát sinh.
- Lệnh `git ls-files --error-unmatch .env` xác nhận `.env` không được Git theo dõi.
- Lệnh `git log --all --oneline -- .env` không tìm thấy commit chứa đường dẫn `.env`.
- Kiểm tra nội dung hiện tại bằng `git grep` không phát hiện secrets trong các từ khóa đã tìm kiếm.
- Kiểm tra lịch sử Git bằng `git log -G` phát hiện một commit khớp từ khóa `password`, nhưng đã xác minh đó chỉ là tiêu đề tài liệu Security Checklist.
- Chưa thực hiện quét bằng công cụ chuyên dụng như Gitleaks hoặc TruffleHog.

**Kết luận:** Chưa phát hiện secrets qua các bước kiểm tra cơ bản. Kết quả không thay thế cho kiểm toán bảo mật toàn diện.

## 2. Kiểm tra dữ liệu đầu vào (Input Validation)

**Trạng thái:** ĐÃ LÀM

- Kiểm tra `order_id` và `product_id`.
- Kiểm tra `quantity`, `unit_price` và `reported_sales_amount`.
- Phát hiện dữ liệu thiếu hoặc không hợp lệ.
- Phân loại dữ liệu thành các dòng hợp lệ và bị từ chối.
- Xuất dữ liệu bị từ chối cùng lý do lỗi để phục vụ truy vết.

**Minh chứng:** `src/quality/`, `data/rejected/`, `docs/test-report.md`.

## 3. Phân quyền truy cập (Authorization)

**Trạng thái:** KHÔNG ÁP DỤNG

- Phiên bản BT3 là chương trình ETL chạy cục bộ, không cung cấp API, đăng nhập hoặc tài khoản người dùng.
- Không có chức năng truy cập dữ liệu theo từng chủ sở hữu.
- Nếu triển khai hệ thống nhiều người dùng trong tương lai, cần bổ sung xác thực và phân quyền truy cập dữ liệu.

**Minh chứng:** `run_etl.py`, `docker-compose.yml`.

## 4. Bảo vệ mật khẩu và mã hóa (Password Protection)

**Trạng thái:** KHÔNG ÁP DỤNG

- Hệ thống hiện tại không lưu tài khoản hoặc mật khẩu người dùng.
- SQLite Warehouse hoạt động dưới dạng file cục bộ.
- Chưa có cơ chế mã hóa dữ liệu SQLite ở trạng thái lưu trữ.

**Lưu ý:** Khi sử dụng dữ liệu bán hàng thực tế trong môi trường production, cần đánh giá yêu cầu mã hóa và quyền truy cập file database.

## 5. Xử lý lỗi an toàn (Safe Error Handling)

**Trạng thái:** ĐÃ LÀM MỘT PHẦN

- ETL kiểm tra sự tồn tại của các file đầu vào cần thiết.
- Dữ liệu không hợp lệ được ghi vào file rejected.
- Quá trình tạo SQLite sử dụng database tạm để hạn chế thay thế database đang có khi phát sinh lỗi.
- Chưa kiểm thử đầy đủ việc che giấu đường dẫn nội bộ hoặc thông tin nhạy cảm trong thông báo lỗi.

**Minh chứng:** `src/extract/extract_csv.py`, `src/quality/reject_logger.py`, `src/warehouse/build_sqlite_dwh.py`.

## 6. Bảo mật nhật ký (Secure Logging)

**Trạng thái:** ĐÃ LÀM MỘT PHẦN

- ETL in thống kê số dòng nguồn, hợp lệ, bị từ chối và số dòng Warehouse.
- Chưa tích hợp hệ thống ghi log tập trung.
- Chưa hoàn tất việc kiểm tra toàn bộ log để bảo đảm không xuất hiện dữ liệu cá nhân hoặc thông tin bí mật.

**Minh chứng:** `run_etl.py`.

## 7. Quản lý thư viện và kiểm tra lỗ hổng (Dependency Security)

**Trạng thái:** ĐÃ LÀM (kiểm tra cơ bản)

### Biện pháp đã thực hiện

- Cố định phiên bản thư viện Python trong `requirements.txt`:
  - `pandas==2.3.3`
  - `pytest==9.2.0`
- Dockerfile sử dụng Python `3.10.11-slim`.
- Sử dụng công cụ `pip-audit` để kiểm tra các lỗ hổng bảo mật đã được công bố.

### Kết quả kiểm tra thực tế

**Lệnh thực hiện:**

```bat
.venv\Scripts\python.exe -m pip_audit -r requirements.txt
```

**Kết quả:** PASS – Không phát hiện lỗ hổng bảo mật đã biết tại thời điểm kiểm tra.

**Minh chứng:**

- `requirements.txt`
- `Dockerfile`
- Kết quả chạy `pip-audit` trên Terminal.

### Giới hạn

- Kết quả quét chỉ phản ánh thông tin lỗ hổng đã biết tại thời điểm thực hiện.
- Cần quét lại dependency định kỳ khi triển khai hoặc nâng cấp hệ thống.
- Chưa thực hiện kiểm tra bảo mật toàn bộ Docker image.

## Kết luận

Hệ thống Mekong Mobile đã có các biện pháp bảo vệ cơ bản phù hợp với phạm vi đồ án ETL chạy cục bộ.

Những nội dung chưa hoàn tất gồm:

- Rà soát secrets trong lịch sử Git.
- Kiểm tra thông tin nhạy cảm trong log và thông báo lỗi.
- Quét lỗ hổng các thư viện phụ thuộc.
- Kiểm thử Docker trên môi trường triển khai thực tế.

Checklist phản ánh trạng thái hiện tại của dự án, không khẳng định hệ thống đã đáp ứng đầy đủ yêu cầu bảo mật production.
