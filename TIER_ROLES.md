# 🤖 TIER ROLES & AGENT DIRECTIVES (SCHR-BENCH)
> **Quy định nhiệm vụ và chỉ dẫn tự động hóa cho các máy ảo / AI Agent trong mạng 3-Tier**

---

## 🖥️ TIER 1: HOST MSI (WSL2 UBUNTU) - GPU INFERENCE HUB
* **Thiết bị:** Laptop MSI CPU i7-10750H, GPU NVIDIA RTX, RAM 16GB.
* **Vai trò:** Trung tâm cung cấp mô hình ngôn ngữ lớn (LLM Inference Server).
* **Công việc chính:**
  - Khởi chạy Ollama phục vụ các Tier khác qua địa chỉ LAN: `http://0.0.0.0:11434`.
  - Quản lý 2 model: `llama3.1:8b` (General LLM) và `qwen2.5-coder:14b` (Code-Specialized LLM).
  - Viết tài liệu, tổng hợp bài báo Springer LNICST, quản lý Git Master.
* **Nguyên tắc:** Không chạy các công cụ decompiler nặng làm nghẽn CPU trong lúc GPU đang suy luận.

---

## 🐧 TIER 2: KALI LINUX VM (VMWARE) - EXECUTION & EVALUATION HUB
* **Thiết bị:** Máy ảo Kali Linux (4 vCPU, 6GB-8GB RAM).
* **Vai trò:** Trung tâm biên dịch, dịch ngược tự động và chạy Pipeline đo lường.
* **Công việc chính:**
  1. **Biên dịch:** Dùng MinGW-w64 (`x86_64-w64-mingw32-gcc -s`) để build 80 file PE từ source code C trong `dataset/`.
  2. **Dịch ngược tự động:** Chạy Ghidra 11.x Headless với script `ExportRE.java` để sinh ra file `decompiled_contexts_80.json`.
  3. **Benchmark:** Gửi prompt tới Tier 1 (Ollama `192.168.86.1:11434` hoặc IP host) qua 4 tầng Context Escalation (CT1 -> CT4).
  4. **Thống kê:** Chạy script tính toán chỉ số SCHR, Miss Rate, kiểm định McNemar Test và Wilson Score Interval 95%.
* **Lệnh chạy chuẩn:**
  ```bash
  # Cập nhật code mới nhất từ Git
  git pull origin main

  # Chạy script thực nghiệm
  python3 scripts/step3_mcp_server_and_benchmark.py
  python3 scripts/step4_compute_statistics_and_tables.py
  ```

---

## 🪟 TIER 3: WINDOWS 11 VM (VMWARE) - ISOLATED MALWARE SANDBOX
* **Thiết bị:** Máy ảo Windows 11 Pro (`CLIENT01.lab.local`, 2 vCPU, 4GB RAM).
* **Vai trò:** Sandbox cách ly an toàn phục vụ phân tích tĩnh mẫu mã độc thực tế (**Gh0stRAT PE32**).
* **Công việc chính:**
  - Sử dụng **Detect It Easy (DIE)** kiểm tra PE Header, Compiler Signature, đồ thị Entropy.
  - Sử dụng **PE-bear** soi bảng Import Address Table (IAT) để bóc tách các API:
    - Persistence: `RegOpenKeyExA`, `RegSetValueExA` (khóa Registry Run).
    - Anti-Analysis: `IsDebuggerPresent`, `CheckRemoteDebuggerPresent`.
  - Chụp ảnh màn hình minh chứng lưu vào thư mục `tier3_win11/Image_Result/`.
* **Nguyên tắc sống còn:**
  - Tuyệt đối KHÔNG commit mẫu mã độc sống lên Git.
  - Chỉ commit ảnh chụp màn hình phân tích, ghi chú IOC và bảng trích xuất API.
