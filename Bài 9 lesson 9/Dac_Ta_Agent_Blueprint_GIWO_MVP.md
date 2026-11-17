# TÀI LIỆU AGENT BLUEPRINT (GIWO): CHẨN ĐOÁN TỒN KHO HÀNG TƯƠI SỐNG CHO SẢN PHẨM MVP TẠI WINCOMMERCE

- **Mã bài tập:** `AI301_S09_BTVN_M1_BT1`
- **Học phần:** AI301 - AI Agent (Session 09: Xây dựng Business AI Agent MVP)
- **Đơn vị:** Chuỗi bán lẻ WinCommerce (Tập đoàn Masan)
- **Mảng:** Phân tích dữ liệu (Data Analytics)

---

## 1. Bối cảnh & Nỗi đau Vận hành Hiện tại (Business Pain Points)

WinCommerce quản lý hơn 3.600 siêu thị WinMart/WinMart+. Ngành hàng tươi sống có hạn dùng ngắn (24 - 72 giờ). Quản trị tồn kho thủ công hiện nay gặp 3 nút thắt lớn:

- **Kiểm đếm thủ công tốn thời gian:** Nhân viên mất 3 - 4 giờ mỗi sáng đối chiếu Excel rời rạc, dễ sai sót.
- **Tỷ lệ hủy hàng cao:** Chậm phát hiện hàng cận date khiến tỷ lệ hủy hàng tươi sống lên tới **6.8% doanh thu ngành hàng**, gây thiệt hại lớn.
- **Thiếu giảm giá động (Dynamic Markdown):** Cửa hàng trưởng thiếu công cụ dự báo sức mua, dẫn đến xả hàng quá muộn hoặc giảm giá sâu gây thâm hụt lợi nhuận.

---

## 2. Bản Đặc tả Agent Blueprint Chuẩn Khung GIWO cho MVP

Tác tử **Fresh Inventory Diagnostic Agent** được thiết kế theo chuẩn GIWO:

```mermaid
flowchart LR
    G["Goal: Giảm tỷ lệ hủy < 3.5%"] --> I["Inputs: Tồn kho ERP & Shelf-life Matrix"]
    I --> W["Workflow: Ingest -> Profile -> Predict -> Alert"]
    W --> O["Outputs: Dashboard & Đề xuất Chiết khấu"]
```

### 1. Goal (Mục tiêu SMART)
- Giảm tỷ lệ hủy hàng tươi sống từ **6.8% xuống dưới 3.5%** tại 50 cửa hàng thử nghiệm MVP trong 90 ngày.
- Rút ngắn thời gian chẩn đoán tồn kho từ **4 giờ xuống dưới 5 phút** trước 06:30 sáng.
- Đạt độ chính xác dự báo hàng cận date trên **92%**.

### 2. Inputs (Khế ước Dữ liệu Đầu vào)
- Dữ liệu tồn kho ERP: Mã cửa hàng (`store_id`), mã SKU, số lượng tồn và giờ nhập kho.
- Ma trận vòng đời sản phẩm (**Shelf-life Matrix**): Hạn dùng chuẩn (24h/48h/72h).
- Lịch sử bán hàng 30 ngày qua giao thức MCP Read-only.

### 3. Workflow (Luồng Vận hành Tác tử)
1. **Thu thập dữ liệu (Ingest):** Tự động truy vấn tồn kho ERP lúc 06:00 sáng.
2. **Chẩn đoán rủi ro (Predict):** So khớp hạn dùng với tốc độ bán bình quân (Sales Velocity), phân loại 3 mức: An toàn, Chậm luân chuyển, Cận date.
3. **Đề xuất hành động (Optimize):** Sinh mức giảm giá giờ vàng (15%, 30%, 50%) theo khung giờ chiều.
4. **Phát hành báo cáo (Dispatch):** Xuất báo cáo Markdown gửi Cửa hàng trưởng trước 06:30 sáng.

### 4. Outputs (Định dạng Sản phẩm Đầu ra)
- **Daily Inventory Health Dashboard:** Bảng điều khiển phân loại hàng tồn theo rủi ro cận date.
- **Dynamic Markdown Clearance Plan:** Danh mục mặt hàng cần xả kho kèm mức chiết khấu chuẩn hóa.

---

## 3. Thiết lập Hàng rào An toàn (Safety Guardrails)

Hệ thống thiết lập 02 hàng rào an toàn bắt buộc:

1. **Read-Only Data Boundary:** Tác tử chỉ được cấp quyền đọc (`SELECT`) qua giao thức MCP, nghiêm cấm quyền ghi/sửa trên cơ sở dữ liệu kho ERP để bảo vệ an toàn hệ thống phân tán.
2. **Human Approval Gate (HITL):** Đề xuất giảm giá trên 30% hoặc lô hàng trị giá trên 5 triệu VNĐ bắt buộc phải có phê duyệt của Cửa hàng trưởng trước khi áp dụng lên POS.
