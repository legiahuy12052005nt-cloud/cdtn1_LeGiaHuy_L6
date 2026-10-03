# Đặc tả Yêu cầu Dữ liệu (Data Requirements) - Track DA

**Dự án:** Kho dữ liệu bán hàng và báo cáo doanh thu
**Sinh viên:** Lê Gia Huy (MSSV: 2374802010175)

---

## 1. Câu hỏi phân tích (Analytical Questions)
Hệ thống Data Warehouse và Dashboard báo cáo được xây dựng nhằm mục đích trả lời các câu hỏi nghiệp vụ sau cho Ban giám đốc:
1. Tổng doanh thu và số lượng sản phẩm bán ra theo từng tháng/quý/năm là bao nhiêu? Xu hướng tăng hay giảm so với kỳ trước?
2. Top 10 sản phẩm (hoặc danh mục sản phẩm) mang lại doanh thu cao nhất là gì?
3. Cửa hàng hoặc khu vực địa lý nào có hiệu suất bán hàng tốt nhất và kém nhất?
4. Tỷ lệ khách hàng mua hàng (có thông tin) so với khách vãng lai (không có thông tin) là bao nhiêu?

## 2. Phát biểu GRAIN (Mức độ chi tiết của dữ liệu)
*Định nghĩa mức độ chi tiết sâu nhất mà một dòng dữ liệu (row) trong bảng sự kiện (Fact Table) sẽ lưu trữ.*

**Phát biểu GRAIN:** "Mỗi một dòng (row) trong bảng `Fact_Sales` đại diện cho **số lượng và doanh thu của một sản phẩm (Item) được bán ra trong một hóa đơn (Order)** tại một cửa hàng vào một thời điểm cụ thể."

## 3. Từ điển dữ liệu nguồn (Source Data Dictionary) & Tỷ lệ thiếu
Quá trình phân tích (profiling) các file dữ liệu thô (Excel/CSV) đầu vào ghi nhận các trường thông tin sau:

| Bảng/File Nguồn | Tên Cột (Column) | Kiểu Dữ Liệu | Ý nghĩa / Mô tả | Tỷ lệ thiếu (Missing Rate) |
| :--- | :--- | :--- | :--- | :--- |
| `Sales_Data.xlsx` | OrderID | String | Mã hóa đơn giao dịch | 0% |
| `Sales_Data.xlsx` | OrderDate | Date | Ngày giờ thực hiện giao dịch | 0% |
| `Sales_Data.xlsx` | ProductID | String | Mã định danh sản phẩm | 0.5% |
| `Sales_Data.xlsx` | StoreID | String | Mã cửa hàng thực hiện giao dịch | 0% |
| `Sales_Data.xlsx` | Quantity | Integer | Số lượng sản phẩm bán ra trong dòng đó | ~2.1% |
| `Sales_Data.xlsx` | UnitPrice | Decimal | Đơn giá bán của sản phẩm | 0% |
| `Sales_Data.xlsx` | CustomerPhone | String | Số điện thoại của khách hàng (nếu có) | ~25.5% |

## 4. Quy tắc chất lượng dữ liệu (Data Quality Rules)
Để đảm bảo tính chính xác cho báo cáo Power BI, dữ liệu trước khi nạp vào kho (Load) phải vượt qua các quy tắc làm sạch (Cleansing Rules) sau:

*   **Rule 1 (Tính hợp lệ - Validity):** Cột `Quantity` (Số lượng) và `UnitPrice` (Đơn giá) phải luôn mang giá trị lớn hơn hoặc bằng 0. Các dòng có giá trị âm sẽ bị loại bỏ hoặc đưa vào bảng `Error_Log`.
*   **Rule 2 (Tính hợp lý - Plausibility):** Cột `OrderDate` không được chứa ngày của tương lai (lớn hơn ngày hiện tại chạy luồng ETL).
*   **Rule 3 (Xử lý Missing Data):** 
    * Nếu cột `CustomerPhone` bị trống (null), hệ thống sẽ tự động điền giá trị mặc định là "Unknown" (Khách vãng lai).
    * Nếu cột `ProductID` bị trống, loại bỏ toàn bộ dòng dữ liệu đó vì không thể phân tích doanh thu sản phẩm.
*   **Rule 4 (Tính toàn vẹn tham chiếu - Integrity):** Bất kỳ mã `ProductID` hoặc `StoreID` nào xuất hiện trong file Sales đều bắt buộc phải tồn tại trong bảng danh mục (Dimension tables: `Dim_Product`, `Dim_Store`).