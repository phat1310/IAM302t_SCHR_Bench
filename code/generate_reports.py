# -*- coding: utf-8 -*-
"""
Script to generate:
1. G7_Bao_Cao_Tien_Do_Va_Ke_Hoach_RBL.md
2. G7_Bao_Cao_Tien_Do_Va_Ke_Hoach_RBL.docx

Cập nhật chính xác:
- Thời điểm: Cuối Tuần 5 (Cuối W5 / Chuyển giao sang W6).
- Phase 1 (W1-W2: D1) và Phase 2 (W3-W4: D2) ĐÃ HOÀN THÀNH 100%.
- Phase 3 (W5-W6) đang triển khai ở cuối W5 (đạt ~80% tiến độ Phase 3).
- Phân công thành viên chuẩn hóa:
  * Trưởng nhóm (Group Leader): Nguyễn Tấn Phát (SE173285)
  * Thành viên 1: Đỗ Thiện Nhân (SE194134) - C/Binary & Mutation Engineer (Phụ trách D2 - Đã hoàn thành)
  * Thành viên 2: Nguyễn Tấn Phát (SE173285) & Nguyễn Trọng Duy (SE194413) - Decompiler & MCP Pipeline Engineers (Phụ trách Live Demo D3)
  * Thành viên 3: Nguyễn Trọng Duy (SE194413) - Metrics & Automated Evaluation Specialist (Phụ trách D3/D4)
  * Thành viên 4: Võ Hồng Phúc (SE203844) - Statistical Analyst, Qualitative Evaluator & Lead Author (Phụ trách Thống kê, Mẫu Gh0stRAT & Paper)
"""

import os
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls

OUT_DIR = r"D:\ATTT\ATTT_FPT\KY_5_FALL_2026\IAM302t\05_Du_An_Nhom_IAM302t\G7_IAM302t_IA2007"
MD_PATH = os.path.join(OUT_DIR, "G7_Bao_Cao_Tien_Do_Va_Ke_Hoach_RBL.md")
DOCX_PATH = os.path.join(OUT_DIR, "G7_Bao_Cao_Tien_Do_Va_Ke_Hoach_RBL.docx")

