# ĐỀ ÁN THIẾT KẾ: CẤU HÌNH CƠ CHẾ ĐIỂM DỪNG PHÊ DUYỆT (APPROVAL BREAKPOINT) TRONG MÔ HÌNH HITL TẠI VIETTEL SOLUTIONS

- **Mã bài tập:** `AI301_S08_BTVN_M3_BT1`
- **Học phần:** AI301 - AI Agent (Session 08: Multi-Agent & System Optimization)
- **Đơn vị:** Tổng công ty Giải pháp Doanh nghiệp Viettel (Viettel Solutions)
- **Gói thầu:** Hạ tầng Viễn thông & Đám mây Doanh nghiệp (50 tỷ VNĐ)

---

## 1. Bối cảnh & Phân vùng Kiểm soát Nghiệp vụ (Dual-Zone Governance)

Tại Viettel Solutions, các gói thầu hạ tầng viễn thông và CNTT quy mô lớn đòi hỏi sự linh hoạt giá nhưng gắn liền trách nhiệm tài chính nghiêm ngặt. Để dung hòa giữa tự động hóa và quản trị rủi ro, hệ thống Multi-Agent áp dụng phân vùng kiểm soát 2 cấp độ:

- **Vùng Xanh (Green Zone - Tự trị):** Gồm nghiên cứu thị trường, trích xuất hồ sơ mời thầu và lập dự toán nội bộ. Research Agent và Finance Agent được tự chủ vận hành, gọi công cụ và xử lý dữ liệu mà không cần con người phê duyệt từng bước.
- **Vùng Đỏ (Red Zone - Bắt buộc duyệt):** Gồm cam kết giá chào thầu, chiết khấu thương mại và phát hành hồ sơ tài chính. Mọi hành động tại đây bắt buộc kích hoạt Điểm dừng Phê duyệt (**Approval Breakpoints**) để Giám đốc Khách hàng Doanh nghiệp thẩm định qua mô hình Con người trong Vòng lặp (**Human-in-the-Loop - HITL**).

---

## 2. Nhiệm vụ 1: Thiết lập Cấu hình Điểm dừng Phê duyệt trong Orchestrator

Trên Google Antigravity, Orchestrator quản lý máy trạng thái luồng thầu. Khi Proposal Agent đưa mức chiết khấu 16% (vượt ngưỡng an toàn 10%), Orchestrator chuyển sang trạng thái tạm dừng `APPROVAL_PENDING`:

```python
# Cấu hình Trigger Rule cho Approval Breakpoint tại Orchestrator
BREAKPOINT_RULES = {
    "max_discount_rate": 0.10,        # Chiết khấu >= 10% kích hoạt Vùng Đỏ
    "min_contract_value": 10e9        # Hợp đồng >= 10 tỷ VNĐ bắt buộc duyệt
}

def check_approval_breakpoint(proposal: dict) -> str:
    discount = proposal.get("discount_rate", 0.0)
    value = proposal.get("total_value", 0)
    if discount >= BREAKPOINT_RULES["max_discount_rate"] or value >= BREAKPOINT_RULES["min_contract_value"]:
        return "TRIGGER_APPROVAL_BREAKPOINT"
    return "AUTO_PROCEED"
```

Khi kích hoạt breakpoint, Orchestrator gửi cờ `RequestFeedback: true` qua Antigravity Artifact, tạm dừng quyền xuất hồ sơ của Proposal Agent để chờ phê duyệt.

---

## 3. Nhiệm vụ 2: Thiết kế Giao diện Phiếu Trình Duyệt Thầu (Bid Approval Artifact)

Giao diện Phiếu Trình Duyệt Thầu hiển thị dưới dạng Artifact tương tác, tóm lược các thông số then chốt:

| Chỉ số Thẩm định | Giá trị Cụ thể | Đánh giá & Rủi ro |
| :--- | :--- | :--- |
| **Tên dự án** | Hạ tầng Viễn thông & Đám mây Doanh nghiệp | Mã hồ sơ: `VT-BID-2026-CLOUD50` |
| **Giá trị ban đầu** | 50.000.000.000 VNĐ (50 tỷ VNĐ) | Dự toán định mức Viettel Solutions |
| **Tỷ lệ chiết khấu** | **16.0%** (Giảm 8.000.000.000 VNĐ) | Đề xuất tối đa từ Proposal Agent |
| **Giá sau giảm** | **42.000.000.000 VNĐ** (42 tỷ VNĐ) | Mức giá cạnh tranh trực tiếp |
| **Biên lợi nhuận gộp** | Giảm từ 28.5% xuống **14.2%** | Cận kề ngưỡng an toàn (Sàn: 12.0%) |

### Phân tích Rủi ro & Lợi thế Cạnh tranh:
1. **Rủi ro Tài chính:** Mức giảm 16% khiến biên lợi nhuận gộp còn 14.2%, tạo rủi ro lớn nếu chi phí thiết bị mạng biến động tỷ giá, kèm rủi ro phạt tiến độ SLA 0.5%/ngày.
2. **Lợi thế Cạnh tranh:** Mức giá 42 tỷ VNĐ thấp hơn 7.5% so với đối thủ VNPT/FPT. Viettel Solutions làm chủ 100% trục cáp quang và hạ tầng Cloud đạt chuẩn an toàn thông tin.

---

## 4. Nhiệm vụ 3: Giả lập Quy trình Phản hồi Tương tác (Interactive Guidance)

Cơ chế HITL của Antigravity cho phép người quản lý hướng dẫn tác tử điều chỉnh trực tiếp:

- **Bước 1 (Chỉ thị của Giám đốc):**
  *"Mức giảm 16% làm biên lợi nhuận quá mỏng. Hãy điều chỉnh chiết khấu về 12% (giá thầu 44 tỷ VNĐ). Để bù đắp cạnh tranh, bổ sung gói miễn phí 06 tháng giám sát SOC Cloud trị giá 180 triệu VNĐ từ quỹ xúc tiến bán hàng."*

- **Bước 2 (Tác tử Tái Tính toán Tức thì):**
  Proposal Agent tiếp nhận chỉ thị, tự động cập nhật mô hình tài chính trong 15 giây:
  - Giá chào thầu mới: **44.000.000.000 VNĐ** (Chiết khấu 12%).
  - Biên lợi nhuận gộp phục hồi đạt **17.8%** (Đạt vùng sinh lời an toàn).
  - Chi phí gói SOC Cloud (180 triệu VNĐ) hạch toán vào chi phí bán hàng, bảo đảm biên lợi nhuận ròng đạt mục tiêu 11.5%.

- **Bước 3 (Phê duyệt Hoàn tất):**
  Orchestrator tạo bản dự thảo V2.0, Giám đốc bấm `[Approve & Submit Bid]`. Hệ thống mở khóa Vùng Đỏ và tự động phát hành hồ sơ thầu.

---

## 5. Kết luận & Giá trị Quản trị của Cơ chế HITL

Mô hình Điểm dừng Phê duyệt tại Viettel Solutions kết hợp linh hoạt giữa tốc độ tự động hóa của AI và tư duy chiến lược con người. Hệ thống kiểm soát an toàn ngân sách ở Vùng Đỏ nhưng duy trì tối đa năng suất ở Vùng Xanh, bảo đảm hiệu quả kinh doanh bền vững.
