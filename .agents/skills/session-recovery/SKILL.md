---
name: session-recovery
description: >-
  Use this skill to detect, diagnose, and recover interrupted or crashed sessions.
  It audits the filesystem against the latest checkpoint, identifies completed
  vs unfinished tasks, and restores state safely without losing newer progress.
---

# Session Recovery Skill

Skill này tự động can thiệp khi một phiên làm việc bị ngắt đột ngột (mất mạng, người dùng tắt trình duyệt, timeout hoặc lỗi hệ thống).

## 1. Trigger Conditions
- Tự động kích hoạt khi `session-start` phát hiện phiên trước còn cờ `ACTIVE`.
- Người dùng gõ `/session-recovery` hoặc yêu cầu: "Khôi phục phiên làm việc", "Khắc phục phiên bị lỗi".

## 2. Quy trình Thực thi

### Bước 1: Phát hiện Bất thường (Anomaly Detection)
- Đọc `cases/<CASE_ID>/state/session-state.json`.
- Kiểm tra `status == "ACTIVE"` và `last_checkpoint_id`.
- Đọc danh sách các checkpoint snapshot trong `cases/<CASE_ID>/state/sessions/CKPT-*.json`.

### Bước 2: Đối chiếu Checkpoint với Filesystem (Diff Analysis)
- Đọc checkpoint gần nhất:
  - So sánh danh sách artifacts đã ghi nhận trong checkpoint với filesystem thực tế.
  - Xác định các file đã tạo xong nhưng chưa kịp close session.
  - Xác định các task dở dang.

### Bước 3: Đề xuất Phương án Phục hồi
Hệ thống cung cấp 2 lựa chọn:
1. **RESUME:** Tiếp tục phiên hiện hành từ checkpoint gần nhất.
2. **CLEAN CLOSE:** Đóng an toàn phiên bị gián đoạn, ghi nhận những gì đã làm được và sẵn sàng mở phiên mới.

### Bước 4: Thực thi Phục hồi & Lưu Báo cáo
```python
from state_engine import recover_interrupted_session
sess, recovery_md = recover_interrupted_session(case_id, action="RESUME")
```
- Tạo tệp `cases/<CASE_ID>/state/sessions/RECOVERY-<SESSION_ID>.md`.
- Báo cáo rõ: Checkpoint ID đã khôi phục, chênh lệch filesystem, và các bước tiếp theo.

