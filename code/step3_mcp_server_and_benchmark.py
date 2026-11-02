# -*- coding: utf-8 -*-
"""
SCHR-Bench: Step 3 — Model Context Protocol (MCP) Server & LLM Benchmark Runner
Connects to local Ollama (http://localhost:11434 or http://192.168.86.1:11434) to evaluate:
  - Model 1: llama3.1:8b (General-Purpose Open-Weight LLM)
  - Model 2: qwen2.5-coder:14b (Code-Specialized Open-Weight LLM)

Supports two evaluation modes:
  1. `--mode return` (default, used for the 540 logged runs in `results/benchmark_raw_logs.json`):
     Queries exact integer return value (`predicted_return`) and natural language explanation.
  2. `--mode mcq` (evaluates the 160 balanced MCQ items in `dataset/gold_set_mcq.json`
     using `prompts/mcq_system_prompt.txt`).
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
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

RESULTS_DIR = PROJECT_DIR / "results" if (PROJECT_DIR / "results").exists() else PROJECT_DIR / "Results"
CONTEXTS_FILE = RESULTS_DIR / "decompiled_contexts_80.json"
MCQ_FILE = PROJECT_DIR / "dataset" / "gold_set_mcq.json"
MCQ_PROMPT_FILE = PROJECT_DIR / "prompts" / "mcq_system_prompt.txt"

DEFAULT_HOST = os.environ.get("OLLAMA_HOST", "http://192.168.86.1:11434")
OLLAMA_URL = f"{DEFAULT_HOST.rstrip('/')}/api/generate"
DEFAULT_MODELS = ["llama3.1:8b", "qwen2.5-coder:14b"]

FIXED_SYSTEM_PROMPT = (
    "You are an expert binary reverse engineer analyzing stripped x86-64 PE functions. "
    "Do NOT guess based on typical malware templates; trace the exact control flow and dataflow shown in the provided context. "
    "Compute the exact integer return value of `FUN_140001140(param_1, param_2, param_3)` for the given inputs. "
    "Respond strictly in valid JSON format with keys: "
    "{\"predicted_return\": <integer>, \"security_interpretation\": \"<1-2 sentence explanation of what the function does>\"}"
)

STRATIFIED_PAIR_ORDER = [
    # Round 1: 15 pairs across all 5 categories & difficulty levels
    "A01", "S01", "P01", "E01", "C01",   # Easy tier (5 pairs = 10 variants; also used as E4 pilot subset)
    "A03", "S04", "P05", "E03", "C05",   # Medium tier
    "A06", "S06", "P06", "E06", "C08",   # Tricky tier
    # Round 2: Remaining 25 pairs to complete all 40 pairs (80 variants)
    "A02", "S02", "P02", "E02", "C02",
    "A04", "S03", "P03", "E04", "C03",
    "A05", "S05", "P04", "E05", "C04",
    "A07", "S07", "P07", "E07", "C06",
    "A08", "S08", "P08", "E08", "C07",
]


class SCHRBenchMCPServer:
    def __init__(self, contexts_path: Path):
        raw_list = json.loads(contexts_path.read_text(encoding="utf-8"))
        self.records = {r["sample_key"]: r for r in raw_list}

    def mcp_get_function_context(self, sample_key: str, tier: str = "CT1", obf: str = None) -> str:
        rec = self.records[sample_key]
        if obf and obf in rec["obfuscated_ct1"]:
            return rec["obfuscated_ct1"][obf]
        return rec["contexts"].get(tier, rec["contexts"]["CT1"])

    def build_user_prompt(self, sample_key: str, test_idx: int = 0, tier: str = "CT1", obf: str = None) -> str:
        rec = self.records[sample_key]
        test = rec["tests"][test_idx]
        ctx = self.mcp_get_function_context(sample_key, tier=tier, obf=obf)
        prompt = (
            f"### Reverse Engineering Context ({obf if obf else tier}):\n"
            f"```c\n{ctx}\n```\n\n"
            f"### Security-Critical Query:\n"
            f"- Question: {rec['question']}\n"
            f"- Concrete Input Vector: `param_1 = {test['a']}, param_2 = {test['b']}, param_3 = {test['c']}`\n\n"
            f"Determine the exact integer return value for this input vector and explain the branch/dataflow logic. "
            f"Return JSON only: {{\"predicted_return\": <int>, \"security_interpretation\": \"...\"}}"
        )
        return prompt

    def build_mcq_prompt(self, mcq_item: dict) -> str:
        skey = f"{mcq_item['function_id']}_{mcq_item['variant']}"
        tier = mcq_item["context_tier"]
        ctx = self.mcp_get_function_context(skey, tier=tier)
        opts = mcq_item["options"]
        opt_lines = "\n".join(f"  {k}: {v}" for k, v in sorted(opts.items()))
        return (
            f"### Reverse Engineering Context ({tier}):\n"
            f"```c\n{ctx}\n```\n\n"
            f"### Multiple-Choice Question:\n"
            f"{mcq_item['question']}\n\n"
            f"Options:\n{opt_lines}\n\n"
            f"Select the single accurate option (A, B, C, or D) and return JSON only: "
            f"{{\"reasoning\": \"...\", \"choice\": \"<A|B|C|D>\"}}"
        )


def query_ollama(model: str, system_prompt: str, user_prompt: str, ollama_url: str = None, timeout: int = 120) -> dict:
    target_url = ollama_url or OLLAMA_URL
    payload = {
        "model": model,
        "system": system_prompt,
        "prompt": user_prompt,
        "stream": False,
        "format": "json",
        "options": {
            "temperature": 0.0,
            "seed": 42,
            "num_predict": 160
        }
    }
    req = urllib.request.Request(
        target_url,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST"
    )
    t0 = time.time()
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        body = json.loads(resp.read().decode("utf-8"))
    elapsed = round(time.time() - t0, 2)
    raw_text = body.get("response", "{}")

    predicted_val = None
    choice_val = None
    explanation = raw_text
    try:
        parsed = json.loads(raw_text)
        if parsed.get("predicted_return") is not None:
            if isinstance(parsed.get("predicted_return"), bool):
                predicted_val = 1 if parsed.get("predicted_return") else 0
            else:
                predicted_val = int(parsed.get("predicted_return"))
        if parsed.get("choice") is not None:
            choice_val = str(parsed.get("choice")).strip().upper()[:1]
        explanation = str(parsed.get("security_interpretation") or parsed.get("reasoning") or "")
    except Exception:
        m = re.search(r'"predicted_return"\s*:\s*(-?\d+)', raw_text)
        if m:
            predicted_val = int(m.group(1))
        mc = re.search(r'"choice"\s*:\s*"([A-D])"', raw_text, re.I)
        if mc:
            choice_val = mc.group(1).upper()

    return {
        "predicted_return": predicted_val,
        "choice": choice_val,
        "explanation": explanation,
        "raw_response": raw_text,
        "latency_sec": elapsed
    }


def check_ollama_online(host: str = None) -> list:
    base = (host or DEFAULT_HOST).rstrip('/')
    try:
        req = urllib.request.Request(f"{base}/api/tags", method="GET")
        with urllib.request.urlopen(req, timeout=5) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            return [m["name"] for m in data.get("models", [])]
    except Exception:
        return []


def run_benchmark_suite(mcp: SCHRBenchMCPServer, models: list, tiers: list, max_pairs: int = 40, run_obf: bool = True, ollama_url: str = None):
    import step4_compute_statistics_and_tables as step4

    target_url = ollama_url or OLLAMA_URL
    log_path = RESULTS_DIR / "benchmark_raw_logs.json"
    existing_logs = json.loads(log_path.read_text(encoding="utf-8")) if log_path.exists() else {}

    pair_ids = STRATIFIED_PAIR_ORDER[:max_pairs]
    print(f"[+] Running return-value benchmark on {len(pair_ids)} pairs ({len(pair_ids)*2} variants) across models={models}, tiers={tiers}")

    for model in models:
        print(f"\n==================================================================")
        print(f"[*] MODEL: {model}")
        print(f"==================================================================")
        for pair_idx, sid in enumerate(pair_ids, 1):
            for variant in ("original", "mutant"):
                skey = f"{sid}_{variant}"
                rec = mcp.records[skey]
                test = rec["tests"][0]
                truth = int(test[variant])
                other_truth = int(test["original" if variant == "mutant" else "mutant"])

                for tier in tiers:
                    log_id = f"{model}__{tier}__{skey}"
                    if log_id in existing_logs:
                        continue
                    prompt = mcp.build_user_prompt(skey, test_idx=0, tier=tier)
                    res = query_ollama(model, FIXED_SYSTEM_PROMPT, prompt, ollama_url=target_url)
                    is_correct = (res["predicted_return"] == truth)
                    existing_logs[log_id] = {
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
                        "latency_sec": res["latency_sec"]
                    }
                    log_path.write_text(json.dumps(existing_logs, indent=2, ensure_ascii=False), encoding="utf-8")
                    mark = "[PASS]" if is_correct else "[SCHR]"
                    print(
                        f"  [{pair_idx:02d}/{len(pair_ids):02d} | {model:17s} | {tier} | {skey:12s}] "
                        f"Truth={truth:3d} Pred={str(res['predicted_return']):4s} -> {mark} ({res['latency_sec']}s)"
                    )

                if run_obf and pair_idx <= 5:
                    for obf_lvl in ("Obf1_CFF", "Obf2_Sub", "Obf3_Combined"):
                        obf_log_id = f"{model}__{obf_lvl}__{skey}"
                        if obf_log_id in existing_logs:
                            continue
                        prompt = mcp.build_user_prompt(skey, test_idx=0, tier="CT1", obf=obf_lvl)
                        res = query_ollama(model, FIXED_SYSTEM_PROMPT, prompt, ollama_url=target_url)
                        is_correct = (res["predicted_return"] == truth)
                        existing_logs[obf_log_id] = {
                            "model": model,
                            "tier": obf_lvl,
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
                            "latency_sec": res["latency_sec"]
                        }
                        log_path.write_text(json.dumps(existing_logs, indent=2, ensure_ascii=False), encoding="utf-8")
                        mark = "[PASS]" if is_correct else "[SCHR]"
                        print(
                            f"  [E4-OBF | {model:17s} | {obf_lvl:13s} | {skey:12s}] "
                            f"Truth={truth:3d} Pred={str(res['predicted_return']):4s} -> {mark} ({res['latency_sec']}s)"
                        )

            step4.main()


def run_mcq_suite(mcp: SCHRBenchMCPServer, models: list, ollama_url: str = None):
    target_url = ollama_url or OLLAMA_URL
    mcq_items = json.loads(MCQ_FILE.read_text(encoding="utf-8"))
    sys_prompt = MCQ_PROMPT_FILE.read_text(encoding="utf-8").strip() if MCQ_PROMPT_FILE.exists() else FIXED_SYSTEM_PROMPT
    mcq_log_path = RESULTS_DIR / "benchmark_mcq_logs.json"
    existing = json.loads(mcq_log_path.read_text(encoding="utf-8")) if mcq_log_path.exists() else {}

    print(f"[+] Running 160-item Gold Set MCQ evaluation across models={models}")
    for model in models:
        for idx, item in enumerate(mcq_items, 1):
            gid = item["gold_id"]
            log_id = f"{model}__{gid}"
            if log_id in existing:
                continue
            prompt = mcp.build_mcq_prompt(item)
            res = query_ollama(model, sys_prompt, prompt, ollama_url=target_url)
            is_correct = (res["choice"] == item["ground_truth_choice"])
            existing[log_id] = {
                "model": model,
                "gold_id": gid,
                "function_id": item["function_id"],
                "variant": item["variant"],
                "context_tier": item["context_tier"],
                "ground_truth_choice": item["ground_truth_choice"],
                "predicted_choice": res["choice"],
                "is_correct": is_correct,
                "is_schr_hallucination": not is_correct,
                "reasoning": res["explanation"],
                "latency_sec": res["latency_sec"]
            }
            mcq_log_path.write_text(json.dumps(existing, indent=2, ensure_ascii=False), encoding="utf-8")
            print(f"  [{idx:03d}/160 | {model} | {gid}] Truth={item['ground_truth_choice']} Pred={res['choice']} ({res['latency_sec']}s)")


def main():
    parser = argparse.ArgumentParser(description="SCHR-Bench MCP Benchmark Runner")
    parser.add_argument("--mode", choices=["return", "mcq"], default="return", help="Evaluation mode: 'return' (default 540-run oracle) or 'mcq' (160-item gold_set_mcq.json)")
    parser.add_argument("--demo", action="store_true", help="Run 5-pair subset")
    parser.add_argument("--max-pairs", type=int, default=40, help="Number of pairs to evaluate (default: 40 = all 80 variants)")
    parser.add_argument("--models", nargs="+", default=DEFAULT_MODELS, help="Ollama models to evaluate")
    parser.add_argument("--tiers", nargs="+", default=["CT1", "CT2", "CT3"], help="Context tiers to evaluate")
    parser.add_argument("--no-obf", action="store_true", help="Skip E4 obfuscation evaluation")
    parser.add_argument("--host", default=DEFAULT_HOST, help="Ollama server host URL (default: %(default)s)")
    args = parser.parse_args()

    ollama_host = args.host.rstrip('/')
    ollama_gen_url = f"{ollama_host}/api/generate"

    online_models = check_ollama_online(ollama_host)
    if not online_models:
        print(f"[!] Ollama server is NOT running or unreachable at {ollama_host}.")
        sys.exit(1)

    print(f"[+] Connected to Ollama at {ollama_host}. Available models: {online_models}")
    mcp = SCHRBenchMCPServer(CONTEXTS_FILE)
    if args.mode == "mcq":
        run_mcq_suite(mcp, args.models, ollama_url=ollama_gen_url)
    else:
        max_p = 5 if args.demo else args.max_pairs
        run_benchmark_suite(mcp, args.models, args.tiers, max_pairs=max_p, run_obf=not args.no_obf, ollama_url=ollama_gen_url)


if __name__ == "__main__":
    main()
