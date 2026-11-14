# BẢNG KHAI BÁO SỬ DỤNG CÔNG CỤ AI HỖ TRỢ

**Học phần:** Chuyên đề Tốt nghiệp 1  
**Học kỳ:** HK1, Năm học 2026 – 2027  
**Bài nộp:** Bài tập 3 – Kiểm thử và Đóng gói prototype  
**Giai đoạn khai báo:** BT1, BT2 và BT3

---

## I. THÔNG TIN SINH VIÊN

- **Họ và tên:** Lê Gia Huy
- **Mã số sinh viên:** 2374802010175
- **Lớp:** 71K29CNTT02
- **Chuyên ngành (Track):** DA – Data Analytics
- **Luồng nghiệp vụ:** L6 – Kho dữ liệu bán hàng
- **Đề tài:** Xây dựng kho dữ liệu bán hàng và Dashboard phân tích doanh thu cho Mekong Mobile

---

## II. BẢNG KHAI BÁO SỬ DỤNG AI

### 1. Giai đoạn BT1 – Xác định yêu cầu và thiết kế

| Công cụ AI | Dùng vào việc gì | File / Mục áp dụng | Cách kiểm chứng và chỉnh sửa |
|---|---|---|---|
| Gemini | Gợi ý các file dữ liệu phù hợp với đề tài | Phiếu phạm vi đề tài BT1 | Đã mở và kiểm tra các file dữ liệu trước khi lựa chọn. |
| Gemini | Giải thích User Story và các yêu cầu nghiệp vụ | Phiếu phạm vi đề tài BT1 | Đọc, tìm hiểu và điều chỉnh nội dung theo đề tài Mekong Mobile. |
| Gemini | Gợi ý cách xây dựng sơ đồ kiến trúc hệ thống | `docs/architecture.drawio` | Đối chiếu yêu cầu và chỉnh sửa sơ đồ bằng draw.io. |

### 2. Giai đoạn BT2 – Xây dựng prototype

| Công cụ AI | Dùng vào việc gì | File / Mục áp dụng | Cách kiểm chứng và chỉnh sửa |
|---|---|---|---|
| ChatGPT | Hướng dẫn xây dựng quy trình ETL gồm Extract, Transform, Quality và Load | `run_etl.py`, `src/` | Chạy ETL, kiểm tra dữ liệu đầu ra và điều chỉnh các phần không phù hợp. |
| ChatGPT | Hỗ trợ xây dựng các quy tắc kiểm tra chất lượng dữ liệu | `src/quality/`, `generate_reject_demo.py` | Kiểm thử dữ liệu hợp lệ và dữ liệu lỗi giả lập, kiểm tra kết quả từ chối. |
| ChatGPT | Hướng dẫn xây dựng và kiểm thử SQLite Data Warehouse | `src/warehouse/`, `data/warehouse/` | Kiểm tra bảng dữ liệu, số dòng, khóa chính, khóa ngoại và kết quả chạy lại. |
| ChatGPT | Hướng dẫn xây dựng Dashboard, Measure DAX và xử lý lỗi dữ liệu nguồn | `powerbi/Mekong_Mobile_Dashboard_BT2_Final.pbit` | Mở Power BI Desktop, kiểm tra KPI và thử thay đổi đường dẫn dữ liệu. |

### 3. Giai đoạn BT3 – Kiểm thử và đóng gói prototype

| Công cụ AI | Dùng vào việc gì | File / Mục áp dụng | Cách kiểm chứng và chỉnh sửa |
|---|---|---|---|
| ChatGPT | Hỗ trợ lập kế hoạch kiểm thử và xây dựng báo cáo test case | `docs/test-plan.md`, `docs/test-report.md` | Đối chiếu với yêu cầu BT3 và thực hiện các test case, ghi nhận kết quả kiểm thử. |
| ChatGPT | Hỗ trợ phân tích nguyên nhân lỗi và cách sửa | `docs/bug-log.md`, các file mã nguồn liên quan | Kiểm tra kết quả sau sửa và lưu các commit tương ứng trên GitHub. |
| ChatGPT | Hướng dẫn cấu hình Docker để đóng gói môi trường ETL | `Dockerfile`, `docker-compose.yml`, `.dockerignore`, `.env.example` | Kiểm chứng bằng GitHub Actions trên Ubuntu Linux, xác nhận Docker build và ETL chạy thành công. |
| ChatGPT | Hỗ trợ xây dựng chương trình đánh giá ba chiều chất lượng dữ liệu | `scripts/check_data_quality_bt3.py` | Chạy chương trình trên dữ liệu nguồn, kiểm tra số liệu Completeness, Validity và Consistency; giữ nguyên các kết quả FAIL thực tế. |
| ChatGPT | Hỗ trợ phân tích định dạng ngày và sửa hàm kiểm tra tính hợp lệ | `scripts/check_data_quality_bt3.py` | Kiểm tra dữ liệu ngày thực tế, bổ sung định dạng và chạy lại chương trình để xác nhận kết quả. |
| ChatGPT | Hỗ trợ xây dựng quy tắc kiểm tra khóa liên kết và đối soát doanh thu | `scripts/check_data_quality_bt3.py`, `docs/srs.md` | Đối chiếu các quy tắc BR02, BR05, BR06, BR09 với SRS; loại bỏ phép kiểm tra `ma_don` duy nhất không phù hợp BR06. |
| ChatGPT | Gợi ý bài kiểm thử tự động cho chức năng đối soát | `tests/test_sales_reconciliation_bt3.py` | Chạy kiểm thử, đồng thời kiểm tra toàn bộ 35.697 dòng nguồn để xác nhận 35.177 MATCH và 520 MISMATCH. |
| ChatGPT | Hỗ trợ soạn hướng dẫn triển khai và kiểm tra bảo mật | `docs/deployment-guide.md`, `docs/security-checklist.md` | Đối chiếu cấu hình Docker, kết quả GitHub Actions và các minh chứng kiểm tra bảo mật của dự án. |
| ChatGPT | Hỗ trợ rà soát yêu cầu nộp bài và lập bảng khai báo AI | `docs/ai-disclosure.md` | Đối chiếu nội dung khai báo với các file và công việc thực tế trong BT3. |

