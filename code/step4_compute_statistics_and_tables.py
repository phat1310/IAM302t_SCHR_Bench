# -*- coding: utf-8 -*-
"""
SCHR-Bench: Step 4 — Compute Statistical Metrics & Generate All Paper Tables
Automatically computes from `results/benchmark_raw_logs.json` (540 logged runs):
  1. Core Evaluation Table (CT1-CT3, N=80): SCHR (%), 95% Wilson CI, Mutant Miss Rate (%),
     Pairwise BLEU (All / Error Pairs vs. Error-Free Pairs), Spearman rho (p-value), Mean Latency.
  2. Category Matrix (Categories A, S, P, E, C; n=16 per category, N=80).
  3. Mutation Operator Family Matrix (M1-M5 mapping from all 11 manifest operator tags; N=80).
  4. Experiment E4 Obfuscation Table (Obf0-Obf3 on the 5-pair easy-tier pilot subset; N=10).
  5. McNemar's Paired Statistical Test (CT1 vs. CT2/CT3; alpha=0.05).
  6. Deterministic CT1 Failure Mechanism Breakdown (N=50 logged CT1 errors: 31 LLaMA + 19 Qwen).
"""

import json
import math
from collections import Counter, defaultdict
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_DIR = SCRIPT_DIR.parent
RESULTS_DIR = PROJECT_DIR / "results" if (PROJECT_DIR / "results").exists() else PROJECT_DIR / "Results"
LOG_FILE = RESULTS_DIR / "benchmark_raw_logs.json"

# Explicit, deterministic mapping from the 11 manifest `mutation_operator` tags
# across all 40 pairs (80 variants) to the 5 formal Mutation Operator Families (M1 - M5):
OPERATOR_TO_FAMILY_M1_M5 = {
    # M1: Condition & Boolean Inversion (12 pairs = 24 variants)
    "condition_inversion": "M1_Invert",     # 7 pairs (14 variants)
    "boolean_operator": "M1_Invert",        # 3 pairs (6 variants)
    "condition_weakening": "M1_Invert",     # 1 pair  (2 variants)
    "boolean_precedence": "M1_Invert",      # 1 pair  (2 variants)
    # M2: Constant & Arithmetic Alteration (12 pairs = 24 variants)
    "constant_change": "M2_Const",          # 8 pairs (16 variants)
    "arithmetic_operator": "M2_Const",      # 3 pairs (6 variants)
    "bitwise_operator": "M2_Const",         # 1 pair  (2 variants)
    # M3: Target / Effect Swap (5 pairs = 10 variants)
    "api_effect_swap": "M3_Swap",           # 4 pairs (8 variants)
    "mock_api_swap": "M3_Swap",             # 1 pair  (2 variants)
    # M4: Relational Boundary Shift (8 pairs = 16 variants)
    "relational_boundary": "M4_Bound",      # 8 pairs (16 variants)
    # M5: Step Omission (3 pairs = 6 variants)
    "step_omission": "M5_Omit",             # 3 pairs (6 variants)
}


def wilson_ci_95(k: int, n: int):
    if n == 0:
        return (0.0, 0.0, 0.0)
    z = 1.96
    p = k / n
    denom = 1.0 + (z * z) / n
    center = (p + (z * z) / (2.0 * n)) / denom
    half = (z * math.sqrt((p * (1.0 - p) + (z * z) / (4.0 * n)) / n)) / denom
    low = max(0.0, (center - half) * 100.0)
    high = min(100.0, (center + half) * 100.0)
    return (round(p * 100.0, 1), round(low, 1), round(high, 1))


def mcnemar_test(b: int, c: int):
    if b + c == 0:
        return 0.0, 1.0
    chi2 = ((abs(b - c) - 1.0) ** 2) / (b + c)
    p_val = math.erfc(math.sqrt(chi2 / 2.0))
    return round(chi2, 3), round(p_val, 4)


