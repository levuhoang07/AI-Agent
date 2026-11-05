---
name: xlsx-specialist
description: >-
  Use this skill to build, manipulate, and audit Excel workbooks (.xlsx).
  Supports multi-sheet models (Raw Data, Calculations, Summary Dashboard),
  formula creation, data dictionary, charts, and independent calculation verification.
---

# XLSX Specialist Skill

Skill này điều khiển quá trình xây dựng mô hình bảng tính, tính toán công thức tài chính và đảm bảo chất lượng cho file Excel (`.xlsx`).

## 1. Trigger Conditions
- Người dùng yêu cầu: "Tạo bảng tính Excel", "Xây dựng mô hình tài chính", "Tính toán ROI bằng Excel", "Kiểm tra công thức Excel".

## 2. Quy trình Thực thi

### Bước 1: Chuẩn bị Dữ liệu và Công thức
- Tách bạch rõ 3 tầng dữ liệu:
  - Tầng 1: Dữ liệu nguồn thô (`Raw Data`).
  - Tầng 2: Bảng tính toán trung gian (`Calculations`) chứa các công thức (`=SUM`, `=AVERAGE`, `=IF`, `=VLOOKUP`).
  - Tầng 3: Bảng chỉ số tổng quan (`Summary Dashboard`) chứa KPI và Biểu đồ.

### Bước 2: Tạo Workbook bằng XLSX Helper
Sử dụng `shared/utilities/xlsx_helper.py`:
```python
from xlsx_helper import create_case_workbook

raw_data = [
    {"Tháng": "Tháng 1", "Chi phí Nhân sự": 50000000, "Chi phí AI Agent": 12000000, "Tiết kiệm": 38000000},
    {"Tháng": "Tháng 2", "Chi phí Nhân sự": 50000000, "Chi phí AI Agent": 10000000, "Tiết kiệm": 40000000},
    {"Tháng": "Tháng 3", "Chi phí Nhân sự": 50000000, "Chi phí AI Agent": 8500000, "Tiết kiệm": 41500000}
]

calculations = [
    {"Hạng mục": "Tổng chi phí tiết kiệm", "Công thức": "=SUM(C2:C4)", "Đơn vị": "VNĐ"},
    {"Hạng mục": "Tiết kiệm trung bình tháng", "Công thức": "=AVERAGE(C2:C4)", "Đơn vị": "VNĐ"}
]

kpi_summary = [
    {"metric": "Tỷ lệ Hoàn vốn (ROI)", "value": "245%", "unit": "%", "notes": "Tính trên chu kỳ 12 tháng"},
    {"metric": "Thời gian Hoàn vốn (Payback)", "value": 3.2, "unit": "Tháng", "notes": "Điểm hòa vốn sau khi khấu hao đầu tư"}
]

chart_info = {
    "type": "col",
    "title": "Biểu đồ So sánh Tiết kiệm Chi phí",
    "x_title": "Tháng",
    "y_title": "Chi phí (VNĐ)",
    "val_col": 4,
    "cat_col": 1
}

output_path = create_case_workbook(
    output_path="cases/<CASE_ID>/output/final/<CASE_ID>_Model.xlsx",
    raw_data=raw_data,
    calculations=calculations,
    kpi_summary=kpi_summary,
    chart_info=chart_info
)
```

### Bước 3: Độc lập Kiểm chứng Công thức (Independent Recalculation Audit)
- Kiểm tra tính hợp lệ của cú pháp công thức qua `inspect_and_verify_xlsx()`.
- Chạy đối chiếu toán học độc lập: Tính lại tổng bằng Python và so sánh với logic công thức để đảm bảo không bị nhầm lẫn giữa cached value và formula thật.

## 3. Tiêu chí Đạt chuẩn (Quality Gate PASS Criteria)
- Đầy đủ các sheet theo thiết kế (Raw Data, Calculations, Summary Dashboard).
- Không có lỗi công thức Excel (`#REF!`, `#DIV/0!`, `#VALUE!`).
- Biểu đồ tham chiếu đúng cột/dòng dữ liệu.
