#!/usr/bin/env bash
# ==============================================================================
# SCHR-Bench: Two-Mode Reproducibility Script (Artifact Evaluation Standard)
# Mode A (Default): Offline E0 binary execution verification + statistical table reproduction
# Mode B (--live-ollama): Full live LLM benchmark execution via local Ollama server
# ==============================================================================
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

MODE="offline"
if [ "${1:-}" = "--live-ollama" ]; then
    MODE="live"
fi

echo "========================================================================"
echo "  SCHR-Bench: Reproducibility Pipeline (Mode: $MODE)"
echo "  Artifact Package: SOC-RL-v2.0"
echo "========================================================================"

echo ""
echo "[Step 1A/5] Running Standalone Binary Build & Assertion Suite (check_suite.py)..."
python3 dataset/SCHR_Bench_C_Functions/tools/check_suite.py

echo ""
echo "[Step 1B/5] Generating E0 Sanity Check Report & Table 1 (step0_verify_e0_windows.py)..."
python3 code/step0_verify_e0_windows.py

echo ""
echo "[Step 1C/5] Building & Verifying 30 Obfuscated PE64 Binaries (build_and_verify_obfuscated_pe64.py)..."
python3 code/build_and_verify_obfuscated_pe64.py

echo ""
echo "[Step 2/5] Generating Leak-Free Normalized Contexts (decompiled_contexts_80.json)..."
python3 code/extract_contexts.py

echo ""
echo "[Step 3/5] Reproducing Statistical Tables (SCHR, 95% Wilson CI, M1-M5, Spearman rho, McNemar, AUROC)..."
python3 code/step4_compute_statistics_and_tables.py

echo ""
echo "[Step 4/5] Computing Dual-Annotator Free-Form Explanation Audit (Cohen's Kappa, N=80)..."
python3 code/step6_compute_cohens_kappa.py

echo ""
echo "[Step 5/5] Verifying 20-Pair Stratified Q4 vs. FP16 Control Protocol Baseline..."
python3 code/step5_fp16_api_subset_ablation.py --baseline-only

if [ "$MODE" = "live" ]; then
    echo ""
    echo "[Live Mode] Executing Full LLM Benchmark Suite via Ollama (--max-pairs 40)..."
    python3 code/step3_mcp_server_and_benchmark.py --mode return --max-pairs 40
    python3 code/step3_mcp_server_and_benchmark.py --mode mcq
fi

echo ""
echo "========================================================================"
echo "  [OK] SCHR-Bench Reproducibility Pipeline Completed (Mode: $MODE)!"
echo "========================================================================"
