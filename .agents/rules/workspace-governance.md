---
description: "Workspace Governance Rule: Enforces boundary integrity, safe path resolution, and prevents unauthorized system changes or file deletion"
trigger: always_on
---

# RULE 01 — WORKSPACE GOVERNANCE

## 1. Ranh giới Không gian làm việc (Workspace Boundary)
- Thư mục gốc cố định của dự án là `D:\antigravity\AI-Agent PJ`.
- Tuyệt đối **KHÔNG** tự ý tạo hoặc chuyển sang Workspace mới ngoài thư mục này.
- Mọi đường dẫn tệp tin nội bộ phải được xử lý theo đường dẫn tương đối (relative paths) từ Workspace root để đảm bảo tính di động (portability) của dự án.

## 2. Kiểm soát Thao tác Tệp tin (File Operations Safety)
- **Không tự ý xóa file:** Tuyệt đối không xóa bất kỳ tệp tin nào của người dùng hoặc tệp tin trạng thái đã tồn tại nếu chưa được người dùng phê duyệt rõ ràng tại Gate D (High-Risk Operation).
- **Nguyên tắc Safe Atomic Write:** Khi cập nhật các file trạng thái quan trọng (`.json`), luôn ghi ra file tạm `.tmp`, xác thực tính toàn vẹn (validate schema), sau đó thực hiện lệnh thay thế nguyên tử (`os.replace`) để tránh lỗi hỏng file (file corruption) trên Windows NTFS.
- **Bảo toàn dữ liệu gốc:** Các tài liệu bài tập, đề cương và dữ liệu nguồn trong thư mục `cases/<CASE_ID>/input/` phải được duy trì ở trạng thái chỉ đọc (read-only); không được sửa trực tiếp vào file gốc.

## 3. Quản trị Cấu hình Hệ thống (System Configuration)
- Không tự ý cài đặt package toàn cục (`pip install`) hoặc thay đổi file cấu hình ngoài Workspace nếu chưa có sự đồng ý của người dùng.
- Mọi hoạt động kiểm thử phải tận dụng tối đa các thư viện đã cài sẵn hoặc thư viện chuẩn `unittest` của Python.

