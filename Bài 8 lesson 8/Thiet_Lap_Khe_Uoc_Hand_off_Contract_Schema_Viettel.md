# BÁO CÁO KỸ THUẬT: THIẾT LẬP KHẾ ƯỚC CHUYỂN GIAO DỮ LIỆU (HAND-OFF CONTRACT SCHEMA) GIỮA CÁC TÁC TỬ TẠI VIETTEL SOLUTIONS

- **Mã bài tập:** `AI301_S08_BTVN_M2_BT1`
- **Học phần:** AI301 - AI Agent (Session 08: Tư duy Multi-Agent và tối ưu hệ thống AI Agent)
- **Đơn vị:** Tổng công ty Giải pháp Doanh nghiệp Viettel (Viettel Solutions)
- **Chuỗi tác tử:** Research Agent -> Scoring Agent -> Proposal Agent

---

## 1. Bối cảnh & Mục tiêu Thiết lập Khế ước Bàn giao Dữ liệu

Trong hệ thống Sales Intelligence tự động tại Viettel Solutions, luồng nghiệp vụ vận hành qua chuỗi ba tác tử chuyên trách: **Research Agent** (thu thập hồ sơ doanh nghiệp), **Scoring Agent** (chấm điểm tiềm năng Lead) và **Proposal Agent** (xây dựng đề xuất kỹ thuật - thương mại). Khi luân chuyển dữ liệu bằng ngôn ngữ tự nhiên không cấu trúc, hệ thống đối mặt với nguy cơ suy giảm ngữ cảnh (Context Drift), thiếu sót trường dữ liệu và ảo giác thông tin (Hallucination), gây chấm điểm sai và lãng phí nguồn lực tiếp cận.

Khế ước Bàn giao Dữ liệu (**Hand-off Contract Schema**) đóng vai trò là giao thức dữ liệu chuẩn tắc (Strict Data Protocol). Khế ước quy định ranh giới kiểu dữ liệu, các thuộc tính bắt buộc và ràng buộc định dạng khắt khe, giúp loại bỏ hoàn toàn hiểu lầm ngữ cảnh và bảo đảm tính toàn vẹn dữ liệu trước khi kích hoạt Scoring Agent.

---

## 2. Nhiệm vụ 1: Định nghĩa Cấu trúc JSON Schema cho Hand-off Contract

Gói tin dữ liệu chuyển giao giữa Research Agent và Scoring Agent (`ResearchToScoringPayload`) được định nghĩa theo chuẩn JSON Schema Draft-07, kiểm soát chặt chẽ 6 trường nghiệp vụ bắt buộc:

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "ResearchToScoringPayload",
  "type": "object",
  "properties": {
    "customer_id": { "type": "string", "pattern": "^CUST-VT-[0-9]{4,6}$" },
    "company_name": { "type": "string", "minLength": 3 },
    "estimated_revenue": { "type": "number", "minimum": 0 },
    "employee_count": { "type": "integer", "minimum": 1 },
    "tech_requirements": { "type": "array", "items": { "type": "string" }, "minItems": 1 },
    "decision_makers": {
      "type": "array", "minItems": 1,
      "items": {
        "type": "object",
        "properties": {
          "name": { "type": "string", "minLength": 2 },
          "role": { "type": "string", "enum": ["CIO", "CTO", "CEO", "CISO", "IT_Director"] },
          "email": { "type": "string", "format": "email" },
          "influence_level": { "type": "string", "enum": ["High", "Medium", "Low"] }
        },
        "required": ["name", "role", "email", "influence_level"]
      }
    }
  },
  "required": ["customer_id", "company_name", "estimated_revenue", "employee_count", "tech_requirements", "decision_makers"],
  "additionalProperties": false
}
```

Schema áp dụng biểu thức chính quy cho mã khách hàng (`customer_id`), ràng buộc số dương cho doanh thu và nhân sự, đồng thời bắt buộc danh sách người ra quyết định phải có đầy đủ họ tên, vai trò lãnh đạo, email và mức độ ảnh hưởng.

---

## 3. Nhiệm vụ 2: Quy tắc Kiểm thực Khế ước qua Prompting

Nhằm ngăn chặn gói tin rác hoặc thiếu trường lọt vào Scoring Agent, Orchestrator tích hợp chốt chặn kiểm duyệt runtime thông qua System Prompt:

```text
[VAI TRÒ]: Bạn là Data Gatekeeper của Orchestrator tại Viettel Solutions.
[NHIỆM VỤ]: Thẩm định tính toàn vẹn gói tin JSON từ Research Agent theo schema 'ResearchToScoringPayload' trước khi kích hoạt Scoring Agent.
[QUY TẮC KIỂM THỰC]:
1. Xác thực cú pháp JSON hợp lệ.
2. Kiểm tra đủ 6 trường: customer_id (^CUST-VT-[0-9]{4,6}$), company_name (>=3 ký tự), estimated_revenue (>=0), employee_count (>=1), tech_requirements và decision_makers không rỗng.
3. Phân luồng:
   - Hợp lệ: {"status": "VALID", "next_agent": "ScoringAgent", "payload": <data>}
   - Sai sót: {"status": "INVALID", "error_code": "SCHEMA_VIOLATION", "missing_fields": [...], "action": "REJECT_AND_RETRY"}