def simple_bleu_similarity(text_a: str, text_b: str) -> float:
    toks_a = [w.lower() for w in text_a.split() if w.strip()]
    toks_b = [w.lower() for w in text_b.split() if w.strip()]
    if not toks_a or not toks_b:
        return 0.0
    precisions = []
    for n in (1, 2, 3):
        if len(toks_a) < n or len(toks_b) < n:
            precisions.append(0.5)
            continue
        ngrams_a = Counter(tuple(toks_a[i:i+n]) for i in range(len(toks_a) - n + 1))
        ngrams_b = Counter(tuple(toks_b[i:i+n]) for i in range(len(toks_b) - n + 1))
        overlap = sum((ngrams_a & ngrams_b).values())
        total = sum(ngrams_b.values())
        precisions.append(max(1e-4, overlap / total))
    geo_mean = (precisions[0] * precisions[1] * precisions[2]) ** (1.0 / 3.0)
    bp = 1.0 if len(toks_b) > len(toks_a) else math.exp(1.0 - len(toks_a) / max(1, len(toks_b)))
    return round(bp * geo_mean, 3)


def rankdata(a):
    n = len(a)
    ivec = sorted(range(n), key=lambda i: a[i])
    svec = [a[i] for i in ivec]
    sumranks = 0
    dupcount = 0
    newarray = [0.0] * n
    for i in range(n):
        sumranks += i
        dupcount += 1
        if i == n - 1 or svec[i] != svec[i + 1]:
            averank = sumranks / float(dupcount) + 1.0
            for j in range(i - dupcount + 1, i + 1):
                newarray[ivec[j]] = averank
            sumranks = 0
            dupcount = 0
    return newarray


def spearman_corr(x, y):
    if len(x) < 3 or len(x) != len(y):
        return 0.0, 1.0
    rx = rankdata(x)
    ry = rankdata(y)
    n = len(x)
    mx = sum(rx) / n
    my = sum(ry) / n
    num = sum((rx[i] - mx) * (ry[i] - my) for i in range(n))
    den = math.sqrt(sum((rx[i] - mx) ** 2 for i in range(n)) * sum((ry[i] - my) ** 2 for i in range(n)))
    r = num / den if den > 0 else 0.0
    if abs(r) >= 1.0:
        p = 0.0
    else:
        t = r * math.sqrt((n - 2) / (1.0 - r * r))
        p = math.erfc(abs(t) / math.sqrt(2.0))
    return round(r, 3), round(p, 4)


