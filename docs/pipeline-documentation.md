# TÀI LIỆU QUY TRÌNH ETL – MEKONG MOBILE

## 1. Tổng quan quy trình ETL

Hệ thống Mekong Mobile sử dụng quy trình ETL để xử lý dữ liệu bán hàng từ các file CSV, làm sạch dữ liệu, đối soát doanh thu và xây dựng kho dữ liệu SQLite theo mô hình Star Schema.

Hệ thống được phát triển bằng Python 3.10.11 và thư viện pandas.

### 1.1. Sơ đồ quy trình

```text
Dữ liệu nguồn CSV
        |
        v
Đọc dữ liệu (Extract)
        |
        v
Chuẩn hóa và biến đổi (Transform)
        |
        v
Kiểm tra chất lượng dữ liệu
        |
        +------> Dữ liệu bị từ chối (Rejected CSV)
        |
        v
Đối soát doanh thu
        |
        v
Dữ liệu chi tiết đã xử lý (Processed CSV)
        |
        v
Xây dựng bảng Fact và Dimension
        |
        v
Xuất các bảng Warehouse dạng CSV
        |
        v
Nạp SQLite Data Warehouse
        |
        v
Power BI Dashboard
```

File thực thi chính của quy trình là `run_etl.py`.

### 1.2. Mục tiêu

- Chuẩn hóa dữ liệu bán hàng từ các nguồn CSV.
- Kiểm tra dữ liệu đầu vào theo quy tắc nghiệp vụ.
- Phân loại dữ liệu hợp lệ và dữ liệu bị từ chối.
- Bảo toàn doanh thu gốc và ghi nhận các trường hợp chênh lệch.
- Xây dựng các bảng Fact và Dimension phục vụ phân tích.
- Tạo kho dữ liệu SQLite có thể kiểm tra và tái lập.

## 2. Nguồn dữ liệu đầu vào

Quy trình ETL sử dụng bốn file CSV chính.

| File nguồn | Nội dung |
|---|---|
| `orders_2024_2026.csv` | Thông tin đơn hàng, ngày bán và cửa hàng |
| `order_items.csv` | Chi tiết sản phẩm trong đơn hàng |
| `products.csv` | Danh mục sản phẩm |
| `stores.csv` | Danh mục cửa hàng |

Thư mục dữ liệu nguồn mặc định: `data/raw/`.

Đối với môi trường Docker, bốn file mẫu trong `data/sample/` được sao chép vào `data/raw/` bên trong container khi xây dựng Docker Image.

File `customers_raw.csv` không được sử dụng trong quy trình ETL hiện tại vì nằm ngoài phạm vi Star Schema đã triển khai.

### 2.1. Quy tắc liên kết dữ liệu nguồn

| Quy tắc | Nội dung |
|---|---|
| BR02 | `orders.ma_cua_hang` tham chiếu `stores.store_code` |
| BR03 | `order_items.product_id` tham chiếu `products.product_id` |
| BR04 | Ngày được chuẩn hóa theo định dạng nguồn; không tự tạo ngày khi bị thiếu |
| BR05 | Giữ nguyên doanh thu nguồn và tính thêm giá trị đối chiếu |
| BR06 | Không sử dụng `ma_don` làm khóa duy nhất |
| BR07 | Mỗi dòng dữ liệu cần có định danh ổn định |
| BR08 | Tổng số đơn hàng được tính theo `DISTINCT order_id` |
| BR09 | Dòng chênh lệch doanh thu phải được đánh dấu phục vụ đối soát |

Các quy tắc được định nghĩa trong `docs/srs.md`.

## 3. Các bảng đích và mức độ chi tiết dữ liệu

Kho dữ liệu sử dụng mô hình Star Schema gồm một bảng Fact và ba bảng Dimension.

| Bảng | Mức độ chi tiết (Grain) |
|---|---|
| `Fact_Sales` | Một dòng chi tiết sản phẩm trong đơn hàng nguồn |
| `Dim_Date` | Một ngày hợp lệ |
| `Dim_Product` | Một sản phẩm duy nhất |
| `Dim_Store` | Một cửa hàng duy nhất |

