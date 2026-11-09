# BẢNG KẾT QUẢ THỰC NGHIỆM SCHR-BENCH (GENERATED AUTOMATICALLY BY `step4_compute_statistics_and_tables.py`)

## 1. Bảng Trung Tâm Layer 1 (E1 + E2 + E3): SCHR (%), 95% Wilson CI, Miss Rate, BLEU & Spearman $\rho$

- **Kiểm định Recompilability (E2 — `gcc -fsyntax-only` trên 80 hàm CT1):** **100.0% (80/80)** biên dịch thành công (kể cả toàn bộ 40/40 biến thể đột biến ngược logic an ninh), chứng minh *"biên dịch lại được"* không đồng nghĩa *"đúng hành vi an ninh"*.

| Mô hình (LLM) | Tầng Ngữ cảnh | Số mẫu ($N$) | Lỗi Ảo giác | **SCHR (%) [95% Wilson CI]** | Miss Rate trên Mutant (%) | BLEU (Orig vs Mut) | BLEU (Cặp Lỗi vs Đúng) | Spearman $\rho$ ($p$) | Latency TB (s) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `llama3.1:8b` | **CT1** | 80 | 31 | **38.8%** [28.8%, 49.7%] | 32.5% (13/40) | 0.376 | 0.423 vs 0.234 | +0.326 (`p=0.0335`) | 6.93s |
| `llama3.1:8b` | **CT2** | 80 | 29 | **36.2%** [26.6%, 47.2%] | 27.5% (11/40) | 0.4 | 0.457 vs 0.282 | +0.324 (`p=0.0347`) | 7.33s |
| `llama3.1:8b` | **CT3** | 80 | 30 | **37.5%** [27.7%, 48.5%] | 40.0% (16/40) | 0.383 | 0.447 vs 0.191 | +0.450 (`p=0.0019`) | 5.68s |
| `qwen2.5-coder:14b` | **CT1** | 80 | 19 | **23.8%** [15.8%, 34.1%] | 27.5% (11/40) | 0.358 | 0.497 vs 0.256 | +0.399 (`p=0.0073`) | 26.69s |
| `qwen2.5-coder:14b` | **CT2** | 80 | 16 | **20.0%** [12.7%, 30.0%] | 25.0% (10/40) | 0.403 | 0.584 vs 0.294 | +0.495 (`p=0.0004`) | 26.77s |
| `qwen2.5-coder:14b` | **CT3** | 80 | 19 | **23.8%** [15.8%, 34.1%] | 25.0% (10/40) | 0.398 | 0.477 vs 0.334 | +0.124 (`p=0.4422`) | 34.71s |

## 2. Phân tích SCHR (%) theo Nhóm Hành vi An ninh (Categories A, S, P, E, C; $n=16$ mỗi nhóm)

| Mô hình (LLM) | Tầng | A: Debug Policy | S: Toy Decoder | P: Persistence | E: Env Signal | C: Control Flow |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| `llama3.1:8b` | **CT1** | 43.8% (7/16) | 56.2% (9/16) | 12.5% (2/16) | 43.8% (7/16) | 37.5% (6/16) |
| `llama3.1:8b` | **CT2** | 31.2% (5/16) | 62.5% (10/16) | 6.2% (1/16) | 50.0% (8/16) | 31.2% (5/16) |
| `llama3.1:8b` | **CT3** | 43.8% (7/16) | 50.0% (8/16) | 18.8% (3/16) | 50.0% (8/16) | 25.0% (4/16) |
| `qwen2.5-coder:14b` | **CT1** | 12.5% (2/16) | 56.2% (9/16) | 12.5% (2/16) | 18.8% (3/16) | 18.8% (3/16) |
| `qwen2.5-coder:14b` | **CT2** | 6.2% (1/16) | 56.2% (9/16) | 0.0% (0/16) | 18.8% (3/16) | 18.8% (3/16) |
| `qwen2.5-coder:14b` | **CT3** | 18.8% (3/16) | 56.2% (9/16) | 6.2% (1/16) | 18.8% (3/16) | 18.8% (3/16) |

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
| `llama3.1:8b` | **CT3** | 33.3% (8/24) | 45.8% (11/24) | 20.0% (2/10) | 43.8% (7/16) | 33.3% (2/6) | **37.5%** (30/80) |
| `qwen2.5-coder:14b` | **CT1** | 20.8% (5/24) | 50.0% (12/24) | 10.0% (1/10) | 6.2% (1/16) | 0.0% (0/6) | **23.8%** (19/80) |
| `qwen2.5-coder:14b` | **CT2** | 12.5% (3/24) | 45.8% (11/24) | 0.0% (0/10) | 12.5% (2/16) | 0.0% (0/6) | **20.0%** (16/80) |
| `qwen2.5-coder:14b` | **CT3** | 16.7% (4/24) | 45.8% (11/24) | 10.0% (1/10) | 18.8% (3/16) | 0.0% (0/6) | **23.8%** (19/80) |

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

## 5. Kiểm định Thống kê McNemar's Test — Layer 1 Return-Value ($N=80$ mỗi tầng, $\alpha = 0.05$)

