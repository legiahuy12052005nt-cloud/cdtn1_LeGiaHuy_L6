# TEST REPORT – KIỂM THỬ HỆ THỐNG MEKONG MOBILE

**Sinh viên:** Lê Gia Huy  
**MSSV:** 2374802010175  
**Track:** DA – Luồng L6  
**Đề tài:** Xây dựng kho dữ liệu bán hàng và Dashboard phân tích doanh thu cho Mekong Mobile  
**Bài tập:** BT3 – Kiểm thử và đóng gói prototype  
**Ngày kiểm thử bộ 12 test case:** 07/11/2026  
**Phiên bản kiểm thử ban đầu:** `v0.2`  
**Phiên bản đóng gói BT3:** `v1.0`  
**Repository:** https://github.com/legiahuy12052005nt-cloud/cdtn1_LeGiaHuy_L6

---

## 1. Thông tin kiểm thử

### 1.1. Mục tiêu

Kiểm tra các chức năng chính của hệ thống Mekong Mobile, bao gồm quy trình ETL, kiểm tra chất lượng dữ liệu, đối soát doanh thu, lưu trữ SQLite, Dashboard Power BI và khả năng chạy lại hệ thống.

BT3 bổ sung kiểm chứng triển khai Docker và kiểm thử tự động trên GitHub Actions.

### 1.2. Phạm vi

- Đọc và xử lý bốn file CSV nguồn.
- Chuẩn hóa và kiểm tra dữ liệu.
- Kiểm thử giá trị hợp lệ, giá trị biên và dữ liệu không hợp lệ.
- Xử lý Reject và ghi nhận lý do từ chối.
- Đối soát doanh thu theo BR05 và BR09.
- Xây dựng SQLite Data Warehouse.
- Kiểm tra KPI Power BI với dữ liệu Demo.
- Kiểm tra khả năng chạy lại ETL.
- Kiểm thử tự động bằng pytest.
- Kiểm chứng Docker trên GitHub Actions.

### 1.3. Môi trường kiểm thử

| Thành phần | Môi trường |
|---|---|
| Python | 3.10.11 |
| pandas | 2.3.3 |
| pytest | 9.2.0 |
| Cơ sở dữ liệu | SQLite |
| Dashboard | Power BI Desktop |
| Môi trường phát triển | Windows, VS Code, PowerShell |
| Môi trường Docker | GitHub Actions – Ubuntu Linux |
| Dữ liệu Demo | `data/sample/` |
| Minh chứng test case | `docs/screenshots/` |

### 1.4. Phân biệt các mốc kiểm thử

**Mốc 1 – Kiểm thử chức năng ngày 07/11/2026**

- Thực hiện 12 test case.
- Sử dụng bản clone từ tag `v0.2`.
- Ghi nhận 12/12 test case PASS.
- Bộ pytest tại thời điểm đó có 14 bài PASS.

**Mốc 2 – Kiểm thử đóng gói BT3**

- Bổ sung kiểm thử đối soát doanh thu.
- Tích hợp pytest vào Docker.
- Kiểm tra SQLite và chạy lại ETL bằng GitHub Actions.
- Kiểm chứng clone sạch từ tag `v1.0` và chạy Docker.
- Các workflow liên quan đã được ghi nhận chạy thành công.
- Tổng số pytest PASS của phiên bản mới cần lấy từ log GitHub Actions tương ứng.

Hai mốc kiểm thử được trình bày riêng để tránh nhầm lẫn kết quả cũ với kết quả mới.

---

## 2. Bảng kết quả kiểm thử

Bảng gồm tám trường thông tin: mã test case; nhóm và ưu tiên; dữ liệu thử; tiền điều kiện; bước thực hiện; kết quả mong đợi; kết quả thực tế và trạng thái; minh chứng.

