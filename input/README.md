# THƯ MỤC TIẾP NHẬN TÀI LIỆU ĐẦU VÀO (CENTRAL INPUT HUB)

Thư mục này dùng để tiếp nhận toàn bộ đề bài, tài liệu, đề cương và dữ liệu bài tập cho các Case Study.

---

## Quy tắc Phân loại Đầu vào (Input Organization Protocol)

Để tránh nhầm lẫn giữa các bài tập khác nhau:
1. **Theo từng Case Study / Dự án:**
   Mỗi case sẽ có một thư mục con riêng tương ứng:
   ```text
   input/
   ├── <CASE_ID>/                      # Ví dụ: input/CASE-001/
   │   ├── assignment/                 # Đề bài, rubric, hướng dẫn của giảng viên
   │   ├── templates/                  # Template mẫu Word (.docx), PowerPoint (.pptx)
   │   └── datasets/                   # Dữ liệu nguồn Excel (.xlsx), CSV, JSON
   ```
2. **Kéo thả trực tiếp:**
   - Bạn có thể kéo thả tài liệu trực tiếp vào `input/` hoặc vào `input/<CASE_ID>/`.
   - Khi kích hoạt `/session-start` hoặc `case-intake`, Agent sẽ tự động nhận diện và chuyển vào đúng case đang hoạt động.
