---
description: "Session Governance Rule: Governs session lifecycle, state durability, manual start/close, checkpoint persistence, and task verification"
trigger: always_on
---

# RULE 06 — SESSION GOVERNANCE & LIFECYCLE

## 1. Cơ chế Mở và Đóng Phiên Thủ công (Manual Session Lifecycle)
- Người dùng chủ động bắt đầu phiên qua lệnh `/session-start` và kết thúc phiên qua `/session-close`.
- Agent **không tự ý mở phiên mới ngầm** khi phiên trước đã đóng.
- Mỗi phiên phải sở hữu:
  - `session_id`: Định dạng chuẩn `SESSION-YYYYMMDD-NNN` (ví dụ: `SESSION-20261106-001`).
  - `case_id`: Mã case study liên kết trực tiếp.
  - `started_at` và `closed_at`: Timestamp ISO 8601 có múi giờ thực tế (`+07:00`).
  - Danh sách mục tiêu phiên (`objectives`), tác vụ hoàn thành, tác vụ dang dở, rào cản và quyết định thống nhất.

## 2. Lưu trữ Trạng thái Bền vững (Durable State Persistence)
- Trạng thái phiên làm việc bắt buộc phải lưu trữ bền vững bằng các file JSON và Markdown trên ổ cứng, **không được phụ thuộc hoàn toàn vào bộ nhớ hội thoại của Antigravity**.
- Ngay sau khi hoàn thành một tác vụ quan trọng, tạo một deliverable, hoặc người dùng phê duyệt quyết định, Agent phải tự động ghi Checkpoint (`last_checkpoint_id`).

## 3. Quy tắc Nghiệm thu Tác vụ (Task Completion Verification)
- **Cấm tick DONE ảo:** Tuyệt đối không đánh dấu trạng thái tác vụ là `DONE` trên `task-board.md` hoặc `session-state.json` nếu chưa kiểm tra sự tồn tại thực tế của tệp tin kết quả trên đĩa và xác nhận tệp tin đó vượt qua kiểm tra nghiệm thu (Acceptance Criteria).
- Nếu tệp tin mới chỉ tạo một phần hoặc chưa xác minh, tác vụ phải giữ nguyên trạng thái `IN_PROGRESS` hoặc `REVIEW`.

## 4. Quy tắc Đóng Phiên An toàn (Safe Session Close)
- Một phiên chỉ được đánh dấu là `CLOSED` sau khi toàn bộ các bước sau đã thành công:
  1. File báo cáo phiên `cases/<CASE_ID>/state/sessions/SESSION-YYYYMMDD-NNN.md` được ghi xuống đĩa thành công.
  2. Bảng `task-board.md` của case được cập nhật đúng tiến độ.
  3. Tệp `session-state.json` của case được chuyển sang `status: "CLOSED"`.
  4. Tệp `workspace-state/workspace-registry.json` được cập nhật thông tin phiên mới nhất.
  5. Tệp `workspace-state/active-session.json` được giải phóng hoặc chuyển trạng thái không còn active.
- Nếu xảy ra lỗi ghi file ở bất kỳ bước nào, phiên phải được giữ ở trạng thái có thể khôi phục (`INTERRUPTED` hoặc `RECOVERY_PENDING`) và thông báo chi tiết lỗi cho người dùng.

