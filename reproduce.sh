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
echo "[Step 1/3] Running E0 Ground-Truth Compile & Execution Check (80 variants, 160 assertions)..."
python3 code/step0_verify_e0_windows.py

echo ""
echo "[Step 2/3] Generating Leak-Free Normalized Contexts (decompiled_contexts_80.json)..."
python3 code/extract_contexts.py

echo ""
echo "[Step 3/3] Reproducing Statistical Tables (SCHR, 95% Wilson CI, Spearman rho, McNemar) from 540 Logged Runs..."
python3 code/step4_compute_statistics_and_tables.py

if [ "$MODE" = "live" ]; then
    echo ""
    echo "[Live Mode] Executing Full LLM Benchmark Suite via Ollama (--max-pairs 40)..."
    python3 code/step3_mcp_server_and_benchmark.py --max-pairs 40
fi

echo ""
echo "========================================================================"
echo "  [OK] SCHR-Bench Reproducibility Pipeline Completed (Mode: $MODE)!"
echo "========================================================================"
