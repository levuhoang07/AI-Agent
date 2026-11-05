---
name: case-intake
description: >-
  Use this skill to intake assignment briefs, course rubrics, datasets, and lecturer guidelines.
  It parses problem statements, extracts business requirements, identifies constraints and assumptions,
  and establishes the initial case manifest and deliverables checklist.
---

# Case Intake Skill

Skill này đóng vai trò phễu tiếp nhận và chuẩn hóa mọi yêu cầu bài tập của giảng viên môn "Ứng dụng AI Agent trong công việc".

## 1. Trigger Conditions
- Người dùng cung cấp đề bài, file PDF/DOCX đề cương, rubric hoặc dataset bài tập.
- Người dùng yêu cầu: "Phân tích đề bài", "Bắt đầu case mới", "Đọc yêu cầu bài tập".

## 2. Quy trình Thực thi

### Bước 1: Tiếp nhận & Lưu trữ Dữ liệu Đầu vào (Source Files Intake)
- Lưu trữ tài liệu đề bài vào: `cases/<CASE_ID>/input/assignment/`
- Lưu trữ file template Word/PPTX vào: `cases/<CASE_ID>/input/templates/`
- Lưu trữ bộ dữ liệu (CSV/XLSX) vào: `cases/<CASE_ID>/input/datasets/`

### Bước 2: Bóc tách Yêu cầu Trọng tâm (Requirement Extraction)
Bóc tách thành 6 cấu phần chuẩn:
1. **Bối cảnh Doanh nghiệp (Business Context):** Ngành nghề, quy mô, mô hình kinh doanh, hiện trạng vận hành.
2. **Vấn đề Cốt lõi (Problem Statement):** Nút thắt cổ chai (bottlenecks), lãng phí chi phí, sai sót thủ công hoặc áp lực cạnh tranh.
3. **Mục tiêu Giải pháp (Solution Objectives):** Tự động hóa quy trình bằng AI Agent, nâng cao năng suất, cắt giảm chi phí.
4. **Ràng buộc & Giới hạn (Constraints):** Thời gian thực hiện, ngân sách, hạ tầng kỹ thuật, quy định bảo mật dữ liệu.
5. **Tiêu chuẩn Rubric (Rubric Mapping):** Bảng điểm và tiêu chí đánh giá của giảng viên (ví dụ: Tính sáng tạo, Kiến trúc Agent, Độ chính xác số liệu, Chất lượng báo cáo).
6. **Checklist Sản phẩm Bàn giao (Deliverables Checklist):**
   - Báo cáo phân tích kinh doanh (DOCX).
   - Mô hình tài chính & dữ liệu KPI (XLSX).
   - Slide thuyết trình bảo vệ phương án (PPTX).

### Bước 3: Cập nhật Hồ sơ Case (Case Manifest)
- Cập nhật `cases/<CASE_ID>/state/case-manifest.json` với danh sách requirements và deliverables chuẩn.
- Đặt trạng thái case: `status: "ANALYZED"`.

### Bước 4: Chốt chặn Phê duyệt (Approval Gate A — Scope Approval)
Trình bày tóm tắt đề bài và danh mục deliverables dự kiến để người dùng xác nhận phạm vi trước khi lập kế hoạch chi tiết.
