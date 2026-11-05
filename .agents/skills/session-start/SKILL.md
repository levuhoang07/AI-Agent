---
name: session-start
description: >-
  Use this skill to initialize or resume a working session for a case study.
  It reads the workspace registry and previous state, audits the filesystem,
  verifies completed tasks, displays the Session Opening Report, and establishes
  an active durable session state.
---

# Session Start Skill

Skill này điều khiển quy trình bắt đầu phiên làm việc an toàn, đảm bảo tính liên tục của dự án (Session Continuity) ngay cả khi người dùng mở một cuộc hội thoại mới trong Antigravity.

## 1. Trigger Conditions
- Người dùng gõ `/session-start` hoặc yêu cầu: "Bắt đầu phiên làm việc", "Tiếp tục case", "Mở phiên mới".

## 2. Quy trình Thực thi (Step-by-Step Procedure)

### Bước 1: Kiểm tra Workspace Registry & Xác định Case
- Đọc `workspace-state/workspace-registry.json` bằng script hoặc parser:
  ```python
  from state_engine import get_registry
  reg = get_registry()
  active_case_id = reg.get("active_case_id")
  ```
- Nếu người dùng chỉ định một `CASE_ID` cụ thể (ví dụ: `CASE-001`), chọn case đó.
- Nếu không chỉ định, chọn case gần nhất trong danh sách. Nếu chưa có case nào, hướng dẫn tạo case mới.

### Bước 2: Kiểm tra Phiên Gián đoạn (Interrupted Session Detection)
- Kiểm tra xem case có phiên trước đó bị gián đoạn hay không:
  ```python
  from state_engine import detect_recovery_needed
  needs_rec, reason, prev_sess = detect_recovery_needed(case_id)
  ```
- Nếu `needs_rec == True`, kích hoạt quy trình của skill `session-recovery` để xử lý trước khi mở phiên mới.

### Bước 3: Đối chiếu Filesystem & Kiểm tra Tính xác thực (Integrity Audit)
- Đọc `cases/<CASE_ID>/state/session-state.json` và `cases/<CASE_ID>/state/task-board.md`.
- Kiểm tra các file kết quả (artifacts) được liệt kê trong phiên trước xem có thực sự tồn tại trên ổ cứng hay không.
- Nếu một tác vụ bị đánh dấu `DONE` nhưng không tìm thấy file chứng cứ, chuyển trạng thái tác vụ về `IN_PROGRESS` và ghi cảnh báo.

### Bước 4: Khởi tạo Phiên & Lưu Trạng thái Bền vững
- Kích hoạt khởi tạo phiên thông qua engine:
  ```python
  from state_engine import start_session
  session_data, report_text = start_session(case_id, objectives=["Mục tiêu 1", "Mục tiêu 2"])
  ```
- Ghi trạng thái `ACTIVE` vào `cases/<CASE_ID>/state/session-state.json` và `workspace-state/active-session.json`.

### Bước 5: Xuất Báo cáo Khai mạc Phiên (Session Opening Report)
Bắt buộc in báo cáo ra màn hình chat theo định dạng chuẩn:

```text
==================================================
SESSION OPENING REPORT
==================================================
Case: <CASE_ID>
Session ID: <SESSION-YYYYMMDD-NNN>
Started at: <ISO_TIMESTAMP>
Previous Session: <PREV_SESSION_ID>
Previous Session Status: <CLOSED / FIRST_SESSION>

LAST SESSION SUMMARY
- Completed: <X> tasks
- Partially completed: <Y> tasks
- Blocked: <Z> tasks
- Files produced: <List of files>
- Decisions made: <List of decisions>

CURRENT PROJECT STATUS
- Overall progress: <Percentage or Stage>
- Current milestone: <Milestone Name>
- Pending tasks: <Tasks in TODO/IN_PROGRESS>
- Known issues: <Risks / Blockers>

RECOMMENDED PLAN
1. <Action 1>
2. <Action 2>
3. <Action 3>

Approval required: Review plan and proceed.
==================================================
```

## 3. Error Handling
- Nếu `workspace-registry.json` bị thiếu hoặc hỏng, tự động tạo lại baseline từ cấu trúc thư mục `cases/`.
- Nếu xảy ra lỗi phân quyền ghi file, thử lại tối đa 5 lần với cơ chế atomic write.
