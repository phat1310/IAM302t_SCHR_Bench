#!/usr/bin/env python3
"""
Script: test_inference_lan.py
Purpose: Kiểm tra tốc độ và khả năng suy luận trực tiếp của 2 mô hình LLM trên Ollama Host
Role: Tier 1 (Host MSI - WSL2)
"""

import urllib.request
import json
import time

OLLAMA_URL = "http://localhost:11434/api/generate"
MODELS = ["llama3.1:8b", "qwen2.5-coder:14b"]
TEST_PROMPT = "Explain in one short sentence what 'IsDebuggerPresent' API does in Windows."

def test_model(model_name):
    print(f"\n[*] Đang kiểm thử suy luận với model: [{model_name}]...")
    payload = {
        "model": model_name,
        "prompt": TEST_PROMPT,
        "stream": False,
        "options": {
            "temperature": 0.0,
            "seed": 42
        }
    }
    
    start_time = time.time()
    req = urllib.request.Request(
        OLLAMA_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"}
    )
    
    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            res_data = json.loads(response.read().decode("utf-8"))
            elapsed = time.time() - start_time
            reply = res_data.get("response", "").strip()
            total_duration_sec = res_data.get("total_duration", 0) / 1e9
            eval_count = res_data.get("eval_count", 0)
            eval_duration_sec = res_data.get("eval_duration", 1) / 1e9
            tok_per_sec = eval_count / eval_duration_sec if eval_duration_sec > 0 else 0
            
            print(f"   [+] Thời gian phản hồi: {elapsed:.2f}s (Inference: {eval_duration_sec:.2f}s)")
            print(f"   [+] Tốc độ suy luận: {tok_per_sec:.2f} tokens/s (Số tokens: {eval_count})")
            print(f"   [+] Phản hồi: {reply}")
            print(f"   [PASS] Model [{model_name}] HOẠT ĐỘNG HOÀN HẢO!")
    except Exception as e:
        print(f"   [FAIL] Lỗi kết nối tới [{model_name}]: {e}")

if __name__ == "__main__":
    print("==========================================================")
    print(" BẮT ĐẦU KIỂM TRA INFERENCE CỦA CÁC MÔ HÌNH TẠI TIER 1")
    print("==========================================================")
    for m in MODELS:
        test_model(m)
    print("\n==========================================================")
    print(" KIỂM TRA HOÀN TẤT!")
