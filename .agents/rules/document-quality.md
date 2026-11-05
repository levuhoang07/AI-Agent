---
description: "Document Quality Rule: Sets formatting, visual layout, heading hierarchy, and data consistency standards for DOCX, XLSX, and PPTX"
trigger: always_on
---

# RULE 05 — DOCUMENT QUALITY & CONSISTENCY

## 1. Tiêu chuẩn Báo cáo Word (DOCX Quality Standards)
- **Cấu trúc phân cấp:** Bắt buộc tuân thủ cấp độ Heading chặt chẽ (Title → Heading 1 → Heading 2 → Heading 3). Không nhảy cấp tiêu đề tùy tiện.
- **Trang bìa & Bảng mục lục:** Báo cáo chính thức phải có trang bìa chuẩn mực và mục lục tự động khi dung lượng trên 5 trang.
- **Bảng biểu (Tables):** Mọi bảng dữ liệu phải có Header Row được định dạng nổi bật, căn lề số liệu sang phải, căn lề văn bản sang trái; có số thứ tự và tiêu đề bảng (`Bảng X: ...`).
- **Hình ảnh & Đồ họa:** Phải có chú thích (`Hình X: ...`), tỷ lệ khung hình không bị méo lệch, độ phân giải sắc nét.
- **Bảo toàn Template:** Khi người dùng cung cấp mẫu Word của trường/khoa, giữ nguyên lề giấy (margins), headers, footers, font chữ quy định và logo chuẩn.

## 2. Tiêu chuẩn Bảng tính Excel (XLSX Quality Standards)
- **Cấu trúc Workbook:** Phân tách rõ ràng giữa `Raw Data`, `Cleaned Data`, `Calculations`, và `Executive Dashboard`.
- **Định dạng số liệu:** Số tiền, tỷ lệ %, ngày tháng phải có định dạng rõ ràng (ví dụ: `#,##0 VNĐ`, `0.0%`).
- **Độ chính xác công thức:** Không để xảy ra các lỗi công thức Excel phổ biến như `#REF!`, `#DIV/0!`, `#VALUE!`, `#N/A`.
- **Biểu đồ (Charts):** Đồ thị phải có tiêu đề, chú giải (Legend), nhãn trục (Axis Labels) và liên kết chính xác với vùng dữ liệu nguồn.

## 3. Tiêu chuẩn Thuyết trình PowerPoint (PPTX Quality Standards)
- **Quy tắc Thiết kế:** Bố cục tối giản, phân cấp thị giác rõ ràng, tuân thủ bảng màu đồng nhất (Color Palette).
- **Tránh tràn chữ (Text Overflow Prevention):** Không nhồi nhét quá nhiều chữ trong một hộp văn bản; giới hạn 5-7 dòng gạch đầu dòng mỗi slide; kiểm soát kích thước font tối thiểu 14pt cho body text.
- **Bảo toàn Slide Master:** Giữ nguyên tỷ lệ trình chiếu (16:9), slide layout của giảng viên, vị trí đặt logo và số trang slide.

## 4. Tính Nhất quán Đa định dạng (Cross-Format Consistency)
- Các số liệu kinh doanh trọng yếu (Doanh thu, Chi phí, ROI, Thời gian hoàn vốn, Số lượng nhân sự, v.v.) phải **hoàn toàn trùng khớp** giữa báo cáo chi tiết Word, mô hình bảng tính Excel và slide thuyết trình PowerPoint.
- Cùng một nguồn dữ liệu (Single Source of Truth) từ `analysis/` hoặc `shared/` phải là cơ sở tính toán duy nhất cho cả ba định dạng tài liệu.
