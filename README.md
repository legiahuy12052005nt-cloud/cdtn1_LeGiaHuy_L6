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

### 3.1. Chuẩn bị dự án

Clone repository từ GitHub:

```powershell
git clone https://github.com/legiahuy12052005nt-cloud/cdtn1_LegiaHuy_L6.git
```

Di chuyển vào thư mục dự án:

```powershell
cd cdtn1_LegiaHuy_L6
```

Cài đặt thư viện Python:

```powershell
python -m pip install -r requirements.txt
```

### 3.2. Chuẩn bị dữ liệu nguồn

Đặt các file dữ liệu CSV vào thư mục `data/raw/`:

- `orders_2024_2026.csv`
- `order_items.csv`
- `products.csv`
- `stores.csv`

File `customers_raw.csv` thuộc bộ dữ liệu nghiên cứu,
nhưng chưa được sử dụng trong pipeline Star Schema hiện tại.

Lưu ý: Các file dữ liệu thô không được đưa vào các
commit mới trên GitHub Public.

### 3.3. Chạy quy trình ETL

Tại thư mục gốc của dự án, chạy:

```powershell
python run_etl.py
```

Quy trình sẽ thực hiện các công việc:

1. Đọc dữ liệu nguồn CSV (Extract).
2. Chuẩn hóa tên cột và kiểm tra dữ liệu (Transform, Quality).
3. Ghi nhận các dòng không hợp lệ vào Error Log.
4. Đối soát doanh thu nguồn và doanh thu tính toán.
5. Xây dựng ba bảng Dimension và một bảng Fact.
6. Xuất kết quả vào thư mục `data/warehouse/`.

### 3.4. Kiểm tra kết quả

Sau khi ETL chạy thành công, kiểm tra bốn file:

- `data/warehouse/Dim_Date.csv`
- `data/warehouse/Dim_Product.csv`
- `data/warehouse/Dim_Store.csv`
- `data/warehouse/Fact_Sales.csv`

Kết quả kiểm thử trên bộ dữ liệu hiện tại:

| Bảng | Số dòng |
|---|---:|
| Dim_Date | 792 |
| Dim_Product | 320 |
| Dim_Store | 24 |
| Fact_Sales | 35.697 |

Kết quả kiểm tra chất lượng:

- 520 dòng doanh thu có chênh lệch (MISMATCH).
- 154 dòng Fact_Sales thiếu date_key do 114 đơn hàng thiếu ngày.
- Không có source_line_id trùng lặp.
- Chạy lại ETL trên cùng bộ dữ liệu không làm tăng số dòng Fact_Sales.

Các kết quả trên là số liệu kiểm thử của bộ dữ liệu hiện tại,
không phải số liệu cố định cho mọi bộ dữ liệu.


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



## 6. Trạng thái hiện tại

### 6.1. Các công việc đã hoàn thành

- [x] Khởi tạo repository GitHub và cấu trúc dự án.
- [x] Xây dựng tài liệu SRS và phân tích yêu cầu nghiệp vụ L6.
- [x] Thiết kế Use Case, Architecture, Data Flow và Star Schema.
- [x] Cập nhật tài liệu thiết kế theo phản hồi BT1.
- [x] Xây dựng module Extract để đọc dữ liệu CSV.
- [x] Xây dựng module Transform để chuẩn hóa dữ liệu bán hàng.
- [x] Xây dựng module Quality để kiểm tra và ghi nhận dòng lỗi.
- [x] Xây dựng module Load để lưu dữ liệu đã xử lý.
- [x] Tích hợp quy trình ETL chạy bằng lệnh `python run_etl.py`.
- [x] Xây dựng ba bảng Dimension: Dim_Date, Dim_Product, Dim_Store.
- [x] Xây dựng bảng Fact_Sales theo Star Schema.
- [x] Kiểm tra dữ liệu nguồn và đối soát doanh thu.
- [x] Kiểm thử chạy lại ETL không phát sinh dòng Fact trùng lặp ở mức CSV.

### 6.2. Kết quả kiểm thử hiện tại

| Chỉ tiêu | Kết quả |
|---|---:|
| Tổng số đơn hàng | 26.000 |
| Tổng số dòng chi tiết đơn hàng | 35.697 |
| Số sản phẩm | 320 |
| Số cửa hàng | 24 |
| Số ngày trong Dim_Date | 792 |
| Số dòng Fact_Sales | 35.697 |
| Dòng doanh thu khớp (MATCH) | 35.177 |
| Dòng doanh thu chênh lệch (MISMATCH) | 520 |
| Đơn hàng thiếu ngày | 114 |
| Dòng Fact_Sales thiếu date_key | 154 |
| Tổng doanh thu nguồn | 415.773.438.750 VNĐ |
| Chênh lệch tổng doanh thu nguồn và Fact | 0 VNĐ |

### 6.3. Các công việc đang và sẽ thực hiện

- [ ] Hoàn thiện bộ kiểm thử tự động cho ETL và Data Warehouse.
- [ ] Kiểm tra hiệu năng ETL theo ngưỡng NFR01.
- [ ] Kiểm chứng đầy đủ yêu cầu ghi nhận lỗi theo NFR02.
- [ ] Hoàn thiện chính sách xử lý dữ liệu thiếu và bất thường.
- [ ] Xây dựng Dashboard phân tích doanh thu bằng Power BI.
- [ ] Kiểm thử Dashboard và đối chiếu các chỉ tiêu với Data Warehouse.
- [ ] Hoàn thiện tài liệu báo cáo và minh chứng kiểm thử.

### 6.4. Lưu ý

Pipeline hiện tại xây dựng Data Warehouse dưới dạng các file CSV.

Kết quả kiểm thử NFR03 mới xác nhận việc chạy lại ETL
không làm tăng số dòng Fact_Sales khi ghi đè CSV.
Chưa triển khai và kiểm thử cơ chế upsert trên cơ sở dữ liệu.

Các dòng thiếu ngày vẫn được bảo toàn trong Fact_Sales
và được ghi nhận để xử lý trong quá trình phân tích báo cáo.