Bảng `Fact_Sales` lưu số lượng, đơn giá, doanh thu nguồn, doanh thu tính toán, giá trị chênh lệch và khóa liên kết đến các bảng Dimension.

### 3.1. Vị trí dữ liệu đầu ra

Kho dữ liệu SQLite:

`data/warehouse/mekong_mobile.db`

Các bảng Warehouse dạng CSV được xuất trong:

`data/warehouse/`

Dữ liệu chi tiết đã xử lý:

`data/processed/clean_order_items.csv`

Dữ liệu bị từ chối:

`data/rejected/rejected_order_items.csv`

Cấu trúc cột, kiểu dữ liệu và ràng buộc được mô tả trong `docs/data-dictionary.md`.

## 4. Quy tắc biến đổi và chất lượng dữ liệu

### 4.1. Các bước xử lý

1. Đọc dữ liệu từ bốn file CSV nguồn.
2. Chuẩn hóa tên cột và kiểu dữ liệu.
3. Kiểm tra mã định danh và dữ liệu số.
4. Phân loại dòng hợp lệ và dòng bị từ chối.
5. Tính doanh thu đối chiếu và giá trị chênh lệch.
6. Chuẩn hóa ngày và xây dựng các bảng Dimension.
7. Xây dựng bảng Fact và liên kết khóa.
8. Xuất dữ liệu Warehouse ra CSV.
9. Tạo cơ sở dữ liệu SQLite và kiểm tra khóa ngoại.

### 4.2. Bảng quy tắc xử lý dữ liệu

| Dữ liệu | Quy tắc | Cách xử lý |
|---|---|---|
| `order_id` | Kiểm tra định danh đơn hàng | Đánh giá theo quy tắc kiểm tra dữ liệu đầu vào |
| `product_id` | Kiểm tra định danh sản phẩm | Đánh giá theo quy tắc kiểm tra dữ liệu đầu vào |
| `quantity` | Kiểm tra số lượng | Dữ liệu không hợp lệ được xử lý theo bộ lọc chất lượng |
| `unit_price` | Kiểm tra đơn giá | Dữ liệu không hợp lệ được xử lý theo bộ lọc chất lượng |
| `reported_sales_amount` | Kiểm tra doanh thu nguồn | Giữ nguyên giá trị hợp lệ để đối soát |
| `ngay` | Chuẩn hóa ngày bán | Không tự tạo ngày khi nguồn thiếu |
| `ma_don` | Không yêu cầu duy nhất | Giữ nguyên các giá trị lặp theo BR06 |
| `source_line_id` | Định danh dòng nguồn | Phục vụ bảo toàn dòng và chạy lại ETL |
| Doanh thu chênh lệch | So sánh doanh thu nguồn và doanh thu tính toán | Đánh dấu `MISMATCH`, không tự ghi đè |
| Dòng trùng hoàn toàn | Chưa có quy tắc xác nhận là dữ liệu sai | Không tự động loại bỏ |

Các dòng bị từ chối trong quá trình kiểm tra dữ liệu đầu vào được lưu tại `data/rejected/rejected_order_items.csv`, kèm lý do từ chối.

**Lưu ý:** Bảng trên mô tả các quy tắc theo thiết kế và luồng xử lý hiện tại. Số dòng bị từ chối phải lấy từ kết quả chạy ETL thực tế, không suy ra từ số dòng chênh lệch doanh thu.

### 4.3. Thống kê xử lý dữ liệu nguồn

Kết quả profiling trên bộ dữ liệu đầy đủ:

| Chỉ tiêu | Số lượng |
|---|---:|
| Đơn hàng nguồn | 26.000 |
| Dòng chi tiết bán hàng | 35.697 |
| Sản phẩm | 320 |
| Cửa hàng | 24 |
| Đơn hàng thiếu ngày | 114 |
| Dòng chi tiết có doanh thu khớp | 35.177 |
| Dòng chi tiết có doanh thu chênh lệch | 520 |

