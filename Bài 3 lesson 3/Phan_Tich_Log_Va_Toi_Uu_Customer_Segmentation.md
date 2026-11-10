# BÁO CÁO PHÂN TÍCH NHẬT KÝ VÀ TỐI ƯU HÓA CUSTOMER SEGMENTATION TẠI FPT SMARTBIZ

- **Mã bài tập:** `AI301_S03_BTVN_M2_BT1` (Session 03)
- **Hệ thống:** Sales Lead Qualification Agent (Google Antigravity)
- **Tác tử:** `customer_segmentation` Skill | **Đơn vị:** FPT SmartBiz

---

## 1. Bóc tách lỗi logic trong nhật ký thực thi (Execution Trace)

Tuần đầu chạy thử nghiệm, tác tử phân loại nhầm khách hàng cá nhân thành Hot Lead tại bản ghi `LD-8812`. Nhật ký thực thi:

```json
{
  "lead_id": "LD-8812",
  "budget": 500000000,
  "tax_id": "8012345678",
  "headcount": 1,
  "scores": {"B": 30, "A": 30, "N": 10, "T": 10},
  "score": 80,
  "tier": "Hot Lead"
}
```

### Nguyên nhân gốc rễ (Root Cause):
1. **Thiên vị ngân sách (Budget Bias):** Agent tự động cộng 30 điểm tối đa cho ngân sách 500 triệu VNĐ mà không đối chiếu loại hình tổ chức.
2. **Thiếu kiểm tra tư cách pháp nhân:** Người khai điền chức danh quản lý, Agent chấm thẩm quyền 30 điểm nhưng bỏ qua mã số thuế cá nhân và quy mô 1 nhân sự.
3. **Hệ quả nghiệp vụ:** Bàn giao nhầm cá nhân cho chuyên viên tư vấn ERP doanh nghiệp, gây lãng phí 80% thời gian tiếp cận.

## 2. Tinh chỉnh điều kiện tiên quyết (Prerequisite Conditions)

Bổ sung bộ lọc pháp nhân doanh nghiệp (Corporate Entity Gatekeeper) vào Skill `customer_segmentation`:

```python
def qualify_lead(lead):
    is_corp = lead.get("is_corp", False) and (lead.get("headcount", 0) >= 5)
    raw = sum(lead.get("bant", {}).values())
    s = raw if is_corp else min(raw, 45)
    return s, "Hot" if s >= 75 else ("Warm" if s >= 50 else "Cold")
```

### Quy tắc chốt chặn (Hard Constraint):
Nếu không phải pháp nhân doanh nghiệp có mã số thuế công ty hợp lệ hoặc quy mô dưới 5 người, điểm số tối đa bị giới hạn không quá 45 điểm và tự động phân loại thành Cold Lead để chuyển sang luồng email nuôi dưỡng tự động.

## 3. Kiểm thử hồi quy (Regression Testing) trên 10 Leads mẫu

Chạy lại bộ 10 Leads kiểm thử nhằm xác minh việc sửa lỗi cá nhân và bảo toàn kết quả khách hàng doanh nghiệp:

| Mã Lead | Loại hình | Ngân sách | Pháp nhân | Điểm cũ | Điểm mới | Kết luận |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **LD-8812** | Cá nhân | 500tr | 1 ng (MST CN) | 80 (Hot) | **45 (Cold)** | Đã sửa |
| **LD-8813** | Cá nhân | 300tr | 1 ng (MST CN) | 75 (Hot) | **45 (Cold)** | Đã sửa |
| **LD-8814** | Thép An Phát | 400tr | 50 ng (MST Cty) | 90 (Hot) | **90 (Hot)** | Chuẩn |
| **LD-8815** | May Hòa Bình | 150tr | 30 ng (MST Cty) | 65 (Warm) | **65 (Warm)** | Chuẩn |
| **LD-8816** | Vận tải HP | 30tr | 10 ng (MST Cty) | 25 (Cold) | **25 (Cold)** | Chuẩn |
| **LD-8817** | Hộ kinh doanh | 100tr | 2 ng (MST CN) | 55 (Warm) | **45 (Cold)** | Đã sửa |
| **LD-8818** | Tập đoàn BĐS | 800tr | 200 ng (MST Cty) | 100 (Hot) | **100 (Hot)** | Chuẩn |
| **LD-8819** | Bán lẻ Tiến Phát | 80tr | 20 ng (MST Cty) | 60 (Warm) | **60 (Warm)** | Chuẩn |
| **LD-8820** | Sinh viên | 50tr | 1 ng (MST CN) | 35 (Cold) | **35 (Cold)** | Chuẩn |
| **LD-8821** | TCT Công nghệ | 1.5 tỷ | 500 ng (MST Cty) | 100 (Hot) | **100 (Hot)** | Chuẩn |

## 4. Đánh giá tính hợp lý
Kết quả thử nghiệm đạt tỷ lệ khắc phục lỗi 100% đối với khách hàng cá nhân và bảo toàn 100% khách hàng doanh nghiệp chuẩn. Rào cản điều kiện tiên quyết giúp tối ưu hóa nguồn lực bán hàng B2B của FPT SmartBiz, ngăn ngừa lãng phí thời gian tư vấn giải pháp ERP và nâng cao hiệu quả vận hành tự động của Agent.
