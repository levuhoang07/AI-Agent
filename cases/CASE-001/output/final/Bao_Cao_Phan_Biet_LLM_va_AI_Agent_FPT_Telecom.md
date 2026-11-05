# BÁO CÁO: CƠ CHẾ VẬN HÀNH LLM VÀ AI AGENT TẠI FPT TELECOM

**Mã bài tập:** AI301_S01_BTVN_M1_BT1 | **Học phần:** AI301 - AI Agent  
**Vị trí:** Chuyên viên Phân tích Giải pháp AI — FPT Telecom  

---

### 1. Bóc tách cơ chế kỹ thuật cốt lõi giữa LLM và AI Agent

Mô hình Ngôn ngữ Lớn (LLM) thuần túy vận hành theo chuỗi thụ động: `Input -> Reasoning -> Output (Văn bản)`. Khi nhận truy vấn, LLM chỉ dự đoán token tiếp theo từ tri thức tĩnh đã huấn luyện. Mô hình bị cô lập trong không gian token (zero grounding), không thể truy vấn CSDL hay thực thi tác vụ. Do đó, Chatbot LLM tại FPT Telecom đạt tỷ lệ giải quyết trọn vẹn (FCR) chỉ 22% và chuyển tiếp nhân viên 78% [SIMULATED].

Ngược lại, Kiến trúc AI Agent vận hành tự chủ theo chu trình nhận thức: `Input -> Sense -> Plan -> Tool Calling -> Environment Feedback -> Output`. 
- **Sense:** Nhận diện thuê bao, phân tích ngữ cảnh và thiết bị.
- **Plan:** Dùng LLM làm bộ não suy luận (ReAct) lập kế hoạch hành động.
- **Tool Calling:** Kết nối API trực tiếp tới hệ thống Billing, NMS, CRM.
- **Environment Feedback:** Đọc kết quả môi trường, tự hiệu chỉnh trước khi thực thi hành động thực tế.

---

### 2. Quy trình xử lý ca thực tế: Đo kiểm mạng và nâng gói cước

Khi nhận yêu cầu: *'Kiểm tra giúp tôi đường truyền mạng dạo này chậm và hỗ trợ nâng cấp gói cước mới nhất'*, AI Agent thực hiện 5 bước:

1. **Sense & Định danh:** Nhận diện mã hợp đồng qua Hi FPT; trích xuất ý định: 'mạng chậm' và 'nâng gói'.
2. **Tool Calling 1 (Đo kiểm):** Gọi API `check_modem_signal(contract_id)` tới NMS đo suy hao quang và băng thông.
3. **Feedback & Suy luận:** Thông số modem bình thường nhưng gói 100 Mbps chạm ngưỡng trần. Agent suy luận nghẽn do vượt băng thông gói cũ.
4. **Tool Calling 2 (Tra cứu):** Gọi API `query_packages(profile)` tra cứu gói cước mới (Sky 1 Gbps).
5. **Action & Output:** Giải thích nguyên nhân, đề xuất gói Sky; khi khách hàng xác nhận, Agent gọi API `upgrade_subscription()` cập nhật trực tiếp lên hệ thống Billing.

---

### 3. Đánh giá hiệu quả vận hành và thách thức kỹ thuật

#### 3.1. Hiệu quả giảm tải vận hành
Với 50.000 yêu cầu/ngày tại Trung tâm CSKH [SIMULATED]:
- **Chatbot LLM cũ:** Chuyển tiếp 78%, nhân viên xử lý thủ công **39.000 yêu cầu/ngày** [SIMULATED].
- **AI Agent:** Gọi Tool 100% giúp tăng FCR lên 75%, giảm chuyển tiếp xuống 25% (tương đương **12.500 yêu cầu/ngày**) [SIMULATED].
- **Tỷ lệ giảm tải:** Cắt giảm **26.500 yêu cầu/ngày**, tương đương giảm **67,95% khối lượng công việc leo thang** cho tổng đài viên `((39.000 - 12.500) / 39.000 * 100%)` [INFERENCE].

#### 3.2. Hai thách thức kỹ thuật lớn nhất
1. **Tích hợp Backend cũ và độ trễ (Legacy Integration & Latency):** Hệ thống BSS/OSS và quản lý modem phân tán. Gọi chuỗi công cụ đồng thời dễ nghẽn, đe dọa mục tiêu phản hồi dưới 5 giây.
2. **Nguy cơ ảo giác hành động (Action Hallucination & Safety):** Lỗi suy luận có thể kích hoạt sai lệnh đổi gói hoặc cước phí. Bắt buộc có Human-in-the-Loop, xác thực OTP và cơ chế transaction rollback.

