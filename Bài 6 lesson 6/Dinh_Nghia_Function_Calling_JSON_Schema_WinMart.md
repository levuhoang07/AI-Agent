# BÁO CÁO KỸ THUẬT: ĐỊNH NGHĨA FUNCTION CALLING JSON SCHEMA TẠI WINMART

- **Mã bài tập:** `AI301_S06_BTVN_M1_BT1` (Session 06)
- **Hệ thống:** Data Analytics Agent (Google Antigravity)
- **Đơn vị:** WinCommerce (Tập đoàn Masan)

---

## 1. Đặc tả Function Calling JSON Schema cho công cụ `query_store_sales`

Trong kiến trúc Data Analytics Agent, đặc tả công cụ (Tool Specification) đóng vai trò là cầu nối chuẩn mực chuyển hóa ngôn ngữ tự nhiên thành các lệnh truy vấn có cấu trúc an toàn. Nhằm hỗ trợ tác tử tự động tra cứu dữ liệu bán lẻ trên hệ thống hơn 3.600 siêu thị WinMart và WinMart+, hàm `query_store_sales` được khai báo bằng JSON Schema:

```json
{
  "name": "query_store_sales",
  "description": "Truy vấn doanh thu và số lượng bán lẻ tại siêu thị WinMart theo mốc thời gian và ngành hàng.",
  "parameters": {
    "type": "object",
    "properties": {
      "store_id": { "type": "string", "description": "Mã định danh siêu thị (ví dụ: WM_HN_TIMES_CITY)" },
      "start_date": { "type": "string", "pattern": "^\\\\d{4}-\\\\d{2}-\\\\d{2}$", "description": "Ngày bắt đầu (YYYY-MM-DD)" },
      "category_id": { "type": "string", "description": "Mã ngành hàng (ví dụ: FRESH_FOOD)" }
    },
    "required": ["store_id", "start_date"]
  }
}
```

Schema quy định chặt chẽ kiểu dữ liệu, bắt buộc hai tham số định danh cơ sở và ngày bắt đầu, đồng thời thiết lập mã ngành hàng ở trạng thái tùy chọn nhằm tối ưu hóa tính linh hoạt khi truy vấn tổng thể toàn cửa hàng.

## 2. Mô phỏng lời gọi hàm từ LLM (Function Call Simulation)

Khi người dùng gửi câu hỏi phân tích kinh doanh: *"Kiểm tra doanh thu ngành hàng Thực phẩm tươi sống tại siêu thị WinMart Times City từ ngày 01/10 đến 07/10/2024"*, mô hình LLM tự động trích xuất thực thể, tra cứu danh mục phân loại nội bộ và sinh cấu trúc gọi hàm chuẩn xác:

```json
{
  "name": "query_store_sales",
  "arguments": {
    "store_id": "WM_HN_TIMES_CITY",
    "start_date": "2024-10-01",
    "category_id": "FRESH_FOOD"
  }
}
```

Tác tử đã ánh xạ thành công tên siêu thị Times City thành mã kho `WM_HN_TIMES_CITY`, chuẩn hóa định dạng ngày sang `2024-10-01` và phân loại thực phẩm tươi sống vào nhóm ngành hàng `FRESH_FOOD`.

## 3. Đánh giá cơ chế xác thực tham số runtime (Parameter Validation)

Môi trường runtime của Agent thiết lập cơ chế kiểm định nghiêm ngặt trước khi lệnh truy vấn được chuyển tới cơ sở dữ liệu WinCommerce:

1. **Bắt lỗi định dạng (Format Enforcement):** Nếu LLM truyền sai định dạng ngày tháng như `01/10/2024`, trình kiểm định Pydantic / JSON Schema lập tức chặn lại thông qua ràng buộc biểu thức chính quy (Regex Pattern: `^\\d{4}-\\d{2}-\\d{2}$`).
2. **Bảo vệ hệ thống hạ tầng (System Protection):** Xác thực tại lớp đệm Agent giúp triệt tiêu lỗi cú pháp SQL, ngăn chặn nguy cơ tấn công SQL Injection và tránh nghẽn tải cơ sở dữ liệu phân tán của 3.600 điểm bán.
3. **Cơ chế tự sửa lỗi (Self-Correction Loop):** Khi phát sinh lỗi xác thực `ValidationError`, runtime tự động phản hồi thông điệp lỗi chi tiết cho LLM. Tác tử tiếp nhận lỗi, tự động điều chỉnh tham số về chuẩn `YYYY-MM-DD` và thực thi lại truy vấn thành công, bảo đảm tính ổn định và tự chủ tuyệt đối của Agent trong vận hành bán lẻ thực tế.