| Mô hình (LLM) | Cặp So sánh | $b$ (CT1 Sai $\rightarrow$ Mới Đúng) | $c$ (CT1 Đúng $\rightarrow$ Mới Sai) | Net ($b-c$) | $\chi^2$ (McNemar) | $p$-value | Kết luận Thống kê ($\alpha=0.05$) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `llama3.1:8b` | **CT1 vs CT2** | 6 | 4 | `+2` | 0.1 | `0.7518` | Không có ý nghĩa thống kê ($p \ge 0.05$, xu hướng $\Delta = +2$) |
| `llama3.1:8b` | **CT1 vs CT3** | 8 | 7 | `+1` | 0.0 | `1.0` | Không có ý nghĩa thống kê ($p \ge 0.05$, xu hướng $\Delta = +1$) |
| `qwen2.5-coder:14b` | **CT1 vs CT2** | 5 | 2 | `+3` | 0.571 | `0.4497` | Không có ý nghĩa thống kê ($p \ge 0.05$, xu hướng $\Delta = +3$) |
| `qwen2.5-coder:14b` | **CT1 vs CT3** | 5 | 5 | `+0` | 0.0 | `1.0` | Không có ý nghĩa thống kê ($p \ge 0.05$, xu hướng $\Delta = +0$) |

## 6. Phân loại Thực nghiệm 50 Lỗi CT1 ($N=50$: 31 LLaMA + 19 Qwen) theo Cơ chế Toán tử Đột biến

| Nhóm Cơ chế Lỗi (Mutation Mechanism Group) | Các Toán tử trong Manifest | LLaMA-3.1 8B ($n=31$) | Qwen2.5-Coder 14B ($n=19$) | Tổng cộng ($N=50$) |
| :--- | :--- | :---: | :---: | :---: |
| **Constant & Arithmetic Alteration ($\mathcal{M}_2$)** | `constant_change`, `arithmetic_operator`, `bitwise_operator` | 12 | 12 | **24 (48.0%)** |
| **Condition & Boolean Inversion ($\mathcal{M}_1$)** | `condition_inversion`, `boolean_operator`, `boolean_precedence`, `condition_weakening` | 12 | 5 | **17 (34.0%)** |
| **Relational Boundary Shift ($\mathcal{M}_4$)** | `relational_boundary` | 5 | 1 | **6 (12.0%)** |
| **Target Swap & Step Omission ($\mathcal{M}_3, \mathcal{M}_5$)** | `api_effect_swap`, `mock_api_swap`, `step_omission` | 2 | 1 | **3 (6.0%)** |

## 7. Đánh giá Trắc nghiệm Tự động Gold Set MCQ (`dataset/gold_set_mcq.json` — Thiết kế Ghép cặp Đầy đủ $N=80$ mỗi tầng, 240 mục/model = 480 lượt chạy, tích hợp `objdump` thật ở CT2/CT3)

| Mô hình (LLM) | Tầng Ngữ cảnh (Full-Factorial Paired $N=80$) | Số mục ($N$) | Trả lời Đúng | Lỗi Ảo giác | **MCQ SCHR (%) [95% Wilson CI]** | Độ chính xác (%) | McNemar vs CT1 ($b/c$, $p$-val) | Latency TB (s) |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `llama3.1:8b` | CT1 (Stripped Pseudocode Baseline) | 80 | 49 | 31 | **38.8%** [28.8%, 49.7%] | 61.3% | --- | 1.1s |
| `llama3.1:8b` | CT2 (+Real `objdump -d` Disassembly) | 80 | 44 | 36 | **45.0%** [34.6%, 55.9%] | 55.0% | `b=9, c=14` (`p=0.4042`) | 1.56s |
| `llama3.1:8b` | CT3 (+Real `objdump -d` & Callee Spec) | 80 | 49 | 31 | **38.8%** [28.8%, 49.7%] | 61.3% | `b=11, c=11` (`p=1.0`) | 1.76s |
| `llama3.1:8b` | **Toàn bộ Gold Set (All 3 Tiers Combined)** | 240 | 142 | 98 | **40.8%** [34.8%, 47.1%] | 59.2% | --- | 1.47s |
| `qwen2.5-coder:14b` | CT1 (Stripped Pseudocode Baseline) | 80 | 63 | 17 | **21.2%** [13.7%, 31.4%] | 78.8% | --- | 3.38s |
| `qwen2.5-coder:14b` | CT2 (+Real `objdump -d` Disassembly) | 80 | 59 | 21 | **26.2%** [17.9%, 36.8%] | 73.8% | `b=6, c=10` (`p=0.4533`) | 5.09s |
| `qwen2.5-coder:14b` | CT3 (+Real `objdump -d` & Callee Spec) | 80 | 58 | 22 | **27.5%** [18.9%, 38.1%] | 72.5% | `b=7, c=12` (`p=0.3588`) | 5.04s |
| `qwen2.5-coder:14b` | **Toàn bộ Gold Set (All 3 Tiers Combined)** | 240 | 180 | 60 | **25.0%** [19.9%, 30.8%] | 75.0% | --- | 4.51s |