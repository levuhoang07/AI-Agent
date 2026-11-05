---
name: business-analysis
description: >-
  Use this skill to perform structured business analysis: AS-IS/TO-BE process mapping,
  BPMN diagrams, KPI trees, SWOT/PESTEL, root cause analysis (5 Whys, Ishikawa),
  and functional/non-functional requirement specifications.
---

# Business Analysis Skill

Skill này cung cấp các khung phân tích nghiệp vụ chuẩn mực (Business Analysis Frameworks) nhằm làm rõ hiện trạng và đề xuất quy trình tương lai cho doanh nghiệp trong case study.

## 1. Trigger Conditions
- Phân tích bối cảnh kinh doanh, xác định vấn đề, vẽ quy trình AS-IS/TO-BE hoặc lập yêu cầu hệ thống.
- Kích hoạt khi thực hiện Task phân tích nghiệp vụ trong `cases/<CASE_ID>/analysis/`.

## 2. Các Khung Phân tích Cốt lõi (Core Frameworks)

### 1. Phân tích Nguyên nhân Gốc rễ (Root Cause Analysis - RCA)
- **Fishbone (Ishikawa Diagram) & 5 Whys:** Phân tích nguyên nhân theo 5M1E (Man, Machine, Material, Method, Measurement, Environment).
- Phân định rõ đâu là hiện tượng bề mặt (Symptoms) và đâu là điểm nghẽn gốc rễ (Root Causes).

### 2. Mô hình hóa Quy trình AS-IS vs TO-BE
- **Quy trình Hiện trạng (AS-IS):** Chỉ ra các bước thủ công, thời gian chờ (latency), tỷ lệ lỗi và điểm tắc nghẽn.
- **Quy trình Tương lai (TO-BE):** Tích hợp AI Agent vào các khâu tự động hóa, quy định rõ điểm can thiệp của con người (Human-in-the-Loop).
- Mô hình hóa bằng cú pháp Mermaid BPMN trong file Markdown:
  ```mermaid
  flowchart TD
    A[Tiếp nhận yêu cầu] --> B{AI Agent phân loại}
    B -->|Tự động| C[Xử lý & Tạo tài liệu]
    B -->|Ngoại lệ| D[Chuyển Chuyên viên duyệt]
    C --> E[Bàn giao kết quả]
    D --> E
  ```

### 3. Cây Chỉ số Hiệu năng (KPI Tree)
- Phân rã mục tiêu chiến lược (ví dụ: Tăng lợi nhuận 15%) thành các chỉ số vận hành cụ thể:
  - Giảm thời gian xử lý hồ sơ (Cycle Time).
  - Giảm chi phí nhân sự trên mỗi giao dịch (Cost per Transaction).
  - Tăng tỷ lệ giải quyết lần đầu (First Contact Resolution).

### 4. Bảng Đặc tả Yêu cầu (Requirements Traceability Matrix)
- Yêu cầu kinh doanh (Business Requirements).
- Yêu cầu chức năng (Functional Requirements).
- Yêu cầu phi chức năng (Non-Functional Requirements: Độ trễ, Bảo mật, Sẵn sàng).

## 3. Đầu ra (Deliverables)
- Lưu trữ tài liệu phân tích tại: `cases/<CASE_ID>/analysis/business-analysis-spec.md`.

