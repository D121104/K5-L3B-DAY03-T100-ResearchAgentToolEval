# Báo cáo cá nhân — Nguyễn Minh Nhân

## 1. Thông tin thành viên

- **Họ tên:** Nguyễn Minh Nhân
- **MSSV:** 2A202603723
- **Email:** nhannguyenit04@gmail.com

## 2. Phần việc phụ trách

- **CP2:** Tham gia xây dựng, chỉnh sửa và hoàn thiện các tool của Research Agent.
- **CP3:** Phụ trách phát triển và tích hợp Bonus Tool `compare_sources` vào hệ thống.
- Phối hợp với các thành viên trong nhóm để đảm bảo tool tương thích với cấu trúc chung của dự án.

## 3. Đóng góp cụ thể

### CP2 — Tool Implementation

- Tham gia chỉnh sửa và hoàn thiện các tool theo yêu cầu của bài lab.
- Rà soát cấu trúc input/output và cách xử lý lỗi của các tool.
- Điều chỉnh cấu hình và tích hợp các tool vào hệ thống Research Agent.

### CP3 — Bonus Tool Development

- Xây dựng Bonus Tool `compare_sources` nhằm đối chiếu thông tin từ ít nhất hai nguồn dữ liệu.
- Triển khai logic so sánh các thuộc tính và phân loại kết quả thành `consistent`, `different` và `missing`.
- Bổ sung cơ chế xử lý dữ liệu đầu vào không hợp lệ và trả về thông báo lỗi có cấu trúc.
- Đăng ký tool trong `tools/__init__.py` và khai báo schema trong `artifacts/tools.yaml`.
- Điều chỉnh cấu trúc dữ liệu đầu vào để tương thích với hệ thống đánh giá hiện có.

## 4. Bằng chứng

**Các file liên quan đến phần đóng góp:**

- `tools/compare_sources/tool.py` — Xây dựng logic Bonus Tool.
- `tools/__init__.py` — Đăng ký Bonus Tool.
- `artifacts/tools.yaml` — Khai báo cấu trúc và tham số của tool.

**AI/công cụ đã sử dụng và cách tự kiểm tra:**

- **ChatGPT:** Hỗ trợ tham khảo cách triển khai, phân tích lỗi và điều chỉnh cấu trúc dữ liệu.
- **VS Code, Python:** Viết code, kiểm tra logic và xử lý lỗi trong quá trình phát triển.
- **Git/GitHub:** Quản lý phiên bản và đồng bộ code với nhóm.

Tự kiểm tra bằng cách đối chiếu kết quả trả về với dữ liệu đầu vào, kiểm tra các trường hợp dữ liệu không hợp lệ và xác nhận tool được đăng ký trong hệ thống.

## 5. Tự đánh giá

Tôi đã thực hiện các công việc được phân công trong CP2 và phần xây dựng Bonus Tool thuộc CP3. Trong quá trình triển khai, tôi chủ động tìm hiểu cấu trúc hệ thống, xử lý các vấn đề phát sinh và điều chỉnh tool để phù hợp với yêu cầu của bài lab.

Thông qua quá trình thực hiện, tôi hiểu rõ hơn về cách xây dựng và tích hợp công cụ cho AI Agent, thiết kế input/output schema và xử lý ngoại lệ.