| Mã TC | Nhóm / Ưu tiên | Dữ liệu thử | Tiền điều kiện | Bước thực hiện | Kết quả mong đợi | Kết quả thực tế / Trạng thái | Minh chứng |
|---|---|---|---|---|---|---|---|
| TC-01 | Luồng đúng / Cao | 4 file CSV Demo | Dữ liệu mẫu đã được chuẩn bị tại `data/raw/` | Chạy `python run_etl.py` | ETL hoàn thành và tạo dữ liệu Warehouse | ETL chạy thành công, tạo Warehouse CSV và SQLite. **PASS** | [TC-01](screenshots/TC-01.PNG) |
| TC-02 | Luồng đúng / Cao | SQLite Warehouse Demo | Đã chạy ETL với dữ liệu Demo | Truy vấn `COUNT(*)` của bốn bảng SQLite | `fact_sales=4`, `dim_date=3`, `dim_product=3`, `dim_store=2` | Kết quả đúng 4/3/3/2. **PASS** | [TC-02](screenshots/TC-02.PNG) |
| TC-03 | Luồng đúng / Cao | Power BI Warehouse Demo | Có dữ liệu Warehouse Demo | Mở Power BI Template, cấu hình `ProjectFolder`, kiểm tra KPI | Doanh thu 23.500.000 VND, 3 đơn hàng, số lượng bán 5 | Dashboard tải dữ liệu, AOV khoảng 7.833.333 VND. **PASS** | [TC-03](screenshots/TC-03.PNG) |
| TC-04 | Giá trị biên / Cao | `quantity=0` | Có DataFrame mẫu | Gọi `check_quantity` | Phát hiện số lượng bằng 0; `error_count=1`, `error_rate=100%` | Số lượng 0 được phát hiện không hợp lệ. **PASS** | [TC-04](screenshots/TC-04.PNG) |
| TC-05 | Giá trị biên / Cao | `quantity=1` | Có DataFrame mẫu | Gọi `check_quantity` | Giá trị hợp lệ; `error_count=0`, `error_rate=0%` | Không phát hiện lỗi. **PASS** | [TC-05](screenshots/TC-05.PNG) |
| TC-06 | Dữ liệu sai / Cao | `quantity=-1` | Có DataFrame mẫu | Gọi `check_quantity` | Phát hiện số lượng âm; `error_count=1`, `error_rate=100%` | Số lượng âm được phát hiện. **PASS** | [TC-06](screenshots/TC-06.PNG) |
| TC-07 | Dữ liệu sai / Cao | `unit_price=-1` | Có DataFrame mẫu | Gọi `check_unit_price` | Phát hiện đơn giá âm; `error_count=1`, `error_rate=100%` | Đơn giá âm được phát hiện. **PASS** | [TC-07](screenshots/TC-07.PNG) |
| TC-08 | Dữ liệu sai / Cao | `order_id=None` | Có DataFrame mẫu | Gọi `check_order_id` | Phát hiện mã đơn thiếu; `error_count=1`, `error_rate=100%` | Mã đơn thiếu được phát hiện. **PASS** | [TC-08](screenshots/TC-08.PNG) |
| TC-09 | Chất lượng dữ liệu / Cao | `quantity=2`, `unit_price=10.000.000`, doanh thu nguồn 22.000.000 | Có bài kiểm thử đối soát | Chạy `pytest tests/test_transform_sales.py::test_reconciliation_mismatch -v` | Doanh thu tính 20.000.000; chênh lệch 2.000.000; trạng thái `MISMATCH` | Bài kiểm thử đối soát ghi nhận `1 passed`. **PASS** | [TC-09](screenshots/TC-09.PNG) |
| TC-10 | Chất lượng dữ liệu / Cao | 4 dòng Demo, trong đó 3 dòng lỗi | Có chương trình tạo dữ liệu Reject | Chạy `generate_reject_demo.py`, kiểm tra CSV bị từ chối | 3 dòng bị Reject kèm lý do | File Reject ghi nhận 3 dòng lỗi và nguyên nhân. **PASS** | [TC-10](screenshots/TC-10.PNG) |
| TC-11 | Tái lập / Cao | 4 file CSV Demo không thay đổi | Đã chuẩn bị dữ liệu mẫu | Chạy ETL hai lần, truy vấn SQLite và kiểm tra trùng `sales_key` | Sau mỗi lần `fact_sales=4`, không có khóa trùng | Cả hai lần đều có 4 dòng Fact, số khóa trùng bằng 0. **PASS** | [TC-11](screenshots/TC-11.PNG) |
| TC-12 | Tái lập / Cao | Repository tag `v0.2` | Có môi trường Python và bản clone | Chạy `python -m pytest tests/ -v` | Toàn bộ pytest PASS | Ghi nhận 14 bài pytest PASS tại ngày 07/11/2026. **PASS** | [TC-12](screenshots/TC-12.PNG) |

