NHẬT KÝ THAY ĐỔI THIẾT KẾ – BT1 ĐẾN BT2
Đề tài: Xây dựng kho dữ liệu bán hàng và Dashboard phân tích doanh thu cho Mekong Mobile
Track: DA – Luồng L6
Sinh viên: Lê Gia Huy
MSSV: 2374802010175  
1. Phản hồi của giảng viên ở BT1
ID	Phản hồi BT1	Quyết định	Lý do kỹ thuật
DC01	Star Schema thiếu kiểu dữ liệu và mô tả cột	Điều chỉnh	Bổ sung Data Dictionary để phục vụ thiết kế ETL
DC02	Use Case chưa đúng ký hiệu UML	Điều chỉnh	Dùng actor, ellipse và ranh giới hệ thống đúng chuẩn
DC03	Data Flow thiếu chú thích	Điều chỉnh	Giúp người đọc hiểu ký hiệu và luồng dữ liệu
DC04	Còn các câu nháp chưa xác nhận	Điều chỉnh	Hoàn thiện lập luận và loại bỏ placeholder
DC05	Phụ lục AI quá nhỏ	Điều chỉnh	Chuyển thành bảng văn bản dễ đọc
DC06	Commit message bị lặp	Điều chỉnh	Áp dụng quy ước đặt tên commit có nội dung phân biệt rõ thay đổi
DC07	Nguy cơ công khai dữ liệu khách hàng	Điều chỉnh	Không đưa dữ liệu khách hàng thô vào các commit mới
DC08	GRAIN đã phù hợp	Giữ nguyên	Một dòng Fact tương ứng một dòng chi tiết đơn hàng nguồn
DC09	Quy tắc đối soát 520 dòng lệch ±10%	Giữ nguyên	Chưa đủ bằng chứng xác định nguyên nhân là thuế hoặc giảm giá


2. Trạng thái thực hiện và thay đổi ở BT2
2.1. Điều chỉnh sau phản hồi BT1
- DC01 – Đã điều chỉnh: Bổ sung kiểu dữ liệu và mô tả cột trong thiết kế Star Schema; thông tin chi tiết được ghi tại docs/data-dictionary.md và docs/erd.drawio.
- DC02 – Đã điều chỉnh: Chuẩn hóa ký hiệu Actor, Use Case và System Boundary trong docs/usecase.drawio.
- DC03 – Đã điều chỉnh: Bổ sung chú thích cho sơ đồ luồng dữ liệu tại docs/data-flow.drawio.
- DC04 – Đã điều chỉnh: Rà soát và loại bỏ các nội dung nháp trong tài liệu BT1.
- DC05 – Đã điều chỉnh: Chuyển nội dung khai báo sử dụng AI thành bảng văn bản để dễ kiểm tra.
- DC06 – Đang áp dụng: Đặt thông điệp commit mô tả nội dung thay đổi. Một số commit trước đây sử dụng tiền tố feat:, fix:, docs:; các commit mới có thể dùng mô tả tiếng Việt không dấu để dễ đọc.
- DC07 – Đã giảm thiểu rủi ro: .gitignore bỏ qua data/raw/, data/processed/, data/rejected/, data/warehouse/ và file *.pbix. Việc này không tự xóa dữ liệu nếu chúng từng xuất hiện trong lịch sử Git cũ.
- DC08 – Giữ nguyên: Grain của Fact_Sales là một dòng chi tiết đơn hàng nguồn.
- DC09 – Giữ nguyên: Ghi nhận 520 dòng chênh lệch doanh thu trong dữ liệu đã kiểm thử; không tự động gán nguyên nhân hoặc sửa số tiền.
2.2. Các quyết định hiện thực hóa ở BT2
ID	Nội dung	Quyết định thực tế	Lý do / tác động
BT2-01	Quy trình xử lý dữ liệu	Triển khai một lệnh python run_etl.py, tách các chức năng Extract, Transform, Quality và Load	Dễ chạy lại, kiểm thử và truy vết
BT2-02	Kho dữ liệu	Xuất 4 bảng Fact_Sales, Dim_Date, Dim_Product, Dim_Store ra CSV và lưu thêm SQLite tại data/warehouse/mekong_mobile.db	Hỗ trợ kiểm tra quan hệ dữ liệu và sử dụng Power BI
BT2-03	Nguồn của Power BI	Power BI đọc 4 file CSV Warehouse thông qua Parameter ProjectFolder, chưa truy vấn SQLite trực tiếp	Phù hợp với Template .pbit và dữ liệu mẫu trên máy khác
BT2-04	Kiểm tra chất lượng	Bổ sung 5 hàm kiểm tra dữ liệu đầu vào, thống kê số lượng và tỷ lệ lỗi	Giúp phát hiện lỗi có giải thích rõ ràng
BT2-05	Minh chứng dữ liệu bị từ chối	Sử dụng dữ liệu lỗi giả lập, ghi các dòng bị loại kèm lý do vào file minh chứng Reject	Không cần công khai dữ liệu khách hàng thật
BT2-06	Chạy lại ETL	Kiểm tra số dòng Fact sau khi chạy lại và kiểm tra không trùng sales_key	Hạn chế phát sinh dữ liệu trùng khi chạy lặp trên cùng bộ dữ liệu
BT2-07	Dashboard	Hoàn thiện Template powerbi/Mekong_Mobile_Dashboard_BT2_Final.pbit với 3 trang phân tích	Có thể mở lại trên bản clone GitHub bằng dữ liệu mẫu
BT2-08	Trạng thái Dashboard	Bổ sung thông báo Empty và Error; Loading sử dụng giao diện Refresh mặc định của Power BI	Người dùng phân biệt dữ liệu rỗng và lỗi nguồn; không tuyên bố có Loading tùy chỉnh
BT2-09	Kiểm thử tự động	Chạy toàn bộ bộ kiểm thử bằng pytest, kết quả gần nhất: 14 bài PASS	Bao phủ các trường hợp hợp lệ, giá trị biên và dữ liệu không hợp lệ
BT2-10	Khả năng tái lập	Cung cấp data/sample/, README và Template .pbit; không công khai .pbix chứa dữ liệu Import	Có thể dựng lại luồng ETL và Dashboard bằng dữ liệu giả lập


