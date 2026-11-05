# THƯ MỤC LƯU TRỮ SẢN PHẨM ĐẦU RA (CENTRAL OUTPUT HUB)

Thư mục này là nơi tập trung các sản phẩm bàn giao cuối cùng (Báo cáo Word, Bảng tính Excel, Slide PowerPoint) của tất cả các Case Study.

---

## QUY TẮC BẮT BUỘC: PHÂN TÁCH THEO TỪNG DỰ ÁN / CASE STUDY

> [!IMPORTANT]
> **Tuyệt đối KHÔNG lưu file trực tiếp tại thư mục gốc `output/`.**  
> Mọi sản phẩm bàn giao bắt buộc phải được chia vào các thư mục con riêng biệt theo mã Case/Dự án để tránh lẫn lộn và phục vụ tra cứu sau này.

### Cấu trúc Phân nhánh Chuẩn:
```text
output/
├── <CASE_ID_1>/                       # Ví dụ: output/CASE-001/
│   ├── final/                         # Sản phẩm hoàn chỉnh chính thức để nộp
│   │   ├── CASE-001_Bao_Cao.docx
│   │   ├── CASE-001_Mo_Hinh_Tai_Chinh.xlsx
│   │   └── CASE-001_Slide_Thuyet_Trinh.pptx
│   └── draft/                         # Các bản thảo sơ bộ trong quá trình làm
│
├── <CASE_ID_2>/                       # Ví dụ: output/CASE-002/
│   ├── final/
│   └── draft/
```

- **Quy tắc đặt tên file:** Luôn gắn tiền tố mã case (ví dụ: `CASE-001_...`) vào tên file sản phẩm.
- **Tính độc lập:** Sản phẩm của Case A tuyệt đối không ghi đè hoặc nằm chung với Case B.

