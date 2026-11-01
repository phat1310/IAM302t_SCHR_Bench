# 🔬 SCHR-Bench: Security-Critical Hallucination Rate Benchmark
> **Evaluating Security-Critical Hallucinations of Large Language Models in Binary Reverse Engineering via Controlled Mutation Ground Truth**

[![Học phần](https://img.shields.io/badge/Course-IAM302t--Fall2026-green.svg)](file:///D:/ATTT/ATTT_FPT/KY_5_FALL_2026/IAM302t)
[![Đơn vị](https://img.shields.io/badge/Institution-FPT--University--HCMC-blue.svg)](https://hcmuni.fpt.edu.vn/)
[![Nhóm](https://img.shields.io/badge/Group-IA2007--G7-orange.svg)](#thành-viên-nhóm-7)
[![Hội nghị](https://img.shields.io/badge/Target-EAI--INISCOM--2027--Springer-red.svg)](https://iniscom.eai-conferences.org/)

---

## 📖 1. Giới Thiệu Đề Tài

Dự án **SCHR-Bench** được thực hiện trong khuôn khổ học phần **IAM302t (Malware Analysis and Reverse Engineering)** tại Trường Đại học FPT TP. Hồ Chí Minh theo mô hình **Research-Based Learning (RBL)**.

### Mục Tiêu Nghiên Cứu:
1. **Mục tiêu học phần (IAM302t):** Xây dựng hệ thống kiểm thử tự động đo lường độ chính xác và phát hiện các ảo giác nguy hiểm (Security Hallucination) của LLM khi dịch ngược mã nhị phân stripped x64.
2. **Mục tiêu học thuật:** Công bố bài báo khoa học chuẩn **Springer LNICST** tại hội nghị quốc tế **EAI INISCOM 2027**.

---

## 👥 2. Thành Viên Nhóm 7 (Lớp IA2007)

| STT | Họ và Tên | MSSV | Vai trò chính |
| :---: | :--- | :---: | :--- |
| 1 | **Nguyễn Tấn Phát** | **SE173285** | **Group Leader & Pipeline Co-Engineer** |
| 2 | **Đỗ Thiện Nhân** | **SE194134** | **C/Binary & Mutation Engineer** |
| 3 | **Nguyễn Trọng Duy** | **SE194413** | **Decompiler & Metrics Specialist** |
| 4 | **Võ Hồng Phúc** | **SE203844** | **Statistical Analyst & Lead Author** |

* **Giảng viên hướng dẫn:** Thầy **Đinh Mai Hoàng (DINHMH)**.

---

## 🏗️ 3. Cấu Trúc Hệ Thống Thực Nghiệm 3-Tier

```text
SCHR-Bench Architecture:
├── Tier 1 (Host MSI - WSL2): Ollama GPU Server (llama3.1:8b, qwen2.5-coder:14b)
├── Tier 2 (Kali Linux VM) : MinGW Compiler, Ghidra 11.x Headless, MCP Benchmark Pipeline
└── Tier 3 (Windows 11 VM) : Isolated Malware Sandbox (DIE, PE-bear, Gh0stRAT Case Study)
```

Xem chi tiết phân công và hướng dẫn lệnh tại [TIER_ROLES.md](TIER_ROLES.md).  
Xem nhật ký tiến độ dự án tại [PROJECT_STATUS.md](PROJECT_STATUS.md).

---

## 📂 4. Cấu Trúc Đóng Gói Sản Phẩm Nghiên Cứu (Research Artifact Package Standard)

Cấu trúc Repository tuân thủ 100% quy chuẩn đóng gói sản phẩm nghiên cứu khoa học / Artifact Evaluation chuẩn RBL ĐH FPT (tham chiếu template `SOC-RL-v2.0`):

```text
IAM302t_SCHR_Bench/
├── 📁 code/                    # Toàn bộ script và pipeline tự động hóa (Step 0 -> Step 4, Live Demo, Eval Engine)
├── 📁 dataset/                 # 40 hàm C bảo mật tự viết & 80 file PE x64 stripped đột biến
├── 📁 documentation/           # Master Plan, checklist nghiệm thu (D1 -> D5) & tài liệu kiến trúc
├── 📁 manuscript/              # Bản thảo LaTeX bài báo khoa học Springer LNICST (10-14 trang) & IEEE (8-10 trang)
├── 📁 results/                 # Cơ sở dữ liệu ngữ cảnh decompiled, raw query logs (540 entries) & bảng thống kê
├── 📁 tier1_host/              # Cấu hình GPU Inference Hub, scripts kiểm thử LAN & giám sát Ollama
├── 📁 tier2_kali/              # Môi trường biên dịch MinGW, Ghidra Headless decompiler & bộ ảnh minh chứng 01-12
├── 📁 tier3_win11/             # Môi trường Sandbox cách ly, báo cáo phân tích DIE & PE-bear cho mẫu Gh0stRAT
├── 📄 CITATION.cff             # File định dạng trích dẫn chuẩn cho bài báo khoa học và GitHub
├── 📄 LICENSE                  # Giấy phép mã nguồn mở MIT License
├── 📄 MANIFEST.txt             # Bảng kê khai mục lục toàn bộ file, dữ liệu và mô tả chức năng
├── 📄 README.md                # Tài liệu tổng quan dự án & hướng dẫn vận hành
├── 📄 reproduce.sh             # Script 1-lệnh tự động tái hiện toàn bộ kết quả thực nghiệm
├── 📄 PROJECT_STATUS.md        # Bảng theo dõi tiến độ đồng bộ giữa các Tier
├── 📄 TIER_ROLES.md            # Quy chuẩn phân công nhiệm vụ cho từng máy ảo / AI Agent
└── 📄 .gitignore               # Cấu hình loại trừ file nhị phân mã độc và file đĩa ảo lớn
```

---

## 🌿 5. Chiến Lược Phân Nhánh Git (Branching Workflow)

Để bảo đảm tính ổn định và tách bạch môi trường thực nghiệm, dự án tuân theo quy trình Git-Flow:
* **`main`**: Nhánh bảo vệ (Protected Branch). Chỉ cập nhật khi nghiệm thu hoàn tất các mốc D1 $\rightarrow$ D5 và bản thảo hoàn thiện của bài báo khoa học.
* **`dev`**: Nhánh tích hợp trung tâm (Integration Branch). Nơi hội tụ các kết quả thực nghiệm và tính năng mới từ các Tier.
* **Nhánh theo Tier / Feature**:
  * `tier1-host`: Phục vụ cấu hình Ollama, prompt engineering, paper drafts.
  * `tier2-kali`: Phục vụ MinGW, Ghidra Headless, MCP Benchmark.
  * `tier3-win11`: Phục vụ Sandbox setup, công cụ DIE/PE-bear và bóc tách mẫu Gh0stRAT.

### Luồng làm việc chuẩn:
1. **Lấy code mới nhất từ dev:**
   ```bash
   git checkout dev
   git pull origin dev
   ```
2. **Tạo nhánh làm việc:**
   ```bash
   git checkout -b tier2-kali
   ```
3. **Commit & Push kết quả:**
   ```bash
   git add .
   git commit -m "feat(tier2): cập nhật bảng kết quả thực nghiệm CT1-CT4"
   git push -u origin tier2-kali
   ```
4. **Merge vào `dev`:** Tạo Pull Request trên GitHub từ `tierX` vào `dev` hoặc gộp trực tiếp trên máy sau khi test đạt.
5. **Merge vào `main`:** Nghiệm thu hoàn thiện mốc đồ án rồi merge `dev` $\rightarrow$ `main`.

---

## ⚡ 6. Hướng Dẫn Tái Hiện Thực Nghiệm (1-Click Reproducibility)

Để thẩm định tính toàn vẹn và tái hiện kết quả đo lường ảo giác của đồ án, chỉ cần thực thi kịch bản `reproduce.sh`:

```bash
# Cấp quyền thực thi và chạy kịch bản tái hiện 1-lệnh:
chmod +x reproduce.sh
bash reproduce.sh
```

Luồng tái hiện sẽ tự động thực hiện:
1. **Kiểm tra tính đúng đắn Ground Truth (E0 Sanity Check):** Xác thực 80 test vectors (160 binary execution assertions) trên 40 cặp hàm C bảo mật đạt 100% behavioral divergence.
2. **Động cơ thống kê (Statistical Engine):** Tính toán độ tin cậy Wilson Score Interval 95%, kiểm định McNemar ($N=80$) và xuất bảng LaTeX từ 540 lượt đánh giá thực nghiệm.
3. **Kịch bản Live Demo tương tác (Mốc D3):** Trình diễn trực quan phản ứng của mô hình qua 3 bước (Ground Truth $\rightarrow$ Ảo giác CT1 $\rightarrow$ Đối chiếu CT2 Assembly Anchor).