Tuyệt đối không tự suy diễn hoặc tạo giá trị giả mạo ngoài dữ liệu đầu vào.
```

---

## 4. Nhiệm vụ 3: Kịch bản Xử lý Tình huống Gói tin Không Hợp Lệ

Khi gói tin phát sinh lỗi cấu trúc hoặc thiếu thông tin, Orchestrator triển khai quy trình xử lý 3 giai đoạn:

1. **Trích xuất lỗi chi tiết (Error Diagnostics):** Orchestrator bóc tách cụ thể trường dữ liệu vi phạm (ví dụ: `Missing field: decision_makers` hoặc `Invalid email: contact@corp`) để làm căn cứ phản hồi.
2. **Vòng lặp tự sửa lỗi có kiểm soát (Self-Correction Retry Loop):** Orchestrator gửi gói tin phản hồi lỗi ngược về Research Agent, nêu rõ trường dữ liệu cần bổ sung hoặc điều chỉnh từ nguồn sơ cấp. Thiết lập giới hạn tối đa 2 lần thử lại (`Max Retries = 2`) nhằm ngăn chặn vòng lặp vô tận (Infinite Loop), giúp tối ưu hóa chi phí token và thời gian phản hồi.
3. **Cơ chế ngắt mạch và cách ly (Circuit Breaker & Quarantine):** Nếu sau 2 lần retry mà gói tin vẫn không thỏa mãn schema, Orchestrator kích hoạt Circuit Breaker, dừng luồng tự động để bảo vệ Scoring Agent. Hồ sơ được chuyển vào hàng đợi cách ly (`Quarantine Queue`) và gửi thông báo tới chuyên viên Sales Ops (Human-in-the-Loop) để thẩm định thủ công, ngăn chặn việc đưa dữ liệu lỗi vào mô hình chấm điểm Lead.

---

## 5. Mã Script Python Kiểm thực Độc lập (Runtime Verification)

Hệ thống tích hợp module kiểm thực độc lập sử dụng thư viện `jsonschema` để xác thực runtime trước khi chuyển dữ liệu:

```python
from jsonschema import validate, ValidationError

def verify_handoff_contract(payload: dict, schema: dict) -> dict:
    try:
        validate(instance=payload, schema=schema)
        return {"status": "SUCCESS", "message": "Gói tin đạt chuẩn, chuyển tiếp Scoring Agent."}
    except ValidationError as err:
        return {
            "status": "FAILED",
            "invalid_field": list(err.path),
            "error_detail": err.message
        }
```

Giải pháp kết hợp JSON Schema chuẩn hóa, kiểm định qua Prompting và script runtime giúp Viettel Solutions xây dựng hệ thống Sales Intelligence đa tác tử đạt độ chính xác dữ liệu tuyệt đối.
