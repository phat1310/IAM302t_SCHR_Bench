# BẢNG KẾT QUẢ THỰC NGHIỆM SCHR-BENCH (GENERATED AUTOMATICALLY BY `step4_compute_statistics_and_tables.py`)

## 1. Bảng Trung Tâm (E1 + E2 + E3): SCHR (%), 95% Wilson CI, Miss Rate, BLEU & Spearman $\rho$

| Mô hình (LLM) | Tầng Ngữ cảnh | Số mẫu ($N$) | Lỗi Ảo giác | **SCHR (%) [95% Wilson CI]** | Miss Rate trên Mutant (%) | BLEU (Orig vs Mut) | BLEU (Cặp Lỗi vs Đúng) | Spearman $\rho$ ($p$) | Latency TB (s) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `llama3.1:8b` | **CT1** | 80 | 31 | **38.8%** [28.8%, 49.7%] | 32.5% (13/40) | 0.376 | 0.423 vs 0.234 | +0.326 (`p=0.0335`) | 6.93s |
| `llama3.1:8b` | **CT2** | 80 | 29 | **36.2%** [26.6%, 47.2%] | 27.5% (11/40) | 0.4 | 0.457 vs 0.282 | +0.324 (`p=0.0347`) | 7.33s |
| `llama3.1:8b` | **CT3** | 80 | 28 | **35.0%** [25.5%, 45.9%] | 27.5% (11/40) | 0.462 | 0.532 vs 0.333 | +0.293 (`p=0.0593`) | 7.53s |
| `qwen2.5-coder:14b` | **CT1** | 80 | 19 | **23.8%** [15.8%, 34.1%] | 27.5% (11/40) | 0.358 | 0.497 vs 0.256 | +0.399 (`p=0.0073`) | 26.69s |
| `qwen2.5-coder:14b` | **CT2** | 80 | 16 | **20.0%** [12.7%, 30.0%] | 25.0% (10/40) | 0.403 | 0.584 vs 0.294 | +0.495 (`p=0.0004`) | 26.77s |
| `qwen2.5-coder:14b` | **CT3** | 80 | 15 | **18.8%** [11.7%, 28.7%] | 25.0% (10/40) | 0.409 | 0.582 vs 0.315 | +0.475 (`p=0.0009`) | 26.31s |

## 2. Phân tích SCHR (%) theo Nhóm Hành vi An ninh (Categories A, S, P, E, C; $n=16$ mỗi nhóm)

| Mô hình (LLM) | Tầng | A: Debug Policy | S: Toy Decoder | P: Persistence | E: Env Signal | C: Control Flow |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| `llama3.1:8b` | **CT1** | 43.8% (7/16) | 56.2% (9/16) | 12.5% (2/16) | 43.8% (7/16) | 37.5% (6/16) |
| `llama3.1:8b` | **CT2** | 31.2% (5/16) | 62.5% (10/16) | 6.2% (1/16) | 50.0% (8/16) | 31.2% (5/16) |
| `llama3.1:8b` | **CT3** | 31.2% (5/16) | 62.5% (10/16) | 6.2% (1/16) | 43.8% (7/16) | 31.2% (5/16) |
| `qwen2.5-coder:14b` | **CT1** | 12.5% (2/16) | 56.2% (9/16) | 12.5% (2/16) | 18.8% (3/16) | 18.8% (3/16) |
| `qwen2.5-coder:14b` | **CT2** | 6.2% (1/16) | 56.2% (9/16) | 0.0% (0/16) | 18.8% (3/16) | 18.8% (3/16) |
| `qwen2.5-coder:14b` | **CT3** | 6.2% (1/16) | 56.2% (9/16) | 0.0% (0/16) | 18.8% (3/16) | 12.5% (2/16) |

## 3. Phân tích SCHR (%) theo 5 Họ Toán tử Đột biến ($\mathcal{M}_1$–$\mathcal{M}_5$, $N=80$)

- **Mapping 11 toán tử trong manifest sang $\mathcal{M}_1$–$\mathcal{M}_5$:**
  * $\mathcal{M}_1$ (`M1_Invert`, $n=24$): `condition_inversion` (14), `boolean_operator` (6), `condition_weakening` (2), `boolean_precedence` (2).
  * $\mathcal{M}_2$ (`M2_Const`, $n=24$): `constant_change` (16), `arithmetic_operator` (6), `bitwise_operator` (2).
  * $\mathcal{M}_3$ (`M3_Swap`, $n=10$): `api_effect_swap` (8), `mock_api_swap` (2).
  * $\mathcal{M}_4$ (`M4_Bound`, $n=16$): `relational_boundary` (16).
  * $\mathcal{M}_5$ (`M5_Omit`, $n=6$): `step_omission` (6).