**Lưu ý:** Trạng thái PASS trong bảng là kết quả của các test case đã thực hiện và lưu minh chứng ở mốc kiểm thử ban đầu. Kết quả kiểm thử Docker mới được trình bày riêng trong Mục 4.

---

## 3. Tổng hợp kết quả test case

### 3.1. Kết quả chung

| Chỉ tiêu | Kết quả |
|---|---:|
| Tổng số test case | 12 |
| Test case đã thực hiện | 12 |
| PASS | 12 |
| FAIL | 0 |
| Chưa chạy | 0 |
| Tỷ lệ PASS | 100% |
| Nhóm kiểm thử được bao phủ | 5/5 |

### 3.2. Phân loại kiểm thử

| Nhóm kiểm thử | Mã test case | Số lượng |
|---|---|---:|
| Luồng đúng | TC-01, TC-02, TC-03 | 3 |
| Giá trị biên | TC-04, TC-05 | 2 |
| Dữ liệu sai | TC-06, TC-07, TC-08 | 3 |
| Chất lượng dữ liệu | TC-09, TC-10 | 2 |
| Tái lập | TC-11, TC-12 | 2 |
| **Tổng cộng** | **TC-01 đến TC-12** | **12** |

Các test case về chất lượng dữ liệu tập trung vào kiểm tra sai lệch doanh thu và khả năng từ chối dữ liệu lỗi.

Các kiểm tra bảo mật được ghi nhận riêng trong `docs/security-checklist.md`, không xem hai test case Data Quality là bằng chứng kiểm thử bảo mật toàn diện.

---

## 4. Kiểm thử bổ sung và kiểm thử hồi quy BT3

### 4.1. Kiểm thử hồi quy ban đầu

Bộ pytest tại ngày 07/11/2026 ghi nhận:

**14 passed – 0 failed.**

Lệnh:

`python -m pytest tests/ -v`

Kết quả này thuộc môi trường Python của bản clone `v0.2`.

Minh chứng:

- `docs/screenshots/TC-12.PNG`
- `docs/screenshots/regression-after-fixes.PNG`

### 4.2. Kiểm thử đối soát BR05 và BR09

BT3 bổ sung kiểm thử đối soát trên dữ liệu bán hàng nguồn.

Kết quả được ghi nhận:

| Chỉ tiêu | Kết quả |
|---|---:|
| Tổng dòng chi tiết bán hàng | 35.697 |
| `MATCH` | 35.177 |
| `MISMATCH` | 520 |
| Giữ nguyên doanh thu nguồn | PASS |
| Tính lại doanh thu | PASS |
| Tính giá trị chênh lệch | PASS |
| Phân loại trạng thái | PASS |

Chương trình:

`src/transform/transform_sales.py`

Bài kiểm thử bổ sung:

`tests/test_sales_reconciliation_bt3.py`

**Kết luận:** Chức năng đối soát hoạt động đúng theo các quy tắc đã kiểm tra.

Việc có 520 dòng `MISMATCH` là vấn đề chất lượng dữ liệu nguồn cần tiếp tục đối chiếu nghiệp vụ, không phải bằng chứng cho thấy hàm đối soát kiểm thử thất bại.

### 4.3. Đánh giá chất lượng dữ liệu ba chiều

Chương trình:

`scripts/check_data_quality_bt3.py`

Phạm vi kiểm tra: 27 cột thuộc bốn file CSV nguồn.