3. Kết quả kiểm chứng và giới hạn
- Kiểm thử tự động: Đã ghi nhận 14 passed in 5.38s trên môi trường Python 3.10.11.
- Chạy lại ETL: Với bộ dữ liệu đã kiểm thử, Fact_Sales có 35.697 dòng và không có khóa sales_key trùng sau khi chạy lại. Kết quả này không thay thế cho việc chứng minh mọi tình huống cập nhật dữ liệu đều idempotent.
- Kiểm tra Dashboard Demo: Template cuối cùng đã được mở với dữ liệu mẫu, hiển thị tổng doanh thu 23.500.000 VND, 3 đơn hàng và 5 sản phẩm bán.
- Error State: Khi chuyển ProjectFolder tới thư mục không tồn tại, Dashboard không tiếp tục hiển thị doanh thu cũ và xuất thông báo lỗi thân thiện. Cơ chế kiểm tra nguồn chủ yếu xử lý trường hợp file bị thiếu hoặc không đọc được; chưa khẳng định bao phủ mọi dạng sai cấu trúc CSV.
- Empty State: Hiển thị thông báo riêng khi bộ lọc không có dữ liệu và nguồn dữ liệu vẫn hợp lệ.
- Loading State: Sử dụng trạng thái tải/Refresh có sẵn của Power BI Desktop, chưa xây dựng một màn hình Loading tùy biến.
- Bảo mật dữ liệu: Các file CSV thực và .pbix không được bổ sung vào commit công khai mới. Cần rà soát riêng lịch sử Git trước đây nếu muốn xác nhận dữ liệu cũ đã được loại bỏ hoàn toàn.
Minh chứng tham khảo:
- docs/evidence/data_quality_reject_demo.PNG
- docs/evidence/nfr03_etl_rerun.PNG
- docs/evidence/dashboard_bt2_final_normal.PNG
- docs/evidence/dashboard_empty_state.PNG
- docs/evidence/dashboard_error_state_actual.PNG
- docs/evidence/dashboard_loading_state.PNG
- docs/evidence/e2e_github_clone_pytest.PNG
4. Kết luận
Từ BT1 sang BT2, dự án đã chuyển từ thiết kế sang hiện thực hóa ETL, kiểm tra chất lượng dữ liệu, tạo Data Warehouse và xây dựng Dashboard Power BI. Những quyết định được giữ nguyên gồm grain của Fact_Sales và nguyên tắc ghi nhận chênh lệch doanh thu mà không tự suy đoán nguyên nhân.

Trước khi nộp BT2, cần kiểm tra lại khả năng chạy từ bản clone sạch, hoàn thiện tài liệu kiến trúc thực tế và khai báo sử dụng AI, sau đó mới tạo tag v0.2 trên GitHub.