MD_CONTENT = r"""# BÁO CÁO TIẾN ĐỘ & KẾ HOẠCH TRIỂN KHAI CHI TIẾT ĐỀ TÀI RBL
## HỌC KỲ FALL 2026 — MÔN HỌC: IAM302T (MALWARE ANALYSIS & REVERSE ENGINEERING)
### 📍 MỐC BÁO CÁO: CUỐI TUẦN 5 (W5) — BƯỚC SANG TUẦN 6 (W6)

---

**Cơ sở đào tạo:** Trường Đại học FPT — Phân hiệu TP. Hồ Chí Minh  
**Bộ môn:** An toàn Thông tin (Information Assurance)  
**Lớp học phần:** IA2007  
**Nhóm sinh viên thực hiện:** Nhóm 7 (G7)  
**Giảng viên hướng dẫn:** Thầy Đinh Mai Hoàng (DINHMH)  
**Tên đề tài chính thức:** **SCHR-Bench: Đo Lường Hallucination Security-Critical của LLM trong Reverse Engineering bằng Ground Truth từ Binary Mutation**  
*(Đã chuẩn hóa và thu hẹp trọng tâm nghiên cứu theo văn bản định hướng của Giảng viên)*  

---

## 👥 THÀNH VIÊN VÀ PHÂN CÔNG VAI TRÒ NHÓM 7

| STT | Họ và Tên | Mã số SV | Vai trò chính trong dự án | Trách nhiệm cốt lõi & Deliverables phụ trách |
| :---: | :--- | :---: | :--- | :--- |
| 1 | **Nguyễn Tấn Phát** | SE173285 | **Project Leader & MCP Pipeline Co-Engineer** *(Trưởng nhóm)* | • Điều phối toàn diện tiến độ 10 tuần RBL và làm việc với GVHD.<br>• Cùng Duy phụ trách xây dựng MCP Pipeline kết nối Ghidra Headless với LLM APIs & Ollama.<br>• Phân tích định tính mẫu Gh0stRAT và tổng hợp nộp D1–D5 & Paper. |
| 2 | **Đỗ Thiện Nhân** | SE194134 | **Thành viên 1: C/Binary & Mutation Engineer** | • Xây dựng toàn bộ dataset 40 hàm C security-critical (Anti-debug, Decryption, Persistence, Anti-VM).<br>• Cài đặt 5 toán tử Binary Mutation; biên dịch qua GCC/MSVC + OLLVM 3 mức độ.<br>• Chạy kiểm thử E0 (loại bỏ mutation trung tính). **Đã hoàn thành xuất sắc D2**. |
| 3 | **Nguyễn Trọng Duy** | SE194413 | **Thành viên 2 & 3: Pipeline & Metrics Specialist** | • Cùng Phát viết script Ghidra Headless tự động hóa decompile pseudocode/ASM và cấu hình MCP Server.<br>• Quản lý giao thức Context Escalation (CT1–CT4).<br>• Thiết kế bộ câu hỏi MCQ Mutation-Aware (Gold Set); viết Python script tự động đo SCHR, BLEU, Recompilability. Phụ trách **Live Demo D3 & D4**. |
| 4 | **Võ Hồng Phúc** | SE203844 | **Thành viên 4: Statistical Analyst & Lead Author** | • Thực hiện các kiểm định thống kê chuyên sâu: McNemar Test (so sánh cặp context) và Wilson Confidence Interval cho SCHR.<br>• Phân loại lỗi chất lượng (Missed mutation, Fabricated API).<br>• Đồng tác giả chủ trì biên soạn Báo cáo D3–D5 và bài báo khoa học chuẩn IEEE/Q1. |

---

## I. TỔNG QUAN ĐỀ TÀI & ĐIỀU CHỈNH HƯỚNG ĐI THEO ĐỊNH HƯỚNG CỦA GIẢNG VIÊN

### 1. Quá trình tiếp thu phản hồi và tái cấu trúc đề tài
- **Ý tưởng ban đầu (Proposal D1):** Nhóm đề xuất mô hình *Multi-Engine Consensus Analysis (kết hợp Ghidra + IDA Pro qua MCP Agent và Context Escalation 4 tầng trên mã độc Gh0stRAT)*. Tuy nhiên, theo văn bản định hướng chi tiết của Thầy Đinh Mai Hoàng, nhóm nhận thấy một số thách thức kỹ thuật lớn:
  1. Phụ thuộc vào license thương mại IDA Pro (không phù hợp triển khai rộng rãi trong môi trường lab học thuật).
  2. Việc phân tích trực tiếp mẫu malware bị pack nặng bởi VMProtect khiến decompiler chỉ sinh ra mã giả vô nghĩa, gây rủi ro an toàn và không tạo được ground truth rõ ràng.
  3. Thiếu một thước đo định lượng độc lập để đánh giá liệu LLM "thật sự hiểu sâu luồng điều khiển" hay chỉ "đoán mò theo quán tính".
- **Điều chỉnh trọng tâm sang SCHR-Bench (Chủ đề 3):**
  - Nhóm đã chuyển hướng toàn diện sang đề tài **SCHR-Bench (Security-Critical Hallucination Rate Benchmark)**.
  - Sử dụng phương pháp **Binary Mutation Testing** trên tập các hàm C tự viết làm Ground Truth tuyệt đối, kết hợp công cụ dịch ngược mã nguồn mở **Ghidra Headless**.
  - Đây là hướng đi khoa học chuẩn mực, an toàn tuyệt đối (không kích hoạt malware sống), loại bỏ hoàn toàn sự phụ thuộc vào IDA Pro và VMProtect, đảm bảo tính khả thi cao và chuẩn đầu ra bài báo IEEE/Q1.

### 2. Định vị học thuật: Khác biệt rõ ràng giữa SCHR-Bench (Nhóm 7) và VeRA (Nhóm 1)

| Tiêu chí so sánh | Đề tài VeRA (Nhóm 1) | Đề tài SCHR-Bench (Nhóm 7) |
| :--- | :--- | :--- |
| **Bản chất Ground Truth** | Code tự viết + Test vector thực thi động thông thường. | **Binary Mutation có kiểm soát**: Thay đổi chính xác 1 yếu tố an ninh cốt lõi giữa bản gốc và đột biến. |
| **Câu hỏi cốt lõi** | "Bao nhiêu claim của LLM là đúng/sống sót qua kiểm chứng?" *(Đúng hay Sai)* | **"LLM có nhận ra sự thay đổi nguy hiểm (security-critical) hay bỏ sót và đoán mò theo thói quen?"** |
| **Trọng tâm đóng góp** | Bộ Verifier tĩnh + động kiểm tra từng atomic claim. | **Hệ thống đo lường chuyên biệt (Metric SCHR)** vạch trần hạn chế của BLEU & Recompilability. |

### 3. Bốn Câu hỏi Nghiên cứu (RQ) và Bốn Giả thuyết Khoa học (H)
* **RQ1:** Khi một hàm security-critical bị đột biến (đảo điều kiện anti-debug, đổi hằng số khóa XOR, thay đổi API persistence), LLM có nhận ra sự thay đổi hành vi không, hay tiếp tục lặp lại mô tả rập khuôn của bản gốc? *(Đo bằng chỉ số SCHR).*
* **RQ2:** Chỉ số SCHR có gì vượt trội so với các thước đo truyền thống như BLEU score hay Tỷ lệ biên dịch lại (Recompilability)? SCHR có bắt được những sai sót chết người mà các thước đo trên bỏ sót không? *(So sánh trực tiếp SCHR với BLEU và Recompilability).*
* **RQ3:** Việc cung cấp thêm mã máy Assembly (mỏ neo ground truth) và mô tả API trong giao thức Context Escalation có giúp giảm SCHR so với việc chỉ cấp mã giả (pseudocode) hay không? *(Đo SCHR biến thiên qua 4 cấp độ ngữ cảnh CT1 $\rightarrow$ CT4).*
* **RQ4:** Các kỹ thuật làm rối mã ở mức nhẹ và trung bình (Control-Flow Flattening, String Encryption qua OLLVM) làm tỷ lệ ảo giác SCHR gia tăng ở mức độ nào? *(Đo SCHR theo 4 mức Obfuscation từ Mức 0 đến Mức 3).*

**Các giả thuyết khoa học tương ứng:**
- **H1:** LLM có xu hướng bỏ sót mutation rất cao, đặc biệt là lỗi đảo điều kiện logic (LLM giải thích theo "khuôn mẫu đã học" của hàm anti-debug thay vì nhìn vào câu lệnh rẽ nhánh thực tế).
- **H2:** Chỉ số BLEU gần như không đổi giữa bản gốc và bản mutation (do từ vựng tương tự), trong khi mã biên dịch lại được vẫn có thể sai hoàn toàn luồng dữ liệu. SCHR phản ánh chính xác sai khác an ninh này.
- **H3:** Bổ sung Assembly (CT2, CT3) làm giảm SCHR đáng kể vì buộc LLM phải đối chiếu logic máy thay vì suy diễn cảm tính từ mã C giả bị lỗi thời của decompiler.
- **H4:** Obfuscation làm méo mó mã giả của Ghidra, khiến LLM mất phương hướng và đẩy SCHR tăng vọt.

---

## II. THIẾT KẾ GIẢI PHÁP KỸ THUẬT & HỆ THỐNG THỰC NGHIỆM

### 1. Kiến trúc Pipeline Thực nghiệm Độc lập (End-to-End Architecture)
Hệ thống thử nghiệm SCHR-Bench được thiết kế thành một chuỗi khép kín, tự động hóa bằng Python và Ghidra Headless:

```
[40 C Security Functions] (Tự viết)
       │ (Cài đặt 5 Mutation Operators)
       ▼
[Original & Mutated Source] ──(MSVC / GCC + OLLVM 0-3)──► [Stripped Binaries]
                                                                  │
                                                                  ▼
                                                      [Ghidra Headless Analyzer]
                                                                  │
                                            ┌─────────────────────┴─────────────────────┐
                                            ▼                                           ▼
                                   [Ghidra Pseudocode]                         [Raw Assembly Listings]
                                            └─────────────────────┬─────────────────────┘
                                                                  │
                                                                  ▼
                                                      [MCP Context Generator]
                                                      (CT1: Pseudo | CT2: +Asm | CT3: +API | CT4: +Neighbor)
                                                                  │
                                                                  ▼
                                                      [LLM Inference Engine]
                                                      (Ollama LLaMA-3 / Qwen2.5-Coder 14B)
                                                                  │
                                            ┌─────────────────────┴─────────────────────┐
                                            ▼                                           ▼
                                  [Layer 1: Auto-MCQ Evaluator]              [Layer 2: Free-form Evaluator]
                                  (Khớp đáp án trắc nghiệm)                  (FActScore Claim + Cohen's Kappa)
                                            └─────────────────────┬─────────────────────┘
                                                                  │
                                                                  ▼
                                                      [Statistical Analysis Module]
                                                      (SCHR %, Miss Rate, BLEU, McNemar Test, Wilson CI)
```

### 2. Định nghĩa Binary Mutation Operators (Được điều chỉnh riêng cho Binary RE)
Nhóm thiết kế riêng 5 toán tử đột biến đặc thù cho mã nhị phân Windows PE:
1. **Đảo điều kiện logic (Invert Condition):** Chuyển `if (IsDebuggerPresent())` $\rightarrow$ `if (!IsDebuggerPresent())`. Logic an ninh bị đảo ngược hoàn toàn.
2. **Thay đổi hằng số mã hóa (Alter Constant):** Đổi khóa XOR (`0x5A` $\rightarrow$ `0xA5`) hoặc thay đổi chu kỳ CPU `rdtsc`.
3. **Thay đổi API hệ thống (Substitute API):** Đổi `RegSetValueEx` $\rightarrow$ `RegDeleteValue`. Đảo ngược hành vi persistence từ thêm mới sang gỡ bỏ.
4. **Thay đổi toán tử quan hệ (Relational Operator Mutation):** Đổi `>` thành `<=`, `==` thành `!=`. Gây sai lệch điều kiện biên giải mã shellcode.
5. **Loại bỏ bước phòng thủ (Omit Defense Step):** Xóa bỏ một tầng kiểm tra `CheckRemoteDebuggerPresent` trong chuỗi phòng thủ nhiều lớp.

### 3. Phân tầng Ngữ cảnh (Context Escalation Levels - CT1 đến CT4)
- **CT1 (Baseline):** Chỉ cung cấp mã giả C (pseudocode) do Ghidra trích xuất.
- **CT2 (Ground Truth Assembly Anchor):** Cung cấp mã giả Ghidra + Toàn bộ Disassembly Assembly của hàm.
- **CT3 (Context Enrichment):** Cung cấp CT2 + Bản tóm tắt đặc tả các Windows API xuất hiện trong hàm.
- **CT4 (Extended Neighborhood Context):** Cung cấp CT3 + Mã assembly của các hàm lân cận và bảng cross-references (X-refs).

### 4. Thiết kế Chuỗi Thí nghiệm Thực nghiệm (E0 $\rightarrow$ E5, E6)

| Mã TN | Mục tiêu nghiên cứu | Dữ liệu đầu vào & Phương pháp | Trạng thái thực tế (Cuối W5) |
| :---: | :--- | :--- | :---: |
| **E0** | **Kiểm tra dữ liệu (Sanity Check)** | Chạy Test Vectors thực thi trên bản gốc và mutation; kiểm tra khả năng decompile của Ghidra. | **ĐÃ HOÀN THÀNH 100% (W4)**<br>100% mutation gây đổi hành vi thực tế; loại sạch mutation trung tính. |
| **E1** | **Đo SCHR Cơ sở (RQ1)** | Cấp ngữ cảnh CT1 cho LLM; đo tỷ lệ mô tả sai hoặc bỏ sót mutation trên tập hàm. | **ĐÃ HOÀN THÀNH LƯỢT 1 (W5)**<br>Đã có kết quả sơ bộ trên LLaMA-3: SCHR đảo điều kiện đạt >40%. |
| **E2** | **So sánh Thước đo (RQ2)** | Tính điểm BLEU score giữa câu trả lời bản gốc và mutation; đo tỷ lệ Recompilability. | **ĐANG TRIỂN KHAI (W5–W6)**<br>Script đã lập trình xong; đang nạp dữ liệu từ log E1. |
| **E3** | **Hiệu quả Ngữ cảnh (RQ3)** | Đánh giá SCHR biến thiên qua các tầng ngữ cảnh CT1, CT2, CT3, CT4. | **ĐANG CHẠY LOGS (W5–W6)**<br>Đang chạy batch inference trên LLaMA-3 và Qwen2.5-Coder 14B. |
| **E4** | **Tác động Obfuscation (RQ4)** | Biên dịch mã ở 4 mức (Không làm rối, Flattening, String Encrypt, Kết hợp). | **SẴN SÀNG CHẠY (W6)**<br>Binaries OLLVM đã chuẩn bị xong từ Phase 2. |
| **E5** | **Gold Set & Đánh giá Tự do** | 100–150 cặp câu hỏi; tách atomic claims kiểu FActScore; 2 người chấm độc lập. | **CHUẨN BỊ CHO W7**<br>Đã soạn xong 120 cặp câu hỏi; chuẩn bị rubric chấm độc lập. |
| **E6** | **Mở rộng Đa Decompiler** *(Tùy chọn)* | Đối chiếu mã giả giữa Ghidra và RetDec / Binary Ninja Education. | **GIAI ĐOẠN DỰ PHÒNG (W8)** |

---

## III. BÁO CÁO TIẾN ĐỘ THỰC HIỆN ĐẾN CUỐI TUẦN 5 (W5)

Nhóm 7 xin báo cáo với Thầy Đinh Mai Hoàng chi tiết tình trạng thực hiện các hạng mục công việc tính đến **hết Tuần 5**:

### 1. Phase 1 (W1–W2): Lab Setup & Proposal — ĐÃ HOÀN THÀNH 100%
- ✅ Hoàn thành và nộp **Deliverable D1 (Proposal & Lab Setup Report)**.
- ✅ Cấu hình thành công lab Ghidra Headless Analyzer 11.x và môi trường suy luận cục bộ Ollama (LLaMA-3 8B).
- ✅ Khảo sát và bóc tách dữ liệu mẫu thực tế Gh0stRAT PE32 (`ea7cd59c...`) từ MalwareBazaar.

### 2. Phase 2 (W3–W4): Data & Mutation — ĐÃ HOÀN THÀNH 100% (NGHIỆM THU D2)
- ✅ **Xây dựng Dataset 40 hàm C Security-Critical:** Thành viên 1 (Nhân) đã hoàn thành trọn vẹn 40 hàm C thuộc 4 nhóm chính:
  1. *Anti-Debugging:* `IsDebuggerPresent`, `CheckRemoteDebuggerPresent`, `NtGlobalFlag`, RDTSC timing checks.
  2. *String Decryption:* XOR cipher với khóa cố định, RC4, Base64 tùy biến.
  3. *Persistence:* Registry Run Key (`RegSetValueEx`), Scheduled Task, Windows Service registration.
  4. *Anti-VM / Environment:* Kiểm tra thanh ghi CPUID, MAC address ảo hóa, phát hiện tiến trình phân tích.
- ✅ **Cài đặt 5 Binary Mutation Operators & Obfuscation:** Thành viên 1 (Nhân) đã áp dụng thành công các toán tử đột biến và biên dịch qua GCC/MSVC strip symbols kết hợp OLLVM ở 4 cấp độ (Mức 0 đến Mức 3).
- ✅ **Thí nghiệm E0 (Sanity Check Protocol):** 100% các cặp hàm đã được kiểm tra qua test harness thực thi; xác nhận tất cả biến thể đều gây ra sự sai lệch hành vi rõ rệt (loại bỏ hoàn toàn đột biến trung tính).
- ✅ **Nộp Deliverable D2:** Đã hoàn thành và nộp đúng hạn **Báo cáo Phân tích Tĩnh (Static Analysis Report — chiếm 8% điểm tổng kết)** kèm theo toàn bộ source code và stripped binaries.

### 3. Phase 3 (W5–W6): Pipeline & Baselines — ĐANG TRIỂN KHAI TÍCH CỰC Ở CUỐI W5 (~80%)

| Hạng mục công việc | Thành viên phụ trách | Tiến độ (Cuối W5) | Chi tiết kết quả đạt được |
| :--- | :---: | :---: | :--- |
| **Ghidra Headless Automation & JSON Parser** | Nguyễn Tấn Phát & Nguyễn Trọng Duy | **100%** | Script Python/Jython đã tự động hóa decompile toàn bộ dataset, trích xuất chính xác mã C pseudocode và assembly instructions thành file JSON chuẩn. |
| **MCP Server & Pipeline gọi LLM (Ollama LLaMA-3.1 & Qwen2.5-Coder)** | Nguyễn Tấn Phát & Nguyễn Trọng Duy | **90%** | Hoàn thành pipeline kết nối MCP Server với Ollama (LLaMA-3) và Ollama (Qwen2.5-Coder 14B). Prompt template cố định, nhiệt độ kiểm soát ở `temperature=0`, cơ chế strip symbol và giấu nhãn mutation hoạt động hoàn hảo. |
| **Cơ chế Context Escalation (CT1 $\rightarrow$ CT4)** | Nguyễn Trọng Duy & Nguyễn Tấn Phát | **85%** | Đã dựng xong module cấp context tự động theo 4 cấp độ: CT1 (Chỉ C), CT2 (+ASM), CT3 (+API Description), CT4 (+Hàm lân cận & X-refs). |
| **Chạy Thí nghiệm E1 (SCHR cơ sở CT1)** | Nguyễn Trọng Duy & Nguyễn Tấn Phát | **100% (Lượt 1)** | Đã chạy xong lượt 1 trên toàn bộ 40 hàm. Kết quả sơ bộ: LLM có SCHR rất cao ở lỗi đảo điều kiện (SCHR > 40%), chứng minh mạnh mẽ Giả thuyết H1! |
| **Chạy Thí nghiệm E3 (Context Escalation CT1 $\rightarrow$ CT4)** | Nguyễn Tấn Phát & Nguyễn Trọng Duy | **70%** | Đang chạy batch suy luận trên LLaMA-3 và Qwen2.5-Coder 14B để thu thập toàn bộ log thực nghiệm. |
| **Script Đo đạc Metrics (SCHR, BLEU, Recompilability)** | Nguyễn Trọng Duy (Thành viên 3) | **85%** | Script Python tự động phân tích output JSON, tính điểm SCHR theo từng operator, tích hợp NLTK tính BLEU score đối chứng. |
| **Chuẩn bị Gold Set 120 cặp & Rubric Chấm FActScore** | Nguyễn Trọng Duy & Võ Hồng Phúc | **80%** | Đã hoàn thành 120 cặp câu hỏi MCQ Mutation-Aware; xây dựng bảng tiêu chí phân rã atomic claims cho Thí nghiệm E5. |
| **Thiết lập Khung Kiểm định Thống kê & Mẫu Gh0stRAT** | Võ Hồng Phúc (Thành viên 4) | **75%** | Đã viết script tính McNemar Test và Wilson CI; chuẩn bị ma trận đối chiếu định tính các kỹ thuật của mẫu Gh0stRAT với dataset. |

---

## IV. LỘ TRÌNH TRIỂN KHAI 10 TUẦN CẬP NHẬT (THEO SYLLABUS RBL)

```
W1–W2 (Phase 1)          W3–W4 (Phase 2)          W5–W6 (Phase 3)          W7–W8 (Phase 4)          W9–W10 (Phase 5)
[ Lab & Proposal ]  ──►  [ Data & Mutation ]  ──►  [ Pipeline & Base ]  ──►  [ Eval & Gold Set ]  ──►  [ Paper & Defense ]
  (D1: HOÀN THÀNH)         (D2: HOÀN THÀNH)         (Hiện tại: Cuối W5)      (Nộp D3 & Live Demo)     (Nộp D4: 10% | D5: 30%)
```

### Bảng kế hoạch chi tiết từng tuần:

| Tuần | Giai đoạn RBL | Nội dung công việc chi tiết | Sản phẩm đầu ra & Trạng thái |
| :---: | :--- | :--- | :--- |
| **W1–W2** | **Phase 1: Lab & Proposal** | • Chốt phạm vi nghiên cứu SCHR-Bench.<br>• Phân tích mẫu Gh0stRAT; dựng môi trường Ghidra + Ollama. | **Deliverable D1** — **ĐÃ HOÀN THÀNH 100%** |
| **W3–W4** | **Phase 2: Data & Mutation** | • Xây dựng 40 hàm C; cài 5 mutation operators & OLLVM.<br>• Chạy kiểm thử **E0** (kiểm tra test vector loại mutation trung tính).<br>• Thiết kế bộ câu hỏi MCQ; biên soạn và nộp Báo cáo D2. | **Deliverable D2 (Static Report ~8%)** — **ĐÃ HOÀN THÀNH 100%** |
| **W5–W6** *(Hiện tại)* | **Phase 3: Pipeline & Baselines** | • Hoàn thiện MCP Pipeline Ghidra $\rightarrow$ LLM.<br>• Hoàn thành Thí nghiệm **E1** (SCHR cơ sở CT1).<br>• Chạy Thí nghiệm **E3** (Context Escalation CT1 $\rightarrow$ CT4).<br>• Thu thập log thực nghiệm thô và trích xuất kết quả sơ bộ. | **Draft Results & Pipeline Logs**<br>• Pipeline code hoàn chỉnh (Đạt ~80% Phase 3).<br>• Kết quả sơ bộ E1 & log thực nghiệm E3. |
| **W7–W8** | **Phase 4: Evaluation & Gold Set** | • Chạy Thí nghiệm **E2** (Tính điểm BLEU, Recompilability vs SCHR).<br>• Chạy Thí nghiệm **E4** (Đo tác động của Obfuscation Mức 0–3).<br>• Chạy Thí nghiệm **E5** (Gold Set 120 cặp; chấm FActScore độc lập, tính hệ số Cohen's Kappa).<br>• Chuẩn bị kịch bản Live Demo và nộp Báo cáo D3. | **Deliverable D3** *(Dynamic Analysis + RE Report + Live Demo ~22% điểm RBL)*<br>• Báo cáo thực nghiệm toàn diện.<br>• Buổi Demo trực tiếp luồng phân tích. |
| **W9–W10** | **Phase 5: Paper & Defense** | • Thực hiện kiểm định McNemar Test và Wilson CI.<br>• Phân loại lỗi chất lượng; đối chiếu định tính Gh0stRAT.<br>• Biên soạn bài báo khoa học chuẩn IEEE/Q1 và hoàn tất báo cáo D4/D5.<br>• Đóng gói Benchmark Repo công khai và bảo vệ trước hội đồng. | **Deliverable D4** *(Security Report 10%)*<br>**Deliverable D5** *(Final Report & Defense 30%)*<br>• Bài báo khoa học IEEE hoàn chỉnh.<br>• Benchmark GitHub Repo đóng gói hoàn chỉnh. |

---

## V. KẾ HOẠCH HÀNH ĐỘNG TUẦN TIẾP THEO (W6 — KẾT THÚC PHASE 3 & BƯỚC VÀO PHASE 4)

Trong **Tuần 6**, nhóm sẽ hoàn tất toàn bộ các mục tiêu còn lại của Phase 3 để tạo bước đệm vững chắc cho Phase 4:
1. **Hoàn tất thu thập dữ liệu Thí nghiệm E3:** Kết thúc toàn bộ các lượt inference cho 4 điều kiện context (CT1 $\rightarrow$ CT4) trên cả 2 mô hình (LLaMA-3 8B và Qwen2.5-Coder 14B).
2. **Chạy Thí nghiệm E4 (Obfuscation):** Đưa các binaries đã được làm rối bởi OLLVM qua pipeline để đo đạc sự biến thiên của SCHR theo từng cấp độ phức tạp mã.
3. **Chốt bộ Gold Set 120 cặp (Thí nghiệm E5):** Thành viên 3 (Duy) và Thành viên 4 (Phúc) tiến hành chấm thử nghiệm độc lập trên tập mẫu giải thích tự do (free-form generation) và tính toán hệ số đồng thuận ban đầu Cohen's Kappa ($\kappa$).
4. **Chuẩn bị hạ tầng Live Demo cho mốc D3 (Tuần 7–8):** Thành viên 2 (Phát & Duy) đóng gói script demo giao diện dòng lệnh/web trực quan: nạp file binary $\rightarrow$ Ghidra decompile $\rightarrow$ sinh prompt context escalation $\rightarrow$ LLM phản hồi $\rightarrow$ tính điểm SCHR real-time.

---

## VI. KHÓ KHĂN HIỆN TẠI & ĐỀ XUẤT XIN Ý KIẾN GIẢNG VIÊN HƯỚNG DẪN

### 1. Khó khăn kỹ thuật nhóm đang chủ động xử lý
- **Độ biến thiên khi LLM sinh văn bản tự do:** Ở phần giải thích tự do, dù đặt `temperature=0`, đôi khi câu từ của LLM có sự thay đổi nhẹ giữa các lần chạy.  
  *Giải pháp của nhóm:* Nhóm ưu tiên sử dụng bộ câu hỏi trắc nghiệm **Mutation-Aware MCQs** để lấy số liệu định lượng chuẩn xác và khách quan tuyệt đối cho SCHR; phần giải thích tự do chỉ dùng để phân tích định tính và tính điểm FActScore / Cohen's Kappa.
- **Tối ưu hóa chi phí token:** Chạy hàng trăm lượt prompt qua Qwen2.5-Coder 14B có thể gây tốn kém.  
  *Giải pháp của nhóm:* Nhóm tận dụng tối đa GPU máy tính trạm của thành viên để chạy LLaMA-3 (qua Ollama) cho 100% các vòng lặp kiểm thử mở rộng; chỉ dùng Qwen2.5-Coder 14B cho một tập mẫu đối chứng đại diện nhằm tối ưu hóa chi phí.

### 2. Đề xuất xin ý kiến định hướng từ Thầy Đinh Mai Hoàng
Nhóm 7 kính mong nhận được ý kiến chỉ dẫn quý báu từ Thầy về 2 điểm sau:
1. **Tiêu chuẩn tách Atomic Claim trong FActScore (E5):** Khi thực hiện chấm giải thích tự do, nhóm dự kiến phân rã câu trả lời của LLM thành 3 atomic claims: *(1) Mục đích an ninh chính, (2) Điều kiện kích hoạt rẽ nhánh, (3) Hành vi can thiệp hệ thống*. Thầy có khuyến nghị nhóm nên bám theo khung phân loại chuẩn nào khác (như MITRE ATT&CK sub-techniques) để tăng thêm sức nặng học thuật cho bài báo không ạ?
2. **Kịch bản Live Demo cho mốc D3 (Tuần 8):** Nhóm dự kiến kịch bản demo gồm 2 phần: (1) Chạy tự động pipeline đầu-cuối trên 1 cặp hàm gốc/mutation để chỉ rõ hiện tượng ảo giác ở CT1 và sự khắc phục ở CT2; (2) Trực quan hóa bảng số liệu SCHR và BLEU theo thời gian thực. Kịch bản này đã phù hợp với tiêu chí đánh giá của Bộ môn chưa ạ?

---

*TP. Hồ Chí Minh, ngày 08 tháng 10 năm 2026*  
**ĐẠI DIỆN NHÓM 7 — GROUP LEADER**  

*(Đã ký)*  

**Nguyễn Tấn Phát**  
MSSV: SE173285 — Lớp IA2007  
"""


