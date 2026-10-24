# Xây dựng kho dữ liệu bán hàng và Dashboard phân tích doanh thu cho Mekong Mobile

**Sinh viên:**
Lê Gia Huy - 2374802010175 - Lớp: 71K29CNTT02


**Link GitHub:** [Repository đồ án Mekong Mobile](https://github.com/legiahuy12052005nt-cloud/cdtn1_LegiaHuy_L6)


**Học phần:**
Chuyên đề Tốt nghiệp 1 - Lớp HP: 261_71ITGR40203_02

**Luồng nghiệp vụ:**
L6 - (DA) Trích xuất, làm sạch dữ liệu và xây dựng báo cáo

## 1. Mục tiêu
Dự án tự động hóa quá trình trích xuất và làm sạch dữ liệu bán hàng từ các nguồn tài liệu thô (file Excel). Dữ liệu sau khi xử lý sẽ được lưu trữ tập trung để phục vụ việc xây dựng Dashboard trên Power BI, cung cấp báo cáo doanh thu trực quan giúp ban quản lý dễ dàng theo dõi và ra quyết định.

## 2. Yêu cầu môi trường
* Các thư viện Python: xem file `requirements.txt` (pandas, openpyxl,...)
### 2.1. Công cụ sử dụng

- Python 3.10 trở lên
- Visual Studio Code
- Git và GitHub
- Power BI Desktop (sử dụng ở giai đoạn xây dựng Dashboard)

### 2.2. Thư viện Python

Dự án sử dụng thư viện pandas để đọc, xử lý, kiểm tra
và xây dựng dữ liệu kho bán hàng.

Cài đặt các thư viện bằng lệnh:

```powershell
pip install -r requirements.txt
```

### 2.3. Dữ liệu đầu vào

Dự án sử dụng 5 file CSV:

- `customers_raw.csv`: Dữ liệu khách hàng.
- `orders_2024_2026.csv`: Dữ liệu đơn hàng.
- `order_items.csv`: Chi tiết đơn hàng.
- `products.csv`: Danh mục sản phẩm.
- `stores.csv`: Danh mục cửa hàng.

Các file dữ liệu nguồn được lưu trong thư mục `data/raw/`.

**Lưu ý:** Dữ liệu CSV thô không được theo dõi trong
phiên bản Git hiện tại nhằm hạn chế công khai thông tin
khách hàng và giao dịch. Người chạy dự án cần chuẩn bị
dữ liệu nguồn trong thư mục `data/raw/`.

### 2.4. Lệnh chạy ETL

Tại thư mục gốc dự án, chạy:

```powershell
python run_etl.py
```

Chương trình thực hiện:

1. Extract: Đọc dữ liệu từ các file CSV.
2. Transform: Chuẩn hóa và đối soát dữ liệu bán hàng.
3. Quality: Kiểm tra dữ liệu và ghi nhận dòng không hợp lệ.
4. Load: Lưu dữ liệu trung gian và xây dựng Star Schema.

Kết quả được lưu tại:

- `data/processed/clean_order_items.csv`
- `data/rejected/rejected_order_items.csv`
- `data/warehouse/Dim_Date.csv`
- `data/warehouse/Dim_Product.csv`
- `data/warehouse/Dim_Store.csv`
- `data/warehouse/Fact_Sales.csv`



## 3. Hướng dẫn chạy

### 3.1. Clone repository

Mở PowerShell tại thư mục muốn lưu dự án.

Bước 1 – Clone mã nguồn:

```powershell
git clone https://github.com/legiahuy12052005nt-cloud/cdtn1_LegiaHuy_L6.git
```

Bước 2 – Di chuyển vào thư mục dự án:

```powershell
cd cdtn1_LegiaHuy_L6
```

### 3.2. Chuẩn bị môi trường Python

Yêu cầu Python 3.10 trở lên.

Bước 3 – Tạo môi trường ảo:

```powershell
python -m venv .venv
```

Bước 4 – Cài đặt thư viện:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

### 3.3. Chuẩn bị dữ liệu đầu vào

Đặt 4 file CSV vào thư mục `data/raw/`:

- orders_2024_2026.csv
- order_items.csv
- products.csv
- stores.csv

Dữ liệu khách hàng thô không cần thiết cho pipeline hiện tại.

Lưu ý: Dữ liệu gốc không được đưa vào commit mới trên GitHub Public.

Hiện repository chưa cung cấp bộ dữ liệu mẫu công khai để chạy ETL ngay sau khi clone. Cần chuẩn bị dữ liệu theo đúng cấu trúc nguồn hoặc sử dụng bộ dữ liệu mẫu đã được ẩn danh khi bộ dữ liệu đó được bổ sung.

### 3.4. Chạy toàn bộ ETL và SQLite DWH

Bước 5 – Chạy quy trình chính:

```powershell
.\.venv\Scripts\python.exe run_etl.py
```

Quy trình thực hiện:

1. Đọc dữ liệu nguồn CSV.
2. Chuẩn hóa và kiểm tra dữ liệu.
3. Đối soát doanh thu.
4. Xây dựng Fact_Sales và 3 bảng Dimension.
5. Xuất dữ liệu ra CSV Warehouse.
6. Tạo SQLite Data Warehouse với khóa chính, khóa ngoại và các ràng buộc dữ liệu.

Kết quả được lưu tại:

- data/processed/clean_order_items.csv
- data/rejected/rejected_order_items.csv
- data/warehouse/Dim_Date.csv
- data/warehouse/Dim_Product.csv
- data/warehouse/Dim_Store.csv
- data/warehouse/Fact_Sales.csv
- data/warehouse/mekong_mobile.db

### 3.5. Chạy Unit Test

Bước 6 – Chạy toàn bộ bài kiểm thử tự động:

```powershell
.\.venv\Scripts\python.exe -m pytest tests/ -v
```

Kết quả đã xác nhận trên môi trường phát triển:

- 6 Unit Test PASS.
- Có kiểm thử giá trị biên: số lượng bằng 0.
- Có kiểm thử ngoại lệ: số lượng âm.


### 3.6. Mở Dashboard Power BI

Dự án cung cấp Power BI Template tại:

`powerbi/Mekong_Mobile_Sales_Dashboard_Demo_Final.pbit`

Template chứa cấu trúc Dashboard, các biểu đồ, Measure DAX
và mô hình dữ liệu, không đóng gói dữ liệu đã tải vào báo cáo.

**Bước 7 – Chuẩn bị dữ liệu mẫu**

Sao chép 4 file CSV trong `data/sample/` vào `data/raw/`
trước khi chạy ETL.

**Bước 8 – Chạy ETL**

```powershell
.\.venv\Scripts\python.exe run_etl.py
```

Lệnh tạo 4 bảng CSV Warehouse và SQLite Database.

**Bước 9 – Mở Dashboard**

Mở file `Mekong_Mobile_Sales_Dashboard_Demo_Final.pbit`
bằng Power BI Desktop.

Khi hộp thoại Parameter xuất hiện:

- Parameter: `ProjectFolder`
- Giá trị: Đường dẫn tuyệt đối đến thư mục gốc dự án vừa clone.

Ví dụ: Nếu dự án được clone vào `C:\Projects\cdtn1_LeGiaHuy_L6`,
nhập chính đường dẫn đó vào `ProjectFolder`.

Nhấn **Load** để Power BI đọc dữ liệu từ thư mục
`data/warehouse/` và hiển thị Dashboard.

Dashboard gồm 3 trang:

1. Tổng Quan Doanh Thu.
2. Phân Tích Sản Phẩm.
3. Phân Tích Cửa Hàng.

Bộ dữ liệu mẫu có kết quả kỳ vọng:

| KPI | Giá trị |
|---|---:|
| Tổng doanh thu | 23.500.000 VND |
| Tổng đơn hàng | 3 |
| Tổng sản phẩm bán | 5 |
| Giá trị đơn hàng trung bình | 7.833.333 VND |

**Lưu ý:** File `.pbix` sử dụng dữ liệu đầy đủ được giữ
cục bộ và không chia sẻ trên GitHub Public.


### 3.7. Kiểm tra kết quả

Với bộ dữ liệu Mekong Mobile hiện tại, kết quả đã xác nhận:

| Chỉ tiêu | Giá trị |
|---|---:|
| Fact_Sales | 35.697 dòng |
| Dim_Date | 792 dòng |
| Dim_Product | 320 dòng |
| Dim_Store | 24 dòng |
| MATCH | 35.177 dòng |
| MISMATCH | 520 dòng |
| Fact thiếu date_key | 154 dòng |
| Tổng doanh thu | 415.773.438.750 VND |

Các kết quả trên chỉ áp dụng cho bộ dữ liệu đã kiểm thử, không phải kết quả cố định của mọi bộ dữ liệu đầu vào.

## 4. Cấu trúc thư mục
```text
cdtn1_LeGiaHuy_L6/
├── data/
│   ├── raw/              # Dữ liệu CSV nguồn
│   ├── processed/        # Dữ liệu sau khi làm sạch và đối soát
│   ├── rejected/         # Các dòng bị từ chối và lý do lỗi
│   └── warehouse/        # Các bảng Fact và Dimension
│
├── docs/                 # Tài liệu phân tích và thiết kế
│   ├── evidence/         # Ảnh minh chứng kiểm thử
│   ├── srs.md
│   ├── data-requirements.md
│   ├── thay-doi-thiet-ke.md
│   ├── usecase.drawio
│   ├── architecture.drawio
│   ├── data-flow.drawio
│   └── erd.drawio
│
├── src/
│   ├── extract/          # Đọc dữ liệu CSV
│   ├── transform/        # Chuẩn hóa và đối soát doanh thu
│   ├── quality/          # Kiểm tra dữ liệu và ghi Error Log
│   ├── load/             # Lưu dữ liệu đầu ra
│   ├── warehouse/        # Xây dựng Star Schema
│   ├── dashboard/        # Phát triển Dashboard
│   └── etl/              # Smoke test từ giai đoạn đầu
│
├── run_etl.py            # Chạy toàn bộ quy trình ETL
├── requirements.txt      # Thư viện Python
├── .gitignore            # Danh sách file không đưa lên Git
└── README.md             # Hướng dẫn sử dụng dự án
```

### Giải thích

- `src/extract/`: Đọc dữ liệu bán hàng.
- `src/transform/`: Chuẩn hóa tên cột và đối soát doanh thu.
- `src/quality/`: Kiểm tra dữ liệu, ghi nhận bản ghi lỗi.
- `src/load/`: Xuất kết quả xử lý và các bảng kho dữ liệu.
- `src/warehouse/`: Xây dựng `Dim_Date`, `Dim_Product`,
  `Dim_Store` và `Fact_Sales`.
- `run_etl.py`: Điểm chạy chính của toàn bộ pipeline.

Các thư mục `data/raw/`, `data/processed/`, `data/rejected/`
và `data/warehouse/` được loại trừ khỏi các commit mới
để hạn chế công khai dữ liệu nguồn và dữ liệu giao dịch.

## 5. Kiểm thử

### 5.1. Kiểm thử quy trình ETL

Dự án đã thực hiện kiểm thử thủ công thông qua Terminal
để xác nhận các module Extract, Transform, Quality và Load
hoạt động đúng với dữ liệu nguồn.

| Mã kiểm thử | Nội dung | Kết quả | Trạng thái |
|---|---|---|---|
| TC01 | Đọc dữ liệu order_items.csv | 35.697 dòng, 5 cột | PASS |
| TC02 | Chuẩn hóa tên cột dữ liệu bán hàng | Giữ nguyên 35.697 dòng | PASS |
| TC03 | Kiểm tra dữ liệu hợp lệ | 35.697 dòng hợp lệ, 0 dòng bị từ chối | PASS |
| TC04 | Kiểm thử ghi Error Log bằng dữ liệu lỗi giả lập | Phát hiện 1 dòng lỗi và ghi rõ lý do | PASS |
| TC05 | Đối soát doanh thu | 35.177 MATCH, 520 MISMATCH | PASS |
| TC06 | Xây dựng Dim_Date | 792 ngày, không trùng date_key | PASS |
| TC07 | Xây dựng Dim_Product | 320 sản phẩm, không trùng khóa | PASS |
| TC08 | Xây dựng Dim_Store | 24 cửa hàng, không trùng khóa | PASS |
| TC09 | Xây dựng Fact_Sales | 35.697 dòng, 12 cột, không trùng khóa | PASS |
| TC10 | Chạy lại ETL trên cùng dữ liệu | Không tăng số dòng Fact_Sales | PASS |
| TC11 | Kiểm tra dòng Fact thiếu ngày | 154 dòng từ 114 đơn hàng thiếu ngày | PASS |
| TC12 | Đối chiếu tổng doanh thu nguồn và Fact | Chênh lệch 0 VNĐ | PASS |

### 5.2. Kiểm thử các yêu cầu phi chức năng

- **NFR01 – Hiệu năng:** Chưa thực hiện đo thời gian ETL
  để đối chiếu với ngưỡng 120 giây.
- **NFR02 – Ghi nhận dữ liệu lỗi:** Đã kiểm thử ghi Error Log
  bằng một dòng dữ liệu lỗi giả lập. Chưa kiểm chứng đầy đủ
  yêu cầu ghi nhận 100% dòng lỗi trong nhiều tình huống.
- **NFR03 – Không tạo dữ liệu Fact trùng khi chạy lại:**
  Đã kiểm thử thành công trên cùng bộ dữ liệu với
  cơ chế ghi đè file CSV. Chưa kiểm thử upsert trên CSDL.

### 5.3. Kết quả kiểm tra chất lượng dữ liệu

- Phát hiện 520 dòng chênh lệch giữa doanh thu nguồn
  và doanh thu tính toán.
- Giữ nguyên 11 dòng chi tiết đơn hàng trùng hoàn toàn
  để bảo toàn grain theo từng dòng nguồn.
- Ghi nhận 114 đơn hàng thiếu ngày, tương ứng
  154 dòng Fact_Sales thiếu date_key.
- Không tự động sửa doanh thu hoặc gán ngày giả.
- Tổng doanh thu nguồn và Fact_Sales đều bằng
  415.773.438.750 VNĐ.

### 5.4. Bằng chứng kiểm thử

Ảnh minh chứng kiểm thử chạy lại ETL được lưu tại:

`docs/evidence/nfr03_etl_rerun.png`

Các kết quả trên được kiểm tra thủ công thông qua
các lệnh Python trong Terminal.

Bộ kiểm thử tự động sẽ được bổ sung ở giai đoạn tiếp theo.

### 5.5. Kiểm thử End-to-End (E2E) trên bản clone GitHub

Mục tiêu: Kiểm tra khả năng chạy hệ thống sau khi clone repository
từ GitHub vào một thư mục mới, không sử dụng dữ liệu thật.

Quy trình kiểm thử:

1. Clone repository từ GitHub vào thư mục độc lập.
2. Sao chép 4 file CSV giả lập từ `data/sample/` vào `data/raw/`.
3. Chạy `python run_etl.py`.
4. Kiểm tra dữ liệu trong SQLite Data Warehouse.
5. Chạy `python -m pytest tests/ -v`.

Kết quả kiểm thử:

| Hạng mục | Kết quả | Trạng thái |
|---|---|---|
| Clone repository GitHub | Thành công | PASS |
| Đọc dữ liệu CSV giả lập | 4 file | PASS |
| Chạy ETL | Tạo các bảng Warehouse | PASS |
| Tạo SQLite Database | mekong_mobile.db | PASS |
| Dim_Date | 3 dòng | PASS |
| Dim_Product | 3 dòng | PASS |
| Dim_Store | 2 dòng | PASS |
| Fact_Sales | 4 dòng | PASS |
| Kiểm tra khóa ngoại | Không có lỗi | PASS |
| Unit Test | 6 bài kiểm thử PASS | PASS |

Minh chứng:

- `docs/evidence/e2e_github_clone_pytest.PNG`
- `docs/evidence/e2e_github_clone_sqlite.PNG`

Lưu ý: Bài kiểm thử này xác nhận luồng
GitHub → CSV mẫu → ETL → SQLite → pytest.

Dashboard Power BI sử dụng dữ liệu Warehouse CSV và được kiểm thử
riêng; chưa bao gồm trong bài kiểm thử E2E tự động trên bản clone.




## 6. Trạng thái hiện tại

### 6.1. Các công việc đã hoàn thành

- [x] Khởi tạo repository GitHub và cấu trúc dự án.
- [x] Phân tích yêu cầu và xây dựng tài liệu SRS.
- [x] Thiết kế Use Case, Architecture, Data Flow và Star Schema.
- [x] Xây dựng pipeline Extract, Transform, Quality và Load.
- [x] Chuẩn hóa và đối soát dữ liệu doanh thu.
- [x] Xây dựng Dim_Date, Dim_Product, Dim_Store và Fact_Sales.
- [x] Tạo SQLite Data Warehouse với các ràng buộc dữ liệu.
- [x] Kiểm tra khóa chính và khóa ngoại của Data Warehouse.
- [x] Xây dựng Dashboard Power BI gồm 3 trang phân tích.
- [x] Bổ sung đường doanh thu trung bình vào biểu đồ.
- [x] Xây dựng chỉ số tăng trưởng doanh thu theo tháng.
- [x] Xây dựng 6 Unit Test tự động.
- [x] Kiểm thử E2E bằng dữ liệu mẫu trên bản clone GitHub.
- [x] Bổ sung README hướng dẫn chạy dự án.
- [x] Lưu minh chứng kiểm thử trong docs/evidence.
- [x] Đáp ứng yêu cầu tối thiểu 8 Conventional Commits.

### 6.2. Kết quả dữ liệu thực tế

| Chỉ tiêu | Kết quả |
|---|---:|
| Tổng số đơn hàng | 26.000 |
| Tổng số dòng Fact_Sales | 35.697 |
| Số sản phẩm | 320 |
| Số cửa hàng | 24 |
| Số ngày trong Dim_Date | 792 |
| Dòng doanh thu MATCH | 35.177 |
| Dòng doanh thu MISMATCH | 520 |
| Dòng Fact thiếu date_key | 154 |
| Tổng doanh thu | 415.773.438.750 VND |

### 6.3. Công việc cần hoàn thiện

- [ ] Thực hiện Peer Review và ghi nhận nhận xét.
- [ ] Rà soát toàn bộ tài liệu trước khi nộp.
- [ ] Chuẩn bị báo cáo và bài thuyết trình đồ án.

### 6.4. Lưu ý kỹ thuật

- Data Warehouse được lưu dưới dạng SQLite và các file CSV.
- Dashboard Power BI hiện kết nối với CSV Warehouse, chưa đọc trực tiếp từ SQLite.
- Dữ liệu khách hàng thật và file PBIX không được đưa vào các commit mới trên GitHub Public.
- Bộ dữ liệu mẫu trong data/sample/ được sử dụng để kiểm thử và hướng dẫn chạy dự án.
