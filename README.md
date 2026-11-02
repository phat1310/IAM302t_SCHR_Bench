# 🔬 SCHR-Bench: Security-Critical Hallucination Rate Benchmark
> **SCHR-Bench: Evaluating Security-Critical Hallucinations in LLM-Assisted Binary Reverse Engineering via Ground-Truth Mutations**

[![Course](https://img.shields.io/badge/Course-IAM302t--Fall2026-green.svg)](https://github.com/phat1310/IAM302t_SCHR_Bench)
[![Institution](https://img.shields.io/badge/Institution-FPT--University--HCMC-blue.svg)](https://hcmuni.fpt.edu.vn/)
[![Group](https://img.shields.io/badge/Group-IA2007--G7-orange.svg)](#2-thành-viên-nhóm-7-lớp-ia2007)
[![Target](https://img.shields.io/badge/Target-EAI--INISCOM--2027--Springer-red.svg)](https://iniscom.eai-conferences.org/)
[![License](https://img.shields.io/badge/Code--License-MIT-brightgreen.svg)](LICENSE)
[![Dataset](https://img.shields.io/badge/Dataset--License-CC--BY--4.0-yellow.svg)](#7-giấy-phép--cảnh-báo-an-toàn-safety--licensing)

---

## 📖 1. Giới Thiệu Đề Tài

Dự án **SCHR-Bench** được thực hiện trong khuôn khổ học phần **IAM302t (Malware Analysis and Reverse Engineering)** tại Trường Đại học FPT TP. Hồ Chí Minh theo mô hình **Research-Based Learning (RBL)**.

### Mục Tiêu Nghiên Cứu:
1. **Mục tiêu học phần (IAM302t):** Xây dựng bộ khung đánh giá định lượng hiện tượng **Security-Critical Hallucination Rate (SCHR)** và **Mutant Miss Rate** của các mô hình ngôn ngữ lớn (LLMs) khi suy luận kết quả hành vi trên 40 cặp hàm C quyết định bảo mật ($N = 80$ biến thể thực thi, 540 lượt đánh giá).
2. **Mục tiêu học thuật:** Chuẩn bị bản thảo nghiên cứu theo định dạng **Springer LNICST** (hội nghị **EAI INISCOM 2027**) và định dạng **IEEE Conference** (phục vụ báo cáo nghiệm thu học phần IAM302t; hai bản thảo dùng cho mục đích học phần và định dạng mục tiêu, **không nộp trùng lặp — No Dual Submission**).

---

## 👥 2. Thành Viên Nhóm 7 (Lớp IA2007)

| STT | Họ và Tên | MSSV | Vai trò chính |
| :---: | :--- | :---: | :--- |
| 1 | **Nguyễn Tấn Phát** | **SE173285** | **Group Leader & Pipeline Co-Engineer** |
| 2 | **Đỗ Thiện Nhân** | **SE194134** | **C/Binary & Mutation Engineer** |
| 3 | **Nguyễn Trọng Duy** | **SE194413** | **Context Extractor & Metrics Specialist** |
| 4 | **Võ Hồng Phúc** | **SE203844** | **Statistical Analyst & Manuscript Co-Author** |

* **Giảng viên hướng dẫn (Corresponding Author):** Thầy **Đinh Mai Hoàng** (`dinhmh@fe.edu.vn`).

---

## 🏗️ 3. Cấu Trúc Hệ Thống Thực Nghiệm & Môi Trường Tái Lập

```text
SCHR-Bench Architecture:
├── Tier 1 (Host GPU Inference Server) : Ollama Local API (llama3.1:8b, qwen2.5-coder:14b; τ=0.0, seed=42)
└── Tier 2 (Compilation & Benchmark Rig): MinGW-w64 (x86_64-w64-mingw32-gcc 14.2.0), E0 Verifier, Context Extractor & Statistical Engine
```

* **Thông số mô hình & phần cứng (Model Tags & Reproducibility Notes):**
  * Mô hình đánh giá qua Ollama: `llama3.1:8b` (8B parameters, Q4\_0 quantization default tag) và `qwen2.5-coder:14b` (14B parameters, Q4\_K\_M quantization default tag).
  * Tham số giải mã cố định: `temperature = 0.0`, `seed = 42`, `num_predict = 160`, `format = "json"`. Lưu ý: Dù cố định `temperature = 0.0` và `seed = 42`, kết quả suy luận dấu phẩy động trên GPU có thể dao động nhẹ giữa các kiến trúc phần cứng/driver CUDA hoặc phiên bản Ollama khác nhau; do đó toàn bộ **540 raw query logs** đã được lưu trữ đầy đủ tại `results/benchmark_raw_logs.json` để đảm bảo tái lập thống kê chính xác 100% ở chế độ Offline.

---

## 📂 4. Cấu Trúc Đóng Gói Sản Phẩm Nghiên Cứu (theo template `SOC-RL-v2.0`)

```text
IAM302t_SCHR_Bench/
├── 📁 code/                    # Toàn bộ script thực thi (Step 0 -> Step 4, Context Extractor, Live Demo)
├── 📁 dataset/                 # 40 cặp hàm C quyết định bảo mật (80 biến thể), runner.c, manifest & 160 câu MCQ
├── 📁 documentation/           # Tài liệu kế hoạch và ghi chú thiết kế
├── 📁 manuscript/              # Bản thảo LaTeX Springer LNICST & IEEE Conference
├── 📁 results/                 # Ngữ cảnh trích xuất (decompiled_contexts_80.json), 540 raw logs & bảng thống kê
├── 📄 CITATION.cff             # File định dạng trích dẫn chuẩn cho bài báo và GitHub
├── 📄 LICENSE                  # Giấy phép mã nguồn mở MIT License (Code) & CC BY 4.0 (Dataset)
├── 📄 MANIFEST.txt             # Bảng kê khai mục lục file trong dự án
├── 📄 README.md                # Tài liệu tổng quan dự án & hướng dẫn vận hành
└── 📄 reproduce.sh             # Kịch bản tái lập 2 chế độ (Offline Log Verification & Full Live Pipeline)
```

---

## 📊 5. Tóm Tắt Số Liệu Thực Nghiệm Chính ($N = 80$ Variants, 540 Logged Runs)

* **540 lượt đánh giá trong `results/benchmark_raw_logs.json`:** Gồm **480 lượt đánh giá chính** (`2 models × 3 context tiers [CT1, CT2, CT3] × 80 variants`) và **60 lượt đánh giá Obfuscation E4** (`2 models × 3 obfuscation templates [Obf1_CFF, Obf2_Sub, Obf3_Combined] × 10 pilot variants`).
* **Kiểm định thực thi E0 (`step0_verify_e0_windows.py`):** Biên dịch và chạy thật toàn bộ 80 biến thể qua 80 vector đầu vào (160 execution assertions), đạt **40/40 cặp hàm (100%) phân biệt hành vi trên Vector 1 (discriminating input)** và **50/80 tổng số vector phân biệt** (30 vector thứ 2 kiểm tra bảo toàn nhánh biên).
* **Tỷ lệ SCHR & Kiểm định McNemar ($N = 80$):**
  * `llama3.1:8b`: **38.8%** (CT1, 31/80 lỗi) $\rightarrow$ **36.2%** (CT2, 29/80 lỗi) $\rightarrow$ **35.0%** (CT3, 28/80 lỗi); Mutant Miss Rate: `32.5% -> 27.5% -> 27.5%`; McNemar $p \in [0.5791, 0.7518]$ (không có ý nghĩa thống kê ở $\alpha = 0.05$).
  * `qwen2.5-coder:14b`: **23.8%** (CT1, 19/80 lỗi) $\rightarrow$ **20.0%** (CT2, 16/80 lỗi) $\rightarrow$ **18.8%** (CT3, 15/80 lỗi); Mutant Miss Rate: `27.5% -> 25.0% -> 25.0%`; McNemar $p \in [0.2888, 0.4497]$ (không có ý nghĩa thống kê ở $\alpha = 0.05$).
  * **Tương quan hạng Spearman (RQ2):** Độ tương đồng từ vựng BLEU giữa giải thích gốc và đột biến của các cặp bị lỗi SCHR cao hơn nhóm cặp trả lời đúng ($\rho \in [+0.293, +0.495]$), cho thấy chỉ số tương đồng bề mặt không phát hiện được lỗi đảo ngược ngữ nghĩa.

---

## ⚡ 6. Hướng Dẫn Tái Lập Thực Nghiệm (`reproduce.sh` — 2 Chế Độ)

Kịch bản `reproduce.sh` hỗ trợ **2 chế độ tách biệt rõ ràng**:

### Chế độ A (Mặc định — Offline Verification & Statistical Reproduction, không cần GPU/Ollama):
Biên dịch và chạy kiểm định động E0 trên 80 biến thể C (160 assertions), tái tạo ngữ cảnh `decompiled_contexts_80.json` sạch 100% không rò rỉ nhãn, và tính toán lại toàn bộ bảng thống kê (`PAPER_TABLES_SPRINGER.md`) từ 540 log thực nghiệm có sẵn:
```bash
bash reproduce.sh
```

### Chế độ B (Full Live LLM Re-Evaluation — yêu cầu máy chủ Ollama đang chạy):
Chạy lại toàn bộ truy vấn LLM trực tiếp qua API Ollama (cần cài đặt `llama3.1:8b` và `qwen2.5-coder:14b`):
```bash
bash reproduce.sh --live-ollama
```

---

## 🛡️ 7. Giấy Phép & Cảnh Báo An Toàn (Safety & Licensing)

* **Mã nguồn (`code/`):** Phát hành theo giấy phép **MIT License** ([LICENSE](LICENSE)).
* **Bộ dữ liệu (`dataset/`):** Phát hành theo giấy phép **Creative Commons Attribution 4.0 International (CC BY 4.0)**.
* **Cảnh báo An toàn (Safety Notice):** Toàn bộ 40 cặp hàm C trong `dataset/SCHR_Bench_C_Functions/src/` là các hàm tính toán số học/logic cục bộ hoàn toàn vô hại (`int target(int a, int b, int c)`), **không chứa mã độc thực tế và không gọi bất kỳ API hệ điều hành nhạy cảm nào**. Tuy nhiên, một số trình diệt virus nhạy cảm có thể cảnh báo nhầm (false positive) đối với các file `.exe` biên dịch bằng MinGW; vui lòng chỉ biên dịch và chạy trong thư mục làm việc được cô lập. Không commit bất kỳ mẫu mã độc thực tế nào lên kho mã nguồn.