| Chiều chất lượng | PASS | FAIL | N/A |
|---|---:|---:|---:|
| Completeness | 26 | 1 | 0 |
| Validity | 27 | 0 | 0 |
| Consistency | 8 | 1 | 18 |

Các vấn đề được ghi nhận:

- `orders.nhan_vien`: Completeness 96,11%, thấp hơn ngưỡng 99%.
- `order_items.thanh_tien`: Consistency 98,54%, thấp hơn ngưỡng 99%.

Kết quả chi tiết được lưu trong:

- `docs/evidence/data_quality_bt3.json`
- `docs/evidence/data_quality_bt3.csv`

### 4.4. Kiểm thử Docker và GitHub Actions

BT3 sử dụng Docker Compose và GitHub Actions để kiểm chứng khả năng triển khai trên Ubuntu Linux.

Workflow:

`.github/workflows/docker-test.yml`

Các bước kiểm tra gồm:

1. Build Docker Image.
2. Chạy ETL bằng dữ liệu mẫu.
3. Kiểm tra bốn bảng SQLite.
4. Chạy lại ETL.
5. Kiểm tra không phát sinh bản ghi Fact trùng do rerun.
6. Chạy pytest bên trong Docker.

Kết quả workflow mới đã được ghi nhận hoàn tất thành công.

Lệnh chạy pytest trong Docker:

`docker compose run --rm pipeline python -m pytest tests/ -v`

**Số lượng pytest PASS của lần chạy mới:** Xác nhận theo log GitHub Actions và ảnh `docker_pytest_BT3.PNG`.

Không sử dụng con số 14 PASS từ tag `v0.2` làm kết quả của phiên bản Docker mới.

### 4.5. Kiểm chứng clone sạch tag v1.0

Một workflow riêng được sử dụng để clone tag `v1.0`, chạy Docker ETL và kiểm tra SQLite Warehouse.

Kết quả đã ghi nhận:

| Hạng mục | Kết quả |
|---|---|
| Clone đúng tag `v1.0` | PASS |
| Commit được kiểm tra | `61e34ba` |
| Docker ETL | PASS |
| `dim_date` | 3 dòng |
| `dim_product` | 3 dòng |
| `dim_store` | 2 dòng |
| `fact_sales` | 4 dòng |

Việc kiểm chứng này được thực hiện trên GitHub Actions vì máy Windows phát triển chưa chạy Docker trực tiếp thành công.

---

## 5. Bug Log và kiểm thử sau sửa lỗi

Trong quá trình phát triển và kiểm thử, ba lỗi đã được ghi nhận và sửa.

| Bug ID | Mức độ | Nội dung | Hướng sửa | Commit |
|---|---|---|---|---|
| BUG-01 | Major | `UnicodeEncodeError` khi đầu ra console sử dụng bảng mã không hỗ trợ tiếng Việt | Bổ sung xử lý lỗi mã hóa stdout trong `run_etl.py` | `d3fc130` |
| BUG-02 | Minor | CSV hoàn toàn rỗng gây `EmptyDataError` khó hiểu | Bắt lỗi và trả thông báo có đường dẫn file | `8041a81` |
| BUG-03 | Major | Giá trị `order_id` hoặc `product_id` toàn khoảng trắng được xem là hợp lệ | Bổ sung kiểm tra `strip()`, `None`, `NaN` | `28c6f87` |

Tài liệu chi tiết:

`docs/bug-log.md`

Ảnh trước và sau sửa lỗi được lưu trong:

`docs/screenshots/`

### 5.1. Lưu ý về BUG-01

Ở mốc kiểm thử ban đầu, biến môi trường `PYTHONIOENCODING=UTF-8` được sử dụng để hỗ trợ chạy lệnh trên Windows.

Tuy nhiên, cách này chỉ là biện pháp xử lý ở môi trường thực thi.

Sau đó, BUG-01 đã được sửa trong mã nguồn bằng commit `d3fc130`.

