# 🖥️ TÀI LIỆU THIẾT LẬP VÀ TRẠNG THÁI MÁY ẢO WINDOWS 11 PRO (VMWARE)
> **Dự án:** SCHR-Bench (Security-Critical Hallucination Rate Benchmark)  
> **Học phần:** IAM302t — Malware Analysis and Reverse Engineering (Fall 2026, RBL Model)  
> **Đơn vị:** Đại học FPT TP. Hồ Chí Minh — Nhóm 7 (IA2007)  
> **Phân tầng kiến trúc:** **Tier 3 — Isolated Malware Sandbox (CLIENT01)**  
> **Thời điểm cập nhật:** 2026-10-28  

---

## 1. Định Vị Vai Trò Của Máy Ảo Trong Kiến Trúc 3-Tier

Căn cứ theo [Master Plan](../docs/SCHR_BENCH_MASTER_PLAN_OBSIDIAN.md), hệ thống thực nghiệm của đồ án được phân bổ như sau:
* **Tier 1 (Máy thật MSI - WSL2 Ubuntu):** GPU NVIDIA phục vụ Ollama Server (`0.0.0.0:11434`, `llama3.1:8b`, `qwen2.5-coder:14b`).
* **Tier 2 (Máy ảo Kali Linux 7.1.5):** Trung tâm thực thi tự động (MinGW-w64 build 80 PE, Ghidra 11.x Headless trích xuất JSON, MCP Pipeline, tính toán chỉ số SCHR, BLEU, McNemar test).
* **Tier 3 (Máy ảo Windows 11 Pro này - CLIENT01):** 
  * Đóng vai trò là **Sandbox cô lập an toàn** chạy hệ điều hành Windows thật.
  * **Nhiệm vụ cốt lõi:** Chuyên trách phân tích tĩnh mẫu mã độc thực tế **Gh0stRAT PE32** (`ea7cd59c...`) để bóc tách các cơ chế Windows API thực tế (Registry Run Key Persistence, Anti-Debugging).
  * **Đầu ra mục tiêu:** Cung cấp dữ liệu, bằng chứng và hình ảnh thực tế cho **Section 5: Real-World Case Study (Gh0stRAT)** trong bài báo khoa học chuẩn Springer LNICST (EAI INISCOM 2027).
  * **Quy chuẩn tài nguyên:** Giới hạn 2 vCPU, 4GB RAM — tuyệt đối không chạy các tác vụ biên dịch nặng hay Ghidra Headless diện rộng để tránh tràn RAM.

---

## 2. Nhật Ký Khảo Sát Hệ Thống & Cài Đặt (System Diagnostics)

