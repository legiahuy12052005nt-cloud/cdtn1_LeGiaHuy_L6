# ĐẶC TẢ YÊU CẦU RÚT GỌN (SRS)
**Dự án:** Xây dựng kho dữ liệu bán hàng và Dashboard phân tích doanh thu cho Mekong Mobile (Luồng 6)
**Luồng:** L6 — Kho dữ liệu bán hàng | **Track:** DA  
**Sinh viên:** Lê Gia Huy — MSSV: 2374802010175
## 1. Giới thiệu và phạm vi

### 1.1. Bối cảnh và mục tiêu
Dữ liệu bán hàng được lưu ở các tệp CSV chứa hóa đơn (`orders_2024_2026.csv`), chi tiết đơn (`order_items.csv`), sản phẩm (`products.csv`) và cửa hàng (`stores.csv`). Prototype L6 đọc, kiểm tra, chuẩn hóa và tổ chức dữ liệu phục vụ phân tích theo thời gian, sản phẩm, cửa hàng; sau đó cung cấp dữ liệu cho báo cáo Power BI.

**Giới hạn phạm vi:** Quy trình chạy cục bộ, xử lý dữ liệu theo lô; không xây dựng POS, quản lý kho/bảo hành, dự báo AI, phân quyền chi tiết hoặc báo cáo realtime. `customers_raw.csv` là dữ liệu tham khảo, chưa nạp vào Star Schema phạm vi BT1. Chức năng xuất PDF/Excel ở bản SRS trước được chuyển sang hướng mở rộng.

**Quyết định đang chờ xác nhận:** Các dòng `order_items.thanh_tien` chênh ±10% so với `so_luong × don_gia` **chưa biết** do thuế, giảm giá, phụ phí hay dữ liệu mô phỏng. Giữ nguyên tiền nguồn, tạo số đối chiếu và trạng thái cảnh báo; chưa tuyên bố chỉ số nào là doanh thu kế toán cuối cùng.

### 1.2. Thuật ngữ
| Thuật ngữ | Giải nghĩa |
|---|---|
| ETL | Extract – Transform – Load: đọc, chuyển đổi, nạp dữ liệu |
| Staging | Vùng lưu tạm dữ liệu nguồn trước xử lý |
| Data Warehouse | Kho dữ liệu phục vụ phân tích |
| Fact_Sales | Bảng sự kiện dòng bán hàng |
| Dimension | Bảng chiều dùng để nhóm/lọc số liệu |
| GRAIN | Một dòng trong Fact đại diện cho sự kiện ở mức nào |
| DQ | Data Quality — chất lượng dữ liệu |
| KPI | Chỉ số báo cáo |

## 2. Các bên liên quan và vai trò
| Actor | Nhu cầu / hành động trong phạm vi | Ngoài quyền / ngoài phạm vi |
|---|---|---|
| Chuyên viên dữ liệu | Chạy hoặc giám sát ETL; xem lỗi nguồn và kết quả nạp | Không quản lý giao dịch POS |
| Ban giám đốc | Xem KPI và phân tích doanh thu/số lượng theo thời gian, sản phẩm | Không chỉnh sửa dữ liệu nguồn |
| Quản lý cửa hàng | Lọc và so sánh kết quả bán hàng theo cửa hàng/khu vực | Không cấu hình schema kho dữ liệu |

## 3. Yêu cầu chức năng và User Story

