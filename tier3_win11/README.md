# 🖥️ TÀI LIỆU THIẾT LẬP VÀ TRẠNG THÁI MÁY ẢO WINDOWS 11 PRO (VMWARE)
> **Dự án:** SCHR-Bench (Security-Critical Hallucination Rate Benchmark)  
> **Học phần:** IAM302t — Malware Analysis and Reverse Engineering (Fall 2026, RBL Model)  
> **Đơn vị:** Đại học FPT TP. Hồ Chí Minh — Nhóm 7 (IA2007)  
> **Phân tầng kiến trúc:** **Tier 3 — Isolated Malware Sandbox (CLIENT01)**  
> **Thời điểm cập nhật:** 2026-10-26  

---

## 1. Định Vị Vai Trò Của Máy Ảo Trong Kiến Trúc 3-Tier

Căn cứ theo [Master Plan](file:///c:/IAM302t_Proejct/SCHR_BENCH_MASTER_PLAN_OBSIDIAN.md#L168-L207), hệ thống thực nghiệm của đồ án được phân bổ như sau:
* **Tier 1 (Máy thật MSI - WSL2 Ubuntu):** GPU NVIDIA phục vụ Ollama Server (`0.0.0.0:11434`, `llama3.1:8b`, `qwen2.5-coder:14b`).
* **Tier 2 (Máy ảo Kali Linux 7.1.5):** Trung tâm thực thi tự động (MinGW-w64 build 80 PE, Ghidra 11.x Headless trích xuất JSON, MCP Pipeline, tính toán chỉ số SCHR, BLEU, McNemar test).
* **Tier 3 (Máy ảo Windows 11 Pro này - CLIENT01):** 
  * Đóng vai trò là **Sandbox cô lập an toàn** chạy hệ điều hành Windows thật.
  * **Nhiệm vụ cốt lõi:** Chuyên trách phân tích tĩnh mẫu mã độc thực tế **Gh0stRAT PE32** (`ea7cd59c...`) để bóc tách các cơ chế Windows API thực tế (Registry Run Key Persistence, Anti-Debugging).
  * **Đầu ra mục tiêu:** Cung cấp dữ liệu, bằng chứng và hình ảnh thực tế cho **Section 5: Real-World Case Study (Gh0stRAT)** trong bài báo khoa học chuẩn Springer LNICST (EAI INISCOM 2027).
  * **Quy chuẩn tài nguyên:** Giới hạn 2 vCPU, 4GB RAM — tuyệt đối không chạy các tác vụ biên dịch nặng hay Ghidra Headless diện rộng để tránh tràn RAM.

---

## 2. Nhật Ký Khảo Sát Hệ Thống Ban Đầu (System Diagnostics)

| Hạng mục kiểm tra | Trạng thái ghi nhận | Chi tiết & Ghi chú kỹ thuật |
| :--- | :---: | :--- |
| **Hệ điều hành** | ✅ Đạt | Windows 11 Pro 64-bit (chạy trên nền VMware Workstation). |
| **Cấu hình Mạng** | ✅ Đạt | Card mạng NAT: `192.168.86.136`, Gateway: `192.168.86.2`. Ping máy Host (`192.168.86.1`) thông 0ms. |
| **Kết nối Ollama (Host)** | ⚠️ Chưa mở | Kết nối TCP cổng `11434` tới `192.168.86.1` thất bại (Ollama trên Host chưa bind `0.0.0.0:11434` hoặc bị Windows Firewall chặn). |
| **Môi trường cơ bản** | ⚠️ Máy sạch | Chưa cài Python, Git, OpenJDK/Java (trình quản lý gói `winget v1.29` đã có sẵn). |
| **Khảo sát Thư mục Dự án** | ✅ Xác nhận | `C:\IAM302t_Proejct` chứa bộ 80 file C dataset (`SCHR_Bench_C_Functions`), các script tự động hóa từ `step0` đến `step4`. |
| **Mẫu Gh0stRAT** | ❌ Chưa có | Không tìm thấy tệp mã độc `ea7cd59c...` trong thư mục dự án hoặc máy ảo. |
| **Kênh chia sẻ Host - VM** | ✅ Sẵn sàng | Thư mục VMware Shared Folder sẵn sàng tại: `\\vmware-host\Shared Folders\Win11_shared`. |

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

---

## 4. Danh Mục Tệp Đã Được Khởi Tạo Trên Máy

```
C:\IAM302t_Proejct\
├── Win11_Pro_VMware\
│   └── README.md                         <-- (Tệp tài liệu này)
├── setup_pe_tools.ps1                    <-- Script PowerShell tự động tải & cấu hình DIE, PE-bear
└── ... (Các script Pipeline và bộ Dataset C)

C:\Tools\
├── DIE\
│   └── die\die.exe                       <-- Công cụ Detect It Easy Portable
└── PE-bear\
    └── PE-bear.exe                       <-- Công cụ PE-bear Portable

C:\Users\ngtp1\Desktop\
├── Detect It Easy.lnk                    <-- Shortcut Desktop
└── PE-bear.lnk                           <-- Shortcut Desktop
```

---

## 5. Các Bước Kế Tiếp Cần Triển Khai (Action Items)

1. **Tiếp nhận mẫu Gh0stRAT PE32 (`ea7cd59c...`):**
   * Đưa mẫu từ máy Host vào thư mục chia sẻ `\\vmware-host\Shared Folders\Win11_shared`.
   * Di chuyển mẫu vào thư mục làm việc để bảo toàn mẫu an toàn.
2. **Thực hiện phân tích tĩnh (Static RE) mẫu Gh0stRAT:**
   * Mở bằng DIE: Kiểm tra entropy và nhận diện packer.
   * Mở bằng PE-bear: Soi chi tiết IAT, định vị offset của các API liên quan đến Registry Persistence.
3. **Thu thập Artifacts cho Paper (Section 5):**
   * Chụp ảnh màn hình bảng IAT và các chuỗi IOC quan trọng (`Software\Microsoft\Windows\CurrentVersion\Run`, tên key độc hại).
   * Bàn giao kết quả bóc tách cho thành viên **Võ Hồng Phúc (SE203844)** và **Nguyễn Tấn Phát (SE173285)** để tổng hợp vào bài báo khoa học Springer.