| Hạng mục kiểm tra | Trạng thái ghi nhận | Chi tiết & Ghi chú kỹ thuật |
| :--- | :---: | :--- |
| **Hệ điều hành** | ✅ Đạt | Windows 11 Pro 64-bit (chạy trên nền VMware Workstation, hostname: `CLIENT01`). |
| **Cấu hình Mạng & Ollama** | ✅ Đạt | Card mạng NAT `192.168.86.136`. Ping máy Host (`192.168.86.1`) 0ms. Cổng TCP `11434` thông suốt, nhận diện `llama3.1:8b` & `qwen2.5-coder:14b`. |
| **Môi trường Python** | ✅ Đạt | Python 3.12.10 đã cài đặt, cấu hình PATH hoàn chỉnh. Chạy thành công kiểm định E0 Sanity Check (40/40 pairs PASS, 160 assertions). |
| **Môi trường Git** | ✅ Đạt | Git for Windows v2.56.0 đã cài đặt, cấu hình GCM và đồng bộ theo luồng Git-Flow (`main`, `dev`, `tier3-win11`). |
| **Công cụ soạn thảo** | ✅ Đạt | Visual Studio Code đã cài đặt, tích hợp điều khiển Git và Markdown. |
| **Quản lý tài liệu** | ✅ Đạt | Obsidian đã cài đặt phục vụ quản lý Vault đồ án RBL IAM302t. |
| **Khảo sát Thư mục Dự án** | ✅ Chuẩn hóa | Không gian làm việc sạch sẽ, cấu trúc chuẩn 3-Tier đồng bộ 100% với Git. |
| **Công cụ phân tích tĩnh** | ✅ Sẵn sàng | Đã triển khai Detect It Easy v3.21 và PE-bear v0.7.2 Portable (tại `C:\Tools` và Shortcut Desktop). |
| **Kênh chia sẻ Host - VM** | ✅ Sẵn sàng | Thư mục VMware Shared Folder sẵn sàng tại: `\\vmware-host\Shared Folders\Win11_shared` (đã có Shortcut Desktop). |
| **Mẫu Gh0stRAT** | ✅ **ĐÃ SẴN SÀNG** | Tệp ZIP mẫu Gh0stRAT PE32 đã có tại `C:\IAM302t_Github_Project\Malware\` (kích thước nén: ~15.7MB, SHA256: `ea7cd59c402128b0beffba34a6fb7b3f6f9fc5be62cb4aa51e605d3bcaee98be`). Chứa 1 file `.exe` PE32 (17.2MB). Giai đoạn phân tích tĩnh bằng DIE & PE-bear đang được kích hoạt. |

---

## 3. Các Công Cụ Phân Tích Đã Được Cài Đặt (Tools Deployment)

Nhằm giữ cho máy ảo Windows 11 nhẹ nhất có thể và không can thiệp sâu vào Registry hệ thống, toàn bộ công cụ được triển khai dưới dạng **Portable x64**:

### 3.1. Detect It Easy (DIE) v3.21 (x64 Portable)
* **Vị trí cài đặt:** `C:\Tools\DIE\die\die.exe`
* **Lối tắt ngoài màn hình:** Đã tạo shortcut `Detect It Easy.lnk` tại Desktop.
* **Mục đích sử dụng:**
  * Nhận diện chữ ký trình biên dịch (MSVC, GCC), Linker, Subsystem PE.
  * Phân tích đồ thị Entropy để phát hiện xem mã độc có bị đóng gói (packed) hay mã hóa payload hay không.
  * Soi nhanh danh sách Section (`.text`, `.data`, `.rsrc`) và các hàm API được import.

### 3.2. PE-bear v0.7.2 (x64 Portable)
* **Vị trí cài đặt:** `C:\Tools\PE-bear\PE-bear.exe`
* **Lối tắt ngoài màn hình:** Đã tạo shortcut `PE-bear.lnk` tại Desktop.
* **Mục đích sử dụng:**
  * Công cụ trực quan hóa cấu trúc PE Headers chuyên sâu.
  * Kiểm tra và phân tích bảng **Import Address Table (IAT)**: Định vị các Windows API nhạy cảm phục vụ Case Study:
    * API Persistence: `RegOpenKeyExA`, `RegCreateKeyExA`, `RegSetValueExA`.
    * API Anti-Analysis: `IsDebuggerPresent`, `CheckRemoteDebuggerPresent`.

### 3.3. Script cài đặt tự động hóa (PowerShell)
* **Vị trí lưu trữ:** `tier3_win11/scripts/setup_pe_tools.ps1`
* **Cách sử dụng:** Khi dựng lại máy ảo mới, chỉ cần chạy script này để tự động tải DIE và PE-bear, giải nén vào `C:\Tools` và tự tạo Desktop Shortcut.

---

## 4. Danh Mục Tệp Đã Được Chuẩn Hóa Trên Máy

```
C:\IAM302t_Github_Project\IAM302t_SCHR_Bench\
├── dataset/                              <-- Bộ 80 hàm C mẫu và Ground Truth
├── docs/                                 <-- Tài liệu Master Plan & Checklist Giai Đoạn 2
├── results/                              <-- Log benchmark và bảng kết quả Springer
├── scripts/                              <-- Pipeline tự động hóa Step 0 đến Step 4
├── tier2_kali/                           <-- Kế hoạch và báo cáo của Tier 2 Kali Linux
├── tier3_win11/                          <-- (Thư mục làm việc của Tier 3)
│   ├── README.md                         <-- (Tệp tài liệu này)
│   ├── Image_Result/                     <-- Ảnh minh chứng phân tích Gh0stRAT (DIE & PE-bear)
│   └── scripts/
│       └── setup_pe_tools.ps1            <-- Script tự động tải & cấu hình DIE, PE-bear
├── .gitignore
├── PROJECT_STATUS.md
├── README.md
└── TIER_ROLES.md

