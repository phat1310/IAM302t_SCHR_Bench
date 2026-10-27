# 🧭 PROJECT STATUS & AUTOMATION MANIFEST (SCHR-BENCH)
> **Tài liệu theo dõi trạng thái đồng bộ liên Tier (Tier 1 <-> Tier 2 <-> Tier 3)**  
> **Cập nhật lần cuối:** 2026-10-27  
> **Học phần:** IAM302t — Malware Analysis & Reverse Engineering (Fall 2026, RBL Model)  
> **Nhóm thực hiện:** Nhóm 7 (Lớp IA2007) — Trường Đại học FPT TP.HCM  

---

## 📌 1. Tiến Độ Các Mốc Đồ Án (Deliverables D1 -> D5)
- [x] **D1 (Proposal & Re-alignment):** Chuyển hướng thành công sang đề tài **SCHR-Bench** (Ground Truth đột biến C, loại trừ phụ thuộc IDA Pro).
- [x] **D2 (Ground Truth & Sanity Check):** 
  - Hoàn tất bộ 40 hàm C bảo mật tự viết kèm các biến thể đột biến (A, S, P, E, C).
  - Hoàn tất **Thí nghiệm E0**: 40/40 (100% PASS) kiểm định phân biệt, 160 assertions.
- [ ] **D3 (Automated Pipeline & Live Demo):** 
  - [x] Ghidra Headless script trích xuất pseudocode & assembly JSON (`decompiled_contexts_80.json`).
  - [ ] Thực thi MCP Benchmark Agent trên Ollama Server (`llama3.1:8b` & `qwen2.5-coder:14b`).
  - [ ] Tính toán chỉ số SCHR, Miss Rate, McNemar Test.
- [ ] **D4 (Section 5 Case Study):** Phân tích tĩnh mẫu Gh0stRAT PE32 (`ea7cd59c...`) trên Sandbox Tier 3.
- [ ] **D5 (Final Paper & Bảo vệ đồ án):** Hoàn thiện bài báo Springer LNICST (8-10 trang) nộp EAI INISCOM 2027.

---

## ⚡ 2. Trạng Thái Vận Hành Hiện Tại Của Từng Tier

| Phân Tầng (Tier) | Môi Trường | Nhiệm Vụ Cốt Lõi | Trạng Thái Hoạt Động |
| :--- | :--- | :--- | :---: |
| **Tier 1 (Host MSI - WSL2)** | Ubuntu (`0.0.0.0:11434`) | Phục vụ GPU Ollama Server (`llama3.1`, `qwen2.5-coder`) | 🟢 Sẵn sàng |
| **Tier 2 (Kali Linux VM)** | Kali Linux (VMware) | Build 80 PE, Ghidra Headless, Chạy Benchmark Pipeline | 🟡 Đang chờ chạy Step 3 |
| **Tier 3 (Win11 VM)** | Windows 11 Sandbox | Phân tích mẫu Gh0stRAT (DIE, PE-bear, IAT & Run Key) | 🟢 Tools đã cài đặt |

---

## 🚀 3. Hướng Dẫn Tác Vụ Kế Tiếp Cho AI Agent / Thành Viên Nhóm

Khi một AI Agent hoặc thành viên mở workspace này ở bất kỳ Tier nào:
1. Đọc file `TIER_ROLES.md` để xác định rõ quyền hạn và nhiệm vụ của máy tính hiện tại.
2. Kiểm tra thư mục `scripts/` để chạy đúng bước cần thiết.
3. Sau khi thực thi xong, cập nhật log kết quả vào thư mục `results/`, sửa file `PROJECT_STATUS.md` này và chạy lệnh:
   ```bash
   git add results/ PROJECT_STATUS.md
   git commit -m "update: [Tier X] cập nhật kết quả thực nghiệm mới nhất"
   git push origin main
   ```
