---
name: docx-specialist
description: >-
  Use this skill to create, format, inspect, and validate high-quality academic and
  consulting Word documents (.docx). Handles cover pages, heading hierarchies,
  tables, header/footers, and template preservation using python-docx.
---

# DOCX Specialist Skill

Skill này tự động hóa quá trình soạn thảo và kiểm thử chất lượng báo cáo học thuật định dạng Microsoft Word (`.docx`).

## 1. Trigger Conditions
- Người dùng yêu cầu: "Tạo báo cáo Word", "Soạn thảo bài tập Word", "Kiểm tra định dạng file DOCX", "Áp dụng template Word".

## 2. Quy trình Thực thi

### Chế độ 1: Tạo mới Báo cáo Chuẩn mực (New Structured Report)
Sử dụng module helper `shared/utilities/docx_helper.py`:
```python
from docx_helper import create_report_document

sections = [
    {
        "level": 1,
        "heading": "1. Tổng quan Doanh nghiệp & Bài toán Kinh doanh",
        "paragraphs": [
            "Công ty Cổ phần Bán lẻ XYZ hiện đang đối mặt với bài toán tối ưu hóa quy trình...",
            "Việc ứng dụng AI Agent giúp rút ngắn 65% thời gian phản hồi khách hàng."
        ],
        "table": {
            "headers": ["Chỉ số", "Hiện trạng (AS-IS)", "Mục tiêu (TO-BE)"],
            "rows": [
                ["Thời gian phản hồi", "120 phút", "15 phút"],
                ["Chi phí vận hành", "500 triệu VNĐ/tháng", "320 triệu VNĐ/tháng"],
                ["Tỷ lệ lỗi dữ liệu", "8.5%", "0.5%"]
            ]
        }
    },
    {
        "level": 1,
        "heading": "2. Kiến trúc Giải pháp AI Agent",
        "paragraphs": [
            "Hệ thống triển khai mô hình Router Agent kết hợp bộ công cụ chuyên biệt..."
        ]
    }
]

output_path = create_report_document(
    output_path="cases/<CASE_ID>/output/final/<CASE_ID>_Report.docx",
    title="BÁO CÁO TƯ VẤN GIẢI PHÁP ỨNG DỤNG AI AGENT",
    subtitle="Môn học: Ứng dụng AI Agent trong công việc",
    author="Sinh viên thực hiện",
    sections=sections
)
```

### Chế độ 2: Bảo toàn Mẫu có sẵn (Template Preservation Mode)
Khi người dùng cung cấp template của trường/khoa:
1. Sao lưu template gốc tại `cases/<CASE_ID>/input/templates/`.
2. Phân tích styles, fonts, margins và placeholders có sẵn bằng `inspect_docx()`.
3. Nạp template và chèn các nội dung mới mà không làm thay đổi các thiết lập trang bìa hay header/footer mặc định.

### Bước 3: Kiểm định Chất lượng Tài liệu (Quality Gate Audit)
Chạy script kiểm thử chất lượng:
```python
from docx_helper import inspect_docx
audit = inspect_docx("cases/<CASE_ID>/output/final/<CASE_ID>_Report.docx")
assert audit["valid"] is True
assert audit["headings_count"] >= 2
assert audit["tables_count"] >= 1
```

## 3. Tiêu chí Đạt chuẩn (Quality Gate PASS Criteria)
- Tệp tin mở được bình thường, không bị lỗi XML corruption.
- Heading tuân thủ đúng phân cấp (Title -> Heading 1 -> Heading 2).
- Tiếng Việt hiển thị đúng dấu Unicode UTF-8, không lỗi mã font.
- Mọi bảng biểu có tiêu đề cột (Header row) và định dạng màu sắc trang nhã.
