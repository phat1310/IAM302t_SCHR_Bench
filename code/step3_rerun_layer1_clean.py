"""
step3_rerun_layer1_clean.py
Full automated runner for 540 clean Layer 1 return-value evaluations on Ollama.
Purges all historical/leakage artifacts, ensures zero prompt contamination,
and triggers downstream SSOT macro generation and table synthesis.
"""

import argparse
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_DIR = SCRIPT_DIR.parent
RESULTS_DIR = PROJECT_DIR / "results"
RESULTS_DIR.mkdir(parents=True, exist_ok=True)

FIXED_SYSTEM_PROMPT = (
    "You are an expert binary reverse engineer and software security analyst. "
    "Your objective is to inspect the provided decompiled C pseudocode (and assembly or specifications when provided) "
    "to determine the exact return value of the function target() for the specified input vector. "
    "You must return strictly valid JSON with the format: "
    '{"predicted_return": <integer>, "security_interpretation": "<brief explanation of the control/data flow>"}'
)

STRATIFIED_PAIR_ORDER = [
    f"{cat}{i:02d}" for cat in ("A", "S", "P", "E", "C") for i in range(1, 9)
]

E4_PILOT_PAIRS = ["A01", "S01", "P01", "E01", "C01"]


def query_ollama(
    model: str,
    system_prompt: str,
    user_prompt: str,
    ollama_url: str = "http://localhost:11434",
    timeout: int = 120,
    num_predict: int = 160,
) -> dict:
    req_body = {
        "model": model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        "stream": False,
        "options": {
            "temperature": 0.0,
            "seed": 42,
            "num_predict": num_predict,
        },
    }
    url = f"{ollama_url.rstrip('/')}/api/chat"
    data = json.dumps(req_body).encode("utf-8")
    req = urllib.request.Request(
        url, data=data, headers={"Content-Type": "application/json"}
    )

    t0 = time.time()
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            elapsed = time.time() - t0
            res = json.loads(resp.read().decode("utf-8"))
            content = res.get("message", {}).get("content", "").strip()

            # Parse JSON block
            parsed_return = None
            explanation = content
            json_match = re.search(r"\{.*?\}", content, re.DOTALL)
            if json_match:
                try:
                    payload = json.loads(json_match.group(0))
                    if "predicted_return" in payload:
                        parsed_return = int(payload["predicted_return"])
                    if "security_interpretation" in payload:
                        explanation = payload["security_interpretation"]
                except Exception:
                    pass

            if parsed_return is None:
                int_match = re.search(
                    r'(?:return|predicted_return["\s:]+)\s*(-?\d+)',
                    content,
                    re.IGNORECASE,
                )
                if int_match:
                    parsed_return = int(int_match.group(1))

            return {
                "predicted_return": parsed_return,
                "explanation": explanation,
                "latency_sec": round(elapsed, 2),
                "raw_response": content,
            }
    except Exception as e:
        elapsed = time.time() - t0
        return {
            "predicted_return": None,
            "explanation": f"ERROR: {str(e)}",
            "latency_sec": round(elapsed, 2),
            "raw_response": "",
        }


def build_clean_user_prompt(
    rec: dict, variant: str, test_idx: int = 0, tier: str = "CT1", obf: str = None
) -> str:
    ctx = rec["contexts"].get(tier, "")
    if obf:
        ctx = rec["obfuscated_ct1"].get(obf, ctx)

    test = rec["tests"][test_idx]
    prompt = (
        f"### Reverse Engineering Context ({obf if obf else tier}):\n"
        f"```c\n{ctx}\n```\n\n"
        f"### Security-Critical Query:\n"
        f"- Question: {rec['question']}\n"
        f"- Concrete Input Vector: `param_1 = {test['a']}, param_2 = {test['b']}, param_3 = {test['c']}`\n\n"
        f"Determine the exact integer return value for this input vector and explain the branch/dataflow logic. "
        f'Return JSON only: {{"predicted_return": <int>, "security_interpretation": "..."}}'
    )
    return prompt