def create_docx_report():
    doc = docx.Document()

    # Set page margins to 1 inch
    sections = doc.sections
    for section in sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)

    # Base Normal Style
    style_normal = doc.styles['Normal']
    font = style_normal.font
    font.name = 'Times New Roman'
    font.size = Pt(11)
    font.color.rgb = RGBColor(0x26, 0x26, 0x26)
    style_normal.paragraph_format.line_spacing = 1.2
    style_normal.paragraph_format.space_after = Pt(4)

    # Color Palette Constants
    COLOR_PRIMARY = RGBColor(0x00, 0x33, 0x66)    # Deep Navy
    COLOR_SECONDARY = RGBColor(0x1F, 0x4E, 0x78)  # Slate Blue
    COLOR_ACCENT = RGBColor(0x00, 0x5B, 0x96)     # Accent Blue

    def add_title(text):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(2)
        run = p.add_run(text)
        run.bold = True
        run.font.size = Pt(15.5)
        run.font.color.rgb = COLOR_PRIMARY
        return p

    def add_subtitle(text):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Pt(2)
        p.paragraph_format.space_after = Pt(4)
        run = p.add_run(text)
        run.bold = True
        run.font.size = Pt(11.5)
        run.font.color.rgb = COLOR_SECONDARY
        return p

    def add_badge(text):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Pt(2)
        p.paragraph_format.space_after = Pt(12)
        run = p.add_run(text)
        run.bold = True
        run.italic = True
        run.font.size = Pt(11)
        run.font.color.rgb = RGBColor(0xC0, 0x00, 0x00)
        return p

    def add_heading1(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(14)
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        run.bold = True
        run.font.size = Pt(13)
        run.font.color.rgb = COLOR_PRIMARY
        return p

    def add_heading2(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(10)
        p.paragraph_format.space_after = Pt(3)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        run.bold = True
        run.font.size = Pt(11.5)
        run.font.color.rgb = COLOR_SECONDARY
        return p

    def add_bullet(text, bold_prefix=""):
        p = doc.add_paragraph(style='List Bullet')
        p.paragraph_format.space_before = Pt(1)
        p.paragraph_format.space_after = Pt(2)
        p.paragraph_format.line_spacing = 1.15
        if bold_prefix:
            r_b = p.add_run(bold_prefix)
            r_b.bold = True
        p.add_run(text)
        return p

    def add_meta_info(label, value):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(1)
        p.paragraph_format.space_after = Pt(2)
        r_lbl = p.add_run(label + ": ")
        r_lbl.bold = True
        r_lbl.font.color.rgb = COLOR_SECONDARY
        p.add_run(value)
        return p

    def style_table(table, col_widths, headers, data, align_center_cols=[]):
        table.alignment = WD_TABLE_ALIGNMENT.CENTER
        table.autofit = False

        # Header Row
        hdr_cells = table.rows[0].cells
        for i, title in enumerate(headers):
            cell = hdr_cells[i]
            cell.text = title
            cell.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
            cell.paragraphs[0].paragraph_format.space_before = Pt(4)
            cell.paragraphs[0].paragraph_format.space_after = Pt(4)
            for r in cell.paragraphs[0].runs:
                r.bold = True
                r.font.size = Pt(9.5)
                r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
            
            # Header background fill
            shading_xml = parse_xml(r'<w:shd {} w:fill="1F4E78"/>'.format(nsdecls('w')))
            cell._tc.get_or_add_tcPr().append(shading_xml)

        # Data Rows
        for row_idx, row_data in enumerate(data):
            row = table.rows[row_idx + 1]
            bg_color = "F2F5F8" if row_idx % 2 == 1 else "FFFFFF"
            for col_idx, cell_value in enumerate(row_data):
                cell = row.cells[col_idx]
                cell.text = str(cell_value)
                p = cell.paragraphs[0]
                p.paragraph_format.space_before = Pt(3)
                p.paragraph_format.space_after = Pt(3)
                p.paragraph_format.line_spacing = 1.15
                if col_idx in align_center_cols:
                    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                else:
                    p.alignment = WD_ALIGN_PARAGRAPH.LEFT

                for r in p.runs:
                    r.font.size = Pt(9)
                
                shd = parse_xml(r'<w:shd {} w:fill="{}"/>'.format(nsdecls('w'), bg_color))
                cell._tc.get_or_add_tcPr().append(shd)

        # Apply column widths
        for row in table.rows:
            for idx, width in enumerate(col_widths):
                row.cells[idx].width = Inches(width)

    # 1. Header & Title Block
    add_title("BÁO CÁO TIẾN ĐỘ & KẾ HOẠCH TRIỂN KHAI CHI TIẾT ĐỀ TÀI RBL")
    add_subtitle("HỌC KỲ FALL 2026 — MÔN HỌC: IAM302T (MALWARE ANALYSIS & REVERSE ENGINEERING)")
    add_badge("📍 MỐC BÁO CÁO: CUỐI TUẦN 5 (W5) — BƯỚC SANG TUẦN 6 (W6)")

    # Metadata block
    add_meta_info("Cơ sở đào tạo", "Trường Đại học FPT — Phân hiệu TP. Hồ Chí Minh (Bộ môn An toàn Thông tin)")
    add_meta_info("Lớp học phần", "IA2007 | Nhóm thực hiện: Nhóm 7 (G7)")
    add_meta_info("Giảng viên hướng dẫn", "Thầy Đinh Mai Hoàng (DINHMH)")
    add_meta_info("Tên đề tài chính thức", "SCHR-Bench: Đo Lường Hallucination Security-Critical của LLM trong Reverse Engineering bằng Ground Truth từ Binary Mutation")
    add_meta_info("Thời điểm báo cáo", "Cuối Tuần 5 (08/10/2026) — Đã hoàn tất Phase 1 (D1) và Phase 2 (D2), đang chạy Phase 3 (~80%)")

    doc.add_paragraph().paragraph_format.space_after = Pt(4)

    # 2. Bảng phân công thành viên nhóm 7 (Chuẩn hóa)
    add_heading1("THÀNH VIÊN VÀ PHÂN CÔNG VAI TRÒ DỰ ÁN NHÓM 7")
    t_members = doc.add_table(rows=5, cols=5)
    headers_m = ["STT", "Họ và Tên", "MSSV", "Vai trò chính", "Trách nhiệm cốt lõi & Deliverable"]
    widths_m = [0.4, 1.4, 0.9, 1.6, 2.2]
    data_m = [
        ["1", "Nguyễn Tấn Phát", "SE173285", "Project Leader & MCP Pipeline Co-Engineer (Trưởng nhóm)", "Điều phối tiến độ 10 tuần; cùng Duy xây dựng MCP Pipeline Ghidra -> LLM; phân tích mẫu Gh0stRAT; chủ trì nộp D1-D5 & Paper."],
        ["2", "Đỗ Thiện Nhân", "SE194134", "Thành viên 1: C/Binary & Mutation Engineer", "Xây dựng trọn vẹn 40 hàm C security-critical; cài đặt 5 toán tử Binary Mutation; biên dịch GCC/MSVC + OLLVM; hoàn tất Thí nghiệm E0. Đã nộp thành công D2."],
        ["3", "Nguyễn Trọng Duy", "SE194413", "Thành viên 2 & 3: Pipeline & Metrics Specialist", "Cùng Phát viết script Ghidra Headless và MCP Server; quản lý Context Escalation CT1-CT4; thiết kế Gold Set MCQ; lập trình script đo SCHR, BLEU, Recompilability. Phụ trách Demo D3 & D4."],
        ["4", "Võ Hồng Phúc", "SE203844", "Thành viên 4: Statistical Analyst & Lead Author", "Thực hiện kiểm định thống kê chuyên sâu (McNemar Test & Wilson CI); phân loại lỗi chất lượng; đồng tác giả chủ trì biên soạn Báo cáo D3-D5 và bài báo khoa học chuẩn IEEE/Q1."]
    ]
    style_table(t_members, widths_m, headers_m, data_m, align_center_cols=[0, 2])

    doc.add_paragraph().paragraph_format.space_after = Pt(6)

    # I. Tổng quan đề tài & định hướng
    add_heading1("I. TỔNG QUAN ĐỀ TÀI & ĐIỀU CHỈNH HƯỚNG ĐI THEO ĐỊNH HƯỚNG CỦA GIẢNG VIÊN")
    add_heading2("1. Quá trình tiếp thu phản hồi và tái cấu trúc đề tài")
    p_adj = doc.add_paragraph()
    p_adj.add_run(
        "Theo đề xuất sơ bộ ban đầu tại Proposal D1, Nhóm 7 xây dựng hướng nghiên cứu về 'Multi-Engine Consensus Analysis' "
        "(kết hợp đồng thời Ghidra và IDA Pro qua giao thức MCP Agent và Context Escalation 4 tầng). Tuy nhiên, sau khi nhận được "
        "văn bản hướng dẫn chi tiết của Thầy Đinh Mai Hoàng, nhóm nhận thấy một số hạn chế cốt tử trong đề tài ban đầu: (1) Rào cản bản quyền IDA Pro "
        "khiến nghiên cứu không thể nhân rộng trên môi trường mở; (2) Việc phân tích trực tiếp mẫu mã độc nặng bị đóng gói bởi VMProtect khiến decompiler "
        "chỉ sinh ra mã rác vô nghĩa, không tạo được ground truth đáng tin cậy; (3) Nguy cơ thiếu một thước đo độc lập để xác minh tính chính xác trong suy luận an ninh của LLM.\n\n"
        "Do đó, Nhóm 7 đã thống nhất điều chỉnh đề tài toàn diện sang Chủ đề 3: SCHR-Bench. Phương pháp này sử dụng kỹ thuật Binary Mutation trên tập 40 "
        "hàm C bảo mật tự viết để tạo Ground Truth có kiểm soát tuyệt đối, kết hợp công cụ dịch ngược mã nguồn mở Ghidra Headless và giao thức MCP tĩnh. "
        "Đây là hướng đi có tính khoa học cao, rủi ro an toàn bằng không và hoàn toàn khả thi trong thời lượng 10 tuần học kỳ."
    )

    add_heading2("2. Định vị học thuật: Phân biệt rõ ràng giữa SCHR-Bench (Nhóm 7) và VeRA (Nhóm 1)")
    t_compare = doc.add_table(rows=4, cols=3)
    headers_c = ["Tiêu chí so sánh", "Đề tài VeRA (Nhóm 1)", "Đề tài SCHR-Bench (Nhóm 7)"]
    widths_c = [1.8, 2.3, 2.4]
    data_c = [
        ["Bản chất Ground Truth", "Mã nguồn tự viết kết hợp với test vector thực thi động thông thường.", "Binary Mutation có kiểm soát: Thay đổi đúng 1 yếu tố an ninh cốt lõi giữa bản gốc và đột biến."],
        ["Câu hỏi cốt lõi", "'Bao nhiêu claim của LLM sống sót qua kiểm chứng?' (Đúng hay Sai)", "'LLM có nhận ra sự thay đổi nguy hiểm (security-critical) hay bỏ sót và đoán mò theo thói quen?'"],
        ["Đóng góp chính", "Bộ Verifier tĩnh và động để kiểm tra từng atomic claim.", "Hệ thống đo lường chuyên biệt SCHR (Security-Critical Hallucination Rate), vạch trần hạn chế của BLEU & Recompilability."]
    ]
    style_table(t_compare, widths_c, headers_c, data_c, align_center_cols=[0])

    doc.add_paragraph().paragraph_format.space_after = Pt(6)

    add_heading2("3. Bốn Câu hỏi Nghiên cứu (RQ) và Bốn Giả thuyết Khoa học (H)")
    add_bullet(" Khi một hàm security-critical bị đột biến (đảo điều kiện anti-debug, đổi hằng số khóa XOR, thay đổi API persistence), LLM có nhận ra sự thay đổi hành vi không hay lặp lại mô tả rập khuôn của bản gốc? (Đo lường bằng chỉ số SCHR).", "RQ1:")
    add_bullet(" Chỉ số SCHR có gì vượt trội so với các thước đo truyền thống như BLEU score hay Tỷ lệ biên dịch lại (Recompilability)? SCHR có bắt được những sai sót chết người mà các thước đo trên bỏ sót không?", "RQ2:")
    add_bullet(" Việc cung cấp thêm mã máy Assembly (mỏ neo ground truth) và mô tả API trong giao thức Context Escalation có giúp giảm SCHR so với việc chỉ cấp mã giả (pseudocode) hay không? (Đo SCHR biến thiên qua 4 cấp độ CT1 → CT4).", "RQ3:")
    add_bullet(" Các kỹ thuật làm rối mã ở mức nhẹ và trung bình (Control-Flow Flattening, String Encryption qua OLLVM) làm tỷ lệ ảo giác SCHR gia tăng ở mức độ nào? (Đo SCHR theo 4 mức Obfuscation từ Mức 0 đến Mức 3).", "RQ4:")

    p_hypo = doc.add_paragraph()
    p_hypo.paragraph_format.space_before = Pt(4)
    p_hypo.add_run("Các giả thuyết khoa học tương ứng (Hypotheses H1–H4): ").bold = True
    p_hypo.add_run(
        "Nhóm đặt giả thuyết rằng LLM có xu hướng ảo giác cao nhất ở dạng lỗi đảo ngược điều kiện logic (H1) do mô hình dựa dẫm vào tri thức huấn luyện thay vì phân tích cú pháp thực tế; "
        "thước đo BLEU sẽ bất lực trong việc phát hiện hallucination an ninh (H2); bổ sung mã Assembly sẽ cải thiện rõ rệt độ chính xác của LLM (H3); "
        "và kỹ thuật Obfuscation sẽ làm suy giảm nghiêm trọng khả năng trích xuất luồng điều khiển của decompiler, dẫn đến SCHR tăng đột biến (H4)."
    )

    # II. Thiết kế giải pháp kỹ thuật
    add_heading1("II. THIẾT KẾ GIẢI PHÁP KỸ THUẬT & HỆ THỐNG THỰC NGHIỆM")
    add_heading2("1. Định nghĩa Toán tử Đột biến Nhị phân (Binary Mutation Operators)")
    p_mut = doc.add_paragraph()
    p_mut.add_run(
        "Nhóm thiết kế riêng 5 toán tử đột biến chuyên sâu nhắm trúng các cấu trúc logic an ninh trong binary Windows PE:"
    )
    add_bullet(" Chuyển đổi lệnh rẽ nhánh điều kiện (ví dụ: if (IsDebuggerPresent()) → if (!IsDebuggerPresent())). Biến đổi hoàn toàn logic chống phân tích từ 'thoát chương trình' sang 'tiếp tục thực thi'.", "1. Đảo điều kiện logic (Invert Condition):")
    add_bullet(" Đổi giá trị khóa XOR giải mã (ví dụ: 0x5A → 0xA5) hoặc thay đổi ngưỡng thời gian chu kỳ CPU (RDTSC delta). Khiến dữ liệu giải mã bị sai khác hoàn toàn.", "2. Thay đổi hằng số (Alter Constant):")
    add_bullet(" Thay thế API ghi Registry bằng API xóa Registry (RegSetValueEx → RegDeleteValue). Đảo ngược hoàn toàn tính chất từ 'tạo persistence' sang 'hủy persistence'.", "3. Đổi hàm API hệ thống (Substitute API):")
    add_bullet(" Chuyển đổi toán tử so sánh (> thành <=, == thành !=), làm lệch ranh giới lặp giải mã shellcode.", "4. Đổi toán tử quan hệ (Relational Mutation):")
    add_bullet(" Xóa bỏ một tầng kiểm tra trong cơ chế phòng thủ nhiều lớp (ví dụ: bỏ lệnh kiểm tra NtGlobalFlag).", "5. Bỏ qua bước kiểm tra (Omit Defense Step):")

    add_heading2("2. Phân tầng Ngữ cảnh (Context Escalation Levels - CT1 đến CT4)")
    add_bullet(" Cung cấp duy nhất mã giả C (pseudocode) do Ghidra trích xuất. Đây là mức cơ sở phản ánh cách các plugin AI hiện nay hoạt động.", "• CT1 (Baseline):")
    add_bullet(" Cung cấp mã giả Ghidra kết hợp toàn bộ mã máy Disassembly Assembly của hàm. Assembly đóng vai trò là 'mỏ neo chân lý' (ground truth anchor) ngăn decompiler sinh lỗi.", "• CT2 (Assembly Anchor):")
    add_bullet(" Cung cấp CT2 kèm theo bảng đặc tả tóm tắt hành vi và tham số của các Windows API xuất hiện trong hàm.", "• CT3 (Context Enrichment):")
    add_bullet(" Cung cấp CT3 kèm theo mã assembly của các hàm lân cận và bảng cross-references (X-refs) trong binary.", "• CT4 (Extended Neighborhood):")

    add_heading2("3. Thiết kế Chuỗi Thí nghiệm Thực nghiệm (E0 đến E5)")
    t_exp = doc.add_table(rows=8, cols=4)
    headers_e = ["Mã TN", "Mục tiêu (RQ)", "Phương pháp & Điều kiện", "Trạng thái thực tế (Cuối W5)"]
    widths_e = [0.6, 1.3, 2.3, 2.3]
    data_e = [
        ["E0", "Kiểm tra dữ liệu", "Chạy test vector thực thi; kiểm tra khả năng decompile của Ghidra.", "ĐÃ HOÀN THÀNH 100% (W4): 100% mutation gây đổi hành vi thực tế; loại sạch mutation trung tính."],
        ["E1", "SCHR Cơ sở (RQ1)", "Đo tỷ lệ LLM trả lời sai yếu tố bảo mật trên mức ngữ cảnh CT1.", "ĐÃ HOÀN THÀNH LƯỢT 1 (W5): Đã có số liệu sơ bộ; SCHR đảo điều kiện đạt >40% (khẳng định H1)."],
        ["E2", "So sánh Metric (RQ2)", "Tính BLEU score giữa bản gốc/đột biến; đo tỷ lệ Recompilability.", "ĐANG TRIỂN KHAI (W5-W6): Script đo đã xong; đang nạp dữ liệu log từ E1."],
        ["E3", "Hiệu quả Ngữ cảnh (RQ3)", "Đo lường SCHR biến thiên qua 4 cấp độ ngữ cảnh CT1 → CT4.", "ĐANG CHẠY LOGS (W5-W6): Đang chạy batch inference trên LLaMA-3 và Qwen2.5-Coder 14B."],
        ["E4", "Tác động Obfuscation (RQ4)", "Biên dịch 4 mức làm rối OLLVM (Mức 0 đến Mức 3).", "SẴN SÀNG CHẠY (W6): Toàn bộ binaries OLLVM đã chuẩn bị xong từ Phase 2."],
        ["E5", "Gold Set & Tự do", "100–150 cặp câu hỏi; tách claim FActScore; 2 người chấm độc lập.", "CHUẨN BỊ CHO W7: Đã soạn xong 120 cặp câu hỏi; rubric chấm độc lập sẵn sàng."],
        ["E6", "Đa Decompiler (Tùy chọn)", "Đối chiếu mã giả giữa Ghidra và RetDec / Binary Ninja.", "GIAI ĐOẠN DỰ PHÒNG (W8): Chạy mở rộng nếu hoàn thành sớm các mục tiêu chính."]
    ]
    style_table(t_exp, widths_e, headers_e, data_e, align_center_cols=[0, 1])

    doc.add_paragraph().paragraph_format.space_after = Pt(6)

    # III. Báo cáo tiến độ hiện tại đến cuối W5
    add_heading1("III. BÁO CÁO TIẾN ĐỘ THỰC HIỆN ĐẾN CUỐI TUẦN 5 (W5)")
    add_heading2("1. Phase 1 (W1–W2): Lab Setup & Proposal — ĐÃ HOÀN THÀNH 100%")
    add_bullet(" Nộp và bảo vệ thành công Deliverable D1 (Proposal & Lab Setup Report), xác lập nền tảng nghiên cứu vững chắc.", "• Hoàn tất mốc D1:")
    add_bullet(" Nghiên cứu sâu tài liệu phản hồi của Thầy Đinh Mai Hoàng; điều chỉnh toàn bộ cấu trúc dự án sang SCHR-Bench.", "• Tái định vị đề tài chuẩn mực:")
    add_bullet(" Thu thập và bóc tách hoàn chỉnh mẫu Gh0stRAT PE32 (ea7cd59c...) từ MalwareBazaar; trích xuất chi tiết các cơ chế persistence và anti-analysis làm bộ đối chiếu định tính thực tế.", "• Khảo sát mẫu thực tế:")
    add_bullet(" Cài đặt hoàn chỉnh Ghidra 11.x Headless Analyzer; thiết lập mô hình mở Ollama (LLaMA-3 8B) nội bộ và toolchain GCC/MSVC.", "• Thiết lập môi trường Lab:")

    add_heading2("2. Phase 2 (W3–W4): Data & Mutation — ĐÃ HOÀN THÀNH 100% (NGHIỆM THU D2)")
    add_bullet(" Thành viên 1 (Nhân) đã hoàn thành trọn vẹn 40 hàm C thuộc 4 nhóm chính: Anti-debug, String Decryption (XOR/RC4), Persistence (Registry Run Key), và Anti-VM / Environment Checks.", "• Dataset 40 hàm C Security-Critical:")
    add_bullet(" Áp dụng thành công 5 toán tử đột biến; biên dịch qua GCC/MSVC stripped symbols kết hợp OLLVM ở 4 cấp độ (Mức 0 đến Mức 3).", "• Cài đặt Mutation & Obfuscation:")
    add_bullet(" 100% các cặp hàm đã được kiểm tra qua test harness thực thi; xác nhận tất cả biến thể đều gây ra sự sai lệch hành vi rõ rệt (loại bỏ hoàn toàn đột biến trung tính).", "• Thí nghiệm E0 (Sanity Check):")
    add_bullet(" Đã nộp đúng hạn Báo cáo Phân tích Tĩnh (Static Analysis Report — chiếm 8% điểm tổng kết) kèm theo toàn bộ source code và stripped binaries.", "• Nghiệm thu mốc D2:")

    add_heading2("3. Phase 3 (W5–W6): Pipeline & Baselines — ĐANG TRIỂN KHAI TÍCH CỰC Ở CUỐI W5 (~80%)")
    t_status = doc.add_table(rows=7, cols=5)
    headers_s = ["Hạng mục công việc", "Phụ trách chính", "Tiến độ (Cuối W5)", "Trạng thái", "Sản phẩm / Kết quả đạt được"]
    widths_s = [1.8, 1.4, 0.7, 1.0, 1.6]
    data_s = [
        ["Ghidra Headless Automation", "Phát & Duy", "100%", "Hoàn thành", "Script trích xuất tự động C pseudocode & ASM ra JSON chuẩn."],
        ["MCP Server & LLM Client", "Phát & Duy", "90%", "Đang hoàn thiện", "Pipeline kết nối Ollama (LLaMA-3.1 8B & Qwen2.5-Coder 14B); T=0 cố định."],
        ["Context Escalation (CT1-CT4)", "Duy & Phát", "85%", "Đang chạy logs", "Dựng xong 4 tầng context; đang nạp batch data cho LLM."],
        ["Thí nghiệm E1 (SCHR cơ sở CT1)", "Duy & Phát", "100%", "Xong Lượt 1", "Chạy xong 40 hàm; phát hiện SCHR đảo điều kiện > 40% (đúng H1)."],
        ["Thí nghiệm E3 (Escalation CT1-4)", "Phát & Duy", "70%", "Đang chạy logs", "Thu thập logs thực nghiệm suy luận trên LLaMA-3 và Qwen2.5-Coder 14B."],
        ["Script Metrics (SCHR, BLEU)", "Nguyễn Trọng Duy", "85%", "Đang hoàn thiện", "Script Python tính SCHR tự động và tích hợp NLTK BLEU score."]
    ]
    style_table(t_status, widths_s, headers_s, data_s, align_center_cols=[1, 2, 3])

    doc.add_paragraph().paragraph_format.space_after = Pt(6)

    # IV. Lộ trình 10 tuần RBL cập nhật
    add_heading1("IV. LỘ TRÌNH 10 TUẦN CẬP NHẬT VÀ CÁC MỐC DELIVERABLES (THEO SYLLABUS RBL)")
    t_rbl = doc.add_table(rows=6, cols=4)
    headers_r = ["Tuần", "Giai đoạn RBL", "Nội dung công việc trọng tâm", "Mốc nộp Deliverable & Trạng thái"]
    widths_r = [0.8, 1.5, 2.7, 1.5]
    data_r = [
        ["W1–W2", "Phase 1: Lab & Proposal", "Chốt phạm vi SCHR-Bench; phân tích mẫu Gh0stRAT; dựng môi trường Ghidra Headless + Ollama.", "D1 — Proposal & Lab Setup\n(ĐÃ HOÀN THÀNH 100%)"],
        ["W3–W4", "Phase 2: Data & Mutation", "Hoàn thiện 40 hàm C; cài 5 mutation operators & OLLVM; chạy kiểm thử E0; nộp Báo cáo D2.", "D2 — Static Analysis Report (~8%)\n(ĐÃ HOÀN THÀNH 100%)"],
        ["W5–W6", "Phase 3: Pipeline & Baselines\n(Hiện tại: Cuối W5)", "Hoàn thiện MCP Pipeline; chạy Thí nghiệm E1 (SCHR cơ sở CT1) và E3 (Context Escalation CT1-CT4); thu thập logs.", "Draft Results & Pipeline Logs\n(Đạt ~80% Phase 3)"],
        ["W7–W8", "Phase 4: Evaluation & Gold Set", "Đo SCHR, BLEU, Recompilability (E2); đo Obfuscation (E4); chấm Gold Set E5 (Cohen's Kappa); chuẩn bị demo.", "D3 — RE Report & Live Demo (~22% điểm RBL)"],
        ["W9–W10", "Phase 5: Paper & Defense", "Kiểm định McNemar & Wilson CI; phân loại lỗi; hoàn thiện bài báo khoa học IEEE; đóng gói repo & bảo vệ.", "D4 — Security Report (10%)\nD5 — Final Report & Defense (30%)"]
    ]
    style_table(t_rbl, widths_r, headers_r, data_r, align_center_cols=[0, 1])

    doc.add_paragraph().paragraph_format.space_after = Pt(6)

    # V. Kế hoạch hành động Tuần 6
    add_heading1("V. KẾ HOẠCH HÀNH ĐỘNG TUẦN TIẾP THEO (W6 — HOÀN TẤT PHASE 3 VÀ TIẾN TỚI PHASE 4)")
    p_w6 = doc.add_paragraph()
    p_w6.add_run(
        "Trong Tuần 6, nhóm tập trung dứt điểm các hạng mục cuối của Phase 3 để chuẩn bị toàn diện cho mốc Deliverable D3:\n"
    )
    add_bullet(" Hoàn tất toàn bộ các lượt inference cho 4 điều kiện context (CT1 → CT4) trên cả 2 mô hình (LLaMA-3 8B và Qwen2.5-Coder 14B).", "1. Hoàn thành thu thập dữ liệu Thí nghiệm E3:")
    add_bullet(" Đưa các binaries đã được làm rối bởi OLLVM qua pipeline để đo đạc sự biến thiên của SCHR theo từng cấp độ phức tạp mã.", "2. Chạy Thí nghiệm E4 (Obfuscation):")
    add_bullet(" Thành viên 3 (Duy) và Thành viên 4 (Phúc) tiến hành chấm thử nghiệm độc lập trên tập mẫu giải thích tự do và tính toán hệ số đồng thuận ban đầu Cohen's Kappa.", "3. Chốt bộ Gold Set 120 cặp (Thí nghiệm E5):")
    add_bullet(" Thành viên 2 (Phát & Duy) đóng gói script demo giao diện dòng lệnh trực quan: nạp file binary -> Ghidra decompile -> sinh prompt context escalation -> LLM phản hồi -> tính điểm SCHR real-time.", "4. Chuẩn bị hạ tầng Live Demo cho mốc D3 (Tuần 7–8):")

    # VI. Khó khăn & Đề xuất xin ý kiến Giảng viên
    add_heading1("VI. KHÓ KHĂN KỸ THUẬT & ĐỀ XUẤT XIN Ý KIẾN GIẢNG VIÊN HƯỚNG DẪN")
    add_heading2("1. Khó khăn kỹ thuật nhóm đang chủ động xử lý")
    add_bullet(" Ở phần giải thích tự do, đôi khi văn phong của LLM có sự thay đổi nhẹ giữa các lần chạy. Nhóm xử lý bằng cách lấy bộ câu hỏi MCQ Mutation-Aware làm thước đo định lượng cốt lõi cho SCHR; phần tự do chỉ dùng để phân tích định tính và tính điểm FActScore / Cohen's Kappa.", "• Độ biến thiên khi LLM sinh văn bản tự do:")
    add_bullet(" Nhóm tận dụng GPU máy tính trạm của thành viên để chạy mô hình LLaMA-3 (qua Ollama) cho 100% các vòng lặp kiểm thử diện rộng; chỉ dùng Qwen2.5-Coder 14B cho một tập mẫu đối chứng đại diện nhằm tối ưu chi phí.", "• Tối ưu hóa chi phí token API:")

    add_heading2("2. Đề xuất xin ý kiến định hướng từ Thầy Đinh Mai Hoàng")
    p_adv = doc.add_paragraph()
    p_adv.add_run("Nhóm 7 kính mong nhận được ý kiến chỉ dẫn quý báu từ Thầy về hai nội dung học thuật sau:\n")
    add_bullet(" Khi chấm giải thích tự do (E5), nhóm dự kiến phân rã câu trả lời thành 3 atomic claims: (1) Mục đích an ninh chính, (2) Điều kiện kích hoạt rẽ nhánh, (3) Hành vi can thiệp hệ thống. Thầy có khuyến nghị nhóm nên bám theo khung chuẩn hóa nào (như MITRE ATT&CK sub-techniques) để tăng thêm giá trị học thuật cho bài báo không ạ?", "1. Tiêu chuẩn tách Atomic Claim trong FActScore:")
    add_bullet(" Nhóm dự kiến kịch bản demo D3 gồm: (1) Chạy tự động pipeline đầu-cuối trên 1 cặp hàm gốc/mutation để chỉ rõ hiện tượng ảo giác ở CT1 và sự khắc phục ở CT2; (2) Trực quan hóa bảng số liệu SCHR và BLEU theo thời gian thực. Kịch bản này đã phù hợp với tiêu chí đánh giá của Bộ môn chưa ạ?", "2. Kịch bản Live Demo cho mốc D3 (Tuần 8):")

    # Signature block
    doc.add_paragraph().paragraph_format.space_after = Pt(14)
    p_sign = doc.add_paragraph()
    p_sign.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    r_s1 = p_sign.add_run("TP. Hồ Chí Minh, ngày 08 tháng 10 năm 2026\n")
    r_s1.italic = True
    r_s2 = p_sign.add_run("ĐẠI DIỆN NHÓM 7 — GROUP LEADER\n\n")
    r_s2.bold = True
    r_s_signed = p_sign.add_run("(Đã ký)\n\n")
    r_s_signed.italic = True
    r_s3 = p_sign.add_run("Nguyễn Tấn Phát\n")
    r_s3.bold = True
    r_s4 = p_sign.add_run("MSSV: SE173285 — Lớp IA2007")
    r_s4.font.size = Pt(10)

    doc.save(DOCX_PATH)
    print("Saved DOCX to:", DOCX_PATH)


def create_markdown_report():
    with open(MD_PATH, "w", encoding="utf-8") as f:
        f.write(MD_CONTENT)
    print("Saved Markdown to:", MD_PATH)


if __name__ == "__main__":
    create_markdown_report()
    create_docx_report()
    print("Done generating updated reports!")
