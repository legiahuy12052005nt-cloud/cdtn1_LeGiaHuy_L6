
# HƯỚNG DẪN TRIỂN KHAI – MEKONG MOBILE DATA WAREHOUSE

## 1. Yêu cầu môi trường

### 1.1. Phần mềm cần thiết

Để triển khai quy trình ETL bằng Docker, máy tính cần:

- Hệ điều hành: Windows, Linux hoặc macOS có hỗ trợ Docker.
- Git: Dùng để tải mã nguồn từ GitHub.
- Docker Engine hoặc Docker Desktop: Có hỗ trợ Docker Compose V2.
- Kết nối Internet: Dùng để tải mã nguồn và xây dựng Docker Image.
- Dung lượng trống: Khuyến nghị tối thiểu 2 GB cho Docker Image và dữ liệu mẫu.

Kiểm tra Docker:

```bash
docker --version
```

Kiểm tra Docker Compose:

```bash
docker compose version
```

Phiên bản Python bên trong Docker Image là Python 3.10.11.

Không cần cài Python trực tiếp trên máy để chạy ETL bằng Docker.

### 1.2. Cổng kết nối

ETL là chương trình xử lý dữ liệu theo lô, không chạy Web Server.

Vì vậy, hệ thống không yêu cầu cổng HTTP riêng như 8000 hoặc 8080.

### 1.3. Lưu ý về môi trường

Đã kiểm thử Docker Compose thành công trên GitHub Actions sử dụng Ubuntu Linux.

Chưa xác minh Docker Desktop trực tiếp trên máy Windows phát triển.

---

## 2. Các bước dựng và chạy hệ thống

### 2.1. Tải mã nguồn

Dự án sử dụng GitHub Repository công khai:

https://github.com/legiahuy12052005nt-cloud/cdtn1_LeGiaHuy_L6

Tải đúng phiên bản phát hành BT3:

```bash
git clone --branch v1.0 https://github.com/legiahuy12052005nt-cloud/cdtn1_LeGiaHuy_L6.git
```

Di chuyển vào thư mục dự án:

```bash
cd cdtn1_LeGiaHuy_L6
```

Lưu ý: Tag v1.0 phải được tạo và đẩy lên GitHub trước khi thực hiện bước này.

### 2.2. Khởi động quy trình ETL

Sau khi vào thư mục dự án, chạy:

```bash
docker compose run --build --rm pipeline
```

Đây là một lệnh Docker Compose để xây dựng Image và thực thi ETL.

Quy trình sẽ tự động:

1. Tạo môi trường Python trong Docker.
2. Cài đặt thư viện từ requirements.txt.
3. Nạp dữ liệu mẫu đã đóng gói.
4. Đọc dữ liệu CSV.
5. Chuẩn hóa và kiểm tra dữ liệu đầu vào.
6. Phân loại dữ liệu hợp lệ và bị từ chối.
7. Đối soát doanh thu.
8. Xây dựng bảng Dimension và Fact.
9. Tạo các file Warehouse CSV.
10. Tạo SQLite Data Warehouse.

ETL là chương trình chạy theo lô. Container kết thúc sau khi hoàn thành xử lý là hành vi bình thường, không phải lỗi.

### 2.3. Các file cấu hình triển khai

| File | Chức năng |
|---|---|
| Dockerfile | Xây dựng Docker Image chứa môi trường Python và mã nguồn ETL |
| docker-compose.yml | Khai báo dịch vụ ETL và thư mục dữ liệu đầu ra |
| .dockerignore | Loại bỏ các file không cần thiết khỏi Docker build context |
| .env.example | Ghi chú các đường dẫn cấu hình tham khảo |
| requirements.txt | Khai báo phiên bản thư viện Python |
| run_etl.py | Điểm bắt đầu thực thi quy trình ETL |

---

## 3. Biến môi trường và cấu hình

Dự án có file `.env.example` gồm các thông tin:

| Biến | Ý nghĩa | Giá trị mẫu | Bắt buộc |
|---|---|---|---|
| SOURCE_DIR | Thư mục dữ liệu nguồn | data/raw | Không |
| OUTPUT_DIR | Thư mục dữ liệu đã xử lý | data/processed | Không |
| DWH_URL | Đường dẫn SQLite Data Warehouse | sqlite:///data/warehouse/mekong_mobile.db | Không |

### 3.1. Giới hạn cấu hình

Trong phiên bản BT3, chương trình ETL đang sử dụng các đường dẫn tương đối được khai báo trực tiếp trong mã nguồn.

Các biến trong `.env.example` chỉ có mục đích mô tả cấu hình tham khảo.

Việc thay đổi các biến này chưa làm thay đổi đường dẫn xử lý dữ liệu của chương trình.

Vì vậy, không cần tạo file `.env` để chạy bản Docker mẫu hiện tại.

### 3.2. Bảo mật cấu hình

Không đưa mật khẩu, API Key hoặc thông tin nhạy cảm vào GitHub Repository.

File `.env` được loại khỏi Git thông qua `.gitignore`.

---

## 4. Dữ liệu mẫu và kết quả xử lý

### 4.1. Dữ liệu mẫu

Bốn file CSV dùng để kiểm thử triển khai được lưu tại:

```text
data/sample/
```

Gồm:

- orders_2024_2026.csv
- order_items.csv
- products.csv
- stores.csv

Khi xây dựng Docker Image, các file này được sao chép tự động vào thư mục `data/raw/` bên trong container.

Không cần thực hiện thao tác nhập dữ liệu mẫu thủ công.

### 4.2. Dữ liệu đầu ra

Sau khi ETL chạy thành công, chương trình tạo các file:

```text
data/
├── processed/
│   └── clean_order_items.csv
├── rejected/
│   └── rejected_order_items.csv
└── warehouse/
    ├── Dim_Date.csv
    ├── Dim_Product.csv
    ├── Dim_Store.csv
    ├── Fact_Sales.csv
    └── mekong_mobile.db
```

Các thư mục đầu ra được ánh xạ từ container ra máy chạy Docker thông qua docker-compose.yml.

### 4.3. Số lượng dữ liệu mẫu mong đợi

| Bảng SQLite | Số bản ghi |
|---|---:|
| dim_date | 3 |
| dim_product | 3 |
| dim_store | 2 |
| fact_sales | 4 |

Các số liệu này chỉ áp dụng cho bộ dữ liệu mẫu dùng trong Docker.

Bộ dữ liệu đầy đủ được sử dụng để phân tích chất lượng dữ liệu có quy mô lớn hơn và không được nhầm lẫn với dữ liệu mẫu Docker.

---

## 5. Kiểm tra hệ thống đã chạy đúng

### 5.1. Kiểm tra thông báo ETL

Sau khi chạy Docker Compose, Terminal phải hiển thị thông báo hoàn thành:

```text
=== HOAN THANH ETL ===
```

Nếu chương trình báo lỗi hoặc kết thúc bất thường, cần kiểm tra log thực thi.

### 5.2. Kiểm tra cơ sở dữ liệu SQLite

Sau khi ETL hoàn thành, chạy lệnh sau tại thư mục gốc dự án:

```bash
docker compose run --rm pipeline python -c "import sqlite3; c=sqlite3.connect('data/warehouse/mekong_mobile.db'); print({t:c.execute('SELECT COUNT(*) FROM '+t).fetchone()[0] for t in ['dim_date','dim_product','dim_store','fact_sales']})"
```

Kết quả mong đợi:

```text
{'dim_date': 3, 'dim_product': 3, 'dim_store': 2, 'fact_sales': 4}
```

Lệnh này kiểm tra trực tiếp số bản ghi trong SQLite Data Warehouse.

### 5.3. Kiểm tra khả năng chạy lại

Chạy lại:

```bash
docker compose run --rm pipeline
```

Kết quả mong đợi:

- ETL hoàn thành không có lỗi.
- Cơ sở dữ liệu SQLite được tạo lại thành công.
- Bảng fact_sales vẫn có 4 bản ghi.
- Không phát sinh dữ liệu trùng do chạy lại trên cùng bộ dữ liệu mẫu.

### 5.4. Chạy bộ kiểm thử tự động

Bộ kiểm thử Python được lưu trong thư mục:

```text
tests/
```

Để chạy trực tiếp ngoài Docker, cần cài Python và các thư viện trong requirements.txt.

Sau khi cài đặt phụ thuộc, thực thi từ thư mục gốc dự án:

```bash
python -m pytest tests/ -v
```

Kết quả mong đợi: Các test case hợp lệ của bộ kiểm thử phải PASS.

Lưu ý: Lệnh này sử dụng môi trường Python của máy thực thi, không phải container ETL. Docker Image hiện tại chưa đóng gói thư mục tests/.

### 5.5. Minh chứng kiểm thử Docker

Quy trình Docker đã được kiểm thử trên GitHub Actions.

Các phép kiểm tra đã PASS:

- Xây dựng Docker Image.
- Chạy ETL.
- Tạo SQLite Data Warehouse.
- Kiểm tra bốn bảng SQLite.
- Chạy lại ETL.
- Xác nhận dữ liệu không bị nhân đôi.

Minh chứng:

`docs/evidence/docker_pass_BT3.PNG`

GitHub Actions Workflow:

`.github/workflows/docker-test.yml`

### 5.6. Dashboard Power BI

File Dashboard:

`powerbi/Mekong_Mobile_Dashboard_BT2_Final.pbit`

Power BI Dashboard chạy riêng bằng Power BI Desktop trên Windows.

Docker chỉ đóng gói quy trình ETL và SQLite Data Warehouse, không tự khởi động giao diện Power BI.

---

## 6. Kết luận triển khai

Trạng thái triển khai: ĐÃ KIỂM THỬ THÀNH CÔNG TRÊN GITHUB ACTIONS.

Quy trình ETL đã được xây dựng và chạy bằng Docker Compose trên môi trường Ubuntu Linux.

Hệ thống có dữ liệu mẫu tự động, tạo được SQLite Data Warehouse và có thể chạy lại mà không nhân đôi dữ liệu.

Chưa kiểm chứng Docker Desktop chạy trực tiếp trên máy Windows phát triển.

Giới hạn hiện tại:

- Chưa triển khai dịch vụ Web.
- Chưa có lịch chạy ETL tự động.
- Chưa có Incremental Loading.
- Chưa đóng gói Power BI vào Docker.
- Chưa triển khai cơ chế mã hóa file SQLite.