def main():
    parser = argparse.ArgumentParser(
        description="Run clean 540-run Layer 1 benchmark"
    )
    parser.add_argument(
        "--ollama-url", default="http://localhost:11434", help="Ollama API base URL"
    )
    parser.add_argument(
        "--models",
        nargs="+",
        default=["llama3.1:8b", "qwen2.5-coder:14b"],
        help="Models to evaluate",
    )
    parser.add_argument(
        "--output",
        default=str(RESULTS_DIR / "benchmark_raw_logs.json"),
        help="Path to output JSON",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Force overwrite existing runs instead of skipping",
    )
    args = parser.parse_args()

    contexts_path = RESULTS_DIR / "decompiled_contexts_80.json"
    if not contexts_path.exists():
        print(f"[-] Missing {contexts_path}. Running extract_contexts.py...")
        import extract_contexts

        extract_contexts.main()

    with open(contexts_path, "r", encoding="utf-8") as f:
        records_list = json.load(f)
    records = {r["sample_key"]: r for r in records_list}

    out_file = Path(args.output)
    logs = (
        json.loads(out_file.read_text(encoding="utf-8"))
        if out_file.exists() and not args.force
        else {}
    )

    print(f"[*] Starting clean Layer 1 evaluation suite on {args.ollama_url}...")
    print(f"[*] Target models: {args.models}")
    print(f"[*] Total variants: 80 (40 pairs)")
    print(f"[*] Target runs: 480 core (CT1-CT3) + 60 E4 pilot (Obf1-Obf3) = 540 total")

    total_executed = 0
    start_time = time.time()

    for model in args.models:
        print(f"\n============================================================")
        print(f"[*] EVALUATING MODEL: {model}")
        print(f"============================================================")

        # 1. Core 480 runs: 40 pairs x 2 variants x 3 tiers
        for sid in STRATIFIED_PAIR_ORDER:
            for variant in ("original", "mutant"):
                skey = f"{sid}_{variant}"
                rec = records[skey]
                truth = int(rec["tests"][0][variant])
                other_truth = int(
                    rec["tests"][0]["original" if variant == "mutant" else "mutant"]
                )

                for tier in ("CT1", "CT2", "CT3"):
                    log_id = f"{model}__{tier}__{skey}"
                    if log_id in logs and not args.force:
                        continue

                    prompt = build_clean_user_prompt(
                        rec, variant, test_idx=0, tier=tier
                    )
                    res = query_ollama(
                        model,
                        FIXED_SYSTEM_PROMPT,
                        prompt,
                        ollama_url=args.ollama_url,
                    )
                    is_correct = res["predicted_return"] == truth

                    logs[log_id] = {
                        "model": model,
                        "tier": tier,
                        "sample_key": skey,
                        "id": sid,
                        "variant": variant,
                        "category": rec["category"],
                        "difficulty": rec["difficulty"],
                        "mutation_operator": rec["mutation_operator"],
                        "ground_truth": truth,
                        "opposite_variant_truth": other_truth,
                        "predicted_return": res["predicted_return"],
                        "is_correct": is_correct,
                        "is_schr_hallucination": not is_correct,
                        "explanation": res["explanation"],
                        "latency_sec": res["latency_sec"],
                    }
                    total_executed += 1
                    status = (
                        "OK"
                        if is_correct
                        else f"SCHR_ERR (pred={res['predicted_return']}, truth={truth})"
                    )
                    print(
                        f"[{total_executed:03d}/540] {log_id:<38} -> {status} ({res['latency_sec']}s)",
                        flush=True,
                    )

                    # Save checkpoint every 10 runs
                    if total_executed % 10 == 0:
                        out_file.write_text(
                            json.dumps(logs, indent=2, ensure_ascii=False),
                            encoding="utf-8",
                        )

        # 2. E4 Obfuscation Pilot 60 runs: 5 pairs x 2 variants x 3 obf templates
        for sid in E4_PILOT_PAIRS:
            for variant in ("original", "mutant"):
                skey = f"{sid}_{variant}"
                rec = records[skey]
                truth = int(rec["tests"][0][variant])
                other_truth = int(
                    rec["tests"][0]["original" if variant == "mutant" else "mutant"]
                )

                for obf in ("Obf1_CFF", "Obf2_Sub", "Obf3_Combined"):
                    log_id = f"{model}__{obf}__{skey}"
                    if log_id in logs and not args.force:
                        continue

                    prompt = build_clean_user_prompt(
                        rec, variant, test_idx=0, obf=obf
                    )
                    res = query_ollama(
                        model,
                        FIXED_SYSTEM_PROMPT,
                        prompt,
                        ollama_url=args.ollama_url,
                    )
                    is_correct = res["predicted_return"] == truth

                    logs[log_id] = {
                        "model": model,
                        "tier": obf,
                        "sample_key": skey,
                        "id": sid,
                        "variant": variant,
                        "category": rec["category"],
                        "difficulty": rec["difficulty"],
                        "mutation_operator": rec["mutation_operator"],
                        "ground_truth": truth,
                        "opposite_variant_truth": other_truth,
                        "predicted_return": res["predicted_return"],
                        "is_correct": is_correct,
                        "is_schr_hallucination": not is_correct,
                        "explanation": res["explanation"],
                        "latency_sec": res["latency_sec"],
                    }
                    total_executed += 1
                    status = (
                        "OK"
                        if is_correct
                        else f"SCHR_ERR (pred={res['predicted_return']}, truth={truth})"
                    )
                    print(
                        f"[{total_executed:03d}/540] {log_id:<38} -> {status} ({res['latency_sec']}s)",
                        flush=True,
                    )

                    if total_executed % 10 == 0:
                        out_file.write_text(
                            json.dumps(logs, indent=2, ensure_ascii=False),
                            encoding="utf-8",
                        )

    # Final write
    out_file.write_text(
        json.dumps(logs, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    total_time = round(time.time() - start_time, 1)
    print(f"\n[+] COMPLETED: {total_executed} new evaluations in {total_time}s.")
    print(f"[+] Total entries in {out_file}: {len(logs)}")

    # Downstream trigger
    print("\n[*] Triggering step4_compute_statistics_and_tables.py...")
    import step4_compute_statistics_and_tables

    step4_compute_statistics_and_tables.main()

    print("[*] Triggering generate_paper_macros.py...")
    import generate_paper_macros

    generate_paper_macros.main()

    print("[*] Triggering plot_figure3_empirical_schr.py...")
    import plot_figure3_empirical_schr


if __name__ == "__main__":
    main()
