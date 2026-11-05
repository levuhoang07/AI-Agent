# AI CASE STUDY WORKSPACE
## Hệ thống Quản trị & Tự động hóa Giải bài toán Tình huống bằng AI Agent

Workspace này được thiết kế chuyên biệt cho sinh viên và chuyên viên học tập, nghiên cứu môn **Ứng dụng AI Agent trong công việc**. Hệ thống cung cấp đầy đủ công cụ điều phối, quản lý vòng đời phiên làm việc bền vững (Durable Session Lifecycle), tuân thủ chuẩn mực học thuật và tự động hóa sản xuất tài liệu đa định dạng (**Word DOCX, Excel XLSX, PowerPoint PPTX**).

---

## 1. Cấu trúc Thư mục Chuẩn (Workspace Structure)

```text
D:\antigravity\AI-Agent PJ\
├── AGENTS.md                          # Identity & Hướng dẫn điều phối Agent
├── README.md                          # Hướng dẫn tổng quan Workspace
├── .agents/
│   ├── skills/                        # 13 Agent Skills (P0 & P1)
│   │   ├── session-start/             # [P0] Khởi tạo phiên, đối chiếu state, báo cáo
│   │   ├── session-close/             # [P0] Đóng phiên an toàn, kiểm tra deliverable
│   │   ├── session-recovery/          # [P0] Phục hồi phiên gián đoạn từ checkpoint
│   │   ├── case-intake/               # [P0] Tiếp nhận & bóc tách đề bài, rubric
│   │   ├── case-planning/             # [P0] Lập WBS, Task Board, rủi ro, DoD
│   │   ├── business-analysis/         # [P1] BA frameworks (AS-IS/TO-BE, BPMN, SWOT)
│   │   ├── research-validation/       # [P1] Nghiên cứu, fact-checking, taxonomy
│   │   ├── data-analysis/             # [P1] EDA, thống kê, KPI calculation
│   │   ├── agent-solution-design/     # [P1] Thiết kế kiến trúc AI Agent, prompt, eval
│   │   ├── docx-specialist/           # [P1] Soạn thảo báo cáo Word chuẩn mực
│   │   ├── xlsx-specialist/           # [P1] Xử lý bảng tính, công thức, bảo toàn dữ liệu
│   │   ├── pptx-specialist/           # [P1] Soạn slide thuyết trình, visual layout QA
│   │   └── deliverable-qa/            # [P1] QA chéo, đối chiếu nhất quán số liệu
│   └── rules/                         # 7 Workspace Rules có YAML frontmatter
│       ├── workspace-governance.md    # Ranh giới workspace, an toàn tệp tin
│       ├── case-isolation.md          # Cô lập tuyệt đối dữ liệu giữa các case
│       ├── data-integrity.md          # Chống bịa đặt dữ liệu (Zero Hallucination)
│       ├── evidence-policy.md         # Phân loại FACT, ASSUMPTION, INFERENCE, REC
│       ├── document-quality.md        # Tiêu chuẩn kỹ thuật DOCX, XLSX, PPTX
│       ├── session-governance.md      # Quy tắc mở/đóng phiên & checkpoint
│       └── academic-standards.md      # Chuẩn mực học thuật & rubric môn học
├── workspace-state/                   # Durable State Engine
│   ├── workspace-registry.json        # Danh mục quản trị toàn bộ các case
│   ├── active-session.json            # Trạng thái phiên hiện hành
│   ├── global-progress.md             # Bảng theo dõi tiến độ tổng thể
│   └── sessions/                      # Lịch sử các báo cáo đóng phiên
├── cases/                             # Thư mục lưu trữ các Case Study độc lập
│   ├── _template/                     # Khung mẫu chuẩn khi khởi tạo case mới
│   └── <CASE_ID>/                     # Từng case nghiên cứu riêng biệt
│       ├── input/                     # Đề bài, templates mẫu, datasets
│       ├── research/                  # Tài liệu nghiên cứu, trích dẫn
│       ├── analysis/                  # Phân tích nghiệp vụ, EDA, mô hình
│       ├── solution/                  # Đặc tả kiến trúc AI Agent
│       ├── output/                    # Bản thảo (draft) và bản nộp (final)
│       ├── qa/                        # Báo cáo kiểm định chất lượng
│       └── state/                     # Task board, decisions, session-state
├── shared/                            # Tài nguyên dùng chung
│   ├── utilities/                     # Engine safe_io, state_engine, docx, xlsx, pptx
│   └── schemas/                       # JSON schemas xác thực dữ liệu
├── tests/                             # Bộ kiểm thử tự động Gate G1 - G10
│   └── results/bootstrap-test-report.md # Báo cáo kiểm thử 100% PASS
└── docs/                              # Tài liệu kiến trúc và hướng dẫn vận hành
```

