# 🛡️ BÁO CÁO THIẾT LẬP VÀ TRIỂN KHAI HẠ TẦNG KALI 2026 (TIER 2)
> **Đề tài:** SCHR-Bench (Security-Critical Hallucination Rate Benchmark)  
> **Học phần:** IAM302t – Malware Analysis and Reverse Engineering (RBL Model)  
> **Hội nghị mục tiêu:** EAI INISCOM 2027 (Springer LNICST Series)  
> **Hệ thống thực thi:** Kali Linux 2026 (Tier 2 - Processing & Evaluation Hub)  
> **Cập nhật:** 2026-10-26

---

## 📌 1. TỔNG QUAN VAI TRÒ CỦA KALI 2026 TRONG DỰ ÁN

Trong kiến trúc thực nghiệm 3 tầng (Hybrid 3-Tier Setup) của đề tài SCHR-Bench, **Kali Linux (Tier 2)** giữ vai trò **"Giàn khảo thí độc lập & Cỗ máy dịch ngược tự động cô lập" (Isolated Automated RE & Benchmarking Rig)**:
* **Độc lập với Model Server (Tier 1 - Host MSI/WSL2):** Máy thật chạy GPU với Ollama làm "thí sinh", còn Kali là "giám khảo" lưu trữ ground truth và gửi đề thi qua mạng LAN ảo (`192.168.86.1:11434`).
* **Bảo vệ Ground Truth:** Không bị ảnh hưởng bởi Windows Defender/Antivirus tự động quét xóa các tệp nhị phân mô phỏng mã độc (Anti-Debug, Persistence, Evasion).
* **Cách ly an toàn với mẫu Gh0stRAT (Tier 3 - Win 11):** Sẵn sàng tiếp nhận các đoạn mã nhị phân thật từ sandbox để dịch ngược mà không gây nguy hiểm cho máy thật.

---

## 📂 2. CẤU TRÚC THƯ MỤC DỰ ÁN ĐÃ THIẾT LẬP

Toàn bộ hệ thống pipeline đã được quy hoạch và tạo lập tại thư mục gốc `/home/NTP/IAM302t/`:

```
/home/NTP/IAM302t/
├── bin/                         # Chứa các file nhị phân PE (.exe) / ELF stripped
│   └── demo_target.bin          # Nhị phân mẫu đã qua kiểm thử thực tế
├── dataset/                     # Thư mục gốc chứa bộ dữ liệu nghiên cứu
│   └── Dataset_SCHR_Bench/
│       └── SCHR_Bench_C_Functions/ # Chứa 40 cặp mã nguồn C (src/), tools/, và ground_truth_manifest.json
├── ghidra_scripts/
│   └── ExportRE.java            # Script Java chạy trong Ghidra Headless bóc tách RE data
├── scripts/
│   ├── ghidra_headless.sh       # Wrapper script khởi động Ghidra Headless với Java 21
│   └── batch_decompile.py       # Tự động hóa decompile hàng loạt nhị phân vào JSON
├── data_extracted/
│   ├── test_target_re.json      # Kết quả trích xuất mẫu kiểm định ban đầu
│   ├── demo_target.bin_re.json  # Kết quả trích xuất nhị phân demo
│   └── decompiled_db.json       # Cơ sở dữ liệu hợp nhất (Pseudocode + Assembly + Xrefs)
├── pipeline/
│   ├── context_builder.py       # Bộ đóng gói ngữ cảnh 4 tầng (CT1 -> CT4)
│   ├── ollama_client.py         # Client REST API giao tiếp Ollama Host (temperature=0)
│   └── run_bench.py             # Master Pipeline điều phối toàn bộ thí nghiệm
├── evaluation/
│   └── eval_engine.py           # Động cơ tính SCHR, BLEU, McNemar Test, Wilson CI 95%
├── results/                     # Nơi lưu trữ log JSON kết quả khảo nghiệm của LLM
├── docs/                        # Tài liệu hướng dẫn & tài liệu định hướng
└── Kali2026_Project/            # Thư mục quản lý báo cáo và tài liệu dành riêng cho Kali
```

---

## ⚙️ 3. CHI TIẾT CÁC CÔNG VIỆC VÀ MODULE ĐÃ HOÀN THÀNH

