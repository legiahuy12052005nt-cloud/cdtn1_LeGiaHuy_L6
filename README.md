# Xây dựng kho dữ liệu bán hàng và Dashboard phân tích doanh thu cho Mekong Mobile

**Sinh viên:**
Lê Gia Huy - 2374802010175 - Lớp: 71K29CNTT02


**Link GitHub:** [Repository đồ án Mekong Mobile](https://github.com/legiahuy12052005nt-cloud/cdtn1_LegiaHuy_L6)


**Học phần:**
Chuyên đề Tốt nghiệp 1 - Lớp HP: 261_71ITGR40203_02

**Luồng nghiệp vụ:**
L6 - (DA) Trích xuất, làm sạch dữ liệu và xây dựng báo cáo

1. Mục tiêu
Dự án xây dựng quy trình ETL để trích xuất, làm sạch, kiểm tra và đối soát dữ liệu bán hàng từ các file CSV. Dữ liệu sau xử lý được lưu trong kho dữ liệu SQLite và các bảng CSV theo mô hình Star Schema, phục vụ Dashboard Power BI để theo dõi doanh thu, sản phẩm và cửa hàng.
2. Yêu cầu môi trường
- Các thư viện Python: xem file requirements.txt.
2.1. Công cụ sử dụng
- Python 3.10 trở lên.
- Visual Studio Code.
- Git và GitHub.
- Power BI Desktop để mở Dashboard.
2.2. Thư viện Python
Dự án sử dụng các thư viện trong requirements.txt để xử lý dữ liệu và chạy kiểm thử. Cài đặt bằng lệnh:
python -m pip install -r requirements.txt
2.3. Dữ liệu đầu vào
Pipeline ETL hiện sử dụng 4 file CSV:
- orders_2024_2026.csv: Dữ liệu đơn hàng.
- order_items.csv: Chi tiết đơn hàng.
- products.csv: Danh mục sản phẩm.
- stores.csv: Danh mục cửa hàng.
Các file được đặt trong thư mục data/raw/.

Lưu ý: File customers_raw.csv không được sử dụng trong pipeline hiện tại. Dữ liệu giao dịch và khách hàng thật không được đưa vào các commit công khai mới; bản GitHub cung cấp dữ liệu giả lập để kiểm thử.
2.4. Lệnh chạy ETL
Tại thư mục gốc dự án, chạy:
python run_etl.py
Chương trình thực hiện:
1. Extract: Đọc dữ liệu từ các file CSV.
2. Transform: Chuẩn hóa và đối soát dữ liệu bán hàng.
3. Quality: Kiểm tra dữ liệu, thống kê lỗi và ghi nhận dòng không hợp lệ.
4. Load: Lưu dữ liệu đã xử lý và xây dựng Star Schema.
Kết quả được lưu tại:
- data/processed/clean_order_items.csv
- data/rejected/rejected_order_items.csv (khi có dữ liệu bị từ chối).
- data/warehouse/Dim_Date.csv
- data/warehouse/Dim_Product.csv
- data/warehouse/Dim_Store.csv
- data/warehouse/Fact_Sales.csv
- data/warehouse/mekong_mobile.db
3. Hướng dẫn chạy
3.1. Clone repository
Mở PowerShell tại thư mục muốn lưu dự án.

Bước 1 – Clone mã nguồn:
git clone https://github.com/legiahuy12052005nt-cloud/cdtn1_LegiaHuy_L6.git
Bước 2 – Di chuyển vào thư mục dự án:
cd cdtn1_LegiaHuy_L6
Khi giảng viên yêu cầu kiểm thử đúng phiên bản Bài tập 2, có thể chuyển sang tag v0.2 sau khi tag được tạo và đẩy lên GitHub:
git fetch --tags
git checkout v0.2
3.2. Chuẩn bị môi trường Python
Yêu cầu Python 3.10 trở lên.

Bước 3 – Tạo môi trường ảo:
python -m venv .venv
Bước 4 – Cài đặt thư viện:
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
3.3. Chuẩn bị dữ liệu đầu vào
Chạy thử bằng dữ liệu mẫu từ GitHub:

Repository cung cấp 4 file CSV giả lập trong data/sample/ để chạy thử mà không cần sử dụng dữ liệu khách hàng thật.

Tại thư mục gốc dự án, chạy PowerShell:
New-Item -ItemType Directory -Force data/raw | Out-Null
Copy-Item data/sample/orders_2024_2026.csv data/raw/ -Force
Copy-Item data/sample/order_items.csv data/raw/ -Force
Copy-Item data/sample/products.csv data/raw/ -Force
Copy-Item data/sample/stores.csv data/raw/ -Force
Không sao chép data/sample/rejected_order_items_demo.csv vào data/raw/: đây là file minh chứng Reject, không phải đầu vào ETL.

Chạy với dữ liệu nguồn riêng: Đặt đúng 4 file CSV có cấu trúc phù hợp vào data/raw/ thay cho bộ dữ liệu mẫu. Không đưa dữ liệu thật lên GitHub Public.
3.4. Chạy toàn bộ ETL và SQLite DWH
Bước 5 – Chạy quy trình chính:
.\.venv\Scripts\python.exe run_etl.py
Quy trình thực hiện:
1. Đọc dữ liệu nguồn CSV.
2. Chuẩn hóa và kiểm tra chất lượng dữ liệu.
3. Đối soát doanh thu giữa nguồn và giá trị tính toán.
4. Xây dựng Fact_Sales và 3 bảng Dimension.
5. Xuất các bảng CSV Warehouse.
6. Tạo SQLite Data Warehouse với khóa và ràng buộc dữ liệu.
Kết quả được lưu tại:
- data/processed/clean_order_items.csv
- data/rejected/rejected_order_items.csv (nếu có dòng bị từ chối).
- data/warehouse/Dim_Date.csv
- data/warehouse/Dim_Product.csv
- data/warehouse/Dim_Store.csv
- data/warehouse/Fact_Sales.csv
- data/warehouse/mekong_mobile.db
Có thể chạy lại lệnh ETL trên cùng dữ liệu và đối chiếu số dòng để kiểm tra việc không phát sinh Fact trùng.
3.5. Chạy Unit Test
Bước 6 – Chạy toàn bộ bài kiểm thử tự động:
.\.venv\Scripts\python.exe -m pytest tests/ -v
Các nhóm kiểm thử bao gồm:
- Trường hợp dữ liệu hợp lệ.
- Giá trị biên, ví dụ quantity = 0.
- Dữ liệu không hợp lệ, ví dụ số lượng âm và thiếu thông tin.
- Các hàm kiểm tra chất lượng dữ liệu.
- Ghi nhận dòng lỗi và lý do Reject.
Số bài kiểm thử PASS cuối cùng được xác nhận bằng kết quả thực tế của lệnh trên; không cố định theo phiên bản README.
3.6. Mở Dashboard Power BI
Dự án cung cấp Power BI Template cho Bài tập 2 tại:

powerbi/Mekong_Mobile_Dashboard_BT2_Final.pbit

Template chứa cấu trúc Dashboard, các biểu đồ, Measure DAX và mô hình dữ liệu; không đóng gói dữ liệu đã Import vào báo cáo.

Bước 7 – Chuẩn bị dữ liệu mẫu

Sao chép đúng 4 file CSV từ data/sample/ vào data/raw/ theo hướng dẫn tại mục 3.3.

Bước 8 – Chạy ETL
.\.venv\Scripts\python.exe run_etl.py
Lệnh tạo 4 bảng CSV Warehouse và SQLite Database.

Bước 9 – Mở Dashboard

Mở file Mekong_Mobile_Dashboard_BT2_Final.pbit bằng Power BI Desktop.

Khi hộp thoại Parameter xuất hiện:
- Parameter: ProjectFolder.
- Giá trị: Đường dẫn tuyệt đối đến thư mục gốc dự án vừa clone.
Ví dụ: Nếu dự án được clone vào C:\Projects\cdtn1_LegiaHuy_L6, nhập đường dẫn này vào ProjectFolder.

Nhấn Load để Power BI đọc các file trong data/warehouse/ và hiển thị Dashboard.

Dashboard gồm 3 trang:
1. Tổng Quan Doanh Thu.
2. Phân Tích Sản Phẩm.
3. Phân Tích Cửa Hàng.
Bộ dữ liệu mẫu có kết quả kỳ vọng khi các bộ lọc ở trạng thái All:
KPI	Giá trị
Tổng doanh thu	23.500.000 VND
Tổng đơn hàng	3
Tổng sản phẩm bán	5
Giá trị đơn hàng trung bình	7.833.333 VND


Các trạng thái đã kiểm tra trong Power BI:
- Normal: Có dữ liệu, KPI và biểu đồ hiển thị bình thường.
- Empty: Nguồn hợp lệ nhưng bộ lọc không có dữ liệu; hiển thị thông báo không có dữ liệu phù hợp.
- Error: Không đọc được nguồn CSV; KPI không giữ số liệu cũ và hiển thị thông báo lỗi thân thiện, không hiện đường dẫn nội bộ trong thông báo cho người dùng.
- Loading: Sử dụng trạng thái tải/Refresh mặc định của Power BI Desktop, chưa triển khai giao diện Loading tùy chỉnh.
Lưu ý: Việc xử lý Error State dựa trên khả năng đọc các file CSV; chưa phải cơ chế kiểm tra đầy đủ mọi lỗi cấu trúc hay tính hợp lệ của dữ liệu.

Lưu ý: Các file .pbix được giữ cục bộ và không chia sẻ trên GitHub Public.
3.7. Kiểm tra kết quả
Với bộ dữ liệu Mekong Mobile đầy đủ đã kiểm thử trên máy phát triển:
Chỉ tiêu	Giá trị
Fact_Sales	35.697 dòng
Dim_Date	792 dòng
Dim_Product	320 dòng
Dim_Store	24 dòng
MATCH	35.177 dòng
MISMATCH	520 dòng
Fact thiếu date_key	154 dòng
Tổng doanh thu	415.773.438.750 VND


Với dữ liệu Demo công khai:
Chỉ tiêu	Giá trị
Fact_Sales	4 dòng
Dim_Date	3 dòng
Dim_Product	3 dòng
Dim_Store	2 dòng
Tổng doanh thu	23.500.000 VND


Các kết quả trên chỉ áp dụng cho đúng bộ dữ liệu đã kiểm thử, không phải kết quả cố định của mọi đầu vào.
4. Cấu trúc thư mục
cdtn1_LegiaHuy_L6/
├── data/
│   ├── raw/                  # Dữ liệu CSV nguồn (không commit dữ liệu thật)
│   ├── sample/               # Dữ liệu CSV giả lập và minh chứng Reject
│   ├── processed/            # Dữ liệu sau làm sạch và đối soát
│   ├── rejected/             # Các dòng bị từ chối và lý do lỗi
│   └── warehouse/            # Fact, Dimension và SQLite DWH
│
├── docs/                     # Tài liệu phân tích và thiết kế
│   ├── evidence/             # Ảnh minh chứng kiểm thử
│   ├── srs.md
│   ├── data-requirements.md
│   ├── data-dictionary.md
│   ├── data-quality-profiling.md
│   ├── dashboard-validation.md
│   ├── peer-review.md
│   ├── ai-disclosure.md
│   ├── thay-doi-thiet-ke.md
│   ├── usecase.drawio
│   ├── architecture.drawio
│   ├── data-flow.drawio
│   └── erd.drawio
│
├── powerbi/
│   └── Mekong_Mobile_Dashboard_BT2_Final.pbit
│
├── src/
│   ├── extract/              # Đọc dữ liệu CSV
│   ├── transform/            # Chuẩn hóa và đối soát doanh thu
│   ├── quality/              # Kiểm tra chất lượng, Reject
│   ├── load/                 # Lưu dữ liệu đầu ra
│   ├── warehouse/            # Xây dựng Star Schema
│   ├── dashboard/            # Phát triển Dashboard
│   └── etl/                  # Các thành phần ETL bổ trợ
│
├── tests/                    # Kiểm thử tự động
├── generate_reject_demo.py   # Tạo dữ liệu lỗi giả lập để minh chứng
├── run_etl.py                # Chạy toàn bộ quy trình ETL
├── requirements.txt          # Thư viện Python
├── .gitignore                # Danh sách file không đưa lên Git
└── README.md                 # Hướng dẫn sử dụng dự án
Giải thích
- src/extract/: Đọc dữ liệu bán hàng.
- src/transform/: Chuẩn hóa tên cột và đối soát doanh thu.
- src/quality/: Kiểm tra chất lượng dữ liệu, thống kê lỗi và ghi nhận bản ghi Reject.
- src/load/: Xuất dữ liệu đã xử lý.
- src/warehouse/: Xây dựng Dim_Date, Dim_Product, Dim_Store và Fact_Sales.
- tests/: Chứa các bài kiểm thử tự động.
- run_etl.py: Điểm chạy chính của toàn bộ pipeline.
- powerbi/Mekong_Mobile_Dashboard_BT2_Final.pbit: Template Dashboard để tái lập trên máy khác.
Các thư mục data/raw/, data/processed/, data/rejected/ và data/warehouse/ được bỏ qua trong các commit mới để hạn chế công khai dữ liệu nguồn và dữ liệu giao dịch.
5. Kiểm thử
5.1. Kiểm thử quy trình ETL
Dự án đã kiểm thử thủ công qua Terminal và xây dựng thêm các bài kiểm thử tự động để xác nhận các module Extract, Transform, Quality và Load.
Mã kiểm thử	Nội dung	Kết quả	Trạng thái
TC01	Đọc dữ liệu order_items.csv	35.697 dòng, 5 cột	PASS
TC02	Chuẩn hóa tên cột dữ liệu bán hàng	Giữ nguyên 35.697 dòng	PASS
TC03	Kiểm tra dữ liệu nguồn đầy đủ	35.697 dòng được xử lý, 0 dòng bị từ chối trong lần chạy đã đối chiếu	PASS
TC04	Kiểm thử ghi Reject bằng dữ liệu giả lập	4 dòng đầu vào, 1 hợp lệ, 3 bị từ chối có lý do	PASS
TC05	Đối soát doanh thu	35.177 MATCH, 520 MISMATCH	PASS
TC06	Xây dựng Dim_Date	792 ngày, không trùng date_key	PASS
TC07	Xây dựng Dim_Product	320 sản phẩm, không trùng khóa	PASS
TC08	Xây dựng Dim_Store	24 cửa hàng, không trùng khóa	PASS
TC09	Xây dựng Fact_Sales	35.697 dòng, 12 cột, không trùng khóa	PASS
TC10	Chạy lại ETL trên cùng dữ liệu	Không tăng số dòng Fact_Sales trong lần kiểm tra	PASS
TC11	Kiểm tra Fact thiếu ngày	154 dòng từ 114 đơn hàng thiếu ngày	PASS
TC12	Đối chiếu doanh thu nguồn và Fact	Chênh lệch 0 VND	PASS


5.2. Kiểm thử các yêu cầu phi chức năng
- NFR01 – Hiệu năng: Chưa có số đo thời gian chạy ETL cuối cùng để xác nhận ngưỡng 120 giây.
- NFR02 – Ghi nhận dữ liệu lỗi: Đã có 5 hàm kiểm tra chất lượng dữ liệu và minh chứng Reject với 3 dòng lỗi giả lập. Chưa khẳng định đã bao phủ 100% mọi tình huống dữ liệu lỗi thực tế.
- NFR03 – Không tạo dữ liệu Fact trùng khi chạy lại: Đã kiểm tra chạy lại ETL trên cùng bộ dữ liệu, không tăng số dòng Fact. Không đồng nghĩa đã triển khai cơ chế upsert.
5.3. Kết quả kiểm tra chất lượng dữ liệu
- Kiểm tra 5 trường: order_id, product_id, quantity, unit_price, reported_sales_amount.
- Ghi nhận số lượng và tỷ lệ lỗi theo từng phép kiểm tra trong quy trình ETL.
- Tạo dữ liệu giả lập 4 dòng để minh chứng cơ chế Reject: 1 dòng hợp lệ, 3 dòng không hợp lệ kèm lý do.
- Phát hiện 520 dòng có chênh lệch giữa doanh thu nguồn và doanh thu tính toán.
- Giữ nguyên 11 dòng chi tiết đơn hàng trùng hoàn toàn để bảo toàn grain theo từng dòng nguồn.
- Ghi nhận 114 đơn hàng thiếu ngày, tương ứng 154 dòng Fact_Sales thiếu date_key.
- Không tự động sửa doanh thu hoặc gán ngày giả.
- Tổng doanh thu nguồn và Fact_Sales đều bằng 415.773.438.750 VND trên dữ liệu đầy đủ đã kiểm thử.
5.4. Bằng chứng kiểm thử
Các ảnh minh chứng được lưu tại docs/evidence/, bao gồm:
- nfr03_etl_rerun.PNG: Chạy lại ETL.
- data_quality_reject_demo.PNG: Kiểm tra dữ liệu lỗi giả lập và Reject.
- warehouse_integrity_check.PNG: Kiểm tra kho dữ liệu.
- e2e_github_clone_pytest.PNG: Chạy pytest trên bản clone GitHub.
- e2e_github_clone_sqlite.PNG: Kiểm tra SQLite trên bản clone.
- dashboard_bt2_final_normal.PNG: Dashboard Normal với dữ liệu Demo.
- dashboard_empty_state.PNG: Dashboard Empty State.
- dashboard_empty_page_filter.PNG: Trường hợp lọc không có dữ liệu.
- dashboard_error_state_actual.PNG: Dashboard Error State khi không đọc được nguồn.
- dashboard_loading_state.PNG: Trạng thái Refresh mặc định của Power BI.
Minh chứng ảnh hỗ trợ việc đối chiếu kết quả, không thay thế cho việc chạy lại các lệnh ETL và pytest.
5.5. Kiểm thử End-to-End (E2E) trên bản clone GitHub
Mục tiêu: Kiểm tra khả năng tái lập hệ thống sau khi clone repository vào thư mục độc lập, không sử dụng dữ liệu thật.

Quy trình kiểm thử:
1. Clone repository từ GitHub vào thư mục độc lập.
2. Sao chép đúng 4 file CSV mẫu từ data/sample/ vào data/raw/.
3. Chạy python run_etl.py.
4. Kiểm tra các bảng trong SQLite Data Warehouse.
5. Chạy python -m pytest tests/ -v.
6. Mở Power BI Template, nhập đường dẫn thư mục clone ở Parameter ProjectFolder và kiểm tra KPI Demo.
Kết quả đã ghi nhận:
Hạng mục	Kết quả	Trạng thái
Clone repository GitHub	Thành công	PASS
Đọc dữ liệu CSV giả lập	4 file	PASS
Chạy ETL	Tạo các bảng Warehouse	PASS
Tạo SQLite Database	mekong_mobile.db	PASS
Dim_Date	3 dòng	PASS
Dim_Product	3 dòng	PASS
Dim_Store	2 dòng	PASS
Fact_Sales	4 dòng	PASS
Kiểm tra khóa ngoại	Không phát hiện lỗi trong lần kiểm tra	PASS
Dashboard Demo	Doanh thu 23.500.000 VND	PASS
Pytest	Có kiểm thử tự động; chạy lại để xác nhận tổng số PASS hiện tại	Cần xác nhận


Minh chứng:
- docs/evidence/e2e_github_clone_pytest.PNG
- docs/evidence/e2e_github_clone_sqlite.PNG
- docs/evidence/dashboard_bt2_final_normal.PNG
Lưu ý: Dashboard Power BI được kiểm thử thủ công từ các file Warehouse CSV, chưa nằm trong bộ kiểm thử E2E tự động Python.
6. Trạng thái hiện tại
6.1. Các công việc đã hoàn thành
- [x] Khởi tạo repository GitHub và cấu trúc dự án.
- [x] Phân tích yêu cầu và xây dựng tài liệu SRS.
- [x] Thiết kế Use Case, Architecture, Data Flow và Star Schema.
- [x] Xây dựng pipeline Extract, Transform, Quality và Load.
- [x] Chuẩn hóa và đối soát dữ liệu doanh thu.
- [x] Xây dựng Dim_Date, Dim_Product, Dim_Store và Fact_Sales.
- [x] Tạo SQLite Data Warehouse với các ràng buộc dữ liệu.
- [x] Kiểm tra khóa chính và khóa ngoại của Data Warehouse.
- [x] Bổ sung 5 phép kiểm tra chất lượng dữ liệu và minh chứng Reject.
- [x] Xây dựng Dashboard Power BI gồm 3 trang phân tích.
- [x] Bổ sung đường doanh thu trung bình vào biểu đồ.
- [x] Xây dựng chỉ số tăng trưởng doanh thu theo tháng.
- [x] Kiểm thử Normal, Empty và Error State; ghi nhận Loading mặc định khi Refresh.
- [x] Có Unit Test tự động và minh chứng kiểm thử E2E từ GitHub clone.
- [x] Bổ sung README hướng dẫn chạy dự án.
- [x] Lưu minh chứng kiểm thử trong docs/evidence/.
6.2. Kết quả dữ liệu thực tế
Chỉ tiêu	Kết quả
Tổng số đơn hàng	26.000
Tổng số dòng Fact_Sales	35.697
Số sản phẩm	320
Số cửa hàng	24
Số ngày trong Dim_Date	792
Dòng doanh thu MATCH	35.177
Dòng doanh thu MISMATCH	520
Dòng Fact thiếu date_key	154
Tổng doanh thu	415.773.438.750 VND


6.3. Công việc cần hoàn thiện
- [ ] Chạy lại toàn bộ pytest và ghi nhận chính xác số bài PASS hiện tại.
- [ ] Kiểm tra đủ các tài liệu Bài tập 2 và tính nhất quán với mã nguồn.
- [ ] Kiểm tra Template .pbit không chứa thông tin cá nhân hoặc cấu hình nhạy cảm trước khi công khai.
- [ ] Tạo và đẩy tag v0.2 sau khi kiểm tra khả năng tái lập.
- [ ] Hoàn thiện báo cáo PDF Bài tập 2 và bài thuyết trình.
6.4. Lưu ý kỹ thuật
- Data Warehouse được lưu dưới dạng SQLite và các file CSV.
- Dashboard Power BI kết nối với CSV Warehouse, chưa đọc trực tiếp từ SQLite.
- Cơ chế Error State kiểm tra khả năng đọc CSV, chưa bao phủ mọi trường hợp dữ liệu sai cấu trúc.
- Loading State sử dụng giao diện Refresh mặc định của Power BI Desktop, chưa có Loading tùy chỉnh.
- Dữ liệu khách hàng thật và file .pbix không được đưa vào các commit mới trên GitHub Public.
- Bộ dữ liệu mẫu trong data/sample/ được sử dụng để kiểm thử và hướng dẫn chạy dự án.