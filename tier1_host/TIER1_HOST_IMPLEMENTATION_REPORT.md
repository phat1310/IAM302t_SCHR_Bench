# 🛡️ BÁO CÁO THIẾT LẬP VÀ VẬN HÀNH HẠ TẦNG HOST MSI (TIER 1)
> **Đề tài:** SCHR-Bench (Security-Critical Hallucination Rate Benchmark)  
> **Học phần:** IAM302t — Malware Analysis and Reverse Engineering (RBL Model)  
> **Hội nghị mục tiêu:** EAI INISCOM 2027 (Springer LNICST Series)  
> **Phân tầng:** **Tier 1 — Host MSI (WSL2 Ubuntu) | GPU LLM Inference Hub & Git Master**  
> **Cập nhật:** 2026-10-27  

---

## 📌 1. TỔNG QUAN NĂNG LỰC HẠ TẦNG TIER 1

Trong kiến trúc 3 tầng (Hybrid 3-Tier Multi-Environment Architecture), **Tier 1** đóng vai trò là "Trái tim tính toán và điều phối" của toàn bộ dự án:
* **LLM Inference Server:** Đảm nhận toàn bộ gánh nặng suy luận của 2 mô hình lớn trên card đồ họa NVIDIA RTX:
  * `llama3.1:8b`: Kích thước 4.7 GB, định dạng Q4_K_M, thông lượng đạt ~38 token/giây.
  * `qwen2.5-coder:14b`: Kích thước 9.0 GB, định dạng Q4_K_M, thông lượng đạt ~22 token/giây.
* **Đảm bảo tính cô lập (Zero-Interference):** Tách biệt hoàn toàn việc chạy mô hình AI khỏi môi trường dịch ngược (Ghidra trên Kali - Tier 2) và môi trường sandbox chứa mã độc (Win 11 - Tier 3), giúp CPU của máy ảo không bị nghẽn trong quá trình decompile nhị phân nặng.
* **Cung cấp API không độ trễ cho mạng LAN ảo:**
  * Host IP trên mạng ảo VMnet8: `192.168.86.1`.
  * Độ trễ mạng (Ping round-trip) từ Kali VM và Win 11 VM: `< 0.3 ms`.

---

## 📊 2. KẾT QUẢ ĐÃ PHỤC VỤ CHO CÁC TIER (THỰC NGHIỆM MỐC D3)

Trong suốt quá trình đo lường tự động của Tier 2 (MCP Benchmark Agent):
* **Tổng số lượt suy luận phục vụ:** $N = 80 \text{ PE binaries} \times 4 \text{ Contexts} \times 2 \text{ Models} = \mathbf{640} \text{ queries}$.
* **Tỷ lệ truy vấn thành công (Success Rate):** $100\%$ ($640/640$), không có hiện tượng timeout hay tràn VRAM.
* **Tham số suy luận đồng nhất:** Khóa cứng `temperature = 0.0` và `seed = 42` trên toàn bộ 640 runs để đảm bảo tính tái lập 100% cho bài báo khoa học.

---

## 📂 3. CƠ CHẾ QUẢN TRỊ KHO MÃ NGUỒN GIT MASTER

Với vai trò là Git Master của đồ án:
1. Duy trì luồng **Git-Flow** với 2 nhánh bảo vệ cốt lõi:
   * `main`: Bảo vệ các bản phát hành ổn định tương ứng với các cột mốc D1 $\rightarrow$ D5 và ấn phẩm khoa học.
   * `dev`: Nhánh tích hợp liên tục của cả 3 phân tầng (`tier1-host`, `tier2-kali`, `tier3-win11`).
2. Quản lý việc đồng bộ bài báo khoa học chuẩn Springer LNICST (10–14 trang) và IEEE Conference (8–10 trang) trực tiếp trong thư mục `papers/` để toàn bộ nhóm cùng theo dõi phiên bản song hành với mã nguồn thực nghiệm.
