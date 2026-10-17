
# NHẬT KÝ THAY ĐỔI THIẾT KẾ – BT1

**Đề tài:** Kho dữ liệu bán hàng Mekong Mobile  
**Track:** DA – Luồng L6  
**Sinh viên:** Lê Gia Huy  
**MSSV:** 2374802010175  

## 1. Phản hồi của giảng viên

| ID | Phản hồi BT1 | Quyết định | Lý do kỹ thuật |
|---|---|---|---|
| DC01 | Star Schema thiếu kiểu dữ liệu và mô tả cột | Điều chỉnh | Bổ sung Data Dictionary để phục vụ thiết kế ETL |
| DC02 | Use Case chưa đúng ký hiệu UML | Điều chỉnh | Dùng actor, ellipse và ranh giới hệ thống đúng chuẩn |
| DC03 | Data Flow thiếu chú thích | Điều chỉnh | Giúp người đọc hiểu ký hiệu và luồng dữ liệu |
| DC04 | Còn các câu nháp chưa xác nhận | Điều chỉnh | Hoàn thiện lập luận và loại bỏ placeholder |
| DC05 | Phụ lục AI quá nhỏ | Điều chỉnh | Chuyển thành bảng văn bản dễ đọc |
| DC06 | Commit message bị lặp | Điều chỉnh | Áp dụng Conventional Commits |
| DC07 | Nguy cơ công khai dữ liệu khách hàng | Điều chỉnh | Không đưa dữ liệu khách hàng thô lên GitHub |
| DC08 | GRAIN đã phù hợp | Giữ nguyên | Một dòng Fact tương ứng một dòng chi tiết hóa đơn nguồn |
| DC09 | Quy tắc đối soát 520 dòng lệch ±10% | Giữ nguyên | Chưa đủ bằng chứng xác định thuế hoặc giảm giá |


## 2. Trạng thái thực hiện

Sau khi tiếp nhận phản hồi BT1 của giảng viên, sinh viên đã rà soát và thực hiện các điều chỉnh sau:

- **DC01 – Đã điều chỉnh:** Bổ sung kiểu dữ liệu và mô tả các thuộc tính trong Star Schema (`docs/erd.drawio`).
- **DC02 – Đã điều chỉnh:** Chuẩn hóa Actor, Use Case, System Boundary và các đường liên kết theo ký hiệu UML (`docs/usecase.drawio`).
- **DC03 – Đã điều chỉnh:** Bổ sung bảng chú thích cho Data Flow Diagram (`docs/data-flow.drawio`).
- **DC04 – Đã điều chỉnh:** Loại bỏ các câu nháp chưa xác nhận và hoàn thiện lập luận kiến trúc trong báo cáo BT1.
- **DC05 – Đã điều chỉnh:** Chuyển bảng khai báo sử dụng AI từ hình ảnh sang bảng văn bản trong báo cáo BT1.
- **DC06 – Đang áp dụng:** Sử dụng Conventional Commits với các tiền tố `fix:`, `docs:`, `feat:` và nội dung tiếng Việt.
- **DC07 – Đã thực hiện một phần:** Cập nhật `.gitignore` và ngừng theo dõi các file CSV thô trong phiên bản Git mới. Các file vẫn có thể tồn tại trong lịch sử commit trước đó.
- **DC08 – Giữ nguyên:** Grain của `Fact_Sales` là một dòng chi tiết đơn hàng nguồn.
- **DC09 – Giữ nguyên:** Tiếp tục ghi nhận 520 dòng có chênh lệch ±10% để phục vụ đối soát, chưa tự suy luận nguyên nhân là thuế hoặc giảm giá.

## 3. Kết luận

Các điều chỉnh tập trung vào việc chuẩn hóa tài liệu thiết kế, tăng tính rõ ràng và khả năng truy vết giữa yêu cầu nghiệp vụ, kiến trúc hệ thống và mô hình dữ liệu.

Những nội dung đã được giảng viên đánh giá phù hợp như grain, quy tắc đối soát dữ liệu và lập luận lựa chọn kiến trúc AD01–AD03 được giữ nguyên.

Trong giai đoạn tiếp theo, sinh viên sẽ triển khai ETL theo các lớp Extract, Transform, Quality và Load; kiểm thử quy tắc chất lượng dữ liệu; và đối chiếu kết quả thực hiện với các ngưỡng NFR đã xác định.
