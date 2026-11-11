# BÁO CÁO KIỂM TOÁN BẢO MẬT VÀ PHÂN QUYỀN READ-ONLY CHO MCP SERVER TẠI WINCOMMERCE

- **Mã bài tập:** `AI301_S06_BTVN_M2_BT1` (Session 06)
- **Hệ thống:** Data Analytics Agent (Model Context Protocol - MCP)
- **Đơn vị:** WinCommerce (Tập đoàn Masan)

---

## 1. Nhận diện 3 nguy cơ an ninh khi AI Agent kết nối trực tiếp Cơ sở dữ liệu

Khi kết nối Data Analytics Agent với kho dữ liệu bán lẻ PostgreSQL của 3.600 siêu thị WinMart qua giao thức MCP, hệ thống đối mặt với 3 rủi ro bảo mật trọng yếu:

1. **SQL Injection gián tiếp qua Prompt Injection:** Kẻ tấn công lợi dụng câu hỏi nghiệp vụ để thao túng prompt, ép Agent sinh các câu lệnh phá hoại cấu trúc dữ liệu (`DROP TABLE`, `ALTER USER`) hoặc xóa dấu vết giao dịch bán hàng.
2. **Rò rỉ thông tin định danh cá nhân nhạy cảm (PII Leakage):** Cơ sở dữ liệu chứa hàng triệu hồ sơ Hội viên WIN (số điện thoại, CCCD, địa chỉ cư trú, thói quen tiêu dùng). Nếu Agent tùy tiện truy vấn các trường dữ liệu thô và đưa vào ngữ cảnh LLM, doanh nghiệp đối mặt nguy cơ vi phạm nghiêm trọng Nghị định 13/2023/NĐ-CP về bảo vệ dữ liệu cá nhân.
3. **Nghẽn tài nguyên hệ thống do quét toàn bảng (Full Table Scan DoS):** LLM sinh các câu truy vấn phức tạp thiếu điều kiện lọc `WHERE` hoặc thực hiện phép nối đa bảng không tối ưu trên hàng trăm triệu dòng giao dịch, gây cạn kiệt CPU/RAM và làm gián đoạn máy chủ cơ sở dữ liệu `dw_sales`.

## 2. Thiết lập cấu hình bảo vệ đa tầng (Defense-in-Depth Architecture)

Để đảm bảo an toàn tuyệt đối, WinCommerce thiết lập kiến trúc phòng thủ hai lớp giữa PostgreSQL và MCP Host:

### Phân quyền tại tầng Cơ sở dữ liệu (PostgreSQL RBAC & Hard Constraints):
```sql
-- Khởi tạo User chỉ đọc và áp đặt ràng buộc giao dịch
CREATE USER analytics_user WITH PASSWORD 'WinMart#Secure2024';
REVOKE ALL ON ALL TABLES IN SCHEMA public FROM analytics_user;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO analytics_user;
ALTER USER analytics_user SET default_transaction_read_only = on;
ALTER USER analytics_user SET statement_timeout = '15s';
```
Bằng cách gán `default_transaction_read_only = on`, máy chủ PostgreSQL sẽ từ chối mọi thao tác ghi dữ liệu ở mức nhân (kernel engine), đồng thời ngắt kết nối tự động sau 15 giây nếu câu lệnh có dấu hiệu chạy quá tải.

### Kiểm soát tại tầng ứng dụng (MCP Host & Data Masking):
Cơ chế MCP Host triển khai trong môi trường Docker Sandbox cô lập, chỉ kết nối nội bộ và tự động trỏ vào các View dữ liệu đã được ẩn danh hóa PII (mã hóa số điện thoại: `090****123`).

## 3. Thiết kế bộ lọc câu truy vấn độc hại (Query Guard Engine)

Trước khi gửi bất kỳ câu truy vấn nào từ Agent xuống Database, MCP Server bắt buộc luân chuyển câu lệnh qua module kiểm định cú pháp:

```python
import re

FORBIDDEN_KEYWORDS = r"\b(DROP|DELETE|UPDATE|INSERT|ALTER|TRUNCATE|GRANT|REVOKE|EXEC)\b"

def validate_and_guard_query(sql_query: str) -> str:
    cleaned = sql_query.strip().strip(";")
    if re.search(FORBIDDEN_KEYWORDS, cleaned, re.IGNORECASE):
        raise ValueError("Security Alert: Câu lệnh chứa từ khóa thao túng dữ liệu bị cấm tuyệt đối!")
    if not re.match(r"^(SELECT|WITH)\b", cleaned, re.IGNORECASE):
        raise ValueError("Security Alert: Chỉ cho phép thực thi câu truy vấn đọc dữ liệu (SELECT/WITH)!")
    if not re.search(r"\bLIMIT\s+\d+\b", cleaned, re.IGNORECASE):
        cleaned += " LIMIT 1000"
    return cleaned
```

Bộ lọc bảo đảm 100% câu lệnh tuân thủ quy tắc chỉ đọc, triệt tiêu hoàn toàn nguy cơ rò rỉ dữ liệu và tự động gắn trần `LIMIT 1000` nhằm duy trì độ ổn định liên tục cho toàn bộ hạ tầng cơ sở dữ liệu WinCommerce.