Theo kết quả kiểm thử ETL đã ghi nhận trong Data Dictionary, bảng `Fact_Sales` chứa 35.697 dòng trên bộ dữ liệu đầy đủ.

Số dòng hợp lệ và số dòng bị từ chối ở bước lọc đầu vào cần đối chiếu trực tiếp với log ETL và file `rejected_order_items.csv` của cùng lần chạy trước khi đưa vào bảng thống kê chính thức.

### 4.4. Công thức đối soát doanh thu

Các công thức được sử dụng:

`calculated_sales_amount = quantity × unit_price`

`difference_amount = reported_sales_amount - calculated_sales_amount`

Quy tắc phân loại:

- `MATCH`: Doanh thu nguồn bằng doanh thu tính toán.
- `MISMATCH`: Doanh thu nguồn khác doanh thu tính toán.

Hệ thống giữ nguyên `reported_sales_amount` nhằm bảo toàn dữ liệu phục vụ kiểm toán và đối soát.

### 4.5. Kết quả kiểm thử BR05 và BR09

Hai quy tắc BR05 và BR09 đã được kiểm tra trên toàn bộ 35.697 dòng chi tiết bán hàng thực tế.

| Nội dung kiểm tra | Kết quả |
|---|---|
| Tổng dòng dữ liệu | 35.697 |
| Dòng `MATCH` | 35.177 |
| Dòng `MISMATCH` | 520 |
| Giữ nguyên doanh thu nguồn | PASS |
| Tính doanh thu đối chiếu | PASS |
| Tính giá trị chênh lệch | PASS |
| Phân loại trạng thái đối soát | PASS |

**Kết luận: Kiểm thử chức năng BR05/BR09 đạt PASS.**

520 dòng có chênh lệch được giữ lại phục vụ đối soát, không bị tự động chỉnh sửa hoặc loại bỏ.

Kết quả PASS thể hiện **chức năng đối soát hoạt động đúng**, không có nghĩa là 100% doanh thu nguồn đã khớp với doanh thu tính toán.

### 4.6. Đánh giá ba chiều chất lượng dữ liệu

Chương trình kiểm tra chất lượng:

`python scripts/check_data_quality_bt3.py`

Phạm vi: 27 cột thuộc bốn file CSV nguồn.

| Chiều chất lượng | PASS | FAIL | N/A |
|---|---:|---:|---:|
| Completeness – Tính đầy đủ | 26 | 1 | 0 |
| Validity – Tính hợp lệ | 27 | 0 | 0 |
| Consistency – Tính nhất quán | 8 | 1 | 18 |

Trong đó:

- Completeness đo tỷ lệ dữ liệu không bị thiếu.
- Validity đo tỷ lệ các giá trị không rỗng đáp ứng quy tắc kiểm tra đã triển khai.
- Consistency kiểm tra tính duy nhất, khóa liên kết và đối soát doanh thu ở những cột có quy tắc phù hợp.
- `N/A` nghĩa là không có quy tắc đối chiếu được định nghĩa, không được xem là PASS.

Các ngưỡng kiểm tra là ngưỡng đề xuất phục vụ đồ án sinh viên, không phải tiêu chuẩn chính thức của Mekong Mobile.

Ngưỡng theo từng cột và kết quả chi tiết được lưu trong:

- `docs/evidence/data_quality_bt3.json`
- `docs/evidence/data_quality_bt3.csv`

### 4.7. Các vấn đề chất lượng dữ liệu được phát hiện

**DQ-01: Thiếu thông tin nhân viên**

| Thuộc tính | Kết quả |
|---|---|
| File nguồn | `orders_2024_2026.csv` |
| Cột | `nhan_vien` |
| Completeness | 96,11% |
| Ngưỡng yêu cầu | 99% |
| Kết quả | FAIL |

Ảnh hưởng nghiệp vụ: Các báo cáo phân tích doanh thu theo nhân viên có thể không đầy đủ nếu dữ liệu thiếu không được xử lý hoặc phân loại rõ ràng.

**DQ-02: Chênh lệch doanh thu**

