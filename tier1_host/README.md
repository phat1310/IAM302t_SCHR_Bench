# 🖥️ TÀI LIỆU THIẾT LẬP VÀ VẬN HÀNH HOST MSI WSL2 (TIER 1)
> **Dự án:** SCHR-Bench (Security-Critical Hallucination Rate Benchmark)  
> **Học phần:** IAM302t — Malware Analysis & Reverse Engineering (Fall 2026, RBL Model)  
> **Đơn vị:** Nhóm 7 (Lớp IA2007) — Đại học FPT TP. Hồ Chí Minh  
> **Phân tầng kiến trúc:** **Tier 1 — GPU Inference Hub & Git Master**  
> **Cập nhật:** 2026-10-27  

---

## 📌 1. VAI TRÒ CHIẾN LƯỢC CỦA TIER 1

Trong hệ thống kiến trúc 3-Tier độc lập của đề tài SCHR-Bench:
* **Trung tâm Suy Luận LLM (GPU Inference Hub):** Cung cấp tài nguyên tính toán GPU NVIDIA cho 2 mô hình cốt lõi:
  * `llama3.1:8b` (General Purpose LLM, phục vụ đối chứng baseline).
  * `qwen2.5-coder:14b` (Code-Specialized LLM, chuyên gia phân tích logic mã nguồn & assembly).
* **Cung cấp API qua LAN ảo:** Khởi chạy dịch vụ Ollama lắng nghe tại `0.0.0.0:11434`, cho phép:
  * **Tier 2 (Kali Linux VM):** Gửi 640 lượt truy vấn tự động theo 4 cấp độ ngữ cảnh (CT1 $\rightarrow$ CT4) cho 80 file nhị phân PE.
  * **Tier 3 (Windows 11 VM):** Gửi các đoạn mã nhị phân/pseudocode trích xuất từ mẫu Gh0stRAT để kiểm thử ảo giác.
* **Quản trị Git Master & Khoa học:** Điều phối luồng Git-Flow (`main`, `dev`, các nhánh Tier), tổng hợp kết quả thực nghiệm và đồng bộ mã nguồn bài báo khoa học chuẩn **Springer LNICST** nộp **EAI INISCOM 2027**.

---

## ⚙️ 2. THÔNG SỐ PHẦN CỨNG & HẠ TẦNG MÔI TRƯỜNG

| Thông số / Cấu phần | Chi tiết cấu hình | Ghi chú vận hành |
| :--- | :--- | :--- |
| **Thiết bị phần cứng** | Laptop MSI Gaming | CPU Intel Core i7-10750H @ 2.60GHz (12 CPUs), 16GB RAM |
| **GPU tăng tốc** | NVIDIA GeForce RTX Series | CUDA 12.x, VRAM phục vụ suy luận với thông lượng ~38 tok/s |
| **Hệ điều hành Host** | Windows 11 Home / Pro | Chạy nền tảng ảo hóa Hyper-V / WSL2 & VMware Workstation |
| **Môi trường Tier 1** | WSL2 Ubuntu 24.04 LTS | Lưu trữ workspace Git trung tâm, chạy Ollama daemon |
| **Cấu hình Mạng LAN** | VMware Virtual Adapter (VMnet8) | Host IP: `192.168.86.1` (Default Gateway của Tier 2 & Tier 3) |
| **Cổng dịch vụ LLM** | TCP Port `11434` | Binding: `0.0.0.0:11434`, mở Firewall cho dải `192.168.86.0/24` |

---

## 🚀 3. HƯỚNG DẪN KHỞI CHẠY VÀ CẤU HÌNH OLLAMA SERVER

### 3.1. Cấu hình biến môi trường và chạy Ollama trong WSL2
Để Ollama chấp nhận kết nối từ các máy ảo Kali và Windows 11 qua card mạng LAN ảo:
```bash
# Thiết lập Ollama lắng nghe trên tất cả card mạng
export OLLAMA_HOST=0.0.0.0:11434

# Khởi chạy Ollama Service
ollama serve
```

### 3.2. Cấu hình Windows Defender Firewall (Chạy PowerShell với quyền Administrator)
Nếu các máy ảo không kết nối được vào port `11434`, mở cổng trên Windows:
```powershell
New-NetFirewallRule -DisplayName "Ollama API Server (SCHR-Bench)" `
  -Direction Inbound `
  -LocalPort 11434 `
  -Protocol TCP `
  -Action Allow `
  -RemoteAddress 192.168.86.0/24
```

### 3.3. Tải và kiểm tra 2 mô hình nghiên cứu
```bash
# Tải mô hình General LLM
ollama pull llama3.1:8b

# Tải mô hình chuyên biệt mã nguồn
ollama pull qwen2.5-coder:14b

# Liệt kê các model đang có
ollama list
```

---

## 🛠️ 4. BỘ SCRIPTS QUẢN TRỊ TIER 1

Trong thư mục `tier1_host/scripts/`:
* `check_ollama_status.sh`: Kiểm tra trạng thái GPU, VRAM và phản hồi của API `http://localhost:11434/api/tags`.
* `test_inference_lan.py`: Gửi truy vấn kiểm tra phản hồi tức thì từ cả 2 mô hình LLM.

Chạy kiểm tra nhanh:
```bash
bash tier1_host/scripts/check_ollama_status.sh
python3 tier1_host/scripts/test_inference_lan.py
```