---

## III. CÁCH TỰ KIỂM CHỨNG NỘI DUNG CÓ AI HỖ TRỢ

### 1. Kiểm chứng mã nguồn

Các đoạn mã do AI gợi ý được kiểm tra cú pháp, chạy thử và điều chỉnh cho phù hợp với cấu trúc thực tế của dự án.

Không xem mã nguồn do AI đề xuất là đúng khi chưa thực thi và kiểm tra kết quả.

### 2. Kiểm chứng dữ liệu

Kết quả kiểm tra chất lượng dữ liệu được lấy từ quá trình chạy chương trình trên các file CSV nguồn.

Các vấn đề đã phát hiện vẫn được ghi nhận:

- Completeness: 26 PASS, 1 FAIL.
- Validity: 27 PASS theo bộ quy tắc đã triển khai.
- Consistency: 8 PASS, 1 FAIL, 18 N/A.
- Có 520 dòng chi tiết bán hàng chênh lệch doanh thu.
- Không tự động chỉnh sửa doanh thu nguồn để làm đẹp kết quả.

### 3. Kiểm chứng quy trình ETL

Đã kiểm tra việc bảo toàn dữ liệu nguồn, tính doanh thu đối chiếu và phân loại trạng thái MATCH/MISMATCH.

Kết quả kiểm chứng BR05 và BR09 trên 35.697 dòng dữ liệu nguồn: PASS.

### 4. Kiểm chứng Docker

Quy trình Docker đã được kiểm thử bằng GitHub Actions trên môi trường Ubuntu Linux.

Các phép kiểm tra gồm xây dựng Docker Image, chạy ETL, tạo SQLite Warehouse, kiểm tra số dòng, chạy lại ETL và thực thi pytest.

Chưa xác minh việc sử dụng Docker Desktop trực tiếp trên máy Windows phát triển.

### 5. Kiểm chứng tài liệu

Nội dung tài liệu được đối chiếu với yêu cầu bài tập, quy tắc nghiệp vụ, mã nguồn và kết quả chạy thực tế.

Những giới hạn chưa được triển khai hoặc chưa có bằng chứng kiểm thử phải được trình bày rõ ràng, không mô tả thành chức năng đã hoàn thành.

---

## IV. GIỚI HẠN VÀ TRÁCH NHIỆM KHI SỬ DỤNG AI

AI được sử dụng để hỗ trợ học tập, giải thích khái niệm, gợi ý mã nguồn, phân tích lỗi và biên soạn tài liệu.

AI không thay thế việc tự kiểm thử, tự đánh giá và chịu trách nhiệm về kết quả bài làm.

Các số liệu, trạng thái PASS/FAIL và thông tin về chức năng hệ thống phải được đối chiếu với kết quả thực tế.

Sinh viên chịu trách nhiệm giải thích được mã nguồn, quy tắc nghiệp vụ, test case và những thay đổi đã thực hiện trong dự án.

---

## V. CAM KẾT VỀ LIÊM CHÍNH HỌC THUẬT

**Tôi xác nhận đã đọc, hiểu và chịu trách nhiệm về toàn bộ nội dung nộp.**

Tôi có sử dụng công cụ AI để hỗ trợ quá trình học tập và thực hiện đề tài. Các phần có AI hỗ trợ được khai báo trong bảng trên.

Tôi cam kết không cố ý khai báo sai kết quả kiểm thử, không tạo minh chứng giả và không mô tả các chức năng chưa triển khai thành chức năng đã hoàn thành.

**Họ và tên sinh viên:** Lê Gia Huy  
**MSSV:** 2374802010175  
**Ngày cập nhật:** 14/11/2026