### 3.1. Functional Requirements (FR)
| ID | Yêu cầu kiểm chứng được | Mức |
|---|---|---|
| FR01 | Khi kích hoạt quá trình đọc nguồn, hệ thống đọc bốn tệp CSV cấu hình sẵn và ghi số bản ghi từng nguồn; thiếu tệp phải ghi lỗi tên tệp. | MUST |
| FR02 | Hệ thống kiểm tra ngày, số tiền, trường bắt buộc, khóa tham chiếu và ghi lý do cho bản ghi bị cách ly; không tự ý điền ngày thiếu. | MUST |
| FR03 | Hệ thống tính `calculated_amount = so_luong × don_gia`, giữ nguyên `reported_amount = thanh_tien`, gắn trạng thái đối soát cho mỗi dòng. | SHOULD |
| FR04 | Hệ thống nạp các dòng đủ điều kiện vào `Fact_Sales` liên kết `Dim_Date`, `Dim_Product`, `Dim_Store` và có cơ chế tránh nạp lại cùng một dòng nguồn. | MUST |
| FR05 | Hệ thống cung cấp số đơn (`COUNT DISTINCT order_id`), số lượng bán và giá trị bán hàng theo kỳ thời gian, có mô tả phạm vi loại trừ dữ liệu chưa đủ điều kiện. | SHOULD |
| FR06 | Hệ thống hỗ trợ phân tích theo cửa hàng, khu vực và sản phẩm/danh mục thông qua bảng chiều. | SHOULD |
| FR07 | Hệ thống cung cấp bảng xếp hạng sản phẩm theo giá trị bán hàng trong kỳ được chọn. | COULD |


### 3.2. User Stories (5–7 story cho BT1)
| ID | User Story | MoSCoW | Liên kết FR |
|---|---|---|---|
| US01 | Là **Chuyên viên dữ liệu**, tôi muốn đọc dữ liệu bán hàng từ các CSV đã khai báo để có dữ liệu đầu vào nhất quán cho quá trình phân tích. | MUST | FR01 |
| US02 | Là **Chuyên viên dữ liệu**, tôi muốn phát hiện, ghi nhận các bản ghi không hợp lệ để kiểm soát sai lệch trong kết quả nạp. | MUST | FR02 |
| US03 | Là **Chuyên viên dữ liệu**, tôi muốn đối chiếu thành tiền nguồn với số lượng nhân đơn giá để nhận biết dòng cần kiểm tra. | SHOULD | FR03 |
| US04 | Là **Chuyên viên dữ liệu**, tôi muốn nạp dữ liệu chuẩn hóa vào kho để dùng lại nguồn phân tích nhất quán mà không tăng dữ liệu trùng khi chạy lại. | MUST | FR04 |
| US05 | Là **Ban giám đốc**, tôi muốn xem giá trị bán hàng, số đơn và số lượng theo tháng để theo dõi xu hướng hoạt động. | SHOULD | FR05 |
| US06 | Là **Quản lý cửa hàng**, tôi muốn lọc và so sánh số liệu theo cửa hàng và sản phẩm để đánh giá hiệu quả bán hàng. | SHOULD | FR06 |
| US07 | Là **Ban giám đốc**, tôi muốn xem sản phẩm mang lại giá trị bán hàng cao nhất để định hướng phân tích danh mục. | COULD | FR07 |


### 3.3. Acceptance Criteria — story MUST
| AC | Given | When | Then |
|---|---|---|---|
| US01-AC01 | 4 CSV đúng đường dẫn, đọc được | Chạy bước Extract | Hệ thống ghi nhận số dòng từng nguồn |
| US01-AC02 | Không tìm thấy `order_items.csv` | Chạy Extract | Thông báo file thiếu, không nạp Fact |
| US02-AC01 | `ngay` ở một định dạng được hỗ trợ | Chạy Validate/Transform | Ngày được chuẩn hóa thành DATE |
| US02-AC02 | Hóa đơn thiếu `ngay` | Chạy Validate/Transform | Dòng phụ thuộc được cách ly, ghi lý do, không tự gán ngày |
| US02-AC03 | Số tiền không chuyển được thành số | Chạy Validate/Transform | Ghi mã lỗi và giữ giá trị gốc để tra soát |
| US04-AC01 | Dòng đủ điều kiện, tìm được khóa Dim | Chạy Load | Fact được liên kết đúng 3 Dimension |
| US04-AC02 | File nguồn không đổi đã nạp một lần | Chạy Load thêm lần nữa | Số dòng Fact không tăng do trùng lặp |

