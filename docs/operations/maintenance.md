# HƯỚNG DẪN BẢO TRÌ & NÂNG CẤP HỆ THỐNG (MAINTENANCE GUIDE)

**Mục tiêu:** Đảm bảo hệ thống AI Case Study Workspace hoạt động ổn định lâu dài, dễ dàng nâng cấp kỹ năng và sao lưu an toàn mà không làm ảnh hưởng đến các bài tập cũ.

---

## 1. Kiểm tra Định kỳ Hệ thống (Health Check Routine)

Mỗi khi bắt đầu một học kỳ mới hoặc sau khi cập nhật phiên bản Antigravity, chạy lại bộ kiểm thử tự động toàn diện:
```powershell
python tests/test_quality_gates.py
```
Kiểm tra báo cáo tại `tests/results/bootstrap-test-report.md` để đảm bảo cả 10 Quality Gates vẫn đạt trạng thái **PASS**.

---

## 2. Quy trình Bổ sung Agent Skill Mới (Adding New Skills)

Khi môn học yêu cầu thêm kỹ năng mới (ví dụ: `prompt-evaluator`, `diagram-generator`):
1. **Tạo thư mục skill:** `.agents/skills/<new-skill-name>/`
2. **Soạn thảo `SKILL.md`:** Bắt buộc có phần YAML frontmatter hợp lệ:
   ```markdown
   ---
   name: <new-skill-name>
   description: >-
     Describe what the skill does and when to activate it in third-person.
   ---
   # Instructions...
   ```
3. **Thêm Helper Script (nếu có):** Đặt script xử lý vào `shared/utilities/` hoặc thư mục `scripts/` nội bộ của skill.
4. **Cập nhật Inventory:** Cập nhật danh mục trong `docs/audit/skills-inventory.md` và `AGENTS.md`.

---

## 3. Quy trình Sao lưu & Phục hồi Dự án (Backup & Recovery)

### Sao lưu Nhanh qua Git (Recommended):
Toàn bộ mã nguồn, skills, rules và tiến độ case study được quản trị qua Git:
```powershell
git add .
git commit -m "Snapshot: Hoàn thành Case CASE-001"
```

### Sao lưu Ngoại tuyến (Offline Archive):
Nén thư mục `cases/<CASE_ID>/` thành file ZIP để lưu trữ bài tập đã hoàn thành. Khi cần xem lại, chỉ cần giải nén vào thư mục `cases/` và hệ thống sẽ tự động nhận diện lại lịch sử phiên làm việc.

---

## 4. Xử lý Sự cố Thường gặp (Troubleshooting)

| Hiện tượng | Nguyên nhân tiềm ẩn | Giải pháp xử lý |
|---|---|---|
| **Mở phiên mới nhưng Agent không nhớ tiến độ cũ** | Chưa gõ lệnh `/session-start` hoặc file `session-state.json` bị mất | Gõ `/session-start` để ép đọc file trạng thái; nếu lỗi file, gõ `/session-recovery` để khôi phục từ checkpoint. |
| **Báo lỗi PermissionError khi ghi file trên Windows** | Tệp tin Excel hoặc Word đang được mở bởi ứng dụng khác | Đóng tệp tin trên Microsoft Office/Excel; cơ chế Safe Atomic Write trong `safe_io.py` sẽ tự động thử lại sau 0.2s. |
| **Công thức Excel hiển thị `#NAME?`** | Tên hàm viết hoa/thường không chuẩn hoặc sai dấu phân cách | Đảm bảo tên hàm chuẩn tiếng Anh (`=SUM`, `=AVERAGE`, `=IF`) và dùng dấu phẩy `,` ngăn cách tham số. |
| **Slide PowerPoint bị tràn chữ ra ngoài khung** | Đoạn văn bản trong shape quá dài | Kiểm tra bằng `inspect_pptx()`; giới hạn tối đa 5-7 gạch đầu dòng và dưới 500 ký tự cho mỗi slide. |