| Thuộc tính | Kết quả |
|---|---|
| File nguồn | `order_items.csv` |
| Cột | `thanh_tien` |
| Consistency | 98,54% |
| Ngưỡng yêu cầu | 99% |
| Dòng khớp | 35.177 |
| Dòng chênh lệch | 520 |
| Kết quả | FAIL |

Ảnh hưởng nghiệp vụ: Có thể dẫn đến cách diễn giải doanh thu khác nhau nếu chưa xác định được nguyên nhân chênh lệch.

Biện pháp hiện tại: Giữ nguyên dữ liệu nguồn, lưu giá trị tính toán và trạng thái đối soát để phục vụ kiểm tra tiếp theo.

Không tự kết luận các chênh lệch này là thuế, khuyến mãi hoặc lỗi nhập liệu khi chưa có bằng chứng.

### 4.8. Giới hạn của phép đo chất lượng

Đối với các cột văn bản chưa có quy tắc định dạng chuyên biệt, Validity mới được đánh giá ở mức không rỗng.

Do đó, kết quả 27/27 cột đạt ngưỡng Validity không có nghĩa rằng toàn bộ dữ liệu đã được kiểm tra đầy đủ về mặt nghiệp vụ.

Những cột chưa có quy tắc Consistency phù hợp được ghi `N/A` thay vì mặc định đạt 100%.

## 5. Lịch chạy và xử lý lại dữ liệu

### 5.1. Cơ chế chạy hiện tại

Quy trình ETL hoạt động theo mô hình xử lý theo lô (Batch ETL).

Hệ thống hiện được chạy thủ công bằng Python hoặc Docker Compose.

Lệnh chạy bằng Docker:

```bash
docker compose run --build --rm pipeline
```

Chưa triển khai cơ chế lập lịch tự động trên môi trường production.

### 5.2. Chạy lại và xử lý dữ liệu lịch sử

Khi dữ liệu nguồn được sửa hoặc cần xử lý lại dữ liệu lịch sử, hệ thống thực hiện chạy lại ETL trên bộ dữ liệu nguồn đầy đủ.

Quy trình hiện tại sử dụng Full Refresh, chưa hỗ trợ Incremental Loading.

Các bảng Warehouse CSV được tạo lại và cơ sở dữ liệu SQLite được xây dựng lại từ dữ liệu đã xử lý.

Cơ chế này giúp tránh việc nối thêm các bản ghi trùng khi chạy nhiều lần trên cùng bộ dữ liệu không thay đổi.

### 5.3. Kiểm tra khả năng tái lập

Docker đã được kiểm thử trên GitHub Actions với môi trường Ubuntu Linux.

Các bước kiểm tra đã thực hiện:

- Xây dựng Docker Image và chạy ETL.
- Xác nhận SQLite Data Warehouse được tạo.
- Kiểm tra bốn bảng đích.
- Chạy lại ETL trên bộ dữ liệu mẫu.
- Xác nhận không phát sinh bản ghi bán hàng trùng khi chạy lại.

Kết quả: **PASS**.

### 5.4. Dữ liệu mẫu Docker

Bộ dữ liệu Docker được đóng gói từ thư mục `data/sample/`.

Nếu muốn chạy trên bộ dữ liệu khác, cần chuẩn bị dữ liệu nguồn và cấu hình triển khai phù hợp.

Phiên bản hiện tại chưa cung cấp cơ chế tự động đồng bộ dữ liệu mới từ hệ thống bán hàng.

## 6. Giới hạn và rủi ro hiện tại

