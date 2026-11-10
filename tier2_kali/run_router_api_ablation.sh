#!/usr/bin/env bash
# ==============================================================================
# SCHR-Bench: Router API / Full-Precision 20-Pair (N=40) Ablation Runner
# Compatible with both WSL2 (Tier 1 Host) and Kali Linux VM (tier2_kali)
# ==============================================================================
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
cd "$REPO_ROOT"

if [ -z "${ROUTER_API_KEY:-}" ]; then
    echo "========================================================================"
    echo " [!] ROUTER_API_KEY is not set. Running Offline 20-Pair Baseline Mode:"
    echo "========================================================================"
    python3 code/step5_fp16_api_subset_ablation.py --baseline-only
    echo ""
    echo "To run Live Full-Precision / Frontier Model Evaluation via Router API:"
    echo "  export ROUTER_API_BASE=\"https://<your-router-api-domain>/v1\""
    echo "  export ROUTER_API_KEY=\"sk-...\""
    echo "  export ROUTER_MODEL=\"qwen/qwen-2.5-coder-14b-instruct\""
    echo "  bash tier2_kali/run_router_api_ablation.sh"
    exit 0
fi

API_BASE="${ROUTER_API_BASE:-https://api.openai.com/v1}"
MODEL_NAME="${ROUTER_MODEL:-qwen/qwen-2.5-coder-14b-instruct}"

echo "========================================================================"
echo "  SCHR-Bench: Running Live 20-Pair (N=40) Ablation via Router API"
echo "  Endpoint : $API_BASE"
echo "  Model    : $MODEL_NAME"
echo "========================================================================"

python3 code/step5_fp16_api_subset_ablation.py \
    --provider router \
    --api-base "$API_BASE" \
    --api-key "$ROUTER_API_KEY" \
    --model "$MODEL_NAME" \
    --output "results/fp16_api_subset_ablation.json"
