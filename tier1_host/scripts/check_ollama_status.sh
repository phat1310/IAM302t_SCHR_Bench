#!/usr/bin/env bash
# ==============================================================================
# Script: check_ollama_status.sh
# Purpose: Kiểm tra trạng thái GPU NVIDIA, Ollama Daemon và API endpoints
# Role: Tier 1 (Host MSI - WSL2)
# ==============================================================================

set -e

echo "=========================================================="
echo "🖥️  TIER 1 (HOST MSI): OLLAMA & GPU STATUS DIAGNOSTICS"
echo "=========================================================="

echo -e "\n1. [GPU Check] Kiểm tra NVIDIA GPU & VRAM:"
if command -v nvidia-smi &> /dev/null; then
    nvidia-smi --query-gpu=name,memory.total,memory.used,memory.free,temperature.gpu --format=csv,noheader
else
    echo "⚠️ nvidia-smi không tìm thấy trong WSL2, sử dụng CPU/fallback mode."
fi

echo -e "\n2. [Service Check] Kiểm tra tiến trình Ollama:"
if pgrep -x "ollama" > /dev/null; then
    echo "✅ Tiến trình 'ollama' đang chạy (PID: $(pgrep -x ollama | tr '\n' ' '))."
else
    echo "❌ Tiến trình 'ollama' chưa chạy! Vui lòng khởi chạy: 'ollama serve'"
fi

echo -e "\n3. [Network Check] Kiểm tra cổng TCP 11434:"
if curl -s http://localhost:11434/ > /dev/null; then
    echo "✅ Cổng 11434 phản hồi thành công: $(curl -s http://localhost:11434/)"
else
    echo "❌ Không thể kết nối tới http://localhost:11434"
    exit 1
fi

echo -e "\n4. [Model Registry] Danh sách mô hình hiện có trong Ollama:"
curl -s http://localhost:11434/api/tags | python3 -c "
import sys, json
try:
    data = json.load(sys.stdin)
    models = [m['name'] for m in data.get('models', [])]
    print('   Các models đã cài đặt:', models)
    if 'llama3.1:8b' in models and 'qwen2.5-coder:14b' in models:
        print('   ✅ ĐỦ 2 MÔ HÌNH YÊU CẦU CHO SCHR-BENCH!')
    else:
        print('   ⚠️ Lưu ý: Cần kiểm tra lại llama3.1:8b và qwen2.5-coder:14b.')
except Exception as e:
    print('   Lỗi đọc JSON:', e)
"

echo -e "\n=========================================================="
echo "✅ TIER 1 SẴN SÀNG PHỤC VỤ SUY LUẬN CHO TIER 2 VÀ TIER 3!"
echo "=========================================================="