## 4. Yêu cầu phi chức năng (NFR)


| ID | NFR có thể đo | Cách kiểm chứng |
|---|---|---|
| NFR01 | ETL xử lý tối thiểu 26.000 hóa đơn và 35.697 dòng chi tiết trong ≤120 giây trên máy được khai báo cấu hình. | Ghi thời gian bắt đầu–kết thúc chạy |
| NFR02 | 100% dòng không đạt quy tắc validation bắt buộc phải có log gồm nguồn, mã lỗi và lý do. | Đối chiếu tập dòng bị loại và error log |
| NFR03 | Chạy lại cùng bộ dữ liệu 2 lần không làm tăng số dòng Fact tương ứng với cùng định danh nguồn. | So số bản ghi và khóa nguồn trước/sau |
| NFR04 | Trang Power BI tổng quan tải trong ≤5 giây trên máy thử nghiệm được khai báo. | Đo thời gian render dashboard |


## 5. Ràng buộc và quy tắc nghiệp vụ
| Mã | Quy tắc | Cơ sở / ghi chú |
|---|---|---|
| BR01 | `order_items.order_id` tham chiếu `orders_2024_2026.order_id`. | Quan hệ nguồn |
| BR02 | `orders_2024_2026.ma_cua_hang` đối chiếu `stores.store_code`. | Quan hệ nguồn |
| BR03 | `order_items.product_id` đối chiếu `products.product_id`. | Quan hệ nguồn |
| BR04 | Ngày nguồn được chuẩn hóa theo định dạng có trong CSV; thiếu ngày không được tự tạo ngày. | 114 đơn thiếu `ngay` trong bản nguồn đã khảo sát |
| BR05 | Giữ nguyên `order_items.thanh_tien`; tính thêm giá trị đối chiếu `so_luong × don_gia`, không tự động ghi đè. | 520 dòng lệch chính xác ±10% chưa rõ nghiệp vụ |
| BR06 | Không dùng `ma_don` làm khóa duy nhất; không giả định `order_id + product_id` duy nhất cho từng dòng chi tiết. | Có mã đơn lặp, nhiều dòng cùng cặp order/product |
| BR07 | Phải có định danh ổn định cho dòng nguồn để hỗ trợ idempotent load. | `order_items.csv` không có `order_line_id` |
| BR08 | Tổng số đơn = đếm `DISTINCT order_id` từ tập dữ liệu đủ điều kiện, không đếm số dòng Fact. | Một đơn có thể có nhiều sản phẩm |
| BR09 | Các dòng nguồn chưa có kết luận doanh thu phải được đánh dấu phục vụ đối soát. | Chưa đủ bằng chứng về thuế/giảm giá |

**Ràng buộc thiết kế:** Khi sử dụng thứ tự dòng CSV làm định danh, cần lưu thêm dấu vết phiên bản file nguồn; nếu file sắp xếp lại thì định danh có thể thay đổi. Xác nhận quy tắc trước khi triển khai.

## 6. Bảng truy vết yêu cầu
| FR | User Story | Use Case | MoSCoW | Test Case dự kiến (BT3) |
|---|---|---|---|---|
| FR01 | US01 | UC01 | MUST | TC01, TC02 |
| FR02 | US02 | UC02 | MUST | TC03, TC04 |
| FR03 | US03 | UC03 | SHOULD | TC05 (dự kiến) |
| FR04 | US04 | UC04 | MUST | TC06, TC07 |
| FR05 | US05 | UC05 | SHOULD | TC08 (dự kiến) |
| FR06 | US06 | UC06 | SHOULD | TC09 (dự kiến) |
| FR07 | US07 | UC07 | COULD | Chưa hiện thực ở BT2 |