Vì vậy, trạng thái cuối cùng của BUG-01 được đối chiếu với Bug Log và commit sửa lỗi, không chỉ dựa vào biến môi trường.

### 5.2. Kiểm thử hồi quy

Sau khi sửa lỗi, bộ kiểm thử hồi quy đã được chạy và ghi nhận 14 bài PASS ở mốc kiểm thử cũ.

Bản BT3 tiếp tục bổ sung kiểm thử trong Docker.

Kết quả từng mốc được lưu riêng để tránh nhầm lẫn.

---

## 6. Quản lý ảnh minh chứng

### 6.1. Ảnh test case

Các ảnh gốc được lưu tại:

`docs/screenshots/`

| Ảnh | Nội dung |
|---|---|
| `TC-01.PNG` | Chạy ETL |
| `TC-02.PNG` | Số dòng SQLite |
| `TC-03.PNG` | KPI Dashboard |
| `TC-04.PNG` | `quantity=0` |
| `TC-05.PNG` | `quantity=1` |
| `TC-06.PNG` | `quantity=-1` |
| `TC-07.PNG` | `unit_price=-1` |
| `TC-08.PNG` | `order_id=None` |
| `TC-09.PNG` | Doanh thu MISMATCH |
| `TC-10.PNG` | Reject dữ liệu lỗi |
| `TC-11.PNG` | Chạy ETL hai lần |
| `TC-12.PNG` | Bộ pytest tại mốc kiểm thử ban đầu |

### 6.2. Ảnh kiểm thử bổ sung BT3

Các minh chứng triển khai và chất lượng dữ liệu được quản lý tại:

`docs/evidence/`

Bao gồm:

- Kết quả Docker và GitHub Actions.
- Kết quả pytest trong Docker.
- Kiểm chứng clone sạch tag `v1.0`.
- Kết quả Data Quality ba chiều.
- Kiểm tra PII trong SQLite Warehouse.
- Kiểm tra cấu hình bảo vệ secret.

Những ảnh mới chỉ được xem là minh chứng chính thức khi đã được chụp từ quá trình kiểm tra thực tế và lưu đúng vị trí.

---

## 7. Giới hạn kiểm thử

Kết quả kiểm thử hiện tại có các giới hạn:

- Bộ dữ liệu Demo nhỏ hơn nhiều so với dữ liệu bán hàng đầy đủ.
- Chưa thực hiện kiểm thử tải lớn.
- Chưa kiểm chứng Docker Desktop chạy thành công trực tiếp trên máy Windows phát triển.
- Chưa kiểm thử phân quyền người dùng trên hệ thống production.
- Chưa triển khai mã hóa SQLite.
- Một số quy tắc Data Quality chỉ kiểm tra những điều kiện đã lập trình.
- Chưa có kiểm thử lịch chạy ETL tự động hoặc Incremental Loading.
- Các kết quả pytest ở các phiên bản khác nhau không được cộng gộp thành một số liệu chung.

---

## 8. Kết luận

Theo kết quả kiểm thử đã ghi nhận ngày 07/11/2026, hệ thống Mekong Mobile có **12/12 test case PASS**, thuộc năm nhóm kiểm thử.

Ba lỗi được ghi nhận trong Bug Log đã có commit sửa và minh chứng trước/sau.

BT3 tiếp tục bổ sung kiểm thử đối soát doanh thu, đánh giá chất lượng dữ liệu ba chiều, đóng gói ETL bằng Docker và kiểm chứng trên GitHub Actions.

Kết quả Data Quality được báo cáo trung thực, bao gồm cả những chỉ tiêu không đạt ngưỡng.

Các kết quả trên chứng minh những chức năng và tình huống đã được kiểm tra, không khẳng định hệ thống không còn lỗi ngoài phạm vi kiểm thử.

**Tài liệu liên quan:**

- `docs/test-plan.md`
- `docs/bug-log.md`
- `docs/deployment-guide.md`
- `docs/pipeline-documentation.md`
- `docs/data-dictionary.md`
- `docs/security-checklist.md`
- `docs/ai-disclosure.md`
