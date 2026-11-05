---
name: deliverable-qa
description: >-
  Use this skill to perform end-to-end quality assurance and cross-format consistency
  audits across DOCX reports, XLSX workbooks, and PPTX slide decks before final submission.
---

# Deliverable QA Skill

Skill này đóng vai trò chốt chặn kiểm thử chất lượng toàn diện (Quality Assurance Gate) trước khi bàn giao sản phẩm cuối cùng cho người dùng hoặc giảng viên.

## 1. Trigger Conditions
- Sau khi đã tạo đủ 3 định dạng tài liệu (Word, Excel, PowerPoint).
- Người dùng yêu cầu: "Kiểm tra chất lượng tài liệu", "Soát lỗi bài tập", "Kiểm tra tính nhất quán số liệu".

## 2. Quy trình Thực thi

### Bước 1: Kiểm thử Định dạng Độc lập (Format Specific Integrity)
- Gọi `inspect_docx()` để kiểm tra phân cấp heading, bảng biểu và văn bản Word.
- Gọi `inspect_and_verify_xlsx()` để kiểm tra cấu trúc sheet, công thức và biểu đồ Excel.
- Gọi `inspect_pptx()` để kiểm tra số lượng slide, tỷ lệ 16:9 và lỗi tràn văn bản PowerPoint.

### Bước 2: Kiểm thử Tính Nhất quán Đa định dạng (Cross-Format Consistency)
Sử dụng module `shared/utilities/qa_validator.py`:
```python
from qa_validator import cross_validate_deliverables

key_metrics = {
    "ROI": "245%",
    "Reduction_Rate": "65%",
    "Payback_Months": 3.2
}

qa_result = cross_validate_deliverables(
    docx_path="cases/<CASE_ID>/output/final/<CASE_ID>_Report.docx",
    xlsx_path="cases/<CASE_ID>/output/final/<CASE_ID>_Model.xlsx",
    pptx_path="cases/<CASE_ID>/output/final/<CASE_ID>_Presentation.pptx",
    key_metrics=key_metrics
)

print(f"Consistency Score: {qa_result['consistency_score']}%")
```

### Bước 3: Lập Báo cáo Nghiệm thu (QA Sign-off Report)
Lưu báo cáo vào: `cases/<CASE_ID>/qa/qa-signoff-report.md`.
Báo cáo chỉ rõ:
- Tình trạng kiểm tra DOCX: PASS / FAIL
- Tình trạng kiểm tra XLSX: PASS / FAIL
- Tình trạng kiểm tra PPTX: PASS / FAIL
- Điểm nhất quán số liệu (Cross-format score): 100%
- Các khuyến nghị điều chỉnh nếu có.

## 3. Chốt chặn Phê duyệt (Approval Gate C — Deliverable Approval)
Trình báo cáo QA cho người dùng xem xét và phê duyệt trước khi nộp bài.
