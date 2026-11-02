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
echo "  Artifact Package: template SOC-RL-v2.0"
echo "========================================================================"

echo ""
echo "[Step 1A/3] Running Standalone Binary Build & Assertion Suite (check_suite.py)..."
python3 dataset/SCHR_Bench_C_Functions/tools/check_suite.py

echo ""
echo "[Step 1B/3] Generating E0 Sanity Check Report & Table 1 (step0_verify_e0_windows.py)..."
python3 code/step0_verify_e0_windows.py

echo ""
echo "[Step 2/3] Generating Leak-Free Normalized Contexts (decompiled_contexts_80.json)..."
python3 code/extract_contexts.py

echo ""
echo "[Step 3/3] Reproducing Statistical Tables (SCHR, 95% Wilson CI, M1-M5, Spearman rho, McNemar, N=50 Taxonomy)..."
python3 code/step4_compute_statistics_and_tables.py

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
