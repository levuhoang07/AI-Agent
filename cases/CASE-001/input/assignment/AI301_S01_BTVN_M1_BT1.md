# ĐỀ BÀI TẬP VỀ NHÀ: PHÂN BIỆT CƠ CHẾ VẬN HÀNH CỦA LLM TRUYỀN THỐNG VÀ AI AGENT TẠI FPT TELECOM

- **Mã bài tập:** `AI301_S01_BTVN_M1_BT1`
- **Học phần:** AI301 - AI Agent
- **Session:** Session 01 - Tư duy AI Agent và ứng dụng trong doanh nghiệp
- **Mức độ:** Mức 1: Vận dụng cơ bản (VDCB) - Bloom Level 3
- **Thời gian làm bài dự kiến:** 35 phút
- **Hình thức thực hiện:** Cá nhân

---

## 1. Bối cảnh Doanh nghiệp
FPT Telecom là đơn vị cung cấp dịch vụ viễn thông và Internet băng rộng hàng đầu tại Việt Nam, phục vụ hàng triệu thuê bao cá nhân và doanh nghiệp. Trung tâm Chăm sóc Khách hàng tiếp nhận hơn 50.000 yêu cầu mỗi ngày qua các kênh ứng dụng Hi FPT, tổng đài thoại và cổng thông tin trực tuyến.

## 2. Tình huống Thực tế
Bạn được phân công làm Chuyên viên Phân tích Giải pháp AI tại FPT Telecom. Hiện tại trung tâm đang sử dụng một Chatbot hỏi đáp thông thường dựa trên mô hình LLM thuần túy. Chatbot chỉ có thể trả lời các câu hỏi tĩnh theo kịch bản nhưng không thể tra cứu tình trạng hợp đồng, kiểm tra tín hiệu modem từ xa hay tạo phiếu yêu cầu kỹ thuật. Ban Giám đốc yêu cầu bạn lập báo cáo so sánh chi tiết giữa Chatbot LLM hiện tại và một Hệ thống AI Agent tự chủ để chứng minh tính tất yếu của việc nâng cấp công nghệ.

## 3. Dữ liệu Đầu vào (Thông số Vận hành Quy trình Đổi gói cước)
- **Hệ thống hiện tại (Chatbot LLM):**
  - Thời gian phản hồi: 3 giây
  - Khả năng truy vấn CSDL thuê bao: 0%
  - Tỷ lệ giải quyết trọn vẹn (FCR): 22%
  - Tỷ lệ phải chuyển tiếp nhân viên con người: 78%
- **Mục tiêu kỳ vọng với AI Agent:**
  - Thời gian phản hồi trung bình: < 5 giây
  - Khả năng gọi Tool kiểm tra hạ tầng: 100%
  - Tỷ lệ giải quyết trọn vẹn (FCR): 75%
  - Tỷ lệ chuyển tiếp nhân viên con người: giảm còn 25%
*(Ghi chú: Dữ liệu giả định phục vụ mục đích học tập [SIMULATED])*

## 4. Nhiệm vụ Thực hành
- **Nhiệm vụ 1:** Bóc tách cơ chế kỹ thuật cốt lõi: Phân tích sự khác biệt bản chất giữa mô hình LLM đơn lẻ (`Input -> Reasoning -> Output dạng văn bản`) và Kiến trúc AI Agent (`Input -> Sense -> Plan -> Tool Calling -> Environment Feedback -> Output có hành động thực tế`).
- **Nhiệm vụ 2:** Phân tích quy trình xử lý ca thực tế: Minh họa chuỗi các bước mà AI Agent sẽ thực hiện khi nhận yêu cầu: *"Kiểm tra giúp tôi đường truyền mạng dạo này chậm và hỗ trợ nâng cấp gói cước mới nhất"*.
- **Nhiệm vụ 3:** Đánh giá hiệu quả vận hành và đề xuất: Tính toán tỷ lệ giảm tải công việc cho nhân viên tổng đài và nêu 02 thách thức kỹ thuật lớn nhất khi chuyển đổi từ Chatbot tĩnh sang AI Agent tự chủ.

## 5. Yêu cầu Sản phẩm Đầu ra
- **Định dạng:** 01 Báo cáo Markdown (`.md`).
- **Dung lượng:** Từ 450 - 600 từ.
- **Nội dung:** Đầy đủ 3 phần tương ứng 3 nhiệm vụ, lập luận học thuật, có số liệu minh chứng.
