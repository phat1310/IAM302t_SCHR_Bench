---
title: "Tier 2 (Kali Linux) Master Task List & Execution Plan"
project: "SCHR-Bench (Security-Critical Hallucination Rate Benchmark)"
tier: "Tier 2 — Isolated Automated RE & Benchmarking Rig"
os_environment: "Kali Linux 2026 (7.1.5-amd64)"
target_deliverable: "Deliverable D3 (Live Demo & RE Report) & Springer Paper"
author: "Nguyễn Tấn Phát (SE173285) — Group Leader"
created_date: 2026-10-27
tags:
  - KaliLinux
  - Tier2
  - GhidraHeadless
  - MCPAgent
  - Ollama
  - SRE_Benchmark
---

# 🛡️ KẾ HOẠCH HÀNH ĐỘNG CHI TIẾT DÀNH CHO TIER 2 (KALI LINUX 2026)
> <span style="color:#2e7d32; font-size:1.1em; font-weight:bold;">Giàn Khảo Thí Độc Lập & Cỗ Máy Dịch Ngược Tự Động Hóa (Isolated Automated RE & Benchmarking Rig)</span>

---

> [!success] **VỊ TRÍ CHIẾN LƯỢC CỦA TIER 2 TRONG KIẾN TRÚC 3 TẦNG**
> * **Tier 1 (Host MSI / WSL2):** Trung tâm tính toán AI với GPU NVIDIA (`Ollama: 192.168.86.1:11434`).
> * **Tier 2 (Máy ảo Kali Linux này):** Cỗ máy "Giám khảo độc lập", tự động hóa hoàn toàn từ khâu biên dịch, decompile Ghidra headless, đóng gói prompt context (CT1 $\rightarrow$ CT4), gửi đề thi sang Tier 1 và chấm điểm thống kê.
> * **Tier 3 (Máy ảo Win 11 CLIENT01):** Sandbox cô lập phân tích mẫu mã độc thật Gh0stRAT PE32.

---

### 📌 THÔNG TIN HẠ TẦNG & BIẾN MÔI TRƯỜNG KHOA HỌC

* **Hệ điều hành:** Kali Linux 7.1.5 x86_64 (`GNU/Linux`)
* **Thư mục làm việc chuẩn:** `/home/NTP/IAM302t/`
* **Java Runtime chuẩn:** OpenJDK 21 (`/usr/lib/jvm/java-21-openjdk-amd64`)
* **Ghidra Engine:** Ghidra 11.3.2 (Headless Mode, cấp phát 4GB heap RAM)
* **IP kết nối Ollama Server:** `http://192.168.86.1:11434`
* **Tham số suy luận chống nhiễu:** `temperature = 0.0`, `seed = 42`

---

## 🗂️ BẢNG THEO DÕI TIẾN ĐỘ TÁC VỤ VÀ MINH CHỨNG HÌNH ẢNH TIER 2

| Mã Task | Tên Nhiệm vụ Trọng tâm | Trạng thái | Sản phẩm Đầu ra Mục tiêu | Ảnh Minh chứng (`Image_Result/`) |
| :---: | :--- | :---: | :--- | :--- |
| **TASK-1** | Kiểm tra Môi trường & Mạng LAN ảo (Host $\leftrightarrow$ Kali) | ✅ Hoàn thành | Ping 0ms, curl Ollama 200 OK (`llama3.1`, `qwen2.5`) | `01` - `06` (Đã chuẩn hóa) |
| **TASK-2** | Đồng bộ Dataset 40 hàm C & Chạy E0 Sanity Check | ✅ Hoàn thành | 160 assertions PASS, file `results/E0_sanity_kali.txt` | `07_kali_e0_sanity_check_160_pass.png` |
| **TASK-3** | Biên dịch Chéo 80 Binary PE x64 Stripped (`mingw-w64`) | ✅ Hoàn thành | 80 file nhị phân trong `dataset/.../build/pe_x64_O0/` | `08_kali_batch_decompile_80_binaries.png` |
| **TASK-4** | Vận hành Ghidra Headless bóc tách Pseudocode/Assembly | ✅ Hoàn thành | File CSDL `results/decompiled_contexts_80.json` | `08_kali_batch_decompile_80_binaries.png` |
| **TASK-5** | Vận hành MCP Agent & Khảo nghiệm Đa tầng (CT1 $\rightarrow$ CT3) | ✅ Hoàn thành | 480 queries logged trong `results/benchmark_raw_logs.json` | `09_kali_run_bench_multi_context.png` |
| **TASK-6** | Chạy Động cơ Thống kê (SCHR, BLEU, McNemar, Wilson CI) | ✅ Hoàn thành | Bảng Springer trong `results/PAPER_TABLES_SPRINGER.md` | `10_kali_eval_engine_schr_tables.png` |
| **TASK-7** | Đóng gói Kịch bản & Script Live Demo Mốc D3 | ✅ Hoàn thành | Script biểu diễn 1-lệnh `scripts/live_demo.sh` | `11_kali_live_demo_terminal_execution_1` $\rightarrow$ `_4.png` |
| **MỐC D4** | Thực nghiệm Ảo giác Gh0stRAT Case Study & Paper LNICST | ✅ Hoàn thành | Section 5 Paper (`main.pdf`) & `GH0STRAT_EVALUATION.json` | `12_kali_gh0strat_case_study_evaluation.png` |

