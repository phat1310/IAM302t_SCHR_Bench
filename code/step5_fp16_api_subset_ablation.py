#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
step5_fp16_api_subset_ablation.py
Stratified 20-Pair (N=40 Variants) FP16 / Cloud Router API Control Experiment for SCHR-Bench.

Purpose (Addressing Reviewer / Advisor Feedback on 4-Bit Quantization Confounder):
Evaluates a stratified 20-pair subset (4 pairs per functional category A, S, P, E, C:
1 easy, 2 medium, 1 tricky per category = 20 pairs / 40 variants) under unquantized FP16
weights (via Ollama) or full-precision Cloud / Router API models (OpenAI-compatible endpoint)
at temperature=0.0, and compares against the logged 4-bit (Q4_0 / Q4_K_M) baseline on the
exact same 20 pairs.
"""

import argparse
import json
import os
import re
import time
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MANIFEST_PATH = ROOT / "dataset" / "SCHR_Bench_C_Functions" / "ground_truth_manifest.json"
CONTEXTS_PATH = ROOT / "results" / "decompiled_contexts_80.json"
RAW_LOGS_PATH = ROOT / "results" / "benchmark_raw_logs.json"
OUT_PATH = ROOT / "results" / "fp16_api_subset_ablation.json"

# Stratified 20-pair subset: 4 pairs per category (1 easy [01], 2 medium [03, 05], 1 tricky [06])
STRATIFIED_20_PAIRS = [
    "A01", "A03", "A05", "A06",
    "S01", "S03", "S05", "S06",
    "P01", "P03", "P05", "P06",
    "E01", "E03", "E05", "E06",
    "C01", "C03", "C05", "C06",
]

SYSTEM_PROMPT = (
    "You are an expert binary reverse engineer. Analyze the provided stripped C pseudocode "
    "and determine the exact integer return value of `FUN_140001140(param_1, param_2, param_3)` "
    "for the specified input arguments. Respond strictly in valid JSON format with keys: "
    '{"predicted_return": <int>, "explanation": "<concise 1-2 sentence technical explanation>"}.'
)


def parse_json_response(text: str):
    cleaned = re.sub(r"^```(?:json)?\s*|\s*```$", "", text.strip(), flags=re.MULTILINE)
    try:
        obj = json.loads(cleaned)
        return int(obj.get("predicted_return")), str(obj.get("explanation", ""))
    except Exception:
        m = re.search(r'"predicted_return"\s*:\s*(-?\d+)', text)
        pred = int(m.group(1)) if m else None
        return pred, text.strip()


def query_ollama(url: str, model: str, user_prompt: str):
    payload = {
        "model": model,
        "prompt": f"{SYSTEM_PROMPT}\n\n{user_prompt}",
        "stream": False,
        "format": "json",
        "options": {"temperature": 0.0, "seed": 42, "num_predict": 160},
    }
    req = urllib.request.Request(
        f"{url.rstrip('/')}/api/generate",
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
    )
    t0 = time.time()
    with urllib.request.urlopen(req, timeout=180) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    latency = round(time.time() - t0, 2)
    pred, expl = parse_json_response(data.get("response", "{}"))
    return pred, expl, latency


def query_openai_compatible(base_url: str, api_key: str, model: str, user_prompt: str, max_retries: int = 3):
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ],
        "temperature": 0.0,
        "seed": 42,
        "max_tokens": 200,
    }
    endpoint = f"{base_url.rstrip('/')}/chat/completions"
    for attempt in range(1, max_retries + 1):
        try:
            req = urllib.request.Request(
                endpoint,
                data=json.dumps(payload).encode("utf-8"),
                headers={
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {api_key}",
                    "User-Agent": "SCHR-Bench-Evaluator/2.0",
                },
            )
            t0 = time.time()
            with urllib.request.urlopen(req, timeout=180) as resp:
                data = json.loads(resp.read().decode("utf-8"))
            latency = round(time.time() - t0, 2)
            content = data["choices"][0]["message"]["content"]
            pred, expl = parse_json_response(content)
            return pred, expl, latency
        except Exception as err:
            if attempt == max_retries:
                raise
            time.sleep(2.0 * attempt)


def summarize_20_pairs(records_by_key: dict, label: str):
    orig_err = 0
    mut_err = 0
    both_ok = 0
    orig_ok_mut_err = 0
    parroted = 0
    for pid in STRATIFIED_20_PAIRS:
        o = records_by_key[f"{pid}_original"]
        m = records_by_key[f"{pid}_mutant"]
        oe = int(o["is_schr_hallucination"])
        me = int(m["is_schr_hallucination"])
        orig_err += oe
        mut_err += me
        if oe == 0 and me == 0:
            both_ok += 1
        elif oe == 0 and me == 1:
            orig_ok_mut_err += 1
            if m["predicted_return"] == m["opposite_variant_truth"]:
                parroted += 1
    tot_err = orig_err + mut_err
    print(
        f"| {label:<28} | N=40 (20 pairs) | SCHR: {tot_err}/40 ({tot_err*2.5:.1f}%) | "
        f"Orig Err: {orig_err}/20 ({orig_err*5.0:.1f}%) | Mut Err: {mut_err}/20 ({mut_err*5.0:.1f}%) | "
        f"Pair Acc: {both_ok}/20 ({both_ok*5.0:.1f}%) | Parroting: {parroted}/{orig_ok_mut_err} |"
    )


def main():
    parser = argparse.ArgumentParser(description="Run 20-pair FP16 / Router API subset ablation on CT1.")
    parser.add_argument("--baseline-only", action="store_true", help="Print Q4 baseline stats on the 20-pair subset without live inference")
    parser.add_argument("--provider", choices=["ollama", "openai", "router"], default="router")
    parser.add_argument("--model", default=os.environ.get("ROUTER_MODEL", "qwen/qwen-2.5-coder-14b-instruct"), help="FP16 Ollama tag or Router/OpenAI API model ID")
    parser.add_argument("--ollama-url", default=os.environ.get("OLLAMA_URL", "http://127.0.0.1:11434"))
    parser.add_argument(
        "--api-base",
        default=os.environ.get("ROUTER_API_BASE", os.environ.get("OPENAI_BASE_URL", "https://api.openai.com/v1")),
        help="OpenAI-compatible base URL (e.g. Router API https://<your-router-domain>/v1)",
    )
    parser.add_argument(
        "--api-key",
        default=os.environ.get("ROUTER_API_KEY", os.environ.get("OPENAI_API_KEY", "")),
        help="API key for Router API or OpenAI-compatible gateway",
    )
    parser.add_argument("--output", default=str(OUT_PATH), help="Output JSON file path")
    args = parser.parse_args()

    raw_logs = json.loads(RAW_LOGS_PATH.read_text(encoding="utf-8"))
    print("=== STRATIFIED 20-PAIR SUBSET (N=40 VARIANTS, CT1) BASELINE COMPARISON ===")
    for base_model in ("llama3.1:8b", "qwen2.5-coder:14b"):
        subset_recs = {
            f"{pid}_{v}": raw_logs[f"{base_model}__CT1__{pid}_{v}"]
            for pid in STRATIFIED_20_PAIRS
            for v in ("original", "mutant")
        }
        summarize_20_pairs(subset_recs, f"{base_model} (4-bit Q4)")

    if args.baseline_only:
        return

    if args.provider in ("openai", "router") and not args.api_key:
        raise SystemExit(
            "ERROR: Missing API Key. Set ROUTER_API_KEY=... or pass --api-key <key>."
        )

    manifest_list = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    manifest = {item["id"]: item for item in manifest_list}

    contexts_list = json.loads(CONTEXTS_PATH.read_text(encoding="utf-8"))
    contexts = {rec["sample_key"]: rec["contexts"] for rec in contexts_list}

    new_records = {}
    for pid in STRATIFIED_20_PAIRS:
        fmeta = manifest[pid]
        vec = fmeta["tests"][0]
        a_val, b_val, c_val = vec["a"], vec["b"], vec["c"]
        for variant in ("original", "mutant"):
            skey = f"{pid}_{variant}"
            gt = int(vec["original"]) if variant == "original" else int(vec["mutant"])
            opp = int(vec["mutant"]) if variant == "original" else int(vec["original"])
            code_ctx = contexts[skey]["CT1"]
            user_prompt = (
                f"Function Variant under test:\n```c\n{code_ctx}\n```\n"
                f"Input vector: param_1={a_val}, param_2={b_val}, param_3={c_val}.\n"
                f"What is the exact integer return value of `FUN_140001140({a_val}, {b_val}, {c_val})`?"
            )
            if args.provider == "ollama":
                pred, expl, lat = query_ollama(args.ollama_url, args.model, user_prompt)
            else:
                pred, expl, lat = query_openai_compatible(args.api_base, args.api_key, args.model, user_prompt)
            new_records[skey] = {
                "model": args.model,
                "tier": "CT1",
                "sample_key": skey,
                "id": pid,
                "variant": variant,
                "ground_truth": gt,
                "opposite_variant_truth": opp,
                "predicted_return": pred,
                "is_correct": (pred == gt),
                "is_schr_hallucination": (pred != gt),
                "explanation": expl,
                "latency_sec": lat,
            }

    summarize_20_pairs(new_records, f"{args.model} (FP16/API)")
    out_file = Path(args.output)
    out_file.write_text(json.dumps(new_records, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"[+] Saved 40 FP16/API subset evaluations to {out_file}")


if __name__ == "__main__":
    main()
