# KIỂM TOÁN DANH MỤC AGENT SKILLS (SKILLS INVENTORY)

**Thời gian audit:** 2026-11-06T00:52:30+07:00  
**Thực hiện bởi:** AI Workspace Architect

---

## 1. Khảo sát Built-in & Global Skills hiện có

Đã quét thư mục builtin của Antigravity tại `C:\Users\Admin\.gemini\antigravity\builtin\skills`:

| Tên Skill Built-in | Chức năng chính | Đánh giá tái sử dụng cho Case Study Workspace |
|---|---|---|
| `agy-customizations` | Hướng dẫn cấu trúc Rules, Skills, Plugins | **REUSE (REFERENCE):** Dùng làm tiêu chuẩn kỹ thuật khi thiết kế Skills & Rules |
| `antigravity_guide` | Sách hướng dẫn Antigravity 2.0 & IDE | **REUSE (REFERENCE):** Hướng dẫn vận hành IDE |
| `automation` | Thiết kế cron / background task | Không thuộc luồng bài tập Case Study thông thường |
| `generative_ui` | Tạo widget HTML nhúng | Phục vụ trực quan hóa dữ liệu inline khi cần |
| `migrate-workflows` | Chuyển đổi workflow cũ | Không có workflow cũ cần chuyển đổi |
| `permissioned-github` | Quản trị GitHub qua sandbox | Phục vụ Git nếu có remote repo |
| `plugin` | Đóng gói Plugin bundle | Không yêu cầu đóng gói plugin ở phạm vi này |
| `run-workflow` | Chạy workflow JSON cũ | Không dùng |
| `ui-plugin-navigation`| Mở giao diện plugin | Phụ trợ UI |

**Nhận xét:** Không có bất kỳ Built-in Skill nào đáp ứng trực tiếp quy trình chuyên sâu của môn học (Session Lifecycle, Case Intake, Case Planning, Business Analysis, Document Specialists, QA). Cần xây dựng các Workspace Skills chuyên biệt trong `.agents/skills/`.

---

## 2. Kế hoạch Phân loại & Triển khai Workspace Skills

Theo quy định kiến trúc của hệ thống AI Case Study Workspace, 13 Workspace Skills bắt buộc được phân loại như sau:

| STT | Tên Skill | Phân loại | Mức ưu tiên | Chức năng cốt lõi |
|---|---|---|---|---|
| 1 | `session-start` | **CREATE** | **P0** | Khởi tạo phiên, đọc Workspace Registry & Case State, kiểm tra checkpoint, hiển thị Session Opening Report |
| 2 | `session-close` | **CREATE** | **P0** | Đối chiếu task board, kiểm tra file sinh ra, ghi nhận quyết định, lưu báo cáo Markdown, đóng session an toàn |
| 3 | `session-recovery`| **CREATE** | **P0** | Phát hiện session bị treo hoặc mất điện, đối chiếu filesystem với checkpoint gần nhất, khôi phục an toàn |
| 4 | `case-intake` | **CREATE** | **P0** | Tiếp nhận đề bài, rubric, dataset; bóc tách problem statement, constraints, assumptions, deliverables checklist |
| 5 | `case-planning` | **CREATE** | **P0** | Lập Work Breakdown Structure (WBS), Task Board Kanban, rủi ro, Definition of Done, Acceptance Criteria |
| 6 | `business-analysis`| **CREATE** | **P1** | Phân tích vấn đề, stakeholder, quy trình AS-IS/TO-BE, BPMN, KPI Tree, SWOT/PESTEL, Root Cause |
| 7 | `research-validation`| **CREATE** | **P1** | Lập kế hoạch nghiên cứu, kiểm chứng nguồn tin, phân loại FACT/ASSUMPTION/INFERENCE/RECOMMENDATION |
| 8 | `data-analysis` | **CREATE** | **P1** | Data profiling, EDA, xử lý thiếu dữ liệu, tính toán KPI, insight trực quan hóa |
| 9 | `agent-solution-design`| **CREATE** | **P1** | Thiết kế giải pháp AI Agent, kiến trúc use case, human-in-the-loop, prompt engineering, cost/eval |
| 10 | `docx-specialist` | **CREATE** | **P1** | Đọc/phân tích Word template, tạo báo cáo học thuật chuẩn mực, heading hierarchy, bảo toàn template |
| 11 | `xlsx-specialist` | **CREATE** | **P1** | Đọc/ghi workbook, bảo toàn công thức, data dictionary, transformation log, charts, kiểm tra tính toán |
| 12 | `pptx-specialist` | **CREATE** | **P1** | Phân tích slide master/layouts, storyboard, thiết kế slide chuẩn học thuật/tư vấn, visual QA |
| 13 | `deliverable-qa` | **CREATE** | **P1** | Kiểm tra chéo DOCX, XLSX, PPTX, thẩm định tính nhất quán dữ liệu (Cross-Format Consistency) |

---

## 3. Tiêu chuẩn Kỹ thuật cho từng Skill (`Agent Skills Standard`)
Mỗi Skill trong `.agents/skills/<skill-name>/` sẽ bao gồm:
- `SKILL.md`: Frontmatter YAML hợp lệ (`name`, `description`), điều kiện kích hoạt rõ ràng, luồng từng bước, input/output, quality gate và error handling.
- `scripts/`: Chứa các script Python/PowerShell tự động hóa (nếu có tác vụ phức tạp).
- `references/`: Chứa cẩm nang, tài liệu tham chiếu chuyên sâu phục vụ progressive disclosure.