| Giới hạn | Ảnh hưởng |
|---|---|
| Dữ liệu nguồn là file CSV cục bộ | Chưa tự động nhận dữ liệu từ hệ thống bán hàng |
| SQLite là cơ sở dữ liệu dạng file | Chưa phù hợp cho hệ thống nhiều người dùng đồng thời ở quy mô lớn |
| Chưa có Incremental Loading | Phải xử lý lại toàn bộ dữ liệu khi chạy ETL |
| Chưa có lịch chạy tự động | Dữ liệu Dashboard không tự cập nhật theo thời gian thực |
| Chưa hỗ trợ Slowly Changing Dimensions | Chưa lưu lịch sử thay đổi thuộc tính sản phẩm và cửa hàng |
| Chưa triển khai mã hóa file SQLite | Cần kiểm soát quyền truy cập file và môi trường lưu trữ |
| Power BI chạy ngoài Docker | Dashboard không được tự động khởi động cùng container ETL |
| Có 520 dòng chênh lệch doanh thu | Cần đối soát nghiệp vụ trước khi kết luận nguyên nhân |
| Thiếu thông tin nhân viên ở một số đơn hàng | Có thể ảnh hưởng báo cáo phân tích theo nhân viên |
| Chưa kiểm chứng Docker Desktop trực tiếp trên Windows | Minh chứng Docker hiện tại dựa trên GitHub Actions Ubuntu Linux |

### 6.1. Giới hạn về độ trễ dữ liệu

Hệ thống chưa có cơ chế cập nhật tự động hoặc đồng bộ thời gian thực.

Thời điểm dữ liệu xuất hiện trong Warehouse phụ thuộc vào lần thực thi ETL gần nhất.

Do chưa triển khai bộ lập lịch production, hệ thống chưa có cam kết thời gian cập nhật dữ liệu cố định.

## 7. Kiểm chứng kết quả triển khai

### 7.1. Kiểm tra chạy ETL

Khi chạy thành công, chương trình hiển thị:

```text
=== HOAN THANH ETL ===
```

### 7.2. Kiểm tra các bảng SQLite

Các bảng cần tồn tại:

- `dim_date`
- `dim_product`
- `dim_store`
- `fact_sales`

Số dòng mong đợi với dữ liệu mẫu Docker:

| Bảng | Số dòng |
|---|---:|
| `dim_date` | 3 |
| `dim_product` | 3 |
| `dim_store` | 2 |
| `fact_sales` | 4 |

Các số liệu trên áp dụng cho bộ dữ liệu mẫu Docker, không phải toàn bộ dữ liệu bán hàng.

### 7.3. Kiểm thử hồi quy

Bộ kiểm thử hồi quy đã ghi nhận 14 test PASS trong quá trình chuẩn bị BT3.

Bài kiểm thử riêng cho BR05/BR09 cũng được bổ sung để kiểm tra việc bảo toàn doanh thu nguồn, tính chênh lệch và phân loại trạng thái.

### 7.4. Minh chứng

| Minh chứng | Đường dẫn |
|---|---|
| Kết quả Docker PASS | `docs/evidence/docker_pass_BT3.PNG` |
| Cấu hình GitHub Actions | `.github/workflows/docker-test.yml` |
| Báo cáo chất lượng JSON | `docs/evidence/data_quality_bt3.json` |
| Báo cáo chất lượng CSV | `docs/evidence/data_quality_bt3.csv` |
| Chương trình đánh giá chất lượng | `scripts/check_data_quality_bt3.py` |
| Chương trình đối soát doanh thu | `src/transform/transform_sales.py` |
| Data Dictionary | `docs/data-dictionary.md` |
| Quy tắc nghiệp vụ | `docs/srs.md` |

**Kết luận:** Quy trình ETL đã được kiểm thử chức năng đối soát và kiểm chứng chạy Docker trên GitHub Actions. Các vấn đề chất lượng dữ liệu nguồn và giới hạn triển khai vẫn được ghi nhận để tiếp tục theo dõi.
## 11. Data Dictionary chi tiết theo yêu cầu BT3

### 11.1. Quy ước đánh giá

Mỗi cột trong kho dữ liệu được mô tả theo sáu thông tin:

1. **Kiểu dữ liệu:** Kiểu dữ liệu được sử dụng trong SQLite.
2. **Ý nghĩa:** Mục đích và nội dung của cột.
3. **Giá trị hợp lệ:** Miền giá trị hoặc quy tắc kiểm tra.
4. **Cho phép NULL:** Cột có được phép chứa giá trị NULL hay không.
5. **Phân loại dữ liệu:** Mức độ nhạy cảm của thông tin.
6. **Xử lý bảo mật:** Cách quản lý hoặc bảo vệ dữ liệu.

