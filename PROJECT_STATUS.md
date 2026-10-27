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
- [x] **D3 (Automated Pipeline & Live Demo):** 
  - [x] Ghidra Headless script trích xuất pseudocode & assembly JSON (`decompiled_contexts_80.json`).
  - [x] Thực thi MCP Benchmark Agent trên Ollama Server (`llama3.1:8b` & `qwen2.5-coder:14b`) toàn diện 80 binary PE ($N=80$).
  - [x] Tính toán chỉ số SCHR, Miss Rate, McNemar Test, 95% Wilson CI (`PAPER_TABLES_SPRINGER.md`).
  - [x] Đóng gói kịch bản Live Demo 1-lệnh trực quan (`scripts/live_demo.sh`).
- [ ] **D4 (Section 5 Case Study):** Phân tích tĩnh mẫu Gh0stRAT PE32 (`ea7cd59c...`) trên Sandbox Tier 3.
- [ ] **D5 (Final Paper & Bảo vệ đồ án):** Hoàn thiện bài báo Springer LNICST (8-10 trang) nộp EAI INISCOM 2027.

---

## ⚡ 2. Trạng Thái Vận Hành Hiện Tại Của Từng Tier

| Phân Tầng (Tier) | Môi Trường | Nhiệm Vụ Cốt Lõi | Trạng Thái Hoạt Động |
| :--- | :--- | :--- | :---: |
| **Tier 1 (Host MSI - WSL2)** | Ubuntu (`0.0.0.0:11434`) | Phục vụ GPU Ollama Server, Git Master & Đồng bộ Bài báo Springer/IEEE | 🟢 Hoàn tất tài liệu Tier 1, scripts GPU & Tích hợp Papers LaTeX |
| **Tier 2 (Kali Linux VM)** | Kali Linux (VMware) | Build 80 PE, Ghidra Headless, Chạy Benchmark Pipeline | 🟢 Hoàn tất Benchmark 80 PE & Sẵn sàng Live Demo D3 |
| **Tier 3 (Win11 VM)** | Windows 11 Sandbox | Phân tích mẫu Gh0stRAT (DIE, PE-bear, IAT & Run Key) | 🟢 Hoàn tất môi trường & Sẵn sàng phân tích Gh0stRAT |

---

## 🚀 3. Quy Chuẩn Phân Nhánh Git (Git-Flow) & Hướng Dẫn Tác Vụ Cho Từng Tier

Dự án áp dụng mô hình phân nhánh chuẩn **Git-Flow / Feature-Branch**:
* **`main`**: Nhánh ổn định, bảo vệ các mốc nộp đồ án (D1 -> D5) và bài báo Springer chính thức.
* **`dev`**: Nhánh tích hợp trung tâm. Mọi thay đổi của các Tier được merge vào đây để kiểm thử.
* **Nhánh của từng Tier:**
  * `tier1-host`: Phục vụ cấu hình Ollama, prompt engineering, bài báo Springer.
  * `tier2-kali`: Phục vụ MinGW, Ghidra Headless, MCP Benchmark.
  * `tier3-win11`: Phục vụ công cụ DIE/PE-bear và bóc tách mẫu Gh0stRAT.

### Quy trình làm việc chuẩn cho Agent / Thành viên:
1. Luôn xuất phát từ nhánh `dev` mới nhất:
   ```bash
   git checkout dev
   git pull origin dev
   ```
2. Làm việc trên nhánh riêng của Tier:
   ```bash
   git checkout -b tier2-kali    # (Hoặc tier3-win11, tier1-host)
   ```
3. Sau khi hoàn thành tác vụ và kiểm thử thành công:
   ```bash
   git add .
   git commit -m "feat(tierX): nội dung tác vụ vừa hoàn thành"
   git push -u origin tier2-kali
   ```
4. Gộp code vào nhánh `dev` (qua Pull Request trên GitHub hoặc gộp trực tiếp):
   ```bash
   git checkout dev
   git pull origin dev
   git merge tier2-kali
   git push origin dev
   ```
5. **Chỉ merge `dev` vào `main`** khi toàn bộ test suite và mốc đồ án được nghiệm thu đạt 100%.
