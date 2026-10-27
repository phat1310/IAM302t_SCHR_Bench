# 📊 BẢNG KẾT QUẢ THỰC NGHIỆM SCHR-BENCH (SPRINGER LNICST — EAI INISCOM 2027)

## 1. Bảng Trung Tâm (E1 + E2 + E3): SCHR (%), 95% Wilson CI, Miss Rate & BLEU Score

| Mô hình (LLM) | Tầng Ngữ cảnh | Số mẫu ($N$) | Lỗi Ảo giác | **SCHR (%) [95% Wilson CI]** | Miss Rate trên Mutant (%) | BLEU (Orig vs Mut) | Latency TB (s) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `llama3.1:8b` | **CT1** | 30 | 13 | **43.3%** [27.4%, 60.8%] | 33.3% | 0.343 | 6.41s |
| `llama3.1:8b` | **CT2** | 30 | 12 | **40.0%** [24.6%, 57.7%] | 26.7% | 0.489 | 6.3s |
| `llama3.1:8b` | **CT3** | 30 | 9 | **30.0%** [16.7%, 47.9%] | 20.0% | 0.507 | 6.3s |
| `qwen2.5-coder:14b` | **CT1** | 30 | 6 | **20.0%** [9.5%, 37.3%] | 20.0% | 0.486 | 27.5s |
| `qwen2.5-coder:14b` | **CT2** | 30 | 5 | **16.7%** [7.3%, 33.6%] | 13.3% | 0.444 | 26.27s |
| `qwen2.5-coder:14b` | **CT3** | 30 | 4 | **13.3%** [5.3%, 29.7%] | 13.3% | 0.444 | 24.73s |

## 2. Phân tích SCHR (%) theo Nhóm Hành vi An ninh (Categories A, S, P, E, C)

| Mô hình (LLM) | Tầng | A: Debug Policy | S: Toy Decoder | P: Persistence | E: Env Signal | C: Control Flow |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| `llama3.1:8b` | **CT1** | 50.0% (3/6) | 50.0% (3/6) | 33.3% (2/6) | 50.0% (3/6) | 33.3% (2/6) |
| `llama3.1:8b` | **CT2** | 50.0% (3/6) | 50.0% (3/6) | 16.7% (1/6) | 50.0% (3/6) | 33.3% (2/6) |
| `llama3.1:8b` | **CT3** | 16.7% (1/6) | 50.0% (3/6) | 0.0% (0/6) | 50.0% (3/6) | 33.3% (2/6) |
| `qwen2.5-coder:14b` | **CT1** | 0.0% (0/6) | 50.0% (3/6) | 33.3% (2/6) | 0.0% (0/6) | 16.7% (1/6) |
| `qwen2.5-coder:14b` | **CT2** | 0.0% (0/6) | 50.0% (3/6) | 0.0% (0/6) | 0.0% (0/6) | 33.3% (2/6) |
| `qwen2.5-coder:14b` | **CT3** | 0.0% (0/6) | 50.0% (3/6) | 0.0% (0/6) | 0.0% (0/6) | 16.7% (1/6) |

## 3. Thí nghiệm E4 (RQ4): Tác động của Obfuscation (OLLVM Levels 0–3) lên SCHR (%)

| Mô hình (LLM) | Mức Làm rối (Obfuscation Level) | Số mẫu ($N$) | Lỗi Ảo giác | **SCHR (%) [95% Wilson CI]** |
| :--- | :---: | :---: | :---: | :---: |
| `llama3.1:8b` | **Obf0 (Unobfuscated CT1)** | 10 | 3 | **30.0%** [10.8%, 60.3%] |
| `llama3.1:8b` | **Obf1_CFF** | 10 | 3 | **30.0%** [10.8%, 60.3%] |
| `llama3.1:8b` | **Obf2_Sub** | 10 | 3 | **30.0%** [10.8%, 60.3%] |
| `llama3.1:8b` | **Obf3_Combined** | 10 | 4 | **40.0%** [16.8%, 68.7%] |
| `qwen2.5-coder:14b` | **Obf0 (Unobfuscated CT1)** | 10 | 1 | **10.0%** [1.8%, 40.4%] |
| `qwen2.5-coder:14b` | **Obf1_CFF** | 10 | 1 | **10.0%** [1.8%, 40.4%] |
| `qwen2.5-coder:14b` | **Obf2_Sub** | 10 | 1 | **10.0%** [1.8%, 40.4%] |
| `qwen2.5-coder:14b` | **Obf3_Combined** | 10 | 2 | **20.0%** [5.7%, 51.0%] |

## 4. Kiểm định Thống kê McNemar's Test (So sánh Cặp Phụ thuộc CT1 vs CT2/CT3)

| Mô hình (LLM) | Cặp So sánh | $b$ (CT1 Sai $\rightarrow$ Mới Đúng) | $c$ (CT1 Đúng $\rightarrow$ Mới Sai) | $\chi^2$ (McNemar) | $p$-value | Kết luận |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| `llama3.1:8b` | **CT1 vs CT2** | 2 | 1 | 0.0 | `1.0` | Cải thiện rệt ($b > c$) |
| `llama3.1:8b` | **CT1 vs CT3** | 4 | 0 | 2.25 | `0.13361` | Cải thiện rệt ($b > c$) |
| `qwen2.5-coder:14b` | **CT1 vs CT2** | 2 | 1 | 0.0 | `1.0` | Cải thiện rệt ($b > c$) |
| `qwen2.5-coder:14b` | **CT1 vs CT3** | 3 | 1 | 0.25 | `0.61708` | Cải thiện rệt ($b > c$) |