# BÁO CÁO XÂY DỰNG CUSTOM SKILL 'SALES_FOLLOWUP' TẠI FPT SMARTBIZ

- **Mã bài tập:** `AI301_S03_BTVN_M3_BT1` (Session 03)
- **Hệ thống:** Sales Lead Qualification Agent (Google Antigravity)
- **Custom Skill:** `sales_followup` | **Đơn vị:** FPT SmartBiz

---

## 1. Cấu trúc Custom Skill `sales_followup`

Nhằm nâng tỷ lệ phản hồi email chào hàng từ 8% lên trên 25%, FPT SmartBiz thiết kế Custom Skill `sales_followup` theo chuẩn Antigravity:

```text
skills/sales_followup/
├── SKILL.md
├── instructions.md
├── references/tone_of_voice.md
└── templates/
    ├── hot_lead_demo.txt
    ├── warm_lead_case_study.txt
    └── disqualified_freemium.txt
```

### Cấu hình `SKILL.md`:
```yaml
name: sales_followup
description: Tự động trích xuất thực thể Lead và soạn thảo email tiếp cận theo phân khúc BANT.
triggers: [on_lead_classified]
inputs: {lead_profile: object, segment: str}
outputs: {email_message: object}
```

## 2. Quy tắc cá nhân hóa động (Dynamic Personalization Engine)

Tác tử tự động phân tích hồ sơ và trích xuất 4 trường thông tin trọng yếu:
1. **Chức danh (`{title}`):** Chuẩn hóa xưng hô (Tổng Giám đốc quan tâm tối ưu chi phí và ROI).
2. **Quy mô & Ngành (`{industry}`):** Tái hiện bối cảnh (Chuỗi 25 nhà hàng tại TP.HCM).
3. **Nỗi đau vận hành (`{pain}`):** Đưa thất thoát nguyên liệu tươi sống làm tiêu điểm mở đầu thư.
4. **Kêu gọi hành động (`{cta}`):** Đề xuất Demo 20 phút (Hot), gửi Case Study (Warm), hoặc cấp công cụ dùng thử (Disqualified).

## 3. Toàn văn 3 bức thư tiếp cận thực tế theo 3 phân khúc

### Bức thư 1: Phân khúc Hot Lead (Mời hẹn Demo 1:1 giải pháp chuyên sâu)
- **Người nhận:** Tổng Giám đốc chuỗi 25 nhà hàng ăn uống tại TP.HCM (Ngân sách 150 triệu)
- **Tiêu đề:** Giải pháp kiểm soát hao hụt nguyên liệu tươi sống cho chuỗi 25 nhà hàng của Anh/Chị
- **Nội dung:**
> Kính gửi Anh/Chị Tổng Giám đốc,  
> 
> Chúng tôi thấu hiểu việc thất thoát nguyên liệu tươi sống tại 25 chi nhánh đang làm hao hụt từ 5% đến 8% lợi nhuận ròng của chuỗi nhà hàng.  
> 
> FPT SmartBiz F&B cung cấp tính năng định lượng tự động và giám sát hao hụt tức thời tại từng điểm bán, giúp chuỗi tiết kiệm hàng trăm triệu đồng mỗi tháng. Với mức ngân sách 150 triệu, gói triển khai của FPT đáp ứng trọn vẹn bài toán vận hành của Anh/Chị.  
> 
> Em trân trọng mời Anh/Chị tham gia buổi Demo 1:1 trực tuyến 20 phút vào 09h30 Thứ Năm tuần này để cùng phân tích mô hình định lượng tối ưu cho chuỗi.  
> 
> Trân trọng,  
> **Ban Cố vấn Chuyển đổi số FPT SmartBiz**

### Bức thư 2: Phân khúc Warm Lead (Tặng tài liệu Case Study ngành thực tế)
- **Người nhận:** Giám đốc Vận hành chuỗi bán lẻ thời trang 15 cửa hàng
- **Tiêu đề:** Case Study: Tối ưu 30% tồn kho cho chuỗi bán lẻ thời trang 15 điểm bán
- **Nội dung:**
> Kính gửi Anh/Chị Giám đốc Vận hành,  
> 
> Cân đối hàng tồn kho giữa các chi nhánh luôn là thách thức lớn nhất đối với chuỗi bán lẻ thời trang trong giai đoạn tăng trưởng quy mô.  
> 
> FPT SmartBiz xin gửi tặng Anh/Chị bản Case Study độc quyền: *"Kinh nghiệm số hóa quản trị tồn kho và tối ưu vốn lưu động cho chuỗi 15 điểm bán lẻ"*. Tài liệu phân tích quy trình luân chuyển hàng hóa thực tế đã giúp tối ưu 30% chi phí lưu kho sau 60 ngày triển khai.  
> 
> Anh/Chị có thể tải tài liệu đầy đủ tại liên kết đính kèm. Em rất mong có cơ hội trao đổi sau khi Anh/Chị tham khảo.  
> 
> Trân trọng,  
> **Ban Tư vấn Bán lẻ FPT SmartBiz**

### Bức thư 3: Phân khúc Disqualified (Tặng tài nguyên số dùng thử)
- **Người nhận:** Quản lý cơ sở ẩm thực độc lập quy mô 1 điểm bán
- **Tiêu đề:** Tặng bộ bảng tính Excel định lượng nguyên liệu và tài khoản FPT SmartBiz
- **Nội dung:**
> Chào Bạn,  
> 
> Đối với mô hình ẩm thực một điểm bán, kiểm soát chi phí nguyên liệu là nền tảng cốt lõi để duy trì lợi nhuận ổn định.  
> 
> Dù quy mô hiện tại chưa phù hợp để đầu tư hệ thống ERP lớn, FPT SmartBiz vẫn muốn đồng hành cùng Bạn qua bộ quà tặng:  
> 1. Bảng tính Excel chuẩn hóa định lượng nguyên liệu và tự động tính giá vốn món ăn.  
> 2. Tài khoản trải nghiệm miễn phí 30 ngày phần mềm FPT SmartBiz Starter trên đám mây.  
> 
> Bạn có thể bấm vào liên kết đính kèm để kích hoạt và sử dụng ngay hôm nay.  
> 
> Thân mến,  
> **Bộ phận Hỗ trợ Doanh nghiệp FPT SmartBiz**

## 4. Đánh giá tính khả thi và tác động chuyển đổi
Cơ chế tự động của Skill `sales_followup` giúp cá nhân hóa thông điệp tức thời, đánh trúng nỗi đau quản trị của người ra quyết định. Phân luồng thông điệp theo phân khúc giúp tối ưu nguồn lực kinh doanh, duy trì kết nối bền vững và nâng tỷ lệ phản hồi email từ 8% lên trên 25% mục tiêu.
