# BÁO CÁO XÂY DỰNG CUSTOM SKILL 'MARKET_RESEARCH' TÍNH TOÁN TAM/SAM/SOM TẠI FPT CYBERGUARD

- **Mã bài tập:** `AI301_S04_BTVN_M1_BT1` (Session 04)
- **Hệ thống:** Business Development Research Agent (Google Antigravity)
- **Đơn vị:** FPT CyberGuard (Tập đoàn FPT)

---

## 1. Cấu trúc Custom Skill `market_research` (SKILL.md)

FPT CyberGuard chuẩn hóa Custom Skill `market_research` nhằm tự động hóa quy trình phân tích quy mô thị trường SOC-as-a-Service cho khối tài chính ngân hàng tại Việt Nam:

```yaml
name: market_research
description: Tự động tính toán quy mô thị trường TAM, SAM, SOM dịch vụ an ninh mạng theo dữ liệu ngành.
triggers: [on_bizdev_request]
inputs: {industry: str, total_entities: int, spending_per_unit: float, outsource_rate: float, target_share: float}
outputs: {market_report: object}
```

Tác tử tiếp nhận tham số đầu vào, nạp dữ liệu thống kê và kích hoạt script định lượng tự động.

## 2. Kịch bản Prompting định lượng quy mô thị trường

Kịch bản prompt chuẩn mẫu cấu hình cho Agent trên nền tảng Google Antigravity:

> *"Bạn là Chuyên viên Phân tích Thị trường tại FPT CyberGuard. Hãy sử dụng công cụ tính toán để lượng hóa 3 chỉ số TAM, SAM, SOM cho dịch vụ giám sát an toàn thông tin (SOC-as-a-Service) khối ngân hàng tại Việt Nam (39 ngân hàng, chi tiêu 15 tỷ/năm, tỷ lệ thuê ngoài 25%, thị phần mục tiêu 20%). Trả về kết quả song song bằng VNĐ và USD (tỷ giá 25.000 VNĐ/USD) kèm căn cứ pháp lý Thông tư 09/2020/TT-NHNN."*

Agent bóc tách dữ liệu, tự động tính toán độc lập và xuất bản báo cáo tóm tắt cho Ban Giám đốc.

## 3. Mã nguồn Python tính toán và Bảng số liệu định lượng

### Script tính toán quy mô thị trường (scripts/calc_tam_sam_som.py)
```python
def calc_market_size():
    fx, banks, spend, outsource, som_share = 25000, 39, 15e9, 0.25, 0.20
    tam = banks * spend
    sam = tam * outsource
    som = sam * som_share
    return {"TAM": (tam, tam / fx), "SAM": (sam, sam / fx), "SOM": (som, som / fx)}
```

### Bảng số liệu quy mô thị trường SOC-as-a-Service ngân hàng

| Chỉ số | Khái niệm định lượng | Giá trị (VNĐ) | Giá trị (USD) | Căn cứ xác định |
| :--- | :--- | :--- | :--- | :--- |
| **TAM** | Tổng chi tiêu an toàn thông tin 39 ngân hàng | **585,0 tỷ VNĐ** | **23,40 triệu USD** | 39 ngân hàng × 15 tỷ VNĐ/năm |
| **SAM** | Thị trường dịch vụ thuê ngoài SOC khả dụng | **146,25 tỷ VNĐ** | **5,85 triệu USD** | 25% ngân sách dành cho giám sát SOC |
| **SOM** | Thị phần mục tiêu FPT CyberGuard (2 năm) | **29,25 tỷ VNĐ** | **1,17 triệu USD** | 20% thị phần khối ngân hàng mục tiêu |

## 4. Tóm tắt phân tích thị trường và Căn cứ pháp lý
Thị trường giám sát an toàn thông tin ngành ngân hàng sở hữu động lực tăng trưởng bắt buộc theo **Thông tư 09/2020/TT-NHNN** (quy định bắt buộc thiết lập hoặc thuê ngoài trung tâm SOC giám sát 24/7). Ngoài 39 ngân hàng, thị trường mở rộng còn hơn 1.200 tổ chức tài chính chịu áp lực tuân thủ an toàn tương đương. Với SAM đạt 146,25 tỷ VNĐ (5,85 triệu USD), mục tiêu SOM 29,25 tỷ VNĐ (1,17 triệu USD) trong 2 năm hoàn toàn khả thi, tạo đòn bẩy vững chắc để FPT CyberGuard dẫn đầu thị trường.