---

## 📸 QUY CHUẨN ĐẶT TÊN VÀ QUẢN LÝ BỘ ẢNH TIER 2

> [!NOTE] **Bộ ảnh hiện có (01 – 06): Đã chuẩn hóa theo luồng thao tác kỹ thuật**
> 1. `01_kali_ping_host_gateway.png` (Kali: ping gateway 192.168.86.1)
> 2. `02_host_netsh_portproxy_11434.png` (Host: netsh portproxy chuyển tiếp 11434)
> 3. `03_host_firewall_rule_ollama.png` (Host: Windows Firewall mở inbound TCP 11434)
> 4. `04_host_restart_vmware_nat_dhcp.png` (Host: restart VMware NAT Service & VMnetDHCP)
> 5. `05_kali_curl_ollama_api_tags.png` (Kali: curl Ollama tags nhận diện 2 models)
> 6. `06_kali_ghidra_headless_version.png` (Kali: ghidra_headless.sh chạy với Java 21)

> [!IMPORTANT] **Đánh giá & Kết quả hoàn thiện Bộ ảnh Cốt lõi (07 – 12):**
> Bộ 12 ảnh minh chứng cốt lõi của Tier 2 đã được chụp đầy đủ 100%, chuẩn hóa tên file theo quy chuẩn học thuật (không emoji, không icon rườm rà) và lưu trữ trực tiếp tại `tier2_kali/Image_Result/`:
> * `07_kali_e0_sanity_check_160_pass.png`: Kết quả 160 assertions PASS của 40 hàm C (100% non-neutral mutation).
> * `08_kali_batch_decompile_80_binaries.png`: Tiến trình batch decompile Ghidra Headless 80 nhị phân.
> * `09_kali_run_bench_multi_context.png`: Khảo nghiệm benchmark gửi prompt đa tầng sang Ollama.
> * `10_kali_eval_engine_schr_tables.png`: Bảng thống kê SCHR, Wilson CI 95%, kiểm định McNemar.
> * `11_kali_live_demo_terminal_execution_1.png` đến `_4.png`: Chuỗi 4 ảnh trực quan hóa đầy đủ 4 bước Live Demo 1-lệnh Mốc D3.
> * `12_kali_gh0strat_case_study_evaluation.png`: Chạy thực nghiệm ảo giác case study Gh0stRAT Mốc D4.

---

## 📋 HƯỚNG DẪN CHI TIẾT TỪNG BƯỚC CHỤP BỘ ẢNH THỰC NGHIỆM CỐT LÕI (07 – 12)