C:\IAM302t_Github_Project\Malware\       <-- [SANDBOX ONLY - KHÔNG COMMIT LÊN GIT]
└── ea7cd59c...zip                        <-- Mẫu Gh0stRAT PE32 (ZIP, ~15.7MB)

C:\Tools\
├── DIE\
│   └── die\die.exe                       <-- Công cụ Detect It Easy Portable
└── PE-bear\
    └── PE-bear.exe                       <-- Công cụ PE-bear Portable

C:\Users\ngtp1\Desktop\
├── Detect It Easy.lnk                    <-- Shortcut Desktop
├── PE-bear.lnk                           <-- Shortcut Desktop
├── Visual Studio Code.lnk                <-- Shortcut Desktop
├── Obsidian.lnk                          <-- Shortcut Desktop
└── Share_folder.txt                      <-- Đường dẫn \\vmware-host\Shared Folders\Win11_shared
```

---

## 5. Các Bước Kế Tiếp Cần Triển Khai (Action Items — Giai Đoạn 2 / Mốc D4)

> **🔵 TRẠNG THÁI HIỆN TẠI (2026-10-28):** Mẫu Gh0stRAT PE32 đã có trong máy. Bắt đầu thực thi checklist phân tích tĩnh.

1. ✅ **Tiếp nhận mẫu Gh0stRAT PE32:** Đã có tại `C:\IAM302t_Github_Project\Malware\ea7cd59c...zip`.
2. **[TODO] Giải nén mẫu** — Dùng 7-Zip với mật khẩu `infected` (chuẩn MalwareBazaar):
   * Chú ý: Tắt Windows Defender Real-time Protection trước khi giải nén để tránh mẫu bị xóa tự động.
3. **[TODO] Phân tích tĩnh với Detect It Easy (DIE v3.21):**
   * Mở `C:\Tools\DIE\die\die.exe` (hoặc shortcut Desktop).
   * Kéo thả file `.exe` vào DIE, kiểm tra PE Format, Compiler, Linker và Entropy Graph.
   * Chụp ảnh lưu: `tier3_win11/Image_Result/die_entropy_gh0strat.png`
4. **[TODO] Soi bảng IAT với PE-bear v0.7.2:**
   * Mở `C:\Tools\PE-bear\PE-bear.exe` (hoặc shortcut Desktop).
   * Tab **Imports** → `ADVAPI32.dll`: Highlight `RegSetValueExA`, `RegCreateKeyExA`.
   * Tab **Imports** → `KERNEL32.dll`: Highlight `IsDebuggerPresent`.
   * Chụp ảnh lưu: `tier3_win11/Image_Result/pebear_iat_advapi32.png` & `pebear_iat_antidebug.png`
5. **[TODO] Trích xuất chuỗi IOC:**
   * Tìm chuỗi `Software\Microsoft\Windows\CurrentVersion\Run` → Chụp ảnh: `gh0strat_run_key_string.png`
6. **[TODO] Commit ảnh minh chứng lên Git** để Tier 2 (Kali) nhận dữ liệu và chạy Ghidra.

Xem checklist đầy đủ: [PHASE2_GH0STRAT_EXECUTION_CHECKLIST.md](../docs/PHASE2_GH0STRAT_EXECUTION_CHECKLIST.md)
