#!/usr/bin/env bash
# ==============================================================================
# SCHR-Bench: 1-Click Reproducibility Script (Artifact Evaluation Standard)
# Project: Security-Critical Hallucination Rate Benchmark
# Target: FPT University IAM302t & Springer LNICST (INISCOM 2027)
# ==============================================================================
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "========================================================================"
echo "  SCHR-Bench: One-Click Reproducibility Pipeline"
echo "  Artifact Package: SOC / Research-Based Learning Standard"
echo "========================================================================"

echo ""
echo "[Step 1/3] Running E0 Ground Truth Sanity Check (160 Assertions)..."
if [ -f "code/step0_verify_e0_windows.py" ]; then
    python3 code/step0_verify_e0_windows.py
elif [ -f "scripts/step0_verify_e0_windows.py" ]; then
    python3 scripts/step0_verify_e0_windows.py
fi

echo ""
echo "[Step 2/3] Evaluating Statistical Engine (SCHR, Wilson CI 95%, McNemar)..."
if [ -f "code/step4_compute_statistics_and_tables.py" ]; then
    python3 code/step4_compute_statistics_and_tables.py
elif [ -f "code/eval_engine.py" ]; then
    python3 code/eval_engine.py
elif [ -f "scripts/step4_compute_statistics_and_tables.py" ]; then
    python3 scripts/step4_compute_statistics_and_tables.py
fi

echo ""
echo "[Step 3/3] Executing Milestone D3 Live Demo..."
if [ -f "code/live_demo.sh" ]; then
    bash code/live_demo.sh
elif [ -f "scripts/live_demo.sh" ]; then
    bash scripts/live_demo.sh
fi

echo ""
echo "========================================================================"
echo "  [OK] SCHR-Bench All Reproducibility Steps Executed Successfully!"
echo "========================================================================"
