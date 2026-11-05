---
name: pptx-specialist
description: >-
  Use this skill to design, produce, and validate PowerPoint presentations (.pptx).
  Handles 16:9 widescreen slides, slide masters, structured content hierarchy,
  tables, visual consistency, and text overflow prevention.
---

# PPTX Specialist Skill

Skill này điều khiển quá trình xây dựng bài thuyết trình bảo vệ phương án giải pháp bằng Microsoft PowerPoint (`.pptx`).

## 1. Trigger Conditions
- Người dùng yêu cầu: "Tạo slide thuyết trình", "Soạn PowerPoint báo cáo", "Kiểm tra slide PPTX", "Áp dụng template slide".

## 2. Quy trình Thực thi

### Bước 1: Xây dựng Storyboard Thuyết trình (3-5 slides cốt lõi)
1. **Slide 1 — Tiêu đề (Title Slide):** Tên đề tài, môn học, sinh viên thực hiện, ngày báo cáo.
2. **Slide 2 — Bài toán & Phân tích Hiện trạng (Problem & AS-IS):** Nỗi đau của doanh nghiệp, tổn thất chi phí, nguyên nhân gốc rễ.
3. **Slide 3 — Kiến trúc Giải pháp AI Agent (Solution Architecture):** Sơ đồ khối các Agent, luồng xử lý dữ liệu, kiểm soát an toàn con người (Human-in-the-Loop).
4. **Slide 4 — Hiệu quả Kinh tế & Lộ trình Triển khai (ROI & Roadmap):** Thời gian hoàn vốn, chi phí đầu tư, các mốc triển khai (Phases).

### Bước 2: Tạo Presentation bằng PPTX Helper
Sử dụng `shared/utilities/pptx_helper.py`:
```python
from pptx_helper import create_presentation

slides_data = [
    {
        "slide_title": "1. Hiện trạng Vận hành & Nỗi đau Doanh nghiệp",
        "bullets": [
            "Thời gian xử lý trung bình mỗi yêu cầu khách hàng: 120 phút (thủ công 100%).",
            "Tỷ lệ thất thoát dữ liệu và sai sót nhập liệu lên tới 8.5%.",
            "Chi phí làm thêm giờ (overtime) của nhân viên tiêu tốn hơn 150 triệu VNĐ/quý."
        ]
    },
    {
        "slide_title": "2. Kiến trúc Giải pháp AI Agent & Hiệu quả Dự kiến",
        "bullets": [
            "Mô hình ReAct Agent tự động phân loại, trích xuất dữ liệu và soạn thảo phản hồi.",
            "Điểm kiểm soát Human-in-the-Loop: Chỉ phê duyệt các giao dịch > 10 triệu VNĐ.",
            "Hiệu quả dự kiến: Giảm 65% thời gian phản hồi, ROI đạt 245% trong năm đầu."
        ],
        "table": {
            "headers": ["Chỉ số", "Trước triển khai", "Sau triển khai"],
            "rows": [
                ["Thời gian phản hồi", "120 phút", "15 phút"],
                ["Chi phí vận hành", "500 tr VNĐ", "320 tr VNĐ"]
            ]
        }
    }
]

output_path = create_presentation(
    output_path="cases/<CASE_ID>/output/final/<CASE_ID>_Presentation.pptx",
    title="GIẢI PHÁP ỨNG DỤNG AI AGENT TỰ ĐỘNG HÓA",
    subtitle="Đề án Tối ưu hóa Vận hành Doanh nghiệp",
    author="Sinh viên thực hiện",
    slides_data=slides_data
)
```

### Bước 3: Kiểm tra Trực quan & Chống Tràn chữ (Visual QA Audit)
Chạy script kiểm tra:
```python
from pptx_helper import inspect_pptx
audit = inspect_pptx("cases/<CASE_ID>/output/final/<CASE_ID>_Presentation.pptx")
assert audit["valid"] is True
assert audit["slide_count"] >= 3
assert audit["overflow_warnings_count"] == 0 # Không có shape nào bị quá tải chữ
```

## 3. Tiêu chí Đạt chuẩn (Quality Gate PASS Criteria)
- Đầy đủ số lượng slide tối thiểu (ít nhất 3 slide).
- Slide hiển thị ở tỷ lệ chuẩn màn hình rộng 16:9.
- Không có lỗi tràn văn bản (Text Overflow: không vượt quá 600 ký tự trong một textbox).
- Bảng màu đồng nhất, font chữ chuyên nghiệp, không lỗi dấu tiếng Việt.
