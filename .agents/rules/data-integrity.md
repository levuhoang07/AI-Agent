---
description: "Data Integrity Rule: Prevents data fabrication, mandates metadata tagging for simulated/provided data, and requires verified calculations"
trigger: always_on
---

# RULE 03 — DATA INTEGRITY

## 1. Chống Bịa đặt Dữ liệu (Zero Hallucination Mandate)
- Tuyệt đối không tự ý bịa đặt số liệu thống kê, doanh thu, chi phí, quy mô nhân sự hoặc kết quả kinh doanh và coi đó là dữ liệu thực tế của doanh nghiệp.
- Mọi dữ liệu sử dụng trong phân tích và báo cáo phải được gắn nhãn nguồn gốc rõ ràng:
  - `[REAL_OBSERVED]`: Dữ liệu thực tế quan sát được từ đề bài hoặc tài liệu doanh nghiệp.
  - `[USER_PROVIDED]`: Dữ liệu do người dùng hoặc giảng viên cung cấp nhưng chưa qua kiểm định độc lập.
  - `[SIMULATED]`: Dữ liệu giả lập do Agent hoặc người dùng tạo ra phục vụ mục đích kiểm thử, mô phỏng hoặc minh họa.
  - `[ESTIMATED]`: Số liệu ước tính dựa trên mô hình kinh tế/kỹ thuật, bắt buộc phải nêu rõ công thức và cơ sở giả định.

## 2. Bảo toàn Dữ liệu Gốc (Raw Data Preservation)
- Trong các tệp tính toán Excel (`.xlsx`):
  - Sheet `Raw Data` chỉ chứa dữ liệu thô nguyên bản từ đề bài, không được can thiệp sửa đổi trực tiếp.
  - Toàn bộ thao tác làm sạch (data cleaning), lọc trùng lặp, chuẩn hóa định dạng hoặc xử lý missing values phải được thực hiện trên sheet `Cleaned Data` hoặc `Transformed Data`.
  - Mọi bước biến đổi dữ liệu phải được ghi lại trong `Transformation Log` hoặc Data Dictionary.

## 3. Kiểm định Độc lập Công thức Tính toán (Verified Calculations)
- Không được nhầm lẫn giữa công thức tính (`Formula`) và giá trị tĩnh được lưu đệm (`Cached Value`).
- Mọi chỉ số KPI tài chính hoặc vận hành (ROI, NPV, CIR, Churn Rate, Throughput) phải có công thức toán học minh bạch, được kiểm tra đối chiếu bằng Python script hoặc script thẩm định độc lập trước khi đưa vào báo cáo Word hoặc Slide.
