# 📂 KALI 2026 PROJECT REPOSITORY (TIER 2)

Thư mục này lưu trữ các tài liệu, hướng dẫn, báo cáo kỹ thuật và ảnh minh chứng thực nghiệm dành riêng cho **Máy ảo Kali Linux 2026 (Tier 2 - Processing & Evaluation Hub)** trong đề tài nghiên cứu **SCHR-Bench**.

---

## 📑 Tài liệu & Kế hoạch Thực thi:
* ⭐ **[Kế hoạch Hành động & Danh mục Task Tier 2 (TASK_TIER2_KALI_EXECUTION_PLAN.md)](TASK_TIER2_KALI_EXECUTION_PLAN.md)** *(Mới nhất — Checklist từng bước chi tiết kèm lệnh terminal chuẩn và quy hoạch ảnh minh chứng)*
* 👉 **[Báo cáo Tổng hợp Triển khai & Hướng dẫn Vận hành](KALI_TIER2_IMPLEMENTATION_REPORT.md)** *(Báo cáo đầy đủ kiến trúc, kết quả thử nghiệm và bảng kê khai hình ảnh)*

---

## 🖼️ Quản Lý Ảnh Minh Chứng Thực Nghiệm (`Image_Result/`)

Toàn bộ ảnh chụp màn hình minh chứng quá trình thiết lập và thực nghiệm tại Tier 2 được lưu trữ tại thư mục: [`tier2_kali/Image_Result/`](Image_Result/).

### 1. Bộ ảnh Hạ tầng Mạng & Môi trường đã thực hiện (Ảnh 01 – 06)
> [!NOTE]
> Các ảnh được quy chuẩn đặt tên theo đúng thứ tự luồng triển khai thực tế (workflow sequence), không xếp theo mốc thời gian chụp ngẫu nhiên:

| STT | Tên Tệp Ảnh | Môi Trường | Nội Dung & Mục Tiêu Minh Chứng |
| :---: | :--- | :---: | :--- |
| **01** | `01_kali_ping_host_gateway.png` | Kali Linux | Kiểm tra thông mạng LAN ảo: Kali `ping -c 3 192.168.86.1` sang Host Gateway (0% packet loss, RTT ~0.4ms). |
| **02** | `02_host_netsh_portproxy_11434.png` | Host Windows | Cấu hình Windows PowerShell: `netsh interface portproxy` lắng nghe `192.168.86.1:11434` chuyển tiếp vào Ollama `127.0.0.1:11434`. |
| **03** | `03_host_firewall_rule_ollama.png` | Host Windows | Mở Windows Defender Firewall: Tạo quy tắc Inbound Rule cho phép cổng TCP `11434` nhận request từ mạng VM. |
| **04** | `04_host_restart_vmware_nat_dhcp.png` | Host Windows | Khởi động lại dịch vụ ảo hóa VMware: `Restart-Service 'VMware NAT Service'` & `'VMnetDHCP'` để áp dụng route mạng. |
| **05** | `05_kali_curl_ollama_api_tags.png` | Kali Linux | Kiểm tra API Ollama: Kali `curl http://192.168.86.1:11434/api/tags` nhận phản hồi JSON hợp lệ gồm `llama3.1:8b` và `qwen2.5-coder:14b`. |
| **06** | `06_kali_ghidra_headless_version.png` | Kali Linux | Kiểm định runtime Ghidra Headless: Chạy script wrapper với Java 21 OpenJDK (`ghidra_headless.sh --version`) không lỗi. |

### 2. Đánh giá hiện trạng & Kế hoạch bổ sung Bộ ảnh Cốt lõi (Ảnh 07 – 12)
> [!IMPORTANT]
> **Nhận định quan trọng:** 6 ảnh trên (01–06) mới chỉ dừng lại ở bước chứng minh hạ tầng mạng và môi trường thực thi đã thông suốt (Task 1). Chưa có ảnh minh chứng cho **phần năng lực cốt lõi của Tier 2**: kiểm định E0 ground truth, chạy pipeline benchmark tự động, bảng thống kê toán học, kịch bản live demo và đánh giá thực nghiệm ảo giác trên mẫu Gh0stRAT.
> 
> **Đề xuất chụp bổ sung bộ ảnh từ 07 đến 12:**
* **`07_kali_e0_sanity_check_160_pass.png`**: Chạy `tools/check_suite.py` xác thực 160 assertions của 40 cặp hàm C đạt 100% PASS.
* **`08_kali_batch_decompile_80_binaries.png`**: Chạy `scripts/batch_decompile.py` bóc tách hàng loạt 80 nhị phân PE bằng Ghidra Headless vào `decompiled_db.json`.
* **`09_kali_run_bench_multi_context.png`**: Khảo nghiệm benchmark đa tầng ngữ cảnh (CT1 -> CT4) qua `pipeline/run_bench.py` giao tiếp Ollama Server.
* **`10_kali_eval_engine_schr_tables.png`**: Động cơ tính toán `evaluation/eval_engine.py` xuất bảng chỉ số SCHR, Wilson CI 95% và McNemar Chi-square test.
* **`11_kali_live_demo_terminal_execution.png`**: Giao diện thực thi kịch bản Live Demo 1-lệnh (`scripts/live_demo.sh` nghiệm thu Mốc D3).
* **`12_kali_gh0strat_case_study_evaluation.png`**: Thực nghiệm đối chứng ảo giác an ninh trên mẫu Gh0stRAT (`scripts/evaluate_gh0strat_case_study.py` nghiệm thu Mốc D4).

👉 **Checklist hướng dẫn từng bước chi tiết kèm lệnh terminal chuẩn:** Xem mục [Hướng dẫn chụp bộ ảnh cốt lõi 07–12 trong TASK_TIER2_KALI_EXECUTION_PLAN.md](TASK_TIER2_KALI_EXECUTION_PLAN.md#-hướng-dẫn-chi-tiết-từng-bước-chụp-bộ-ảnh-thực-nghiệm-cốt-lõi-07--12).

---

## 📌 Các liên kết nhanh trong thư mục gốc dự án Kali (`/home/NTP/IAM302t/`):
* [Master Plan tổng thể](file:///home/NTP/IAM302t/SCHR_BENCH_MASTER_PLAN_OBSIDIAN.md)
* [Script Ghidra Headless](file:///home/NTP/IAM302t/scripts/ghidra_headless.sh)
* [Script Trích xuất Java](file:///home/NTP/IAM302t/ghidra_scripts/ExportRE.java)
* [Batch Decompiler](file:///home/NTP/IAM302t/scripts/batch_decompile.py)
* [Động cơ Thống kê Evaluation Engine](file:///home/NTP/IAM302t/evaluation/eval_engine.py)
* [Master Evaluation Pipeline](file:///home/NTP/IAM302t/pipeline/run_bench.py)
