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

## 🗂️ BẢNG THEO DÕI TIẾN ĐỘ TÁC VỤ TIER 2 (TASK TRACKING MATRIX)

| Mã Task | Tên Nhiệm vụ Trọng tâm | Trạng thái | Sản phẩm Đầu ra Mục tiêu |
| :---: | :--- | :---: | :--- |
| **TASK-1** | Kiểm tra Môi trường & Mạng LAN ảo (Host $\leftrightarrow$ Kali) | ✅ Hoàn thành | Ping 0ms, curl Ollama 200 OK (`llama3.1`, `qwen2.5`) |
| **TASK-2** | Đồng bộ Dataset 40 hàm C & Chạy E0 Sanity Check | ✅ Hoàn thành | 160 assertions PASS, file `results/E0_sanity_kali.txt` |
| **TASK-3** | Biên dịch Chéo 80 Binary PE x64 Stripped (`mingw-w64`) | 🔄 Sẵn sàng | 80 file nhị phân trong `/home/NTP/IAM302t/bin/` |
| **TASK-4** | Vận hành Ghidra Headless bóc tách Pseudocode/Assembly | 🔄 Sẵn sàng | File CSDL hợp nhất `data_extracted/decompiled_db.json` |
| **TASK-5** | Vận hành MCP Agent & Khảo nghiệm Đa tầng (CT1 $\rightarrow$ CT4) | 🔄 Sẵn sàng | File raw logs `results/kali_benchmark_logs.json` |
| **TASK-6** | Chạy Động cơ Thống kê (SCHR, BLEU, McNemar, Wilson CI) | 🔄 Sẵn sàng | Báo cáo đối chiếu `results/KALI_EVALUATION_REPORT.md` |
| **TASK-7** | Đóng gói Kịch bản & Script Live Demo Mốc D3 | 🔄 Sẵn sàng | Script biểu diễn 1-lệnh `scripts/live_demo.sh` |

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
