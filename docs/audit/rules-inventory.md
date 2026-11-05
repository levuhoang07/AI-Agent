# KIỂM TOÁN QUY TẮC & QUẢN TRỊ (RULES INVENTORY)

**Thời gian audit:** 2026-11-06T00:52:45+07:00  
**Thực hiện bởi:** AI Workspace Architect

---

## 1. Kiểm toán Quy tắc Toàn cục (Global Rules)

Hệ thống ghi nhận 2 quy tắc toàn cục đang được kích hoạt từ `C:\Users\Admin\.gemini\config\rules\`:

### 1.1. `agent-cognitive-brain.md` (Agent Cognitive Brain Protocol)
- **Mục đích:** Tối ưu hóa nhận thức, giảm thiểu tải bộ nhớ làm việc (working memory friction).
- **Yêu cầu cốt lõi:**
  1. *Lead with the next action:* Dòng đầu tiên luôn là hành động thực thi được ngay. Không mở đầu bằng văn mẫu rườm rà.
  2. *Number multi-step tasks:* Đánh số bước rõ ràng.
  3. *End with one concrete next action:* Kết thúc bằng 1 bước tiếp theo cụ thể.
  4. *Working memory anchoring:* Neo giữ trạng thái `[Đã xong] -> [Hiện tại] -> [Kế tiếp]`.
  5. *Bounded Working Set <= 5:* Giới hạn số lượng phần tử hiển thị tối đa 5 để tránh quá tải.
  6. *Matter-of-fact error reporting:* Báo cáo lỗi khách quan 3 phần: Vị trí -> Nguyên nhân -> Phương án khắc phục nhỏ nhất.
  7. *Debug Spiral Breaker & Destructive Safety Gate:* Dừng sau 3 lần sửa thất bại; luôn xin phép trước hành động phá hủy.
- **Tương thích:** **100% ĐỒNG THUẬN.** Workspace Rules sẽ hoàn toàn kế thừa và tuân thủ giao thức này.

### 1.2. `project-organization.md` (Project Organization Rule)
- **Mục đích:** Định hướng các dự án độc lập nằm tại `D:\antigravity\projects\<project-name>`.
- **Ghi nhận đặc thù:** Phiên làm việc hiện tại được người dùng chỉ định trực tiếp tại Workspace root `D:\antigravity\AI-Agent PJ`. Hệ thống sẽ tôn trọng tuyệt đối workspace root này và cô lập các case study bên trong thư mục `cases/<CASE_ID>/` theo đúng nguyên tắc dự án tập trung.

---

## 2. Thiết kế Danh mục Workspace Rules (`.agents/rules/`)

Các quy tắc dự án được thiết kế ngắn gọn, tường minh, có YAML frontmatter và trigger phù hợp:

| Tên Rule | Tệp tin | Phạm vi áp dụng | Nội dung cốt lõi |
|---|---|---|---|
| **Rule 01** | `workspace-governance.md` | Workspace Root & Chung | Xác định ranh giới workspace, cấm xóa file tùy tiện, cấm sửa cấu hình global, ưu tiên đường dẫn tương đối |
| **Rule 02** | `case-isolation.md` | `cases/*` | Cô lập triệt để dữ liệu giữa các case study, không rò rỉ output hay task board |
| **Rule 03** | `data-integrity.md` | `analysis/*`, `output/*` | Chống bịa đặt dữ liệu (Zero Hallucination); gán nhãn `SIMULATED` vs `USER_PROVIDED`; công thức Excel phải được kiểm chứng |
| **Rule 04** | `evidence-policy.md` | `research/*`, `analysis/*` | Phân loại FACT, ASSUMPTION, INFERENCE, RECOMMENDATION; cấm trích dẫn giả mạo; truy vết nguồn gốc |
| **Rule 05** | `document-quality.md` | `output/*`, `shared/templates` | Tiêu chuẩn chất lượng cho DOCX, XLSX, PPTX; bảo toàn template; kiểm tra heading hierarchy, text overflow |
| **Rule 06** | `session-governance.md` | `workspace-state/*`, `state/*` | Quy tắc mở/đóng phiên; cấm tick DONE khi chưa có bằng chứng; lưu trữ trạng thái bền vững; tự động checkpoint |
| **Rule 07** | `academic-standards.md` | Báo cáo, Slide, Đề án | Bám sát đề bài & rubric môn học; đảm bảo tính khả thi, chi phí, rủi ro, văn phong học thuật và tư vấn chuẩn mực |

---

## 3. Quy tắc tích hợp tại Root (`AGENTS.md`)
Tại thư mục gốc `D:\antigravity\AI-Agent PJ\AGENTS.md`, sẽ tạo tài liệu điều phối trung tâm để Antigravity tự động nhận diện danh tính kiến trúc, danh mục Rules và Skills ngay khi mở Workspace.