Các thông tin được xây dựng dựa trên cấu trúc SQLite của dự án tại `src/warehouse/schema.sql`.

### 11.2. Bảng Fact_Sales

| Cột | Kiểu SQLite | Ý nghĩa | Giá trị hợp lệ | NULL | Phân loại | Xử lý bảo mật |
|---|---|---|---|---|---|---|
| `sales_key` | INTEGER | Khóa chính của dòng bán hàng | Số nguyên duy nhất | Không | Nội bộ | Kiểm tra khóa chính |
| `source_line_id` | TEXT | Định danh dòng dữ liệu nguồn | Chuỗi không rỗng, duy nhất | Không | Nội bộ | Kiểm soát truy cập dữ liệu nguồn |
| `order_id` | TEXT | Mã định danh đơn hàng | Chuỗi không rỗng | Không | Nội bộ | Không công khai dữ liệu giao dịch |
| `date_key` | INTEGER | Khóa liên kết ngày bán | Ngày hợp lệ dạng YYYYMMDD hoặc NULL | Có | Nội bộ | Kiểm tra khóa ngoại |
| `product_key` | INTEGER | Khóa liên kết sản phẩm | Khóa tồn tại trong Dim_Product | Không | Nội bộ | Kiểm tra khóa ngoại |
| `store_key` | INTEGER | Khóa liên kết cửa hàng | Khóa tồn tại trong Dim_Store | Không | Nội bộ | Kiểm tra khóa ngoại |
| `quantity` | INTEGER | Số lượng sản phẩm bán | Số nguyên lớn hơn 0 | Không | Nội bộ | Kiểm tra ràng buộc CHECK |
| `unit_price` | INTEGER | Đơn giá sản phẩm | Số nguyên không âm | Không | Nhạy cảm kinh doanh | Hạn chế chia sẻ dữ liệu giá |
| `reported_sales_amount` | INTEGER | Doanh thu được ghi nhận từ nguồn | Số nguyên không âm | Không | Nhạy cảm kinh doanh | Bảo toàn giá trị nguồn, giới hạn truy cập |
| `calculated_sales_amount` | INTEGER | Doanh thu được tính theo số lượng và đơn giá | Bằng `quantity × unit_price` | Không | Nhạy cảm kinh doanh | Kiểm tra công thức tính toán |
| `difference_amount` | INTEGER | Chênh lệch giữa doanh thu nguồn và doanh thu tính toán | Số nguyên, có thể âm, bằng 0 hoặc dương | Không | Nhạy cảm kinh doanh | Lưu để đối soát, không tự chỉnh sửa |
| `reconciliation_status` | TEXT | Trạng thái đối soát doanh thu | `MATCH` hoặc `MISMATCH` | Không | Nội bộ | Kiểm tra trạng thái và lưu kết quả đối soát |

**Tổng số cột: 12.**

### 11.3. Bảng Dim_Date

| Cột | Kiểu SQLite | Ý nghĩa | Giá trị hợp lệ | NULL | Phân loại | Xử lý bảo mật |
|---|---|---|---|---|---|---|
| `date_key` | INTEGER | Khóa chính của ngày | Số nguyên dạng YYYYMMDD, duy nhất | Không | Nội bộ | Kiểm tra khóa chính |
| `full_date` | TEXT | Ngày đầy đủ | Ngày hợp lệ theo định dạng lưu trữ của ETL | Không | Nội bộ | Kiểm tra định dạng ngày |
| `day` | INTEGER | Ngày trong tháng | 1–31, phù hợp ngày thực tế | Không | Nội bộ | Kiểm tra giá trị ngày |
| `month` | INTEGER | Tháng trong năm | 1–12 | Không | Nội bộ | Kiểm tra miền giá trị |
| `quarter` | INTEGER | Quý trong năm | 1–4 | Không | Nội bộ | Kiểm tra tính nhất quán với tháng |
| `year` | INTEGER | Năm của ngày bán | Năm hợp lệ từ ngày nguồn đã chuẩn hóa | Không | Nội bộ | Kiểm tra tính nhất quán với ngày |

