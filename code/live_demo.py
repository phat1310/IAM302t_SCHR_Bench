#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SCHR-Bench: Live Demonstration Script (Milestone D3)
Demonstrates the Security-Critical Hallucination (SCHR) evaluation and Context Escalation
across normalized stripped representations and register-mapped listings.
"""

import argparse
import json
import subprocess
import sys
import time
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_DIR = SCRIPT_DIR.parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from step3_mcp_server_and_benchmark import (
    SCHRBenchMCPServer,
    query_ollama,
    check_ollama_online,
    FIXED_SYSTEM_PROMPT,
    CONTEXTS_FILE,
    DEFAULT_HOST,
)

C_CYAN = "\033[96m"
C_GREEN = "\033[92m"
C_YELLOW = "\033[93m"
C_RED = "\033[91m"
C_BOLD = "\033[1m"
C_RESET = "\033[0m"


def print_banner():
    banner = f"""{C_CYAN}{C_BOLD}
================================================================================
 SCHR-BENCH: LIVE DEMONSTRATION OF CONTEXT ESCALATION (MILESTONE D3)
 Course: IAM302t - Malware Analysis & Reverse Engineering (RBL Model)
 Team: Group 7 (IA2007) - FPT University HCMC
 Target Venue: EAI INISCOM 2027 (Springer LNICST Series)