| Mô hình (LLM) | Tầng | $\mathcal{M}_1$: Invert ($n=24$) | $\mathcal{M}_2$: Const ($n=24$) | $\mathcal{M}_3$: Swap ($n=10$) | $\mathcal{M}_4$: Bound ($n=16$) | $\mathcal{M}_5$: Omit ($n=6$) | Overall SCHR ($N=80$) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `llama3.1:8b` | **CT1** | 50.0% (12/24) | 50.0% (12/24) | 10.0% (1/10) | 31.2% (5/16) | 16.7% (1/6) | **38.8%** (31/80) |
| `llama3.1:8b` | **CT2** | 33.3% (8/24) | 54.2% (13/24) | 10.0% (1/10) | 31.2% (5/16) | 33.3% (2/6) | **36.2%** (29/80) |
| `llama3.1:8b` | **CT3** | 33.3% (8/24) | 54.2% (13/24) | 0.0% (0/10) | 31.2% (5/16) | 33.3% (2/6) | **35.0%** (28/80) |
| `qwen2.5-coder:14b` | **CT1** | 20.8% (5/24) | 50.0% (12/24) | 10.0% (1/10) | 6.2% (1/16) | 0.0% (0/6) | **23.8%** (19/80) |
| `qwen2.5-coder:14b` | **CT2** | 12.5% (3/24) | 45.8% (11/24) | 0.0% (0/10) | 12.5% (2/16) | 0.0% (0/6) | **20.0%** (16/80) |
| `qwen2.5-coder:14b` | **CT3** | 12.5% (3/24) | 41.7% (10/24) | 0.0% (0/10) | 12.5% (2/16) | 0.0% (0/6) | **18.8%** (15/80) |

## 4. Thí nghiệm E4 (RQ4): Tác động của Obfuscation Templates (Obf0–Obf3) trên tập Pilot 5 cặp cơ bản ($N=10$)

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

## 5. Kiểm định Thống kê McNemar's Test (So sánh Cặp Phụ thuộc CT1 vs CT2/CT3, $\alpha = 0.05$)

| Mô hình (LLM) | Cặp So sánh | $b$ (CT1 Sai $\rightarrow$ Mới Đúng) | $c$ (CT1 Đúng $\rightarrow$ Mới Sai) | Net ($b-c$) | $\chi^2$ (McNemar) | $p$-value | Kết luận Thống kê ($\alpha=0.05$) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `llama3.1:8b` | **CT1 vs CT2** | 6 | 4 | `+2` | 0.1 | `0.7518` | Không có ý nghĩa thống kê ($p \ge 0.05$, xu hướng $\Delta = +2$) |
| `llama3.1:8b` | **CT1 vs CT3** | 8 | 5 | `+3` | 0.308 | `0.5791` | Không có ý nghĩa thống kê ($p \ge 0.05$, xu hướng $\Delta = +3$) |
| `qwen2.5-coder:14b` | **CT1 vs CT2** | 5 | 2 | `+3` | 0.571 | `0.4497` | Không có ý nghĩa thống kê ($p \ge 0.05$, xu hướng $\Delta = +3$) |
| `qwen2.5-coder:14b` | **CT1 vs CT3** | 6 | 2 | `+4` | 1.125 | `0.2888` | Không có ý nghĩa thống kê ($p \ge 0.05$, xu hướng $\Delta = +4$) |

## 6. Phân loại Thực nghiệm 50 Lỗi CT1 ($N=50$: 31 LLaMA + 19 Qwen) theo Cơ chế Toán tử Đột biến

| Nhóm Cơ chế Lỗi (Mutation Mechanism Group) | Các Toán tử trong Manifest | LLaMA-3.1 8B ($n=31$) | Qwen2.5-Coder 14B ($n=19$) | Tổng cộng ($N=50$) |
| :--- | :--- | :---: | :---: | :---: |
| **Constant & Arithmetic Alteration ($\mathcal{M}_2$)** | `constant_change`, `arithmetic_operator`, `bitwise_operator` | 12 | 12 | **24 (48.0%)** |
| **Condition & Boolean Inversion ($\mathcal{M}_1$)** | `condition_inversion`, `boolean_operator`, `boolean_precedence`, `condition_weakening` | 12 | 5 | **17 (34.0%)** |
| **Relational Boundary Shift ($\mathcal{M}_4$)** | `relational_boundary` | 5 | 1 | **6 (12.0%)** |
| **Target Swap & Step Omission ($\mathcal{M}_3, \mathcal{M}_5$)** | `api_effect_swap`, `mock_api_swap`, `step_omission` | 2 | 1 | **3 (6.0%)** |