---

## 2. Hướng dẫn Vận hành Cơ bản (Operational Guide)

### 2.1. Bắt đầu Phiên Làm việc
Mở cuộc hội thoại mới trong Antigravity và gõ:
```text
/session-start
```
Agent sẽ tự động:
1. Đọc `workspace-registry.json` và xác định case đang làm dở hoặc case gần nhất.
2. Kiểm tra tính toàn vẹn của các file kết quả trên ổ cứng.
3. Xuất bảng **Session Opening Report** nêu rõ việc đã hoàn thành, việc dở dang và đề xuất kế hoạch thực hiện cho phiên mới.

### 2.2. Khởi tạo một Case Study mới
Khi nhận được bài tập từ giảng viên, cung cấp thông tin cho Agent hoặc yêu cầu:
```text
Tạo case mới mã CASE-001 tiêu đề "Tối ưu hóa Vận hành Bán lẻ XYZ bằng AI Agent"
```
Agent sẽ tự động nhân bản cấu trúc từ `cases/_template/`, đăng ký vào `workspace-registry.json` và thiết lập thư mục cô lập.

### 2.3. Cung cấp Tài liệu Đề bài & Templates
Copy các file của bài tập vào đúng vị trí:
- Đề bài, đề cương: `cases/<CASE_ID>/input/assignment/`
- Mẫu Word/PowerPoint của trường: `cases/<CASE_ID>/input/templates/`
- Tập dữ liệu (CSV/XLSX): `cases/<CASE_ID>/input/datasets/`

### 2.4. Thực thi các Bước Nghiệp vụ & Tạo Tài liệu
Kích hoạt các kỹ năng chuyên biệt:
- **Bóc tách đề bài:** Kích hoạt `case-intake`
- **Lập kế hoạch WBS & Task Board:** Kích hoạt `case-planning`
- **Phân tích nghiệp vụ (AS-IS/TO-BE, BPMN):** Kích hoạt `business-analysis`
- **Phân tích dữ liệu & EDA:** Kích hoạt `data-analysis`
- **Thiết kế kiến trúc AI Agent:** Kích hoạt `agent-solution-design`
- **Tạo báo cáo Word chuẩn mực:** Kích hoạt `docx-specialist`
- **Tạo bảng tính Excel & Biểu đồ:** Kích hoạt `xlsx-specialist`
- **Tạo slide thuyết trình PowerPoint:** Kích hoạt `pptx-specialist`
- **Kiểm định chéo tính nhất quán số liệu:** Kích hoạt `deliverable-qa`

### 2.5. Đóng Phiên An toàn
Khi hoàn thành buổi làm việc, gõ:
```text
/session-close
```
Agent sẽ đối chiếu task board, kiểm tra sự tồn tại thực tế của các file sản phẩm, lưu trữ báo cáo Markdown vào `cases/<CASE_ID>/state/sessions/` và đóng phiên an toàn.

---

## 3. Các Chốt chặn Phê duyệt (Approval Gates)
Để đảm bảo người dùng luôn kiểm soát tiến độ và giải pháp, Agent luôn dừng lại để xin phê duyệt tại:
- **Gate A — Scope Approval:** Thống nhất phạm vi đề bài và danh sách sản phẩm bàn giao.
- **Gate B — Solution Approval:** Phê duyệt kiến trúc AI Agent và mô hình kinh tế trước khi viết báo cáo.
- **Gate C — Deliverable Approval:** Xem xét và chốt bản thảo cuối trước khi nộp bài.
- **Gate D — High-Risk Operation:** Cảnh báo trước các thao tác ghi đè hoặc thay đổi lớn.

---

## 4. Kết quả Kiểm định Chất lượng (Quality Gates)
Hệ thống đã vượt qua toàn bộ 10 Quality Gates (G1 - G10) với tỷ lệ đạt **100% PASS**:
- Chi tiết xem tại: [bootstrap-test-report.md](file:///d:/antigravity/AI-Agent%20PJ/tests/results/bootstrap-test-report.md)

