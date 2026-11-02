# BẢNG KẾT QUẢ THỰC NGHIỆM SCHR-BENCH (SPRINGER LNICST — EAI INISCOM 2027)

## 1. Bảng Trung Tâm (E1 + E2 + E3): SCHR (%), 95% Wilson CI, Miss Rate & Pairwise BLEU

| Mô hình (LLM) | Tầng Ngữ cảnh | Số mẫu ($N$) | Lỗi Ảo giác | **SCHR (%) [95% Wilson CI]** | Miss Rate trên Mutant (%) | BLEU (Orig vs Mut) | BLEU (Cặp Lỗi vs Đúng) | Spearman $\rho$ ($p$) | Latency TB (s) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `llama3.1:8b` | **CT1** | 80 | 31 | **38.8%** [28.8%, 49.7%] | 32.5% (13/40) | 0.376 | 0.423 vs 0.234 | +0.326 (`p=0.0335`) | 6.93s |
| `llama3.1:8b` | **CT2** | 80 | 29 | **36.2%** [26.6%, 47.2%] | 27.5% (11/40) | 0.4 | 0.457 vs 0.282 | +0.324 (`p=0.0347`) | 7.33s |
| `llama3.1:8b` | **CT3** | 80 | 28 | **35.0%** [25.5%, 45.9%] | 27.5% (11/40) | 0.462 | 0.532 vs 0.333 | +0.293 (`p=0.0593`) | 7.53s |
| `qwen2.5-coder:14b` | **CT1** | 80 | 19 | **23.8%** [15.8%, 34.1%] | 27.5% (11/40) | 0.358 | 0.497 vs 0.256 | +0.399 (`p=0.0073`) | 26.69s |
| `qwen2.5-coder:14b` | **CT2** | 80 | 16 | **20.0%** [12.7%, 30.0%] | 25.0% (10/40) | 0.403 | 0.584 vs 0.294 | +0.495 (`p=0.0004`) | 26.77s |
| `qwen2.5-coder:14b` | **CT3** | 80 | 15 | **18.8%** [11.7%, 28.7%] | 25.0% (10/40) | 0.409 | 0.582 vs 0.315 | +0.475 (`p=0.0009`) | 26.31s |

## 2. Phân tích SCHR (%) theo Nhóm Hành vi An ninh (Categories A, S, P, E, C)

| Mô hình (LLM) | Tầng | A: Debug Policy | S: Toy Decoder | P: Persistence | E: Env Signal | C: Control Flow |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| `llama3.1:8b` | **CT1** | 43.8% (7/16) | 56.2% (9/16) | 12.5% (2/16) | 43.8% (7/16) | 37.5% (6/16) |
| `llama3.1:8b` | **CT2** | 31.2% (5/16) | 62.5% (10/16) | 6.2% (1/16) | 50.0% (8/16) | 31.2% (5/16) |
| `llama3.1:8b` | **CT3** | 31.2% (5/16) | 62.5% (10/16) | 6.2% (1/16) | 43.8% (7/16) | 31.2% (5/16) |
| `qwen2.5-coder:14b` | **CT1** | 12.5% (2/16) | 56.2% (9/16) | 12.5% (2/16) | 18.8% (3/16) | 18.8% (3/16) |
| `qwen2.5-coder:14b` | **CT2** | 6.2% (1/16) | 56.2% (9/16) | 0.0% (0/16) | 18.8% (3/16) | 18.8% (3/16) |
| `qwen2.5-coder:14b` | **CT3** | 6.2% (1/16) | 56.2% (9/16) | 0.0% (0/16) | 18.8% (3/16) | 12.5% (2/16) |

## 3. Thí nghiệm E4 (RQ4): Tác động của Obfuscation Templates (Obf0–Obf3) trên tập Pilot 5 cặp cơ bản ($N=10$)

| Mô hình (LLM) | Mức Làm rối (Obfuscation Template) | Số mẫu ($N$) | Lỗi Ảo giác | **SCHR (%) [95% Wilson CI]** |
| :--- | :---: | :---: | :---: | :---: |
| `llama3.1:8b` | **Obf0 (Unobfuscated CT1 Baseline)** | 10 | 3 | **30.0%** [10.8%, 60.3%] |
| `llama3.1:8b` | **Obf1_CFF** | 10 | 3 | **30.0%** [10.8%, 60.3%] |
| `llama3.1:8b` | **Obf2_Sub** | 10 | 3 | **30.0%** [10.8%, 60.3%] |
| `llama3.1:8b` | **Obf3_Combined** | 10 | 4 | **40.0%** [16.8%, 68.7%] |
| `qwen2.5-coder:14b` | **Obf0 (Unobfuscated CT1 Baseline)** | 10 | 1 | **10.0%** [1.8%, 40.4%] |
| `qwen2.5-coder:14b` | **Obf1_CFF** | 10 | 1 | **10.0%** [1.8%, 40.4%] |
| `qwen2.5-coder:14b` | **Obf2_Sub** | 10 | 1 | **10.0%** [1.8%, 40.4%] |
| `qwen2.5-coder:14b` | **Obf3_Combined** | 10 | 2 | **20.0%** [5.7%, 51.0%] |

## 4. Kiểm định Thống kê McNemar's Test (So sánh Cặp Phụ thuộc CT1 vs CT2/CT3, $\alpha = 0.05$)

| Mô hình (LLM) | Cặp So sánh | $b$ (CT1 Sai $\rightarrow$ Mới Đúng) | $c$ (CT1 Đúng $\rightarrow$ Mới Sai) | Net ($b-c$) | $\chi^2$ (McNemar) | $p$-value | Kết luận Thống kê ($\alpha=0.05$) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `llama3.1:8b` | **CT1 vs CT2** | 6 | 4 | `+2` | 0.1 | `0.7518` | Không có ý nghĩa thống kê ($p \ge 0.05$, xu hướng $\Delta = +2$) |
| `llama3.1:8b` | **CT1 vs CT3** | 8 | 5 | `+3` | 0.308 | `0.5791` | Không có ý nghĩa thống kê ($p \ge 0.05$, xu hướng $\Delta = +3$) |
| `qwen2.5-coder:14b` | **CT1 vs CT2** | 5 | 2 | `+3` | 0.571 | `0.4497` | Không có ý nghĩa thống kê ($p \ge 0.05$, xu hướng $\Delta = +3$) |
| `qwen2.5-coder:14b` | **CT1 vs CT3** | 6 | 2 | `+4` | 1.125 | `0.2888` | Không có ý nghĩa thống kê ($p \ge 0.05$, xu hướng $\Delta = +4$) |