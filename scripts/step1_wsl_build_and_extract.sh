#!/usr/bin/env bash
# ==============================================================================
# SCHR-Bench: Step 1 - Build 80 Binaries, Run E0 Sanity Check & Extract ASM/Contexts
# Chạy trên WSL Ubuntu (ntp@NTP) hoặc Kali Linux
# ==============================================================================
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
DATASET_DIR="$PROJECT_DIR/Dataset_SCHR_Bench/SCHR_Bench_C_Functions"
RESULTS_DIR="$PROJECT_DIR/Results"

mkdir -p "$RESULTS_DIR"

echo "=================================================================="
echo " [1/4] KIỂM TRA COMPILER TRÊN WSL UBUNTU / KALI"
echo "=================================================================="
if ! command -v gcc &> /dev/null; then
    echo "[!] Chưa có gcc. Đang cài đặt build-essential..."
    sudo apt update && sudo apt install -y build-essential binutils python3
fi

echo "[+] GCC version: $(gcc --version | head -n 1)"

echo ""
echo "=================================================================="
echo " [2/4] CHẠY THÍ NGHIỆM E0: KIỂM ĐỊNH 80 BUILDS & 160 ASSERTIONS"
echo "=================================================================="
cd "$DATASET_DIR"
python3 tools/check_suite.py | tee "$RESULTS_DIR/E0_sanity_check_report.txt"

echo ""
echo "=================================================================="
echo " [3/4] BIÊN DỊCH & TRÍCH XUẤT MÃ ASSEMBLY X86_64 (O0 & O2)"
echo "=================================================================="
python3 "$SCRIPT_DIR/extract_contexts.py"

echo ""
echo "=================================================================="
echo " [4/4] HOÀN TẤT BƯỚC 1!"
echo " Dữ liệu ngữ cảnh CT1-CT4 đã được lưu tại:"
echo " -> $RESULTS_DIR/decompiled_contexts_80.json"
echo "=================================================================="
