---
name: agent-solution-design
description: >-
  Use this skill to design end-to-end AI Agent architectures: pattern selection
  (ReAct, Router, Multi-Agent), tool calling specs, prompt engineering, memory/state,
  human-in-the-loop controls, risk/safety guardrails, and cost/ROI estimations.
---

# Agent Solution Design Skill

Skill này là trọng tâm kỹ thuật của môn học, chịu trách nhiệm thiết kế kiến trúc hệ thống AI Agent hoàn chỉnh nhằm giải quyết bài toán kinh doanh đã được xác định.

## 1. Trigger Conditions
- Sau khi hoàn thành phân tích nghiệp vụ và dữ liệu.
- Người dùng yêu cầu: "Thiết kế kiến trúc AI Agent", "Lựa chọn mô hình Agent", "Thiết kế prompt và workflow".

## 2. Các Khối Thiết kế Kiến trúc (Architectural Building Blocks)

### 1. Lựa chọn Mô hình Điều phối Agent (Agent Pattern Selection)
- **Single Agent (ReAct / Tool-Use):** Phù hợp với tác vụ tuyến tính, tìm kiếm tài liệu nội bộ (RAG), tạo báo cáo định kỳ.
- **Router Pattern:** Điều phối yêu cầu của người dùng tới các Agent chuyên môn (ví dụ: CSKH, Kỹ thuật, Thanh toán).
- **Multi-Agent Orchestration (Supervisor / Peer-to-Peer):** Phù hợp với bài toán phức tạp đòi hỏi sự phối hợp giữa nhiều vai trò (ví dụ: Planner Agent -> Data Agent -> Report Agent -> Critic Agent).

### 2. Thiết kế Bộ Công cụ (Tool & API Specifications)
- Liệt kê chi tiết các công cụ Agent được phép gọi:
  - Tên Tool (ví dụ: `query_erp_database`, `calculate_loan_schedule`, `send_slack_alert`).
  - Input parameters, Schema, Validation rules.
  - Phân quyền & Giới hạn tỷ lệ gọi (Rate Limits).

### 3. Thiết kế Prompt & Ngữ cảnh (System Prompt & Memory)
- System Prompt chi tiết: Vai trò (Role), Giới hạn (Constraints), Phong cách giao tiếp, Quy trình suy luận (Chain-of-Thought).
- Chiến lược Bộ nhớ (Memory Architecture): Bộ nhớ làm việc ngắn hạn (Working Memory/Scratchpad), Bộ nhớ dài hạn (Vector DB / Knowledge Base).

### 4. Kiểm soát Con người Tham gia (Human-in-the-Loop & Safety Guardrails)
- Xác định rõ các hành động bắt buộc phải có sự phê duyệt của con người trước khi thực thi (ví dụ: Chuyển tiền, xóa dữ liệu, gửi email cho đối tác bên ngoài).
- Thiết lập rào chắn an toàn (Guardrails): Kiểm duyệt nội dung độc hại (Safety filters), ngăn chặn Prompt Injection, bảo vệ dữ liệu cá nhân (PII Masking).

### 5. Ước tính Chi phí & Đánh giá Hiệu quả (TCO, Token Cost & Eval Framework)
- Tính toán lượng Token tiêu thụ dự kiến mỗi tháng dựa trên lưu lượng giao dịch.
- So sánh chi phí API LLM + Hạ tầng so với chi phí nhân sự tiết kiệm được để tính toán thời gian hoàn vốn (Payback Period) và ROI.

## 3. Chốt chặn Phê duyệt (Approval Gate B — Solution Approval)
Trình bày tài liệu thiết kế giải pháp cho người dùng phê duyệt trước khi tiến hành sản xuất tài liệu chính thức (Word, Excel, Slide).

## 4. Đầu ra (Deliverables)
- Bản đặc tả giải pháp: `cases/<CASE_ID>/solution/agent-architecture-spec.md`.
