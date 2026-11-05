# BÁO CÁO KIỂM ĐỊNH CHẤT LƯỢNG (QA SIGN-OFF REPORT) — CASE-001

**Mã bài tập:** `AI301_S01_BTVN_M1_BT1`  
**Tiêu đề:** Phân biệt cơ chế vận hành LLM và AI Agent tại FPT Telecom  
**Ngày thẩm định:** 2026-11-06T01:19:30+07:00  
**Người thẩm định:** Quality Assurance Lead  

---

## 1. Kiểm tra Tiêu chí Đề bài & Rubric (Rubric Compliance)
- [x] **Nhiệm vụ 1 (Cơ chế kỹ thuật):** Phân tích rõ sự khác biệt giữa chuỗi đóng `Input -> Reasoning -> Output` của LLM và chu trình nhận thức mở `Sense -> Plan -> Tool Calling -> Environment Feedback -> Output` của AI Agent. (ĐẠT XUẤT SẮC)
- [x] **Nhiệm vụ 2 (Quy trình thực tế 5 bước):** Minh họa chi tiết quy trình xử lý ca 'mạng chậm & nâng gói cước', nêu rõ các API gọi NMS, Billing, trích xuất hai ý định song song. (ĐẠT XUẤT SẮC)
- [x] **Nhiệm vụ 3 (Hiệu quả & Thách thức):** Tính toán chính xác số liệu giảm tải (50.000 req/ngày, giảm 26.500 cuộc gọi leo thang, tương đương cắt giảm 67.95% việc cho nhân viên) và nêu rõ 2 thách thức (Legacy backend latency, Action hallucination & Safety guardrails). (ĐẠT XUẤT SẮC)

## 2. Kiểm soát Dung lượng Từ (Word Count Audit)
- **Quy định đề bài:** 450 - 600 từ.
- **Thực tế tệp Markdown:** **571 từ** (Nằm hoàn hảo trong ngưỡng yêu cầu, tỷ lệ an toàn 100%).

## 3. Kiểm định Định dạng & Filesystem (Artifact Verification)
- [x] `output/CASE-001/final/Bao_Cao_Phan_Biet_LLM_va_AI_Agent_FPT_Telecom.md` (Tồn tại, đúng chuẩn UTF-8).
- [x] `output/CASE-001/final/Bao_Cao_Phan_Biet_LLM_va_AI_Agent_FPT_Telecom.docx` (Tồn tại, mở hợp lệ, 3 headings, 1 table, bảng màu chuyên nghiệp).

## 4. Kết luận Nghiệm thu: **PASS — ĐẠT CHUẨN NỘP BÀI**
