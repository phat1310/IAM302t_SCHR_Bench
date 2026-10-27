# 📊 BẢNG KẾT QUẢ THỰC NGHIỆM SCHR-BENCH (SPRINGER LNICST — EAI INISCOM 2027)

## 1. Bảng Trung Tâm (E1 + E2 + E3): SCHR (%), 95% Wilson CI, Miss Rate & BLEU Score

| Mô hình (LLM) | Tầng Ngữ cảnh | Số mẫu ($N$) | Lỗi Ảo giác | **SCHR (%) [95% Wilson CI]** | Miss Rate trên Mutant (%) | BLEU (Orig vs Mut) | Latency TB (s) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `llama3.1:8b` | **CT1** | 10 | 3 | **30.0%** [10.8%, 60.3%] | 20.0% | 0.413 | 6.71s |
| `llama3.1:8b` | **CT2** | 10 | 3 | **30.0%** [10.8%, 60.3%] | 20.0% | 0.496 | 7.28s |
| `llama3.1:8b` | **CT3** | 10 | 3 | **30.0%** [10.8%, 60.3%] | 20.0% | 0.533 | 7.54s |
| `qwen2.5-coder:14b` | **CT1** | 10 | 1 | **10.0%** [1.8%, 40.4%] | 20.0% | 0.454 | 30.86s |
| `qwen2.5-coder:14b` | **CT2** | 10 | 1 | **10.0%** [1.8%, 40.4%] | 20.0% | 0.383 | 26.58s |
| `qwen2.5-coder:14b` | **CT3** | 10 | 1 | **10.0%** [1.8%, 40.4%] | 20.0% | 0.34 | 23.44s |

## 2. Phân tích SCHR (%) theo Nhóm Hành vi An ninh (Categories A, S, P, E, C)

| Mô hình (LLM) | Tầng | A: Debug Policy | S: Toy Decoder | P: Persistence | E: Env Signal | C: Control Flow |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| `llama3.1:8b` | **CT1** | 50.0% (1/2) | 50.0% (1/2) | 0.0% (0/2) | 50.0% (1/2) | 0.0% (0/2) |
| `llama3.1:8b` | **CT2** | 50.0% (1/2) | 50.0% (1/2) | 0.0% (0/2) | 50.0% (1/2) | 0.0% (0/2) |
| `llama3.1:8b` | **CT3** | 50.0% (1/2) | 50.0% (1/2) | 0.0% (0/2) | 50.0% (1/2) | 0.0% (0/2) |
| `qwen2.5-coder:14b` | **CT1** | 0.0% (0/2) | 50.0% (1/2) | 0.0% (0/2) | 0.0% (0/2) | 0.0% (0/2) |
| `qwen2.5-coder:14b` | **CT2** | 0.0% (0/2) | 50.0% (1/2) | 0.0% (0/2) | 0.0% (0/2) | 0.0% (0/2) |
| `qwen2.5-coder:14b` | **CT3** | 0.0% (0/2) | 50.0% (1/2) | 0.0% (0/2) | 0.0% (0/2) | 0.0% (0/2) |

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
| `llama3.1:8b` | **CT1 vs CT2** | 0 | 0 | 0.0 | `1.0` | Tương đương |
| `llama3.1:8b` | **CT1 vs CT3** | 0 | 0 | 0.0 | `1.0` | Tương đương |
| `qwen2.5-coder:14b` | **CT1 vs CT2** | 0 | 0 | 0.0 | `1.0` | Tương đương |
| `qwen2.5-coder:14b` | **CT1 vs CT3** | 0 | 0 | 0.0 | `1.0` | Tương đương |