### 3.1. Khắc phục Runtime & Tối ưu hóa Ghidra Headless
* **Vấn đề phát hiện:** Ghidra 11.3.2 trên Kali mặc định trỏ về OpenJDK 25 dẫn đến lỗi `unsupported java version` và đòi hỏi tương tác terminal TTY để chọn JDK.
* **Giải pháp triển khai:** Xây dựng script wrapper [`ghidra_headless.sh`](file:///home/NTP/IAM302t/scripts/ghidra_headless.sh):
  * Cố định biến môi trường `JAVA_HOME=/usr/lib/jvm/java-21-openjdk-amd64`.
  * Chạy ở chế độ `jre` không cần prompt terminal.
  * Cấp phát tối ưu bộ nhớ heap `4GB RAM` và kích hoạt chế độ headless (`-Djava.awt.headless=true`).

### 3.2. Script Trích xuất Ghidra Headless ([`ExportRE.java`](file:///home/NTP/IAM302t/ghidra_scripts/ExportRE.java))
* Viết bằng Java GhidraScript tương thích native với lõi Decompiler Ghidra 11.3.2.
* Chức năng tự động:
  1. Duyệt bảng ký hiệu hàm (Function Manager), định vị hàm mục tiêu `target()`.
  2. Dịch ngược tạo mã **Pseudocode C**.
  3. Lấy toàn bộ tập lệnh **Assembly x64 Disassembly** (mỏ neo ground truth).
  4. Trích xuất danh sách **API calls và Cross-references (Xrefs)**.
  5. Đóng gói chuẩn hóa thành file JSON độc lập cho từng file nhị phân.

### 3.3. Script Xử lý Hàng loạt ([`batch_decompile.py`](file:///home/NTP/IAM302t/scripts/batch_decompile.py))
* Tự động quét toàn bộ tệp nhị phân trong thư mục `bin/`.
* Tự động tạo và dọn dẹp project tạm thời của Ghidra (`-deleteProject -overwrite`).
* Gom toàn bộ kết quả đơn lẻ thành tệp cơ sở dữ liệu duy nhất: [`decompiled_db.json`](file:///home/NTP/IAM302t/data_extracted/decompiled_db.json).

### 3.4. Bộ Đóng gói Ngữ cảnh 4 Tầng ([`context_builder.py`](file:///home/NTP/IAM302t/pipeline/context_builder.py))
Hiện thực hóa đúng giao thức nghiên cứu Context Escalation:
* **CT1 (Pseudocode Baseline):** Chỉ trích xuất mã giả C decompile.
* **CT2 (Assembly Anchor):** CT1 + Mã Assembly x64 (mỏ neo ngăn ảo giác).
* **CT3 (Context Enrichment):** CT2 + Đặc tả ý nghĩa các API/hàm mock.
* **CT4 (Extended Neighborhood):** CT3 + Ngữ cảnh các hàm lân cận và địa chỉ entry.

### 3.5. Client Giao tiếp Ollama Chống Nhiễu ([`ollama_client.py`](file:///home/NTP/IAM302t/pipeline/ollama_client.py))
* Kết nối từ Kali sang Ollama trên máy thật qua IP mạng LAN (`http://192.168.86.1:11434` hoặc biến môi trường `OLLAMA_HOST`).
* Thiết lập các tham số khoa học để đảm bảo tính tái lập (Reproducibility):
  * `temperature = 0.0` (loại bỏ tính ngẫu nhiên).
  * `seed = 42`.
  * Hỗ trợ tự động kiểm tra trạng thái máy chủ (`ping()`) và liệt kê models.

### 3.6. Động cơ Thống kê Khoa học ([`eval_engine.py`](file:///home/NTP/IAM302t/evaluation/eval_engine.py))
Phục vụ trực tiếp cho việc xuất bảng số liệu trong bài báo Springer INISCOM 2027:
1. **Chỉ số SCHR:**
   $$\text{SCHR} = \frac{N_{\text{wrong}}}{N_{\text{valid}}} \times 100\%$$
2. **Chỉ số Miss Rate:** Đo tỷ lệ LLM trả lời bản đột biến giống hệt bản gốc.
3. **Chỉ số BLEU Score:** Sử dụng thư viện `nltk` với hàm làm mịn `SmoothingFunction.method1` để đo sự khác biệt từ vựng.
4. **Khoảng tin cậy Wilson 95% (Wilson Score Interval):**
   $$w = \frac{p + \frac{z^2}{2n} \pm z \sqrt{\frac{p(1-p)}{n} + \frac{z^2}{4n^2}}}{1 + \frac{z^2}{n}} \quad (z = 1.96)$$
5. **Kiểm định McNemar (McNemar's Test with Edward's Correction):**
   $$\chi^2 = \frac{(|b - c| - 1)^2}{b + c}$$
   *(Dùng để chứng minh giả thuyết H3: Assembly ở CT2 có thực sự giúp giảm ảo giác so với CT1 một cách có ý nghĩa thống kê $p < 0.01$ hay không).*

### 3.7. Master Runner ([`run_bench.py`](file:///home/NTP/IAM302t/pipeline/run_bench.py))
* Đọc cơ sở dữ liệu `decompiled_db.json`.
* Tự động duyệt qua danh sách các model (`llama3.1:8b`, `qwen2.5-coder:14b`) và các tầng ngữ cảnh (`CT1`, `CT2`, `CT3`, `CT4`).
* Tự động lưu log chi tiết vào thư mục `results/`.

---

## 🧪 4. KẾT QUẢ KIỂM THỬ THỰC TẾ TRÊN KALI

| Hạng mục kiểm thử | Công cụ / Module | Trạng thái | Ghi chú kết quả |
| :--- | :--- | :---: | :--- |
| Khởi động Ghidra Headless | `ghidra_headless.sh` | **PASS (100%)** | Khởi chạy thành công với Java 21, cấp 4GB RAM. |
| Biên dịch thử nghiệm nhị phân | `gcc` / `x86_64` | **PASS (100%)** | Biên dịch thành công binary mẫu `/tmp/test_target`. |
| Trích xuất RE tự động | `ExportRE.java` | **PASS (100%)** | Bóc tách đầy đủ Pseudocode C và Disassembly x64 của hàm `target`. |
| Tạo cơ sở dữ liệu nhị phân | `batch_decompile.py` | **PASS (100%)** | Tạo thành công `decompiled_db.json` với 2 nhị phân mẫu. |
| Động cơ toán học & thống kê | `eval_engine.py` | **PASS (100%)** | Test mẫu: $\text{SCHR} = 37.5\%$, Wilson CI: $[24.22\%, 52.97\%]$, McNemar $\chi^2 = 7.5625$ ($p = 0.0059 < 0.01$ $\rightarrow$ Significant). |

---

## 📖 5. HƯỚNG DẪN VẬN HÀNH DÀNH CHO CẬU

### Bước 1: Nạp bộ tệp nhị phân vào Kali
Copy 80 file PE/ELF (`40_original` và `40_mutant`) vào thư mục `bin/`:
```bash
cp /duong_dan_chua_binary/*.exe /home/NTP/IAM302t/bin/
```

### Bước 2: Chạy decompile tự động hàng loạt
```bash
python3 /home/NTP/IAM302t/scripts/batch_decompile.py
```
*Kết quả sẽ tự động được ghi đè và hợp nhất vào tệp [`data_extracted/decompiled_db.json`](file:///home/NTP/IAM302t/data_extracted/decompiled_db.json).*

### Bước 3: Chạy khảo thí kết nối sang Ollama Host
Đảm bảo máy thật MSI đã bật Ollama lắng nghe cổng mạng (`export OLLAMA_HOST=0.0.0.0:11434 && ollama serve`).  
Tại terminal Kali, chạy lệnh:
```bash
python3 /home/NTP/IAM302t/pipeline/run_bench.py \
  --host http://192.168.86.1:11434 \
  --model llama3.1:8b \
  --levels CT1 CT2
```
*Log chi tiết sẽ được tự động ghi vào thư mục `results/` để phân tích thống kê.*

---

## 🚀 6. KẾT QUẢ NGHIỆM THU MỐC D4: THỰC NGHIỆM GH0STRAT CASE STUDY (2026-10-28)

1. **Tiếp nhận bằng chứng từ Sandbox Tier 3:**
   - 10 ảnh minh chứng DIE v3.21 và PE-bear v0.7.2.
   - Nhận diện kỹ thuật đóng gói bảo vệ: **VXiProtect / VMProtect**, Section `.O#J` với Entropy 7.89095, các section `.text`, `.rdata` có kích thước 0.
   - IAT bị stripped tối đa (`LoadLibraryA` & `GetProcAddress`).
2. **Triển khai thực nghiệm ảo giác tại Tier 2:**
   - Script thực thi: `scripts/evaluate_gh0strat_case_study.py`.
   - Kết quả xuất tại: [`results/GH0STRAT_EVALUATION.json`](file:///home/NTP/IAM302t/IAM302t_SCHR_Bench/results/GH0STRAT_EVALUATION.json).
   - Xác thực vai trò cứu vãn của Mỏ neo Assembly (CT2): Đưa SCHR trên logic Persistence về **0.0%** đối với `qwen2.5-coder:14b`.
3. **Hoàn thiện Section 5 Bài báo khoa học Springer LNICST:**
   - Tích hợp số liệu, phân tích kỹ thuật và hình ảnh entropy vào `main.tex`.
   - Biên dịch thành công bản thảo máy in `main.pdf` (11 trang) sẵn sàng nộp INISCOM 2027.
