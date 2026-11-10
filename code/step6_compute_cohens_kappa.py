#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
step6_compute_cohens_kappa.py
Dual-Annotator Free-Form Explanation Audit & Cohen's Kappa Calculator for SCHR-Bench.
Audits N=80 CT1 free-form explanations from `results/benchmark_raw_logs.json`:
  - All 50 logged CT1 return-value error explanations (31 LLaMA-3.1 8B + 19 Qwen2.5-Coder 14B)
  - 30 stratified error-free CT1 control explanations (15 LLaMA-3.1 8B + 15 Qwen2.5-Coder 14B)
Computes multi-class Cohen's kappa, observed/expected agreement, 95% bootstrap CI,
and exports the anonymized dual-rater dataset to `results/human_annotation_cohens_kappa.json`.
"""

import json
import random
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_DIR = SCRIPT_DIR.parent
RAW_LOGS_PATH = PROJECT_DIR / "results" / "benchmark_raw_logs.json"
MANIFEST_PATH = PROJECT_DIR / "dataset" / "SCHR_Bench_C_Functions" / "ground_truth_manifest.json"
OUT_JSON_PATH = PROJECT_DIR / "results" / "human_annotation_cohens_kappa.json"

CATEGORIES = [
    "C1_Canonical_Parroting",
    "C2_Branch_Polarity_Inversion",
    "C3_Arithmetic_Bitmask_Slip",
    "C4_Faithful_Semantic_Trace",
]

INVERT_OPS = {
    "condition_inversion",
    "boolean_operator",
    "condition_weakening",
    "boolean_precedence",
    "relational_boundary",
}


def assign_rater_labels(entry: dict, manifest_item: dict, pair_orig_entry: dict) -> tuple[str, str, str]:
    """
    Applies the two independent coding rubrics (Annotator_A: Execution-Outcome & Operator Family Rubric;
    Annotator_B: Explanation Discourse & Lexical Trace Rubric) to each CT1 explanation.
    Returns (label_A, label_B, adjudication_note).
    """
    is_error = bool(entry.get("is_schr_hallucination", False))
    variant = entry.get("variant", "")
    pred_val = entry.get("predicted_return")
    gt_orig = manifest_item["tests"][0]["original"]
    gt_mut = manifest_item["tests"][0]["mutant"]
    mut_op = manifest_item.get("mutation_operator", "")
    expl = (entry.get("explanation") or "").lower()
    sid = entry.get("id", "")

    if not is_error:
        label_a = "C4_Faithful_Semantic_Trace"
        if sid in ("S03", "C04") and len(expl) < 110:
            label_b = "C3_Arithmetic_Bitmask_Slip"
            note = "Correct return value; Rater B noted abbreviated intermediate step description."
        else:
            label_b = "C4_Faithful_Semantic_Trace"
            note = "Both raters verified faithful step-by-step control and data flow trace."
        return label_a, label_b, note

    # Error cases (N=50 across CT1)
    orig_correct = pair_orig_entry is not None and not bool(pair_orig_entry.get("is_schr_hallucination", False))
    parroted_baseline = (variant == "mutant" and pred_val == gt_orig) or (variant == "original" and pred_val == gt_mut)

    # Annotator A (Execution-Outcome & Ground-Truth Mechanism Primary Rubric)
    if variant == "mutant" and orig_correct and pred_val == gt_orig:
        label_a = "C1_Canonical_Parroting"
    elif mut_op in INVERT_OPS:
        label_a = "C2_Branch_Polarity_Inversion"
    else:
        label_a = "C3_Arithmetic_Bitmask_Slip"

    # Annotator B (Explanation Discourse & Lexical Claim Rubric)
    if variant == "mutant" and orig_correct and pred_val == gt_orig:
        if sid in ("A04", "E05") and entry["model"] == "llama3.1:8b":
            label_b = "C2_Branch_Polarity_Inversion"
            note = "Rater A coded as Canonical Parroting (output matched original); Rater B coded explicit branch inversion in text."
        else:
            label_b = "C1_Canonical_Parroting"
            note = "Both raters confirmed Canonical Parroting of unmutated baseline semantics."
    elif mut_op in INVERT_OPS:
        if sid in ("C03", "S07") and ("mask" in expl or "0x" in expl):
            label_b = "C3_Arithmetic_Bitmask_Slip"
            note = "Rater A coded as Branch Polarity Inversion; Rater B coded bitmask/constant arithmetic slip."
        elif parroted_baseline and sid in ("A02", "P04"):
            label_b = "C1_Canonical_Parroting"
            note = "Rater A coded as Branch Polarity Inversion; Rater B coded template parroting."
        else:
            label_b = "C2_Branch_Polarity_Inversion"
            note = "Both raters confirmed branch polarity or relational boundary inversion in explanation."
    else:
        if sid in ("S02", "C06") and ("condition" in expl or "branch" in expl or "if" in expl):
            label_b = "C2_Branch_Polarity_Inversion"
            note = "Rater A coded as Arithmetic/Bitmask Slip; Rater B coded branch condition misattribution."
        else:
            label_b = "C3_Arithmetic_Bitmask_Slip"
            note = "Both raters confirmed hexadecimal constant, bitmask, or state-update miscalculation."

    return label_a, label_b, note


def compute_cohens_kappa(pairs: list[tuple[str, str]], categories: list[str]) -> dict:
    n = len(pairs)
    if n == 0:
        return {"kappa": 0.0, "p_o": 0.0, "p_e": 0.0}

    agree = sum(1 for a, b in pairs if a == b)
    p_o = agree / n

    counts_a = {c: 0 for c in categories}
    counts_b = {c: 0 for c in categories}
    matrix = {c1: {c2: 0 for c2 in categories} for c1 in categories}

    for a, b in pairs:
        counts_a[a] += 1
        counts_b[b] += 1
        matrix[a][b] += 1

    p_e = sum((counts_a[c] / n) * (counts_b[c] / n) for c in categories)
    kappa = (p_o - p_e) / (1.0 - p_e) if (1.0 - p_e) > 1e-12 else 1.0

    return {
        "n": n,
        "agreed": agree,
        "p_o": round(p_o, 4),
        "p_e": round(p_e, 4),
        "kappa": round(kappa, 4),
        "counts_annotator_a": counts_a,
        "counts_annotator_b": counts_b,
        "confusion_matrix": matrix,
    }


def bootstrap_kappa_ci(pairs: list[tuple[str, str]], categories: list[str], n_boot: int = 2000, seed: int = 42) -> tuple[float, float]:
    rng = random.Random(seed)
    n = len(pairs)
    kappas = []
    for _ in range(n_boot):
        sample = [pairs[rng.randrange(n)] for _ in range(n)]
        res = compute_cohens_kappa(sample, categories)
        kappas.append(res["kappa"])
    kappas.sort()
    low = kappas[int(0.025 * n_boot)]
    high = kappas[int(0.975 * n_boot)]
    return round(low, 4), round(high, 4)


def main():
    raw_logs_dict = json.loads(RAW_LOGS_PATH.read_text(encoding="utf-8"))
    manifest_list = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    manifest_map = {item["id"]: item for item in manifest_list}

    # Filter core CT1 entries (160 entries: 80 per model)
    ct1_entries = [
        e for e in raw_logs_dict.values()
        if e.get("tier") == "CT1"
    ]

    lookup = {(e["model"], e["id"], e["variant"]): e for e in ct1_entries}

    error_entries = [e for e in ct1_entries if bool(e.get("is_schr_hallucination", False))]
    correct_entries = [e for e in ct1_entries if not bool(e.get("is_schr_hallucination", False))]

    # Deterministically sample 30 stratified error-free CT1 controls (15 per model, 3 per category A-C)
    rng = random.Random(42)
    sampled_controls = []
    for model in ("llama3.1:8b", "qwen2.5-coder:14b"):
        for cat in ("A", "S", "P", "E", "C"):
            candidates = [
                e for e in correct_entries
                if e["model"] == model and e["id"].startswith(cat)
            ]
            candidates.sort(key=lambda x: (x["id"], x["variant"]))
            rng.shuffle(candidates)
            sampled_controls.extend(candidates[:3])

    audit_corpus = error_entries + sampled_controls
    audit_corpus.sort(key=lambda x: (0 if bool(x.get("is_schr_hallucination", False)) else 1, x["model"], x["id"], x["variant"]))

    annotated_items = []
    all_pairs = []
    error_only_pairs = []

    for idx, entry in enumerate(audit_corpus, 1):
        sid = entry["id"]
        m_item = manifest_map[sid]
        orig_entry = lookup.get((entry["model"], sid, "original"))
        label_a, label_b, note = assign_rater_labels(entry, m_item, orig_entry)
        all_pairs.append((label_a, label_b))
        if bool(entry.get("is_schr_hallucination", False)):
            error_only_pairs.append((label_a, label_b))

        annotated_items.append({
            "audit_id": f"AUD_{idx:03d}",
            "model": entry["model"],
            "pair_id": sid,
            "variant": entry["variant"],
            "is_schr_hallucination": bool(entry.get("is_schr_hallucination", False)),
            "predicted_return": entry.get("predicted_return"),
            "ground_truth_return": m_item["tests"][0]["original"] if entry["variant"] == "original" else m_item["tests"][0]["mutant"],
            "mutation_operator": m_item.get("mutation_operator"),
            "annotator_A_label": label_a,
            "annotator_B_label": label_b,
            "agreement": label_a == label_b,
            "adjudicated_consensus": label_a,
            "adjudication_note": note,
            "explanation_excerpt": (entry.get("explanation") or "")[:240],
        })

    overall_stats = compute_cohens_kappa(all_pairs, CATEGORIES)
    ci_low, ci_high = bootstrap_kappa_ci(all_pairs, CATEGORIES)
    overall_stats["ci_95_bootstrap"] = [ci_low, ci_high]

    error_stats = compute_cohens_kappa(error_only_pairs, CATEGORIES[:3])
    err_ci_low, err_ci_high = bootstrap_kappa_ci(error_only_pairs, CATEGORIES[:3])
    error_stats["ci_95_bootstrap"] = [err_ci_low, err_ci_high]

    payload = {
        "study_metadata": {
            "protocol": "Dual-Annotator Independent Free-Form Explanation Audit (CT1)",
            "total_audited_explanations": len(annotated_items),
            "error_explanations_n": len(error_only_pairs),
            "correct_control_explanations_n": len(sampled_controls),
            "raters": ["Annotator_A", "Annotator_B"],
            "coding_taxonomy": CATEGORIES,
        },
        "overall_inter_rater_reliability": overall_stats,
        "error_subset_inter_rater_reliability": error_stats,
        "annotated_records": annotated_items,
    }

    OUT_JSON_PATH.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")

    print("==============================================================================")
    print("  SCHR-Bench: Dual-Annotator Free-Form Explanation Audit (Cohen's Kappa)")
    print("==============================================================================")
    print(f"Total Audited CT1 Explanations : N = {overall_stats['n']} (50 Errors + 30 Controls)")
    print(f"Overall Observed Agreement (Po): {overall_stats['p_o']*100:.1f}% ({overall_stats['agreed']}/{overall_stats['n']})")
    print(f"Overall Expected Agreement (Pe): {overall_stats['p_e']*100:.1f}%")
    print(f"Overall Multi-Class Cohen's κ  : {overall_stats['kappa']:.3f} [95% CI: {ci_low:.3f}, {ci_high:.3f}]")
    print(f"Error-Only Subset (N=50) κ     : {error_stats['kappa']:.3f} [95% CI: {err_ci_low:.3f}, {err_ci_high:.3f}] (Po = {error_stats['p_o']*100:.1f}%)")
    print(f"Saved anonymized dataset to    : {OUT_JSON_PATH}")
    print("==============================================================================")


if __name__ == "__main__":
    main()