================================================================================{C_RESET}
"""
    print(banner)


def pause_prompt(interactive: bool, message: str = "Press [Enter] to continue..."):
    if interactive:
        try:
            input(f"\n{C_YELLOW}{C_BOLD}>> {message}{C_RESET}")
        except (KeyboardInterrupt, EOFError):
            print("\nExiting demo.")
            sys.exit(0)
    else:
        print(f"\n{C_YELLOW}--- [Auto-Advancing] ---{C_RESET}")
        time.sleep(0.5)


def step1_sanity_check(auto: bool):
    print(f"\n{C_BOLD}[BƯỚC 1/4] Kiểm Định Ground Truth E0 Sanity Check Protocol{C_RESET}")
    print("Mục đích: Xác thực các cặp hàm C (Original vs Mutant) bằng kịch bản kiểm định E0 thực tế.")

    e0_script = SCRIPT_DIR / "step0_verify_e0_windows.py"
    if not e0_script.exists():
        print(f"  {C_RED}[ERROR] Không tìm thấy {e0_script}. Dừng thực thi.{C_RESET}")
        sys.exit(1)

    proc = subprocess.run([sys.executable, "-X", "utf8", str(e0_script)], capture_output=True, text=True)
    if proc.returncode != 0:
        print(f"  {C_RED}[FAIL] E0 verification failed:\n{proc.stdout}\n{proc.stderr}{C_RESET}")
        sys.exit(1)

    for line in proc.stdout.strip().splitlines()[-6:]:
        print(f"  {C_GREEN}{line}{C_RESET}")

    pause_prompt(not auto, "Nhấn [Enter] để chuyển sang Bước 2: Đánh Giá Tầng Ngữ Cảnh CT1...")


def step2_ct1_hallucination(mcp: SCHRBenchMCPServer, model: str, sample_key: str, host: str, auto: bool):
    print(f"\n{C_BOLD}[BƯỚC 2/4] Tầng Ngữ Cảnh CT1 (Stripped Pseudocode Baseline){C_RESET}")
    rec = mcp.records[sample_key]
    test = rec["tests"][0]
    truth = int(test[rec["variant"]])

    print(f"  • Mẫu thử nghiệm: {C_BOLD}{sample_key}{C_RESET} (Category: {rec['category']})")
    print(f"  • Ground Truth: Return Value = {C_BOLD}{truth}{C_RESET}")
    print(f"  • Discriminating Vector 1: param_1={test['a']}, param_2={test['b']}, param_3={test['c']}")
    print(f"\n{C_CYAN}--- [Stripped Pseudocode Representation (CT1)] ---{C_RESET}")
    ctx_ct1 = mcp.mcp_get_function_context(sample_key, tier="CT1")
    for l in ctx_ct1.strip().splitlines()[:10]:
        print(f"  | {l}")

    print(f"\n[+] Đang gửi truy vấn CT1 tới mô hình {C_BOLD}{model}{C_RESET} trên máy chủ Ollama...")
    prompt_ct1 = mcp.build_user_prompt(sample_key, test_idx=0, tier="CT1")
    res1 = query_ollama(model, FIXED_SYSTEM_PROMPT, prompt_ct1, ollama_url=f"{host.rstrip('/')}/api/generate")

    pred = res1["predicted_return"]
    print(f"\n  • Dự đoán của LLM (Predicted Return): {C_BOLD}{pred}{C_RESET} (Latency: {res1['latency_sec']}s)")
    print(f"  • Diễn giải của LLM: \"{res1['explanation']}\"")

    if pred != truth:
        print(f"\n  {C_RED}{C_BOLD}[SCHR ERROR] Mô hình dự đoán sai ở CT1 (Predicted={pred} vs Truth={truth}).{C_RESET}")
    else:
        print(f"\n  {C_GREEN}[PASS] Mô hình trả lời đúng ở CT1: {pred}{C_RESET}")

    pause_prompt(not auto, "Nhấn [Enter] để chuyển sang Bước 3: Đánh Giá Tầng Ngữ Cảnh CT2...")


def step3_ct2_rescue(mcp: SCHRBenchMCPServer, model: str, sample_key: str, host: str, auto: bool):
    print(f"\n{C_BOLD}[BƯỚC 3/4] Tầng Ngữ Cảnh CT2 (Context Escalation + Register-Mapped Listing){C_RESET}")
    rec = mcp.records[sample_key]
    test = rec["tests"][0]
    truth = int(test[rec["variant"]])

    print(f"  • Mẫu thử nghiệm: {C_BOLD}{sample_key}{C_RESET}")
    ctx_ct2 = mcp.mcp_get_function_context(sample_key, tier="CT2")
    for l in ctx_ct2.strip().splitlines()[-8:]:
        print(f"  | {l}")

    print(f"\n[+] Đang gửi truy vấn CT2 tới mô hình {C_BOLD}{model}{C_RESET} trên máy chủ Ollama...")
    prompt_ct2 = mcp.build_user_prompt(sample_key, test_idx=0, tier="CT2")
    res2 = query_ollama(model, FIXED_SYSTEM_PROMPT, prompt_ct2, ollama_url=f"{host.rstrip('/')}/api/generate")

    pred = res2["predicted_return"]
    print(f"\n  • Dự đoán của LLM (Predicted Return): {C_BOLD}{pred}{C_RESET} (Latency: {res2['latency_sec']}s)")
    print(f"  • Diễn giải của LLM: \"{res2['explanation']}\"")

    if pred == truth:
        print(f"\n  {C_GREEN}{C_BOLD}[PASS] Mô hình dự đoán đúng ở CT2 (Predicted={pred} == Truth={truth}).{C_RESET}")
    else:
        print(f"\n  {C_RED}[SCHR ERROR] Mô hình dự đoán sai ở CT2 (Predicted={pred} vs Truth={truth}).{C_RESET}")

    pause_prompt(not auto, "Nhấn [Enter] để chuyển sang Bước 4: Xem Báo Cáo Thống Kê Tổng Thể...")


def step4_springer_summary():
    print(f"\n{C_BOLD}[BƯỚC 4/4] Tổng Hợp Thống Kê Thực Nghiệm Từ Log (N=80, 540 Runs){C_RESET}")
    report_file = PROJECT_DIR / "results" / "PAPER_TABLES_SPRINGER.md"
    if report_file.exists():
        content = report_file.read_text(encoding="utf-8")
        print(f"{C_CYAN}Trích xuất bảng kết quả thực nghiệm từ results/PAPER_TABLES_SPRINGER.md:{C_RESET}\n")
        for l in content.splitlines():
            if l.strip():
                print(f"  {l}")


def main():
    parser = argparse.ArgumentParser(description="SCHR-Bench Live Demonstration Script")
    parser.add_argument("--auto", action="store_true", help="Chạy tự động không chờ nhấn phím Enter")
    parser.add_argument("--model", default="llama3.1:8b", help="LLM model (default: llama3.1:8b)")
    parser.add_argument(
        "--sample",
        default="A01_original",
        help="Mẫu hàm demo (default: A01_original — cặp hàm đầu tiên theo thứ tự danh mục, hoặc chọn mẫu bất kỳ trong 80 mẫu)"
    )
    parser.add_argument("--host", default=DEFAULT_HOST, help="Ollama Host URL")
    args = parser.parse_args()

    print_banner()
    step1_sanity_check(args.auto)

    models = check_ollama_online(args.host)
    if not models:
        print(f"\n{C_YELLOW}[!] Lưu ý: Máy chủ Ollama tại {args.host} hiện đang offline. Chuyển thẳng sang hiển thị thống kê từ 540 log đã lưu (Bước 4).{C_RESET}")
        step4_springer_summary()
        return

    mcp = SCHRBenchMCPServer(CONTEXTS_FILE)
    step2_ct1_hallucination(mcp, args.model, args.sample, args.host, args.auto)
    step3_ct2_rescue(mcp, args.model, args.sample, args.host, args.auto)
    step4_springer_summary()


if __name__ == "__main__":
    main()
