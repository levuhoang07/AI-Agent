---
name: data-analysis
description: >-
  Use this skill to perform exploratory data analysis (EDA), data cleaning,
  statistical profiling, KPI calculations, and chart preparation using Python and Pandas.
---

# Data Analysis Skill

Skill này điều khiển quy trình phân tích định lượng (Quantitative Analysis) bằng Python (`pandas`, `numpy`) trên các tập dữ liệu bài tập trong `cases/<CASE_ID>/input/datasets/`.

## 1. Trigger Conditions
- Người dùng cung cấp tập dữ liệu (CSV, XLSX, JSON).
- Cần tính toán số liệu tài chính, phân bố khách hàng, hiệu suất vận hành, tỷ lệ lỗi.

## 2. Quy trình Thực thi

### Bước 1: Khám phá Hồ sơ Dữ liệu (Data Profiling & EDA)
- Đọc dữ liệu bằng Pandas:
  ```python
  import pandas as pd
  df = pd.read_csv("cases/<CASE_ID>/input/datasets/sales_data.csv")
  print(df.info())
  print(df.describe())
  ```
- Kiểm tra số lượng bản ghi (rows), số lượng cột (columns), kiểu dữ liệu (dtypes).
- Phát hiện các giá trị khuyết thiếu (missing values/NaNs), bản ghi trùng lặp (duplicates), và giá trị dị biệt (outliers).

### Bước 2: Làm sạch & Chuẩn hóa Dữ liệu (Data Cleaning)
- Xử lý missing values theo nguyên tắc nghiệp vụ (thay thế bằng median/mean hoặc loại bỏ có giải trình).
- Chuẩn hóa định dạng ngày tháng, số tiền tệ, mã phân loại.
- Ghi lại toàn bộ thao tác trong `cases/<CASE_ID>/analysis/data-transformation-log.md`.

### Bước 3: Tính toán Chỉ số & Phân tích Tương quan
- Tính toán các chỉ số thống kê mô tả: Tổng, Trung bình, Trung vị, Độ lệch chuẩn.
- Gom nhóm dữ liệu (groupby) theo phòng ban, sản phẩm, kênh phân phối.
- Tính toán các chỉ số KPI tài chính: Doanh thu, Chi phí, Tỷ suất lợi nhuận gộp, ROI.

### Bước 4: Xuất Dữ liệu Sạch sang Excel Helper
- Chuyển kết quả phân tích sang dạng cấu trúc dict/list để `xlsx_helper.py` kết xuất thành tệp Excel hoàn chỉnh có kèm công thức và đồ thị.

## 3. Đầu ra (Deliverables)
- Script phân tích: `cases/<CASE_ID>/analysis/eda_analysis.py` (nếu cần).
- Báo cáo kết quả phân tích: `cases/<CASE_ID>/analysis/data-insights.md`.