**Tổng số cột: 6.**

### 11.4. Bảng Dim_Product

| Cột | Kiểu SQLite | Ý nghĩa | Giá trị hợp lệ | NULL | Phân loại | Xử lý bảo mật |
|---|---|---|---|---|---|---|
| `product_key` | INTEGER | Khóa thay thế của sản phẩm | Số nguyên duy nhất | Không | Nội bộ | Kiểm tra khóa chính |
| `product_id` | TEXT | Mã sản phẩm từ dữ liệu nguồn | Chuỗi không rỗng, duy nhất | Không | Nội bộ | Kiểm tra ràng buộc UNIQUE |
| `product_name` | TEXT | Tên sản phẩm | Chuỗi văn bản hoặc NULL | Có | Nội bộ | Chỉ sử dụng cho mục đích phân tích |
| `brand` | TEXT | Thương hiệu sản phẩm | Chuỗi văn bản hoặc NULL | Có | Nội bộ | Kiểm soát truy cập dữ liệu |
| `category` | TEXT | Nhóm sản phẩm | Chuỗi văn bản hoặc NULL | Có | Nội bộ | Kiểm soát truy cập dữ liệu |

**Tổng số cột: 5.**

### 11.5. Bảng Dim_Store

| Cột | Kiểu SQLite | Ý nghĩa | Giá trị hợp lệ | NULL | Phân loại | Xử lý bảo mật |
|---|---|---|---|---|---|---|
| `store_key` | INTEGER | Khóa thay thế của cửa hàng | Số nguyên duy nhất | Không | Nội bộ | Kiểm tra khóa chính |
| `store_code` | TEXT | Mã cửa hàng từ nguồn | Chuỗi không rỗng, duy nhất | Không | Nội bộ | Kiểm tra ràng buộc UNIQUE |
| `store_name` | TEXT | Tên cửa hàng | Chuỗi văn bản hoặc NULL | Có | Nội bộ | Giới hạn truy cập dữ liệu |
| `city` | TEXT | Thành phố của cửa hàng | Chuỗi văn bản hoặc NULL | Có | Nội bộ | Chỉ sử dụng cho phân tích khu vực |
| `district` | TEXT | Quận/huyện của cửa hàng | Chuỗi văn bản hoặc NULL | Có | Nội bộ | Chỉ sử dụng cho phân tích khu vực |

**Tổng số cột: 5.**

### 11.6. Kiểm tra dữ liệu nhạy cảm và thông tin cá nhân

Dữ liệu nguồn `orders_2024_2026.csv` có chứa các thông tin như `ten_khach` và `so_dien_thoai`.

Các cột này không nằm trong danh sách 28 cột của bốn bảng đích Star Schema hiện tại.

Việc không đưa trực tiếp tên và số điện thoại khách hàng vào bảng Fact và Dimension giúp giảm nguy cơ lộ thông tin cá nhân trong dữ liệu phân tích.

Tuy nhiên, các file CSV nguồn vẫn cần được kiểm soát quyền truy cập và không nên công khai khi chứa dữ liệu cá nhân thực tế.

### 11.7. Tổng hợp Data Dictionary

| Bảng đích | Số cột |
|---|---:|
| Fact_Sales | 12 |
| Dim_Date | 6 |
| Dim_Product | 5 |
| Dim_Store | 5 |
| **Tổng cộng** | **28** |

Toàn bộ 28 cột đã được mô tả theo sáu nhóm thông tin của tiêu chí D2.

Các quy tắc về khóa chính, khóa ngoại, NULL và kiểu dữ liệu cần được đối chiếu với `src/warehouse/schema.sql` khi có thay đổi cấu trúc hệ thống.

**Giới hạn bảo mật:** Phiên bản hiện tại chưa triển khai mã hóa file SQLite ở trạng thái lưu trữ. Các biện pháp kiểm soát truy cập được nêu trong tài liệu là chính sách cần áp dụng tại môi trường sử dụng, không đồng nghĩa với việc hệ thống đã có cơ chế phân quyền người dùng hoàn chỉnh.