def main():
    if not LOG_FILE.exists():
        return

    logs = json.loads(LOG_FILE.read_text(encoding="utf-8"))
    by_model_tier = defaultdict(dict)
    for entry in logs.values():
        m = entry["model"]
        t = entry["tier"]
        skey = entry["sample_key"]
        by_model_tier[(m, t)][skey] = entry

    models = sorted({k[0] for k in by_model_tier.keys()})
    core_tiers = [t for t in ("CT1", "CT2", "CT3") if any((m, t) in by_model_tier for m in models)]
    obf_tiers = [t for t in ("Obf1_CFF", "Obf2_Sub", "Obf3_Combined") if any((m, t) in by_model_tier for m in models)]

    md_lines = [
        "# BẢNG KẾT QUẢ THỰC NGHIỆM SCHR-BENCH (GENERATED AUTOMATICALLY BY `step4_compute_statistics_and_tables.py`)",
        "",
        "## 1. Bảng Trung Tâm (E1 + E2 + E3): SCHR (%), 95% Wilson CI, Miss Rate, BLEU & Spearman $\\rho$",
        "",
        "| Mô hình (LLM) | Tầng Ngữ cảnh | Số mẫu ($N$) | Lỗi Ảo giác | **SCHR (%) [95% Wilson CI]** | Miss Rate trên Mutant (%) | BLEU (Orig vs Mut) | BLEU (Cặp Lỗi vs Đúng) | Spearman $\\rho$ ($p$) | Latency TB (s) |",
        "| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |"
    ]

    for m in models:
        for t in core_tiers:
            records = by_model_tier.get((m, t), {})
            if not records:
                continue
            n_total = len(records)
            n_wrong = sum(1 for r in records.values() if r["is_schr_hallucination"])
            schr, ci_low, ci_high = wilson_ci_95(n_wrong, n_total)

            mutants = sorted([r for r in records.values() if r["variant"] == "mutant"], key=lambda x: x["id"])
            n_missed = sum(1 for r in mutants if r["predicted_return"] == r["opposite_variant_truth"])
            miss_rate = round((n_missed / len(mutants)) * 100.0, 1) if mutants else 0.0

            bleu_scores = []
            pair_errs = []
            for r in mutants:
                orig_key = f"{r['id']}_original"
                if orig_key in records:
                    b_score = simple_bleu_similarity(records[orig_key]["explanation"], r["explanation"])
                    e_cnt = int(r["is_schr_hallucination"]) + int(records[orig_key]["is_schr_hallucination"])
                    bleu_scores.append(b_score)
                    pair_errs.append(e_cnt)

            avg_bleu = round(sum(bleu_scores) / len(bleu_scores), 3) if bleu_scores else 0.0
            bleu_err = [b for b, e in zip(bleu_scores, pair_errs) if e > 0]
            bleu_ok = [b for b, e in zip(bleu_scores, pair_errs) if e == 0]
            b_err_avg = round(sum(bleu_err) / len(bleu_err), 3) if bleu_err else 0.0
            b_ok_avg = round(sum(bleu_ok) / len(bleu_ok), 3) if bleu_ok else 0.0
            rho, rho_p = spearman_corr(bleu_scores, pair_errs)
            avg_lat = round(sum(r.get("latency_sec", 0.0) for r in records.values()) / n_total, 2)

            md_lines.append(
                f"| `{m}` | **{t}** | {n_total} | {n_wrong} | **{schr}%** [{ci_low}%, {ci_high}%] | "
                f"{miss_rate}% ({n_missed}/{len(mutants)}) | {avg_bleu} | {b_err_avg} vs {b_ok_avg} | "
                f"{rho:+.3f} (`p={rho_p}`) | {avg_lat}s |"
            )

    md_lines += [
        "",
        "## 2. Phân tích SCHR (%) theo Nhóm Hành vi An ninh (Categories A, S, P, E, C; $n=16$ mỗi nhóm)",
        "",
        "| Mô hình (LLM) | Tầng | A: Debug Policy | S: Toy Decoder | P: Persistence | E: Env Signal | C: Control Flow |",
        "| :--- | :---: | :---: | :---: | :---: | :---: | :---: |"
    ]

    cats = ["debug_policy", "toy_decoder", "persistence_mock", "environment_mock", "control_flow"]
    for m in models:
        for t in core_tiers:
            records = by_model_tier.get((m, t), {})
            if not records:
                continue
            cat_cells = []
            for c_name in cats:
                c_recs = [r for r in records.values() if r["category"] == c_name]
                if not c_recs:
                    cat_cells.append("-")
                else:
                    w = sum(1 for r in c_recs if r["is_schr_hallucination"])
                    rate = round((w / len(c_recs)) * 100.0, 1)
                    cat_cells.append(f"{rate}% ({w}/{len(c_recs)})")
            md_lines.append(f"| `{m}` | **{t}** | " + " | ".join(cat_cells) + " |")

    # Section 3: Mutation Operator Families M1 - M5
    md_lines += [
        "",
        "## 3. Phân tích SCHR (%) theo 5 Họ Toán tử Đột biến ($\\mathcal{M}_1$–$\\mathcal{M}_5$, $N=80$)",
        "",
        "- **Mapping 11 toán tử trong manifest sang $\\mathcal{M}_1$–$\\mathcal{M}_5$:**",
        "  * $\\mathcal{M}_1$ (`M1_Invert`, $n=24$): `condition_inversion` (14), `boolean_operator` (6), `condition_weakening` (2), `boolean_precedence` (2).",
        "  * $\\mathcal{M}_2$ (`M2_Const`, $n=24$): `constant_change` (16), `arithmetic_operator` (6), `bitwise_operator` (2).",
        "  * $\\mathcal{M}_3$ (`M3_Swap`, $n=10$): `api_effect_swap` (8), `mock_api_swap` (2).",
        "  * $\\mathcal{M}_4$ (`M4_Bound`, $n=16$): `relational_boundary` (16).",
        "  * $\\mathcal{M}_5$ (`M5_Omit`, $n=6$): `step_omission` (6).",
        "",
        "| Mô hình (LLM) | Tầng | $\\mathcal{M}_1$: Invert ($n=24$) | $\\mathcal{M}_2$: Const ($n=24$) | $\\mathcal{M}_3$: Swap ($n=10$) | $\\mathcal{M}_4$: Bound ($n=16$) | $\\mathcal{M}_5$: Omit ($n=6$) | Overall SCHR ($N=80$) |",
        "| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |"
    ]

    m_fams = ["M1_Invert", "M2_Const", "M3_Swap", "M4_Bound", "M5_Omit"]
    for m in models:
        for t in core_tiers:
            records = by_model_tier.get((m, t), {})
            if not records:
                continue
            fam_cells = []
            for mf in m_fams:
                f_recs = [r for r in records.values() if OPERATOR_TO_FAMILY_M1_M5.get(r["mutation_operator"]) == mf]
                w = sum(1 for r in f_recs if r["is_schr_hallucination"])
                rate = round((w / len(f_recs)) * 100.0, 1) if f_recs else 0.0
                fam_cells.append(f"{rate}% ({w}/{len(f_recs)})")
            tot_w = sum(1 for r in records.values() if r["is_schr_hallucination"])
            tot_r = round((tot_w / len(records)) * 100.0, 1)
            md_lines.append(f"| `{m}` | **{t}** | " + " | ".join(fam_cells) + f" | **{tot_r}%** ({tot_w}/{len(records)}) |")

    if obf_tiers:
        md_lines += [
            "",
            "## 4. Thí nghiệm E4 (RQ4): Tác động của Obfuscation Templates (Obf0–Obf3) trên tập Pilot 5 cặp cơ bản ($N=10$)",
            "",
            "| Mô hình (LLM) | Mức Làm rối (Obfuscation Template) | Số mẫu ($N$) | Lỗi Ảo giác | **SCHR (%) [95% Wilson CI]** |",
            "| :--- | :---: | :---: | :---: | :---: |"
        ]
        for m in models:
            for t in ["CT1"] + obf_tiers:
                records = by_model_tier.get((m, t), {})
                if not records:
                    continue
                if t == "CT1":
                    obf_keys = set(by_model_tier.get((m, obf_tiers[0]), {}).keys())
                    records = {k: v for k, v in records.items() if k in obf_keys}
                if not records:
                    continue
                n_total = len(records)
                n_wrong = sum(1 for r in records.values() if r["is_schr_hallucination"])
                schr, ci_low, ci_high = wilson_ci_95(n_wrong, n_total)
                lbl = "Obf0 (Unobfuscated CT1 Baseline)" if t == "CT1" else t
                md_lines.append(f"| `{m}` | **{lbl}** | {n_total} | {n_wrong} | **{schr}%** [{ci_low}%, {ci_high}%] |")

    md_lines += [
        "",
        "## 5. Kiểm định Thống kê McNemar's Test (So sánh Cặp Phụ thuộc CT1 vs CT2/CT3, $\\alpha = 0.05$)",
        "",
        "| Mô hình (LLM) | Cặp So sánh | $b$ (CT1 Sai $\\rightarrow$ Mới Đúng) | $c$ (CT1 Đúng $\\rightarrow$ Mới Sai) | Net ($b-c$) | $\\chi^2$ (McNemar) | $p$-value | Kết luận Thống kê ($\\alpha=0.05$) |",
        "| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |"
    ]

    for m in models:
        base_recs = by_model_tier.get((m, "CT1"), {})
        for comp_tier in ("CT2", "CT3"):
            comp_recs = by_model_tier.get((m, comp_tier), {})
            if not base_recs or not comp_recs:
                continue
            b = c = 0
            for skey, r1 in base_recs.items():
                if skey in comp_recs:
                    r2 = comp_recs[skey]
                    if r1["is_schr_hallucination"] and not r2["is_schr_hallucination"]:
                        b += 1
                    elif not r1["is_schr_hallucination"] and r2["is_schr_hallucination"]:
                        c += 1
            chi2, pval = mcnemar_test(b, c)
            if pval < 0.05:
                sig = f"Có ý nghĩa thống kê ($p < 0.05$, $\\Delta = {b-c:+d}$)"
            else:
                sig = f"Không có ý nghĩa thống kê ($p \\ge 0.05$, xu hướng $\\Delta = {b-c:+d}$)"
            md_lines.append(f"| `{m}` | **CT1 vs {comp_tier}** | {b} | {c} | `{b-c:+d}` | {chi2} | `{pval}` | {sig} |")

    # Section 6: Deterministic CT1 Error Taxonomy (N=50)
    md_lines += [
        "",
        "## 6. Phân loại Thực nghiệm 50 Lỗi CT1 ($N=50$: 31 LLaMA + 19 Qwen) theo Cơ chế Toán tử Đột biến",
        "",
        "| Nhóm Cơ chế Lỗi (Mutation Mechanism Group) | Các Toán tử trong Manifest | LLaMA-3.1 8B ($n=31$) | Qwen2.5-Coder 14B ($n=19$) | Tổng cộng ($N=50$) |",
        "| :--- | :--- | :---: | :---: | :---: |"
    ]
    tax_groups = [
        ("Constant & Arithmetic Alteration ($\\mathcal{M}_2$)", ("M2_Const",), "`constant_change`, `arithmetic_operator`, `bitwise_operator`"),
        ("Condition & Boolean Inversion ($\\mathcal{M}_1$)", ("M1_Invert",), "`condition_inversion`, `boolean_operator`, `boolean_precedence`, `condition_weakening`"),
        ("Relational Boundary Shift ($\\mathcal{M}_4$)", ("M4_Bound",), "`relational_boundary`"),
        ("Target Swap & Step Omission ($\\mathcal{M}_3, \\mathcal{M}_5$)", ("M3_Swap", "M5_Omit"), "`api_effect_swap`, `mock_api_swap`, `step_omission`"),
    ]
    llama_ct1 = [r for r in by_model_tier.get(("llama3.1:8b", "CT1"), {}).values() if r["is_schr_hallucination"]]
    qwen_ct1 = [r for r in by_model_tier.get(("qwen2.5-coder:14b", "CT1"), {}).values() if r["is_schr_hallucination"]]
    total_ct1_err = len(llama_ct1) + len(qwen_ct1)

    for grp_name, fam_keys, op_desc in tax_groups:
        l_cnt = sum(1 for r in llama_ct1 if OPERATOR_TO_FAMILY_M1_M5.get(r["mutation_operator"]) in fam_keys)
        q_cnt = sum(1 for r in qwen_ct1 if OPERATOR_TO_FAMILY_M1_M5.get(r["mutation_operator"]) in fam_keys)
        t_cnt = l_cnt + q_cnt
        pct = round((t_cnt / total_ct1_err) * 100.0, 1) if total_ct1_err else 0.0
        md_lines.append(f"| **{grp_name}** | {op_desc} | {l_cnt} | {q_cnt} | **{t_cnt} ({pct}%)** |")

    out_md = RESULTS_DIR / "PAPER_TABLES_SPRINGER.md"
    out_md.write_text("\n".join(md_lines), encoding="utf-8")


if __name__ == "__main__":
    main()
    print("[+] Updated PAPER_TABLES_SPRINGER.md (including M1-M5 matrix and N=50 CT1 error taxonomy)")
