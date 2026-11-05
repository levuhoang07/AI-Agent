---
name: session-close
description: >-
  Use this skill to close an active session safely. It audits all completed tasks,
  verifies generated deliverables on disk, updates task boards and manifest,
  persists markdown session closing reports, and marks the session CLOSED.
---

# Session Close Skill

Skill này điều khiển quy trình đóng phiên làm việc an toàn, đảm bảo mọi tiến độ, quyết định, file kết quả đều được lưu trữ bền vững trước khi kết thúc cuộc trò chuyện.

## 1. Trigger Conditions
- Người dùng gõ `/session-close` hoặc yêu cầu: "Đóng phiên làm việc", "Kết thúc phiên", "Lưu tiến độ và bàn giao".

## 2. Quy trình Thực thi (Step-by-Step Procedure)

### Bước 1: Kiểm tra Phiên Hiện hành
- Đọc `workspace-state/active-session.json` và `cases/<CASE_ID>/state/session-state.json`.
- Xác định `session_id` và danh sách mục tiêu ban đầu.

### Bước 2: Kiểm chứng Tệp tin Bàn giao (Deliverable Verification)
- Quét toàn bộ danh sách file được báo cáo hoàn thành trong phiên:
  - Báo cáo Word: `cases/<CASE_ID>/output/final/*.docx`
  - Bảng tính Excel: `cases/<CASE_ID>/output/final/*.xlsx`
  - Slide PowerPoint: `cases/<CASE_ID>/output/final/*.pptx`
- Chỉ các file thực sự tồn tại và đọc được mới được đưa vào danh sách `verified_artifacts`.

### Bước 3: Đóng Phiên & Ghi nhận Trạng thái Bền vững
- Kích hoạt engine đóng phiên:
  ```python
  from state_engine import close_session
  sess, report_md = close_session(
      case_id=case_id,
      session_id=session_id,
      completed_tasks=completed_tasks,
      pending_tasks=pending_tasks,
      blocked_tasks=blocked_tasks,
      artifacts=verified_artifacts,
      decisions=decisions,
      issues=issues,
      next_actions=next_actions
  )
  ```
- File báo cáo `cases/<CASE_ID>/state/sessions/<SESSION_ID>.md` và bản lưu tại `workspace-state/sessions/<SESSION_ID>.md` được ghi xuống ổ cứng bằng Safe Atomic Write.
- Tệp `cases/<CASE_ID>/state/task-board.md` được cập nhật đồng bộ các task `[x] DONE`.
- Tệp `workspace-state/active-session.json` được cập nhật trạng thái `CLOSED`.

### Bước 4: Xuất Báo cáo Kết thúc Phiên (Session Closing Report)
In toàn văn báo cáo Markdown ra màn hình chat:

```markdown
# SESSION CLOSING REPORT — <SESSION_ID>

**Case:** <CASE_ID>
**Started at:** <ISO_TIMESTAMP>
**Closed at:** <ISO_TIMESTAMP>

## 1. SESSION OBJECTIVES
## 2. WORK COMPLETED
## 3. ARTIFACTS CREATED / MODIFIED
## 4. VALIDATION RESULTS
## 5. DECISIONS MADE
## 6. UNFINISHED TASKS
## 7. BLOCKERS & RISKS
## 8. CURRENT PROJECT POSITION
## 9. RECOMMENDED NEXT SESSION PLAN
## 10. HANDOVER STATUS
```

## 3. Error Handling
- Nếu có lỗi ghi file ở bất kỳ bước nào, trạng thái phiên không được đánh dấu `CLOSED` mà giữ ở mức `INTERRUPTED` kèm thông báo lỗi chi tiết.
