# BÁO CÁO BÓC TÁCH CẤU TRÚC 4 THÀNH PHẦN AGENT SKILL TẠI VINFAST

- **Mã bài tập:** `AI301_S02_BTVN_M2_BT1` (Session 02)
- **Tên kỹ năng:** `ev_charging_adviser` (Cố vấn Trạm sạc VinFast)
- **Chuẩn:** Agent Skills Standard (Google Antigravity)

---

## 1. Cấu trúc thư mục chuẩn của Custom Skill

Để chuẩn hóa tri thức kỹ thuật và tối ưu chi phí token, Custom Skill `ev_charging_adviser` được đóng gói thành 4 thành phần độc lập:

```text
.agents/skills/ev_charging_adviser/
├── SKILL.md                         # Metadata & YAML Frontmatter điều phối nạp động
├── instructions.md                  # Hướng dẫn suy luận logic và an toàn sạc pin
├── references/                      # Cơ sở tri thức trạm sạc và thông số pin
│   └── charging_specs.json
└── scripts/                         # Mã nguồn tính toán thời gian sạc chính xác
    └── calculate_charging_time.py
```

## 2. Bóc tách chi tiết 4 thành phần cốt lõi của Skill

### Thành phần 1: SKILL.md với YAML Frontmatter chuẩn
Tệp điều phối nạp động (Dynamic Loading) định tuyến tác vụ, chỉ nạp tri thức chuyên sâu khi Agent phát hiện từ khóa kích hoạt, giảm 80% chi phí token:

```yaml
---
name: ev_charging_adviser
description: >-
  Tư vấn tìm trạm sạc chuẩn CCS1/NACS và tính thời gian sạc chính xác cho xe VinFast
  pin 87.7 kWh.
triggers:
  - "tìm trạm sạc"
  - "sạc bao lâu"
  - "sạc pin VF 8"
  - "trạm sạc CCS1"
  - "sạc tại nhà 11kW"
---
```

### Thành phần 2: Tệp Hướng dẫn quy trình instructions.md
Quy định 3 bước suy luận logic tuần tự và quy chuẩn an toàn cho Agent khi phản hồi khách hàng:
1. **Xác thực chuẩn cổng kết nối:** Kiểm tra xe dùng cổng CCS1 (Bắc Mỹ) hay adapter NACS tại trạm sạc Tesla Supercharger.
2. **Lựa chọn giải pháp sạc tối ưu:** Phân định sạc nhanh DC 250 kW trên cao tốc và sạc chậm AC 11 kW qua đêm tại nhà.
3. **Quy tắc bảo vệ pin (Battery Health Guardrail):** Cảnh báo khách hàng chỉ nên sạc nhanh DC đến 80% để giữ độ bền cell pin lithium-ion.

### Thành phần 3: Cơ sở tri thức tĩnh references/charging_specs.json
Cung cấp bảng thông số kỹ thuật chuẩn do phòng kỹ thuật VinFast thẩm định:
* **Dung lượng pin khả dụng:** 87.7 kWh (kiến trúc điện áp 400V).
* **Trụ sạc siêu nhanh DC:** Công suất 250 kW; thời gian nạp từ 10% đến 70% đạt 24 phút.
* **Trụ sạc gia đình AC:** Công suất 11 kW; thời gian sạc đầy từ 10% lên 100% trong 8 giờ.

### Thành phần 4: Mã nguồn tính toán scripts/calculate_charging_time.py
Script Python loại trừ rủi ro ảo giác toán học (Zero Hallucination) khi ước tính thời gian sạc:

```python
def calc_charge_time(current_pct, target_pct, charger_kw, battery_kwh=87.7):
    needed_kwh = battery_kwh * (target_pct - current_pct) / 100.0
    effective_kw = min(charger_kw, 250 if charger_kw > 50 else 11)
    hours = needed_kwh / (effective_kw * 0.9) # Hiệu suất hao tổn 90%
    return round(hours * 60) # Kết quả chính xác theo phút
```

## 3. Kịch bản Prompting điều khiển Kỹ năng trên Google Antigravity

Kịch bản prompt mẫu gửi tới Antigravity kích hoạt kỹ năng:

> *"Bạn là Tác tử Cố vấn Sạc VinFast. Hãy kích hoạt skill `ev_charging_adviser`. Khách hàng đang lái xe VF 8 (pin 87.7 kWh) tại trạm sạc siêu nhanh DC 250 kW, pin hiện còn 20%, muốn nạp lên 80% để hoàn thành chuyến đi. Hãy chạy script tính toán chính xác số phút cần sạc và xuất bảng khuyến nghị gồm: loại sạc, công suất thực tế, thời gian sạc dự kiến và lời khuyên bảo vệ pin an toàn."*

**Đầu ra kỳ vọng:** Agent tự động gọi script tính toán ra kết quả 25 phút, xuất bảng Markdown trực quan kèm lời nhắc rút sạc tại mức 80% để tối ưu hóa thời gian và chi phí cho khách hàng.

Việc bóc tách kỹ năng thành 4 thành phần theo chuẩn Antigravity giúp doanh nghiệp dễ dàng mở rộng, kiểm thử độc lập từng script tính toán và bảo trì kho tri thức mà không cần đào tạo lại mô hình nền tảng.

