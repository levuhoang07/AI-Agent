# PHÂN TÍCH KHOẢNG TRỐNG HỆ THỐNG (GAP ANALYSIS)

**Thời gian audit:** 2026-11-06T00:52:55+07:00  
**Thực hiện bởi:** AI Workspace Architect & Quality Assurance Lead

---

## 1. Bảng đối chiếu Hiện trạng và Mục tiêu

| Hạng mục kiến trúc | Hiện trạng (AS-IS) | Mục tiêu (TO-BE) | Khoảng trống (GAP) | Mức ưu tiên | Hành động xử lý |
|---|---|---|---|---|---|
| **Cấu trúc thư mục** | Thư mục rỗng `D:\antigravity\AI-Agent PJ` | Chuẩn hóa theo thiết kế Phase 1 | Chưa có cây thư mục hoàn chỉnh | **P0** | Khởi tạo cấu trúc scaffolding chuẩn, phân tách `shared/`, `cases/`, `workspace-state/`, `.agents/`, `docs/`, `tests/` |
| **Session State Engine** | Chưa có cơ chế lưu trạng thái file-based | Bền vững qua file JSON, schema validation, checkpoint tự động | Hoàn toàn phụ thuộc vào bộ nhớ chat ngắn hạn | **P0** | Xây dựng engine `session-start`, `session-close`, `session-recovery`, atomic save file |
| **Case Isolation** | Chưa có | Mỗi case 1 thư mục riêng với state, input, analysis, output riêng biệt | Chưa có cơ chế quản lý đa case | **P0** | Xây dựng `workspace-registry.json` và case directory scaffolding |
| **Workspace Rules** | Chỉ có 2 rules global ở cấp máy tính | 7 rules đặc thù bám sát Case Study + AGENTS.md | Chưa có rules quản trị workspace cụ thể | **P0** | Tạo 7 file rules chuẩn YAML frontmatter trong `.agents/rules/` và `AGENTS.md` |
| **Agent Skills** | 0 Workspace Skills | 13 chuyên môn hóa từ Intake đến Deliverables | Thiếu toàn bộ runbooks nghiệp vụ | **P0 & P1** | Xây dựng đầy đủ 13 skills chuẩn Agent Skills Standard |
| **Document Specialist Engines** | Thư viện Python đã cài sẵn (`docx`, `openpyxl`, `pptx`, `pandas`) nhưng chưa có tooling tự động | Scripts tạo tài liệu, validate layout/formula/heading, template preservation | Chưa có helper scripts và schema validation | **P1** | Viết Python helper modules trong `shared/utilities/` cho DOCX, XLSX, PPTX |
| **Automated Quality Gates** | Chưa có kịch bản test | 10 Gates (G1 - G10) kiểm tra toàn diện | Chưa có test fixtures, test runner | **P0** | Viết test suite Python `tests/test_quality_gates.py` chạy qua `unittest` |
| **Tài liệu hướng dẫn** | Chưa có | `README.md`, `quick-start.md`, `workspace-architecture.md`, `maintenance.md` | Người dùng chưa có cẩm nang sử dụng | **P1** | Soạn thảo bộ tài liệu bàn giao chuẩn |

---

## 2. Đánh giá Rủi ro Kỹ thuật & Biện pháp Giảm thiểu

| Rủi ro kỹ thuật | Mức độ | Hậu quả tiềm ẩn | Biện pháp giảm thiểu (Mitigation Strategy) |
|---|---|---|---|
| **Windows NTFS File Lock** | Trung bình | Xung đột khi ghi đồng thời hoặc script ghi đè file đang mở | Áp dụng cơ chế Safe File Write: Ghi vào tệp tạm (`.tmp`), flush & fsync, sau đó dùng lệnh đổi tên nguyên tử (`os.replace`). |
| **Lỗi hỏng công thức Excel khi ghi đè** | Cao | Mất công thức, sai lệch số liệu học thuật | Nguyên tắc bảo toàn: Dữ liệu thô giữ nguyên tại sheet riêng (`Raw Data`); công thức tính tại sheet `Calculations`/`Summary`; luôn validate lại bằng script độc lập. |
| **Tràn chữ (Text Overflow) trong PPTX** | Trung bình | Slide vỡ layout, mất chữ khi nạp nội dung dài | Thuật toán kiểm tra số lượng ký tự trên shape, tỷ lệ khung hình, và cấu hình font size tự co giãn (fit-text heuristic) trong PPTX Specialist. |
| **Mất ngữ cảnh giữa các phiên (Context Drift)** | Cao | Mất thông tin bài tập khi mở phiên hội thoại mới | Độc lập hóa ngữ cảnh bằng file trạng thái `workspace-registry.json`, `active-session.json`, `session-state.json`, đọc báo cáo Session Opening ngay từ đầu phiên. |
| **Thiếu công cụ render trực quan CLI ngoài** | Thấp | Không thể xuất ảnh slide/word qua command-line bên ngoài | Thẩm định sâu cấu trúc DOM/XML (bảng, heading, công thức, số lượng slide) kết hợp cảnh báo phạm vi kiểm thử minh bạch. |

---

## 3. Kế hoạch Hành động Tổng thể

1. **Bước 1 (Approval Gate 0):** Báo cáo kết quả Audit và trình người dùng phê duyệt Kế hoạch Kiến trúc & Triển khai.
2. **Bước 2 (Phase 1 & 2):** Khởi tạo khung cấu trúc thư mục, khởi tạo `git init` cục bộ, viết `AGENTS.md` và 7 Rules trong `.agents/rules/`.
3. **Bước 3 (Phase 3 & 4):** Triển khai 13 Workspace Skills (`SKILL.md`) và các scripts helper DOCX/XLSX/PPTX trong `shared/utilities/`.
4. **Bước 4 (Phase 5 & 6):** Xây dựng Session Engine, Checkpoint Engine, Workspace Registry, Case Templates & Case Scaffolding.
5. **Bước 5 (Phase 7):** Chạy bộ Automated Quality Gates (G1 - G10) trên case giả lập `TEST-SESSION` và `TEST-ISOLATION`. Tạo `tests/results/bootstrap-test-report.md`.
6. **Bước 6 (Phase 8 & 9):** Hoàn thiện bộ tài liệu vận hành và lập Báo cáo Nghiệm thu Tổng kết (Handover Report).

