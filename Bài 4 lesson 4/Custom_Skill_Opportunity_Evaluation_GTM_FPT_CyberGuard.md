# ĐỀ ÁN XÂY DỰNG CUSTOM SKILL 'OPPORTUNITY_EVALUATION' VÀ CHIẾN LƯỢC GTM TẠI FPT CYBERGUARD

- **Mã bài tập:** `AI301_S04_BTVN_M3_BT1` (Session 04)
- **Hệ thống:** Business Development Research Agent (Google Antigravity)
- **Custom Skill:** `opportunity_evaluation` | **Đơn vị:** FPT CyberGuard

---

## 1. Phát triển script Python tính toán Điểm số Cơ hội (Opportunity Score)

Để tối ưu hóa nguồn lực kinh doanh hữu hạn, FPT CyberGuard xây dựng thuật toán chấm điểm đa tiêu chí (Multi-Criteria Decision Matrix) dựa trên 4 trọng số cốt lõi: Quy mô doanh thu (0.35), Mức độ cấp bách pháp lý (0.35), Rào cản gia nhập (0.15) và Mức độ phù hợp năng lực FPT (0.15).

### Script Python tính điểm xếp hạng (scripts/evaluate_opportunity.py)
```python
def rank_opportunities():
    weights = {"rev": 0.35, "law": 0.35, "barrier": 0.15, "fit": 0.15}
    segments = {
        "Khối Ngân hàng": {"rev": 9.5, "law": 10.0, "barrier": 7.5, "fit": 9.0},
        "Khối Bệnh viện": {"rev": 6.5, "law": 7.0, "barrier": 8.0, "fit": 7.5},
        "Khối Bán lẻ": {"rev": 7.5, "law": 6.0, "barrier": 7.0, "fit": 8.0}
    }
    results = {}
    for name, s in segments.items():
        score = sum(s[k] * weights[k] for k in weights)
        results[name] = round(score, 3)
    return sorted(results.items(), key=lambda x: x[1], reverse=True)
```

### Bảng kết quả xếp hạng cơ hội thâm nhập thị trường

| Tiêu chí đánh giá (Trọng số) | Khối Ngân hàng | Khối Bệnh viện | Khối Bán lẻ |
| :--- | :--- | :--- | :--- |
| **Doanh thu tiềm năng (0.35)** | 9.5 (SAM 146,25 tỷ) | 6.5 (Ngân sách hạn chế) | 7.5 (Quy mô chuỗi lớn) |
| **Cấp bách pháp lý (0.35)** | 10.0 (Thông tư 09/NHNN) | 7.0 (Nghị định 13) | 6.0 (Chưa bắt buộc SOC) |
| **Rào cản gia nhập (0.15)** | 7.5 (Cạnh tranh viễn thông) | 8.0 (Thị trường ngách mở) | 7.0 (Đối thủ giải pháp ngoại) |
| **Phù hợp năng lực FPT (0.15)** | 9.0 (Am hiểu Core Banking) | 7.5 (FPT.eHospital) | 8.0 (FPT Retail) |
| **Tổng điểm cơ hội (Thang 10)** | **9.30 (Hạng 1 - Quán quân)** | **7.05 (Hạng 2)** | **6.98 (Hạng 3)** |

## 2. Đóng gói Custom Skill `opportunity_evaluation` hoàn chỉnh

Skill được chuẩn hóa cấu trúc để tái sử dụng trong toàn bộ quy trình BizDev của FPT:

```yaml
name: opportunity_evaluation
description: Tự động phân tích, chấm điểm ma trận cơ hội thị trường và đề xuất chiến lược GTM.
triggers: [on_market_segmented]
inputs: {criteria_weights: dict, sector_metrics: dict}
outputs: {ranked_matrix: list, gtm_recommendation: object}
```

### Quy trình vận hành chuẩn (SOP) và Tiêu chuẩn nghiệm thu:
1. **Bước 1 (Thu thập dữ liệu):** Agent trích xuất dữ liệu dung lượng SAM, văn bản pháp quy và hồ sơ năng lực ngành từ kho tri thức nội bộ.
2. **Bước 2 (Chấm điểm tự động):** Kích hoạt script tính toán, đối chiếu với ngưỡng chấp thuận (Acceptance Criteria: Phân khúc được chọn phải đạt điểm tổng hợp $\ge 8.0$ và điểm pháp lý $\ge 8.5$).
3. **Bước 3 (Xuất bản lộ trình GTM):** Tự động sinh báo cáo hành động chi tiết cho phân khúc chiến thắng.

## 3. Chiến lược Go-To-Market (GTM) 3 bước cho Khối Ngân hàng

Với điểm số quán quân tuyệt đối 9.30 điểm, Khối Ngân hàng là thị trường mục tiêu số 1 cần tập trung toàn lực triển khai theo lộ trình 3 bước:

### Bước 1: Tiếp cận có chủ đích & Chạy thử nghiệm PoC (Tháng 1 – 3)
- **Hành động:** Tập trung tiếp cận nhóm 10 ngân hàng TMCP vừa và nhỏ đang chịu áp lực thanh tra Thông tư 09/2020/TT-NHNN nhưng thiếu nhân sự an ninh mạng nội bộ.
- **Chiến thuật:** Cung cấp gói dịch vụ "Đánh giá lỗ hổng an toàn thông tin độc lập miễn phí" và chương trình chạy thử nghiệm SOC 30 ngày (PoC miễn phí).
- **Mục tiêu:** Chuyển đổi tối thiểu 3 ngân hàng ký kết hợp đồng dịch vụ chính thức.

### Bước 2: Tích hợp sâu hệ thống & Đóng gói giải pháp Banking SOC (Tháng 4 – 8)
- **Hành động:** Triển khai vận hành thực tế cho các khách hàng tiên phong, kết nối trực tiếp hệ thống giám sát FPT CyberGuard vào nền tảng Core Banking (Temenos, Finacle).
- **Chiến thuật:** Đóng gói quy trình giám sát đặc thù ngành ngân hàng thành bộ giải pháp chuẩn "FPT Banking SOC Express" với thời gian kích hoạt dưới 4 tuần.
- **Mục tiêu:** Nâng tổng số khách hàng ngân hàng lên 8 đơn vị, tạo doanh thu định kỳ 800 triệu VNĐ/tháng.

### Bước 3: Mở rộng diện rộng & Thống lĩnh thị trường (Tháng 9 – 24)
- **Hành động:** Phối hợp cùng Hiệp hội Ngân hàng Việt Nam (VNBA) tổ chức chuỗi hội thảo chuyên đề về an toàn thông tin tài chính số.
- **Chiến thuật:** Công bố Whitepaper báo cáo hiệu quả thực tế (giảm 60% cảnh báo giả, tiết kiệm 35% chi phí vận hành), triển khai bán chéo qua mạng lưới FPT IS.
- **Mục tiêu:** Chiếm lĩnh 20% thị phần khối ngân hàng vừa và nhỏ, mang lại doanh thu 29,25 tỷ VNĐ/năm và xác lập vị thế dẫn đầu thị trường.