> **Mục tiêu:** Cung cấp đầy đủ bằng chứng thực nghiệm phục vụ viết bài báo khoa học Springer LNICST (INISCOM 2027) và báo cáo bảo vệ đồ án IAM302t.  
> **Thư mục lưu ảnh:** [`tier2_kali/Image_Result/`](file:///home/NTP/IAM302t/IAM302t_SCHR_Bench/tier2_kali/Image_Result/)  
> **Mẹo chụp ảnh trên Kali Linux:** Nhấn **`Alt + PrintScreen`** để chụp riêng cửa sổ Terminal đang chọn (hoặc mở công cụ `xfce4-screenshooter` chọn chế độ *Active window*).

### ⚙️ Bước 0: Kiểm tra điều kiện cần trước khi thực hiện
- [x] **Nhóm ảnh nội bộ (Ảnh 07, 08, 10):** Chạy 100% nội bộ trên Kali, không yêu cầu Ollama Host.
- [x] **Nhóm ảnh kết nối mạng AI (Ảnh 09, 11, 12):** Yêu cầu máy **Host Windows** đã bật Ollama:
  ```powershell
  # Chạy tại PowerShell Admin máy Host
  ollama serve
  ```
  Kiểm tra kết nối từ terminal Kali:
  ```bash
  curl -s http://192.168.86.1:11434/api/tags | jq .
  ```

---

### 📷 Bước 1: Chụp Ảnh 07 — Ground Truth Sanity Check E0
* **Tên file:** `07_kali_e0_sanity_check_160_pass.png`
* **Mục tiêu trong Paper:** Minh chứng tính tin cậy của bộ Ground Truth tác giả tự viết, không có đột biến trung tính (non-neutral mutation đạt 100%).
* **Lệnh thực thi tại Terminal Kali:**
  ```bash
  cd /home/NTP/IAM302t/IAM302t_SCHR_Bench
  python3 /home/NTP/IAM302t/dataset/Dataset_SCHR_Bench/SCHR_Bench_C_Functions/tools/check_suite.py
  ```
* **Tiêu chuẩn kiểm tra trước khi bấm chụp:**
  - [x] Terminal in ra: `Functions: 40 | Variant builds: 80 | Test assertions: 160`
  - [x] Terminal in ra: `Discriminating mutations: 40`
  - [x] Dòng chữ xanh lá: `PASS: all hand-authored ground-truth assertions matched.`

---

### 📷 Bước 2: Chụp Ảnh 08 — Ghidra Headless Batch Decompile
* **Tên file:** `08_kali_batch_decompile_80_binaries.png`
* **Mục tiêu trong Paper:** Minh chứng pipeline RE tự động hóa của Ghidra Headless trích xuất thành công toàn bộ Pseudocode C và Assembly x64 cho 80 file PE stripped.
* **Lệnh thực thi tại Terminal Kali:**
  ```bash
  cd /home/NTP/IAM302t/IAM302t_SCHR_Bench
  python3 scripts/extract_contexts.py
  ```
  *(Hoặc `python3 /home/NTP/IAM302t/scripts/batch_decompile.py`)*
* **Tiêu chuẩn kiểm tra trước khi bấm chụp:**
  - [x] Terminal hiển thị tiến trình duyệt qua danh sách các binary trong `bin/`.
  - [x] Thông báo hoàn thành hợp nhất dữ liệu vào `results/decompiled_contexts_80.json`.

---

### 📷 Bước 3: Chụp Ảnh 09 — MCP Benchmark Runner Đa Tầng Context
* **Tên file:** `09_kali_run_bench_multi_context.png`
* **Mục tiêu trong Paper:** Minh chứng giàn khảo nghiệm độc lập (Tier 2 Rig) gửi đề thi các tầng ngữ cảnh (CT1, CT2, CT3) sang Model Server qua REST API với `temperature=0.0`, `seed=42`.
* **Lệnh thực thi tại Terminal Kali:**
  ```bash
  cd /home/NTP/IAM302t/IAM302t_SCHR_Bench
  python3 scripts/step3_mcp_server_and_benchmark.py --max-pairs 5
  ```
* **Tiêu chuẩn kiểm tra trước khi bấm chụp:**
  - [x] Terminal hiển thị kết nối thành công tới Host `http://192.168.86.1:11434`.
  - [x] Hiển thị quá trình truy vấn lần lượt `llama3.1:8b` và `qwen2.5-coder:14b` trên từng tầng CT1, CT2, CT3 kèm chỉ số Latency (s).

---

### 📷 Bước 4: Chụp Ảnh 10 — Động Cơ Thống Kê & Bảng Springer LNICST
* **Tên file:** `10_kali_eval_engine_schr_tables.png`
* **Mục tiêu trong Paper:** Bảng định lượng trung tâm (Table 2 & Table 3 của bài báo) xác thực chỉ số SCHR, khoảng tin cậy Wilson CI 95% và kiểm định McNemar Test ($p < 0.01$).
* **Lệnh thực thi tại Terminal Kali:**
  ```bash
  cd /home/NTP/IAM302t/IAM302t_SCHR_Bench
  python3 evaluation/eval_engine.py
  head -n 25 results/PAPER_TABLES_SPRINGER.md
  ```
* **Tiêu chuẩn kiểm tra trước khi bấm chụp:**
  - [x] Terminal hiển thị kết quả kiểm định: `SCHR: 37.50%`, `Wilson 95% CI: [24.22%, 52.97%]`, `McNemar Test: chi2=7.5625, p-value=5.9595e-03, significant=True`.
  - [x] Bảng Markdown đối chiếu đầy đủ các cột: LLM, Tầng Ngữ Cảnh, Lỗi Ảo Giác, SCHR (%), Miss Rate, BLEU Score.

---

### 📷 Bước 5: Chụp Ảnh 11 — Kịch Bản Live Demonstration 1-Lệnh
* **Tên file:** `11_kali_live_demo_terminal_execution_1.png` $\rightarrow$ `_4.png`
* **Mục tiêu trong Paper & Báo cáo:** Minh chứng kịch bản Live Demo bảo vệ đồ án (Mốc D3) trực quan hóa hiện tượng ảo giác an ninh tại CT1 và được khắc phục tại CT2.
* **Lệnh thực thi tại Terminal Kali:**
  ```bash
  cd /home/NTP/IAM302t/IAM302t_SCHR_Bench
  bash scripts/live_demo.sh
  ```
  *(Hoặc `python3 scripts/live_demo.py`)*
* **Tiêu chuẩn kiểm tra trước khi bấm chụp:**
  - [x] Terminal hiển thị Banner: `SCHR-BENCH: LIVE DEMONSTRATION OF CONTEXT ESCALATION (MILESTONE D3)`.
  - [x] Hiển thị luồng demo tương tác 4 bước trực quan giữa CT1 (ảo giác) và CT2 (khắc phục bằng Assembly Anchor).

---

### 📷 Bước 6: Chụp Ảnh 12 — Thực Nghiệm Đánh Giá Ảo Giác Mẫu Gh0stRAT PE32
* **Tên file:** `12_kali_gh0strat_case_study_evaluation.png`
* **Mục tiêu trong Paper:** Dữ liệu thực nghiệm ca thực tế phục vụ **Section 5 (Real-World Malware Case Study: Gh0stRAT PE32)** của bài báo Springer.
* **Lệnh thực thi tại Terminal Kali:**
  ```bash
  cd /home/NTP/IAM302t/IAM302t_SCHR_Bench
  python3 scripts/evaluate_gh0strat_case_study.py
  ```
* **Tiêu chuẩn kiểm tra trước khi bấm chụp:**
  - [x] Terminal hiển thị đánh giá cả 2 ca: `CS01_GH0STRAT_PACKER_ENTRY` (VXiProtect/VMProtect) và `CS02_GH0STRAT_PERSISTENCE_INSTALL` (Registry Run Key).
  - [x] Dòng chữ: `[+] Evaluation Complete! Results saved to: results/GH0STRAT_EVALUATION.json`.

---

### 🚀 Bước 7: Lưu File, Commit Git & Đồng Bộ Nhánh
Sau khi chụp và lưu đủ 6 ảnh mới vào `tier2_kali/Image_Result/`:
```bash
cd /home/NTP/IAM302t/IAM302t_SCHR_Bench

# 1. Commit trên nhánh tier2-kali
git checkout tier2-kali
git add tier2_kali/Image_Result/*.png
git commit -m "feat(tier2): hoàn thành chụp bổ sung 6 ảnh thực nghiệm cốt lõi 07-12 cho paper Springer"

# 2. Merge sang nhánh dev
git checkout dev
git merge tier2-kali

# 3. Đẩy lên GitHub Remote
git push origin dev tier2-kali
```

---

## 🚀 CHI TIẾT TỪNG BƯỚC THỰC HIỆN TRÊN TERMINAL KALI LINUX

---

### 🌐 TASK 1: KIỂM TRA MÔI TRƯỜNG & MẠNG LAN ẢO

> [!tip] **Mục tiêu:** Đảm bảo Kali Linux kết nối thông suốt với Ollama trên máy Host và Ghidra có đủ Java 21 để chạy không lỗi.

- [x] **1.1. Khởi động terminal Kali và di chuyển vào thư mục dự án:**
  ```bash
  cd /home/NTP/IAM302t/
  pwd
  ls -la
  ```
- [x] **1.2. Kiểm tra thông mạng tới máy Host Windows (Ollama Server):**
  ```bash
  # Ping máy Host
  ping -c 3 192.168.86.1

  # Kiểm tra cổng Ollama 11434 từ Kali
  curl -s http://192.168.86.1:11434/api/tags | jq .
  ```
  *Yêu cầu kết quả:* Lệnh `curl` phải trả về JSON chứa danh sách 2 model: `"name": "llama3.1:8b"` và `"name": "qwen2.5-coder:14b"`.

- [x] **1.3. Xác thực Runtime của Ghidra Headless:**
  ```bash
  # Kiểm tra wrapper script với Java 21
  bash scripts/ghidra_headless.sh --version
  ```
  *Yêu cầu kết quả:* Ghidra khởi động bình thường, không báo lỗi `unsupported java version`.

---

### 📦 TASK 2: ĐỒNG BỘ DATASET & KIỂM ĐỊNH E0 SANITY CHECK

> [!tip] **Mục tiêu:** Xác nhận lại toàn bộ 40 cặp hàm C và 160 test vector assertions trên môi trường native Linux của Kali.
> [!note] **Cấu trúc thư mục Dataset thực tế:**  
> Bộ dữ liệu nằm tại: `dataset/Dataset_SCHR_Bench/SCHR_Bench_C_Functions/` (chứa `src/`, `tools/`, và `ground_truth_manifest.json`). Tất cả các lệnh dưới đây đã được cập nhật đường dẫn chuẩn xác khớp với cấu trúc thư mục này.

- [x] **2.1. Kiểm tra bộ mã nguồn C trong thư mục Dataset:**
  ```bash
  cd /home/NTP/IAM302t/
  ls dataset/Dataset_SCHR_Bench/SCHR_Bench_C_Functions/src/ | wc -l
  # Phải đủ 80 file C (40 original + 40 mutant)
  ```
- [x] **2.2. Chạy Thí nghiệm E0 (Sanity Check):**
  ```bash
  cd /home/NTP/IAM302t/
  python3 dataset/Dataset_SCHR_Bench/SCHR_Bench_C_Functions/tools/check_suite.py | tee /home/NTP/IAM302t/results/E0_sanity_kali.txt
  ```
  *Yêu cầu kết quả:*  
  `Functions: 40 | Variant builds: 80 | Test assertions: 160`  
  `Discriminating mutations: 40/40 (100.0% non-neutral)`  
  `PASS: all hand-authored ground-truth assertions matched.`

---

### ⚙️ TASK 3: BIÊN DỊCH CHÉO 80 BINARY PE STRIPPED BẰNG MINGW

> [!tip] **Mục tiêu:** Tạo ra 80 tệp nhị phân thực thi chuẩn Windows PE x64 (hoặc Linux ELF stripped) đã loại bỏ bảng symbol (`-s`), đặt tên ngẫu nhiên hoặc chuẩn hóa để chuẩn bị nạp vào Ghidra.

- [ ] **3.1. Chạy script biên dịch chéo tự động:**
  ```bash
  cd /home/NTP/IAM302t/
  python3 dataset/Dataset_SCHR_Bench/SCHR_Bench_C_Functions/tools/build_pe.py --arch x64 --opt 0
  ```
- [ ] **3.2. Sao chép các tệp nhị phân đã build vào thư mục `bin/` của Kali:**
  ```bash
  mkdir -p /home/NTP/IAM302t/bin/
  cp dataset/Dataset_SCHR_Bench/SCHR_Bench_C_Functions/build/pe_x64_O0/*.exe /home/NTP/IAM302t/bin/
  ls -la /home/NTP/IAM302t/bin/ | wc -l
  # Đảm bảo đủ 80 file binary
  ```

---

### 🔬 TASK 4: VẬN HÀNH GHIDRA HEADLESS BÓC TÁCH JSON (BATCH DECOMPILE)

> [!tip] **Mục tiêu:** Dùng Ghidra Headless phân tích tự động toàn bộ 80 binary, sinh ra mã C Pseudocode, mã Disassembly Assembly x64, bảng API calls và Xrefs hợp nhất vào `decompiled_db.json`.

- [ ] **4.1. Kiểm tra script Java native `ExportRE.java`:**
  ```bash
  cat /home/NTP/IAM302t/ghidra_scripts/ExportRE.java | grep -E "DecompInterface|currentProgram"
  ```
- [ ] **4.2. Khởi chạy Batch Decompile Pipeline:**
  ```bash
  cd /home/NTP/IAM302t/
  python3 scripts/batch_decompile.py
  ```
  *Quy trình thực thi ngầm của script:*
  * Duyệt qua từng file `.exe` trong `bin/`.
  * Gọi `ghidra_headless.sh` nạp binary vào project tạm, thực thi `ExportRE.java`.
  * Trích xuất `target()` $\rightarrow$ xuất JSON trung gian vào `data_extracted/`.
  * Hợp nhất tất cả thành tệp CSDL: `/home/NTP/IAM302t/data_extracted/decompiled_db.json`.

- [ ] **4.3. Kiểm định tệp CSDL đầu ra:**
  ```bash
  jq '. | length' /home/NTP/IAM302t/data_extracted/decompiled_db.json
  # Phải trả về đúng 80 bản ghi
  ```

---

### 🤖 TASK 5: VẬN HÀNH MCP AGENT & MASTER BENCHMARK RUNNER

> [!tip] **Mục tiêu:** Cho Kali đóng vai trò "Giám khảo", lần lượt đóng gói câu hỏi và ngữ cảnh theo 4 tầng (CT1, CT2, CT3, CT4), gửi sang Ollama Host chấm điểm và lưu log.

- [ ] **5.1. Chạy thử nghiệm kiểm tra đơn mẫu (Sanity Query Test):**
  ```bash
  cd /home/NTP/IAM302t/
  python3 -c "
  from pipeline.ollama_client import OllamaClient
  client = OllamaClient(base_url='http://192.168.86.1:11434')
  print('Models online:', client.list_models())
  res = client.query('llama3.1:8b', 'Explain: if (a == 0) return 0; return 1; with a=1. Answer 0 or 1.')
  print('Test response:', res)
  "
  ```

- [ ] **5.2. Chạy Master Benchmark Suite trên Kali:**
  ```bash
  cd /home/NTP/IAM302t/
  # Chạy trước tập 5 cặp demo (10 binaries x 3 tiers = 60 queries/model)
  python3 pipeline/run_bench.py --demo --models llama3.1:8b qwen2.5-coder:14b
  ```
  *Kết quả log tự động ghi vết tại:* `/home/NTP/IAM302t/results/benchmark_raw_logs.json`.

---

### 📊 TASK 6: CHẠY ĐỘNG CƠ THỐNG KÊ (EVALUATION ENGINE)

> [!tip] **Mục tiêu:** Tính toán tự động toàn bộ các chỉ số khoa học để đối chiếu với kết quả máy Host và sẵn sàng đưa vào bài báo Springer INISCOM 2027.

- [ ] **6.1. Khởi chạy Động cơ Tính toán:**
  ```bash
  cd /home/NTP/IAM302t/
  python3 evaluation/eval_engine.py
  ```
- [ ] **6.2. Kiểm tra các chỉ số xuất ra:**
  * **SCHR (%)** trên từng tầng ngữ cảnh CT1, CT2, CT3.
  * **Miss Rate (%)** trên biến thể đột biến (mutant).
  * **BLEU-4 Score** giữa bản gốc và bản đột biến (chứng minh $BLEU \ge 0.40$ nhưng an ninh bị sai).
  * **Khoảng tin cậy Wilson 95% CI** (ví dụ: `30.0% [10.8%, 60.3%]`).
  * **Kiểm định McNemar** ($\chi^2$ và $p$-value so sánh cặp CT1 vs CT2).
- [ ] **6.3. Báo cáo xuất ra tệp Markdown:**
  ```bash
  cat /home/NTP/IAM302t/results/KALI_EVALUATION_REPORT.md
  ```

---

### 🎬 TASK 7: ĐÓNG GÓI KỊCH BẢN LIVE DEMO (MỐC DELIVERABLE D3)

> [!tip] **Mục tiêu:** Tạo 1 script duy nhất để khi trình bày trước Thầy Đinh Mai Hoàng, bạn chỉ cần gõ 1 lệnh là toàn bộ luồng demo chạy mượt mà từ đầu đến cuối.

- [ ] **7.1. Tạo script `scripts/live_demo.sh`:**
  ```bash
  cat << 'EOF' > /home/NTP/IAM302t/scripts/live_demo.sh
  #!/usr/bin/env bash
  clear
  echo "=================================================================="
  echo " 🎬 SCHR-BENCH LIVE DEMONSTRATION (DELIVERABLE D3 - NHÓM 7)"
  echo " Đề tài: Đo lường Ảo giác An ninh trong Dịch ngược bằng Mutation"
  echo " Giảng viên hướng dẫn: Thầy Đinh Mai Hoàng (DINHMH)"
  echo "=================================================================="
  echo ""
  echo "[+] Bước 1: Kiểm định Ground Truth E0 (160 Assertions)..."
  python3 /home/NTP/IAM302t/dataset/Dataset_SCHR_Bench/SCHR_Bench_C_Functions/tools/check_suite.py
  echo ""
  read -p "Nhấn [Enter] để chuyển sang Bước 2: Demo Bắt quả tang Ảo giác CT1..."
  echo ""
  echo "[+] Bước 2: Nạp mẫu P06 (Persistence Mock) qua Ghidra Decompiler..."
  echo "[+] Đang suy luận mô hình LLaMA-3.1 8B tại CT1 (Chỉ Pseudocode)..."
  python3 /home/NTP/IAM302t/pipeline/run_bench.py --sample P06_original --tier CT1
  echo ""
  read -p "Nhấn [Enter] để chuyển sang Bước 3: Khắc phục bằng Context Escalation CT2..."
  echo ""
  echo "[+] Bước 3: Nâng cấp ngữ cảnh lên CT2 (+Assembly Mỏ neo)..."
  python3 /home/NTP/IAM302t/pipeline/run_bench.py --sample P06_original --tier CT2
  echo ""
  echo "=================================================================="
  echo " ✅ LIVE DEMO HOÀN TẤT THÀNH CÔNG!"
  echo "=================================================================="
  EOF
  chmod +x /home/NTP/IAM302t/scripts/live_demo.sh
  ```
- [ ] **7.2. Chạy thử nghiệm toàn bộ kịch bản Live Demo:**
  ```bash
  bash /home/NTP/IAM302t/scripts/live_demo.sh
  ```

---

## 📌 DANH MỤC LỆNH NHANH (CHEATSHEET DÀNH CHO TRƯỞNG NHÓM)

```bash
# 1. Đi vào thư mục
cd /home/NTP/IAM302t/

# 2. Test kết nối Ollama Host
curl -s http://192.168.86.1:11434/api/tags | jq .

# 3. Chạy E0
python3 dataset/Dataset_SCHR_Bench/SCHR_Bench_C_Functions/tools/check_suite.py

# 4. Decompile hàng loạt
python3 scripts/batch_decompile.py

# 5. Chạy Benchmark
python3 pipeline/run_bench.py --demo

# 6. Tính toán Thống kê
python3 evaluation/eval_engine.py

# 7. Bật Live Demo
bash scripts/live_demo.sh
```

---

*Tệp kế hoạch này được lưu trữ chính thức tại:*  
`03_G7_IAM302t_IA2007/Kali2026_Project/TASK_TIER2_KALI_EXECUTION_PLAN.md`
