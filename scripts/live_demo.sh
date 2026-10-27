#!/usr/bin/env bash
# ==============================================================================
# SCHR-Bench: 1-Click Live Demonstration Script (Milestone D3)
# Tự động thực thi kịch bản demo bắt quả tang ảo giác an ninh CT1 và cứu vãn tại CT2
# ==============================================================================

set -e
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(dirname "$SCRIPT_DIR")"

cd "$ROOT_DIR"

# Kiểm tra Python 3
if ! command -v python3 &> /dev/null; then
    echo "[!] Lỗi: python3 không tìm thấy trên hệ thống Kali."
    exit 1
fi

# Chạy live demo
python3 scripts/live_demo.py "$@"
