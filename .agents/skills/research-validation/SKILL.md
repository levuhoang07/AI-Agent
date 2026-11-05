---
name: research-validation
description: >-
  Use this skill to collect academic literature, industry benchmarks, market data,
  validate factual claims, and enforce the 4-tier evidence taxonomy (Fact, Assumption,
  Inference, Recommendation).
---

# Research Validation Skill

Skill này đảm bảo tính xác thực, độ tin cậy và chuẩn mực học thuật cho mọi dữ liệu nghiên cứu thị trường và cơ sở lý thuyết trong case study.

## 1. Trigger Conditions
- Người dùng yêu cầu tìm kiếm số liệu ngành, đối chiếu đối thủ cạnh tranh, hoặc kiểm chứng một nhận định.
- Trước khi đưa các số liệu thị trường vào báo cáo Word hoặc Slide.

## 2. Quy trình Thực thi

### Bước 1: Thu thập Dữ liệu & Bằng chứng
- Tìm kiếm từ các nguồn uy tín: Báo cáo của các công ty tư vấn lớn (McKinsey, BCG, Gartner), báo cáo thống kê chính phủ (GSO), báo cáo tài chính kiểm toán hoặc tài liệu học thuật.
- Ghi lại metadata đầy đủ: Tên báo cáo, tổ chức công bố, năm phát hành, đường dẫn truy cập (nếu có).

### Bước 2: Phân loại Bằng chứng theo 4 Cấp (Evidence Tagging)
Gán nhãn bắt buộc cho mọi luận điểm:
- `[FACT]`: Báo cáo chỉ số e-Conomy SEA 2024 của Google/Temasek chỉ ra quy mô kinh tế số Việt Nam đạt 36 tỷ USD.
- `[ASSUMPTION]`: Giả định doanh nghiệp áp dụng giải pháp AI sẽ giảm được 30% thời gian xử lý thủ công trong năm đầu tiên.
- `[INFERENCE]`: Doanh nghiệp tiết kiệm được khoảng 450 triệu VNĐ chi phí làm thêm giờ hàng năm.
- `[RECOMMENDATION]`: Triển khai hệ thống AI Agent phân loại tự động tại phòng Chăm sóc khách hàng trong Quý 1.

### Bước 3: Độc lập Kiểm chứng (Fact-Checking)
- Kiểm tra chéo giữa ít nhất 2 nguồn dữ liệu độc lập khi gặp các số liệu chênh lệch lớn.
- Tuyệt đối cấm tạo citation giả mạo hoặc gán ghép số liệu sai nguồn.

## 3. Đầu ra (Deliverables)
- Lưu trữ tài liệu nghiên cứu tại: `cases/<CASE_ID>/research/research-synthesis.md`.
