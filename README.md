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

```
SCHR-Bench Architecture:
├── Tier 1 (Host MSI - WSL2): Ollama GPU Server (llama3.1:8b, qwen2.5-coder:14b)
├── Tier 2 (Kali Linux VM) : MinGW Compiler, Ghidra 11.x Headless, MCP Benchmark Pipeline
└── Tier 3 (Windows 11 VM) : Isolated Malware Sandbox (DIE, PE-bear, Gh0stRAT Case Study)
```

Xem chi tiết phân công và hướng dẫn lệnh tại [TIER_ROLES.md](TIER_ROLES.md).  
Xem nhật ký tiến độ dự án tại [PROJECT_STATUS.md](PROJECT_STATUS.md).

---

## 📂 4. Cấu Trúc Thư Mục Repository

```
04_IAM302t_Github_Project/
├── dataset/                    # 40 hàm C bảo mật tự viết & các biến thể đột biến (A, S, P, E, C)
├── docs/                       # Master Plan Obsidian, slide thuyết trình & bài báo Springer
├── results/                    # Bảng kết quả JSON, log thực nghiệm và bảng thống kê E0
├── scripts/                    # Toàn bộ script tự động hóa (Step 0 -> Step 4)
├── tier2_kali/                 # Tài liệu & script hướng dẫn chạy riêng cho máy ảo Kali Linux
├── tier3_win11/                # Tài liệu & script phân tích tĩnh mã độc cho Sandbox Win11
├── .gitignore                  # Cấu hình loại trừ file nhị phân mã độc và file đĩa ảo lớn
├── PROJECT_STATUS.md           # Bảng theo dõi tiến độ đồng bộ giữa các Tier
├── TIER_ROLES.md               # Quy chuẩn phân công nhiệm vụ cho từng máy ảo / AI Agent
└── README.md                   # Tài liệu tổng quan dự án
```

---

## ⚡ 5. Hướng Dẫn Đồng Bộ Giữa Các Máy Ảo

Mỗi khi bắt đầu ca làm việc trên bất kỳ máy ảo nào:
```bash
git pull origin main
```

Sau khi hoàn thành tác vụ (sinh kết quả mới / cập nhật script):
```bash
git add .
git commit -m "update: [Tier X] nội dung công việc vừa hoàn thành"
git push origin main
```
