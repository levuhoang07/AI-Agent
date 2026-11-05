# CẨM NANG VẬN HÀNH NHANH (QUICK START GUIDE)

**Áp dụng cho:** Bắt đầu giải một bài tập Case Study mới hoặc tiếp tục phiên làm việc trong Antigravity.

---

## 1. Quy trình Vận hành 8 Bước Tiêu chuẩn

```text
1. Khởi động Workspace
   Mở Antigravity tại thư mục: D:\antigravity\AI-Agent PJ

2. Bắt đầu phiên làm việc
   Gõ lệnh: /session-start

3. Lựa chọn hoặc Khởi tạo Case Study
   - Tiếp tục case đang dang dở, HOẶC
   - Nhập đề bài mới: "Tạo case CASE-001 [Tên đề bài]"

4. Nạp dữ liệu và tài liệu đầu vào
   - Kéo thả file đề bài vào: cases/<CASE_ID>/input/assignment/
   - Kéo thả file template Word/PPTX vào: cases/<CASE_ID>/input/templates/
   - Kéo thả dữ liệu CSV/Excel vào: cases/<CASE_ID>/input/datasets/

5. Xem xét Kế hoạch & Duyệt Scope (Gate A)
   - Agent kích hoạt case-intake và case-planning
   - Phê duyệt phạm vi và danh sách sản phẩm bàn giao (Deliverables Checklist)

6. Triển khai Nghiệp vụ & Duyệt Giải pháp (Gate B)
   - Agent thực hiện business-analysis, data-analysis, agent-solution-design
   - Phê duyệt kiến trúc AI Agent và mô hình tài chính (ROI, Payback)

7. Sản xuất Tài liệu & Kiểm định Chất lượng (Gate C)
   - Agent tạo Word (DOCX), Excel (XLSX), Slide (PPTX)
   - Agent chạy deliverable-qa kiểm tra chéo số liệu
   - Duyệt bản thảo hoàn chỉnh tại cases/<CASE_ID>/output/final/

8. Đóng phiên an toàn & Lưu trữ bàn giao
   Gõ lệnh: /session-close
   - Hệ thống lưu báo cáo Markdown phiên làm việc
   - Trạng thái được bảo toàn cho phiên tiếp theo
```

---

## 2. Các Lệnh Điều phối Cốt lõi (Slash Commands & Trigger Phrases)

| Lệnh gọi / Trigger | Mục đích sử dụng | Đầu ra chính |
|---|---|---|
| `/session-start` | Khởi tạo phiên, đọc state cũ, báo cáo tiến độ | `SESSION OPENING REPORT` |
| `/session-close` | Kiểm tra nghiệm thu, đóng phiên an toàn | `SESSION CLOSING REPORT` (`.md`) |
| `/session-recovery` | Khôi phục phiên bị ngắt hoặc crash | `SESSION RECOVERY REPORT` |
| "Case Intake" | Tiếp nhận đề bài, bóc tách rubric | `case-manifest.json` cập nhật |
| "Case Planning" | Lập WBS, tiêu chí nghiệm thu | `task-board.md` cập nhật |
| "Business Analysis" | Phân tích AS-IS/TO-BE, BPMN, SWOT | Báo cáo phân tích nghiệp vụ |
| "Agent Solution Design" | Thiết kế kiến trúc AI Agent | Đặc tả kiến trúc kỹ thuật |
| "DOCX Specialist" | Soạn thảo báo cáo Word chuẩn | File `.docx` hoàn chỉnh |
| "XLSX Specialist" | Dựng bảng tính Excel, công thức, chart | File `.xlsx` hoàn chỉnh |
| "PPTX Specialist" | Dựng slide trình chiếu 16:9 | File `.pptx` hoàn chỉnh |
| "Deliverable QA" | Kiểm tra chéo tính nhất quán số liệu | `qa-signoff-report.md` |

