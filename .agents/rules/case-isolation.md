---
description: "Case Isolation Rule: Ensures strict segregation of data, task boards, research, and deliverables between independent case studies"
trigger: always_on
---

# RULE 02 — CASE ISOLATION

## 1. Nguyên tắc Độc lập Tuyệt đối (Strict Data Segregation)
- Mỗi bài toán tình huống (Case Study) bắt buộc phải nằm trong một thư mục con độc lập theo cú pháp:
  `cases/<CASE_ID>/` (Ví dụ: `cases/CASE-001/`, `cases/TEST-SESSION/`).
- Dữ liệu đầu vào, tài liệu nghiên cứu, phân tích nghiệp vụ, mô hình AI và sản phẩm bàn giao (Deliverables) của Case A tuyệt đối **KHÔNG** được ghi đè, tham chiếu chéo hoặc rò rỉ sang Case B.

## 2. Quản lý Trạng thái Độc lập (Independent State Management)
- Mỗi case sở hữu một bảng trạng thái riêng biệt gồm:
  - `cases/<CASE_ID>/state/case-manifest.json`: Siêu dữ liệu định danh case.
  - `cases/<CASE_ID>/state/task-board.md`: Bảng quản lý tiến độ Kanban nội bộ của case.
  - `cases/<CASE_ID>/state/decisions.md`: Nhật ký các quyết định đã được duyệt.
  - `cases/<CASE_ID>/state/session-state.json`: Trạng thái phiên hiện hành của case.
  - `cases/<CASE_ID>/state/sessions/`: Lịch sử các phiên đóng của case.

## 3. Phân định Tài nguyên Dùng chung (Shared Resources Boundary)
- Các tài nguyên đặt tại `shared/` (như templates mẫu, utilities, schemas) là tài nguyên đọc chung (read-only references).
- Khi một case muốn áp dụng template từ `shared/templates/`, hệ thống phải **sao chép** template vào `cases/<CASE_ID>/output/draft/` trước khi tiến hành chỉnh sửa. Tuyệt đối không chỉnh sửa trực tiếp trên file mẫu chung.

## 4. Chuyển đổi Case (Case Switching Protocol)
- Khi người dùng muốn chuyển từ Case A sang Case B, hệ thống phải kiểm tra xem Case A có phiên đang mở (`ACTIVE`) hay không.
- Bắt buộc phải thực hiện đóng phiên an toàn (`/session-close`) hoặc lưu checkpoint cho Case A trước khi chuyển sang kích hoạt phiên của Case B.

## 5. Quản lý Thư mục Input & Output Trung tâm (Central Input & Output Isolation)
- Khi tiếp nhận tài liệu tại `input/`, phân loại tài liệu theo thư mục con `input/<CASE_ID>/`.
- Khi xuất tài liệu sản phẩm tại `output/`, **BẮT BUỘC** phải tạo và lưu trữ vào thư mục con riêng biệt theo từng mã Case/Dự án:
  `output/<CASE_ID>/final/` và `output/<CASE_ID>/draft/`.
- Tuyệt đối **KHÔNG** xuất file của các case khác nhau vào cùng một thư mục chung nhằm bảo đảm không bị lẫn lộn dữ liệu và dễ dàng tìm kiếm sau này.


