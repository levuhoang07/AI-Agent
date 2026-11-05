---
name: case-planning
description: >-
  Use this skill to create work breakdown structures (WBS), prioritize tasks,
  set acceptance criteria and definition of done (DoD), identify risks,
  and establish the initial Kanban task board for a case study.
---

# Case Planning Skill

Skill này lập kế hoạch triển khai chi tiết cho bài toán tình huống dựa trên phạm vi đã thống nhất ở Gate A.

## 1. Trigger Conditions
- Sau khi hoàn thành `case-intake` và được phê duyệt Scope.
- Người dùng yêu cầu: "Lập kế hoạch thực hiện", "Tạo WBS", "Cập nhật task board".

## 2. Quy trình Thực thi

### Bước 1: Xây dựng Cấu trúc Phân rã Công việc (WBS)
Chia nhỏ case thành các gói công việc logic:
1. **Phân tích Nghiệp vụ & Dữ liệu (BA & Data):** Khảo sát quy trình AS-IS, phân tích dữ liệu, tính toán KPI cơ sở.
2. **Thiết kế Giải pháp AI Agent (Solution Architecture):** Lựa chọn kiến trúc Agent (ReAct, Multi-Agent, Tool Calling), phân rã quy trình TO-BE, thiết kế prompt & safety guardrails.
3. **Phát triển Tài liệu & Mô hình (Deliverable Production):** Soạn thảo báo cáo Word, dựng bảng tính Excel, thiết kế slide thuyết trình.
4. **Kiểm thử & Đảm bảo Chất lượng (QA & Cross-Validation):** Kiểm tra tính nhất quán số liệu, rà soát rubric.

### Bước 2: Thiết lập Tiêu chí Nghiệm thu (Acceptance Criteria & DoD)
Mỗi tác vụ phải có tiêu chuẩn rõ ràng:
- *Ví dụ:* Tác vụ "Tạo mô hình tài chính Excel" chỉ đạt `DONE` khi: có đầy đủ 3 sheets, công thức `=SUM` và `=AVERAGE` không lỗi, biểu đồ thể hiện đúng số liệu, và kết quả khớp với báo cáo Word.

### Bước 3: Lập Bảng Quản trị Rủi ro (Risk Register)
Đánh giá xác suất và tác động:
- Rủi ro thiếu dữ liệu -> Giả định hợp lý có gắn nhãn `[SIMULATED]`.
- Rủi ro tràn slide PPTX -> Sử dụng thuật toán đếm ký tự trong `pptx-specialist`.

### Bước 4: Khởi tạo Task Board Kanban
Cập nhật tệp `cases/<CASE_ID>/state/task-board.md` với đầy đủ các task theo thứ tự ưu tiên (Priority P0, P1, P2) và phụ thuộc (Dependencies).
Chuyển trạng thái case: `status: "PLANNED"`.

