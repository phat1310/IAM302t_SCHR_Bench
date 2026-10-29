# -*- coding: utf-8 -*-
"""
SCHR-Bench: Step 4 — Compute Statistical Metrics & Generate Springer LNICST Paper Tables
"""

import json
import math
from collections import Counter, defaultdict
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_DIR = SCRIPT_DIR.parent
RESULTS_DIR = PROJECT_DIR / "results" if (PROJECT_DIR / "results").exists() else PROJECT_DIR / "Results"
LOG_FILE = RESULTS_DIR / "benchmark_raw_logs.json"


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
    return round(chi2, 3), round(p_val, 5)


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
        "# BẢNG KẾT QUẢ THỰC NGHIỆM SCHR-BENCH (SPRINGER LNICST — EAI INISCOM 2027)",
        "",
        "## 1. Bảng Trung Tâm (E1 + E2 + E3): SCHR (%), 95% Wilson CI, Miss Rate & BLEU Score",
        "",
        "| Mô hình (LLM) | Tầng Ngữ cảnh | Số mẫu ($N$) | Lỗi Ảo giác | **SCHR (%) [95% Wilson CI]** | Miss Rate trên Mutant (%) | BLEU (Orig vs Mut) | Latency TB (s) |",
        "| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |"
    ]

    for m in models:
        for t in core_tiers:
            records = by_model_tier.get((m, t), {})
            if not records:
                continue
            n_total = len(records)
            n_wrong = sum(1 for r in records.values() if r["is_schr_hallucination"])
            schr, ci_low, ci_high = wilson_ci_95(n_wrong, n_total)

            mutants = [r for r in records.values() if r["variant"] == "mutant"]
            n_missed = sum(1 for r in mutants if r["predicted_return"] == r["opposite_variant_truth"])
            miss_rate = round((n_missed / len(mutants)) * 100.0, 1) if mutants else 0.0

            bleu_scores = []
            for r in mutants:
                orig_key = f"{r['id']}_original"
                if orig_key in records:
                    b_score = simple_bleu_similarity(records[orig_key]["explanation"], r["explanation"])
                    bleu_scores.append(b_score)
            avg_bleu = round(sum(bleu_scores) / len(bleu_scores), 3) if bleu_scores else 0.0
            avg_lat = round(sum(r.get("latency_sec", 0.0) for r in records.values()) / n_total, 2)

            md_lines.append(
                f"| `{m}` | **{t}** | {n_total} | {n_wrong} | **{schr}%** [{ci_low}%, {ci_high}%] | {miss_rate}% | {avg_bleu} | {avg_lat}s |"
            )

    md_lines += [
        "",
        "## 2. Phân tích SCHR (%) theo Nhóm Hành vi An ninh (Categories A, S, P, E, C)",
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

    if obf_tiers:
        md_lines += [
            "",
            "## 3. Thí nghiệm E4 (RQ4): Tác động của Obfuscation (OLLVM Levels 0–3) lên SCHR (%)",
            "",
            "| Mô hình (LLM) | Mức Làm rối (Obfuscation Level) | Số mẫu ($N$) | Lỗi Ảo giác | **SCHR (%) [95% Wilson CI]** |",
            "| :--- | :---: | :---: | :---: | :---: |"
        ]
        for m in models:
            for t in ["CT1"] + obf_tiers:
                records = by_model_tier.get((m, t), {})
                if not records:
                    continue
                if t == "CT1":
                    # Filter to same subset as Obf1_CFF for fair comparison
                    obf_keys = set(by_model_tier.get((m, obf_tiers[0]), {}).keys())
                    records = {k: v for k, v in records.items() if k in obf_keys}
                if not records:
                    continue
                n_total = len(records)
                n_wrong = sum(1 for r in records.values() if r["is_schr_hallucination"])
                schr, ci_low, ci_high = wilson_ci_95(n_wrong, n_total)
                lbl = "Obf0 (Unobfuscated CT1)" if t == "CT1" else t
                md_lines.append(f"| `{m}` | **{lbl}** | {n_total} | {n_wrong} | **{schr}%** [{ci_low}%, {ci_high}%] |")

    md_lines += [
        "",
        "## 4. Kiểm định Thống kê McNemar's Test (So sánh Cặp Phụ thuộc CT1 vs CT2/CT3)",
        "",
        "| Mô hình (LLM) | Cặp So sánh | $b$ (CT1 Sai $\\rightarrow$ Mới Đúng) | $c$ (CT1 Đúng $\\rightarrow$ Mới Sai) | $\\chi^2$ (McNemar) | $p$-value | Kết luận |",
        "| :--- | :---: | :---: | :---: | :---: | :---: | :---: |"
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
            sig = "Cải thiện rệt ($b > c$)" if b > c else "Tương đương"
            md_lines.append(f"| `{m}` | **CT1 vs {comp_tier}** | {b} | {c} | {chi2} | `{pval}` | {sig} |")

    out_md = RESULTS_DIR / "PAPER_TABLES_SPRINGER.md"
    out_md.write_text("\n".join(md_lines), encoding="utf-8")


if __name__ == "__main__":
    main()
    print("[+] Updated PAPER_TABLES_SPRINGER.md")
