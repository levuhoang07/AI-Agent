import sys
import os

WORKSPACE_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
sys.path.insert(0, os.path.join(WORKSPACE_ROOT, "shared", "utilities"))

import docx_helper

sections = [
    {
        "level": 1,
        "heading": "1. Bóc tách cơ chế kỹ thuật cốt lõi giữa LLM và AI Agent",
        "paragraphs": [
            "Mô hình Ngôn ngữ Lớn (LLM) thuần túy vận hành theo chuỗi thụ động: Input -> Reasoning -> Output (Văn bản). Khi nhận truy vấn, LLM chỉ dự đoán token tiếp theo từ tri thức tĩnh đã huấn luyện. Mô hình bị cô lập trong không gian token (zero grounding), không thể truy vấn CSDL hay thực thi tác vụ. Do đó, Chatbot LLM tại FPT Telecom đạt tỷ lệ giải quyết trọn vẹn (FCR) chỉ 22% và chuyển tiếp nhân viên 78% [SIMULATED].",
            "Ngược lại, Kiến trúc AI Agent vận hành tự chủ theo chu trình nhận thức mở: Input -> Sense -> Plan -> Tool Calling -> Environment Feedback -> Output. Agent sở hữu tri giác môi trường, lập kế hoạch suy luận ReAct, gọi công cụ API kết nối trực tiếp hệ sinh thái BSS/OSS và tự hiệu chỉnh kế hoạch dựa trên phản hồi môi trường trước khi hành động thực tế."
        ],
        "table": {
            "headers": ["Tiêu chí so sánh", "Chatbot LLM thuần túy", "Hệ thống AI Agent tự chủ"],
            "rows": [
                ["Cơ chế vận hành", "Chuỗi đóng: Input -> Output", "Vòng lặp nhận thức: Sense-Plan-Act-Feedback"],
                ["Khả năng gọi Tool", "0% (Không tương tác API)", "100% (Tích hợp NMS, Billing, CRM)"],
                ["Tỷ lệ giải quyết FCR", "22% [SIMULATED]", "75% [SIMULATED] (Kỳ vọng)"],
                ["Tỷ lệ chuyển tiếp nhân viên", "78% [SIMULATED]", "25% [SIMULATED] (Giảm 67.95%)"]
            ]
        }
    },
    {
        "level": 1,
        "heading": "2. Quy trình xử lý ca thực tế: Đo kiểm mạng và nâng gói cước",
        "paragraphs": [
            "Khi nhận yêu cầu: 'Kiểm tra giúp tôi đường truyền mạng dạo này chậm và hỗ trợ nâng cấp gói cước mới nhất', AI Agent thực hiện chuỗi 5 bước tự chủ:",
            "1. Sense & Định danh: Nhận diện mã hợp đồng qua Hi FPT; trích xuất đồng thời hai ý định: báo mạng chậm và nâng gói cước.",
            "2. Tool Calling 1 (Đo kiểm): Gọi API check_modem_signal(contract_id) tới NMS đo suy hao quang và băng thông.",
            "3. Feedback & Suy luận: Nhận kết quả phần cứng bình thường nhưng gói 100 Mbps chạm ngưỡng trần. Agent kết luận nghẽn do vượt băng thông gói cũ.",
            "4. Tool Calling 2 (Tra cứu): Gọi API query_packages(profile) tra cứu gói cước mới phù hợp (gói Sky 1 Gbps).",
            "5. Action & Output: Giải thích nguyên nhân, đề xuất gói Sky; khi khách hàng xác nhận, Agent gọi API upgrade_subscription() cập nhật trực tiếp lên hệ thống Billing."
        ]
    },
    {
        "level": 1,
        "heading": "3. Đánh giá hiệu quả vận hành và thách thức kỹ thuật",
        "paragraphs": [
            "3.1. Hiệu quả giảm tải vận hành: Với lưu lượng 50.000 yêu cầu/ngày tại Trung tâm CSKH [SIMULATED], Chatbot LLM cũ làm phát sinh 39.000 yêu cầu/ngày nhân viên phải xử lý thủ công (78%). Với AI Agent, tỷ lệ chuyển tiếp giảm xuống 25% (12.500 yêu cầu/ngày). Nhờ đó, FPT Telecom cắt giảm trực tiếp 26.500 yêu cầu/ngày, tương đương giảm 67,95% khối lượng công việc leo thang cho tổng đài viên ((39.000 - 12.500) / 39.000 * 100%) [INFERENCE].",
            "3.2. Hai thách thức kỹ thuật lớn nhất:",
            "- Thách thức 1: Tích hợp Backend cũ và độ trễ (Legacy Integration & Latency). Hệ thống BSS/OSS và quản lý modem phân tán. Gọi chuỗi công cụ đồng thời dễ nghẽn, đe dọa mục tiêu phản hồi dưới 5 giây.",
            "- Thách thức 2: Nguy cơ ảo giác hành động (Action Hallucination & Safety). Lỗi suy luận có thể kích hoạt sai lệnh đổi gói hoặc cước phí. Bắt buộc có Human-in-the-Loop, xác thực OTP và cơ chế transaction rollback."
        ]
    }
]

out1 = os.path.join(WORKSPACE_ROOT, "cases", "CASE-001", "output", "final", "Bao_Cao_Phan_Biet_LLM_va_AI_Agent_FPT_Telecom.docx")
out2 = os.path.join(WORKSPACE_ROOT, "output", "CASE-001", "final", "Bao_Cao_Phan_Biet_LLM_va_AI_Agent_FPT_Telecom.docx")

docx_helper.create_report_document(
    out1,
    "BÁO CÁO: CƠ CHẾ VẬN HÀNH LLM VÀ AI AGENT TẠI FPT TELECOM",
    "Học phần AI301: AI Agent - Session 01 | Mã bài tập: AI301_S01_BTVN_M1_BT1",
    "Chuyên viên Phân tích Giải pháp AI",
    sections
)

docx_helper.create_report_document(
    out2,
    "BÁO CÁO: CƠ CHẾ VẬN HÀNH LLM VÀ AI AGENT TẠI FPT TELECOM",
    "Học phần AI301: AI Agent - Session 01 | Mã bài tập: AI301_S01_BTVN_M1_BT1",
    "Chuyên viên Phân tích Giải pháp AI",
    sections
)

audit = docx_helper.inspect_docx(out2)
print(f"DOCX Audit Valid: {audit['valid']}, Headings: {audit['headings_count']}, Tables: {audit['tables_count']}")
