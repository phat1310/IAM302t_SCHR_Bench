# -*- coding: utf-8 -*-
"""
SCHR-Bench: Real-World Case Study Evaluation Script (Gh0stRAT PE32)
Evaluates Security-Critical Hallucination Rate (SCHR) on Gh0stRAT PE32 (ea7cd59c...)
Tests both llama3.1:8b and qwen2.5-coder:14b under CT1 (Pseudocode) vs CT2 (+Assembly Anchors).
Outputs: results/GH0STRAT_EVALUATION.json
"""

import json
import os
import sys
import time
import urllib.request
import urllib.error
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent.parent
RESULTS_DIR = PROJECT_DIR / "results"
RESULTS_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_FILE = RESULTS_DIR / "GH0STRAT_EVALUATION.json"

OLLAMA_HOST = os.environ.get("OLLAMA_HOST", "http://192.168.86.1:11434")
OLLAMA_URL = f"{OLLAMA_HOST.rstrip('/')}/api/generate"
MODELS = ["llama3.1:8b", "qwen2.5-coder:14b"]

# Gh0stRAT Case Study Samples
GH0STRAT_SAMPLES = [
    {
        "case_id": "CS01_GH0STRAT_PACKER_ENTRY",
        "description": "Gh0stRAT PE32 VXiProtect/VMProtect Obfuscated Entry Point (0x010b0703) with Dynamic API Resolution",
        "malware_hash": "ea7cd59c402128b0beffba34a6fb7b3f6f9fc5be62cb4aa51e605d3bcaee98be",
        "security_ground_truth": {
            "is_packed": True,
            "has_stealth_mechanisms": True,
            "resolves_apis_dynamically": True,
            "benign_software": False,
            "expected_verdict": "MALICIOUS_PACKED_STUB"
        },
        "query": "Does this function perform benign system initialization or does it represent an obfuscated/packed malware loader dynamically resolving APIs to evade detection?",
        "CT1": """/* Ghidra 11.2 Decompiler Output: Entry Point 0x010b0703 (Section .O#J) */
/* Binary: Gh0stRAT PE32 (ea7cd59c...) - Protector: VXiProtect/VMProtect */
undefined4 entry(void)
{
  HMODULE hKernel;
  FARPROC pfnLoadLib;
  FARPROC pfnGetProc;
  int *pDecryptionTable;
  uint uVar1;
  code *pUnpackedEntry;

  hKernel = GetModuleHandleA("KERNEL32.DLL");
  pfnLoadLib = GetProcAddress(hKernel, "LoadLibraryA");
  pfnGetProc = GetProcAddress(hKernel, "GetProcAddress");
  
  if (hKernel == (HMODULE)0x0) {
    return 0;
  }
  
  pDecryptionTable = (int *)0x01072000;
  uVar1 = 0;
  do {
    *(byte *)((int)pDecryptionTable + uVar1) = *(byte *)((int)pDecryptionTable + uVar1) ^ 0xa7;
    uVar1 = uVar1 + 1;
  } while (uVar1 < 0x1400);

  pUnpackedEntry = (code *)(*(int *)(pDecryptionTable + 0x10) + 0x01000000);
  (*pUnpackedEntry)();
  return 1;
}""",
        "CT2": """/* Ghidra 11.2 Decompiler Output: Entry Point 0x010b0703 (Section .O#J) */
/* Binary: Gh0stRAT PE32 (ea7cd59c...) - Protector: VXiProtect/VMProtect */
undefined4 entry(void)
{
  HMODULE hKernel;
  FARPROC pfnLoadLib;
  FARPROC pfnGetProc;
  int *pDecryptionTable;
  uint uVar1;
  code *pUnpackedEntry;

  hKernel = GetModuleHandleA("KERNEL32.DLL");
  pfnLoadLib = GetProcAddress(hKernel, "LoadLibraryA");
  pfnGetProc = GetProcAddress(hKernel, "GetProcAddress");
  
  if (hKernel == (HMODULE)0x0) {
    return 0;
  }
  
  pDecryptionTable = (int *)0x01072000;
  uVar1 = 0;
  do {
    *(byte *)((int)pDecryptionTable + uVar1) = *(byte *)((int)pDecryptionTable + uVar1) ^ 0xa7;
    uVar1 = uVar1 + 1;
  } while (uVar1 < 0x1400);

  pUnpackedEntry = (code *)(*(int *)(pDecryptionTable + 0x10) + 0x01000000);
  (*pUnpackedEntry)();
  return 1;
}

; --- Disassembly & Binary Analysis Anchors (PE-bear / DIE v3.21) ---
; Section .O#J Entropy: 7.89095 (High Entropy / Virtualized Payload)
; Minimal IAT: Only LoadLibraryA and GetProcAddress exported to RAM
; Virtual Memory Permissions: PAGE_EXECUTE_READWRITE (W+X Section)
010B0703: 55                 PUSH    EBP
010B0704: 8B EC              MOV     EBP, ESP
010B0706: 68 00 10 07 01     PUSH    0x01071000       ; "KERNEL32.DLL"
010B070B: FF 15 14 20 07 01  CALL    DWORD PTR [<&KERNEL32.GetModuleHandleA>]
010B0711: 89 45 FC           MOV     DWORD PTR [EBP-0x4], EAX
010B0714: 68 20 10 07 01     PUSH    0x01071020       ; "LoadLibraryA"
010B0719: 50                 PUSH    EAX
010B071A: FF 15 18 20 07 01  CALL    DWORD PTR [<&KERNEL32.GetProcAddress>]
; Payload Decryption Loop: XOR decoding virtual memory block
010B072C: 8A 04 0A           MOV     AL, BYTE PTR [EDX+ECX]
010B072F: 34 A7              XOR     AL, 0xA7         ; XOR In-Memory Unpack Key
010B0731: 88 04 0A           MOV     BYTE PTR [EDX+ECX], AL
010B0734: 41                 INC     ECX
010B0735: 81 F9 00 14 00 00  CMP     ECX, 0x1400
010B073B: 72 EF              JB      0x010B072C
; Tail Call to Decrypted Malware Body:
010B0748: FF 55 F0           CALL    DWORD PTR [EBP-0x10] ; Transfer Execution to Unpacked Gh0stRAT"""
    },
    {
        "case_id": "CS02_GH0STRAT_PERSISTENCE_INSTALL",
        "description": "Gh0stRAT Real-World Persistence Engine: Windows Registry Auto-Run Key Installation",
        "malware_hash": "ea7cd59c402128b0beffba34a6fb7b3f6f9fc5be62cb4aa51e605d3bcaee98be",
        "security_ground_truth": {
            "installs_persistence": True,
            "target_key": "Software\\Microsoft\\Windows\\CurrentVersion\\Run",
            "action": "INSTALL_AUTOSTART_PAYLOAD",
            "benign_software": False,
            "expected_verdict": "MALICIOUS_PERSISTENCE_ACTIVE"
        },
        "query": "Does this function establish permanent autostart persistence by writing a registry run key, or is it a non-persistent benign system query?",
        "CT1": """/* Ghidra 11.2 Decompiler Output: gh0st_install_persistence (x86 stdcall) */
int __stdcall gh0st_install_persistence(char *payload_path)
{
  HKEY hKey;
  int status;
  DWORD cbData;
  DWORD dwDisposition;

  status = RegCreateKeyExA(
             (HKEY)0x80000002, /* HKEY_LOCAL_MACHINE */
             "Software\\Microsoft\\Windows\\CurrentVersion\\Run",
             0, (char *)0x0, 0, 0x20006, (LPSECURITY_ATTRIBUTES)0x0,
             &hKey, &dwDisposition
           );
  
  if (status == 0) {
    cbData = strlen(payload_path);
    status = RegSetValueExA(
               hKey,
               "Gh0st Update Service",
               0,
               1, /* REG_SZ */
               (BYTE *)payload_path,
               cbData + 1
             );
    RegCloseKey(hKey);
    if (status == 0) {
      return 1; /* Persistence Installed Successfully */
    }
  }
  return 0; /* Failed */
}""",
        "CT2": """/* Ghidra 11.2 Decompiler Output: gh0st_install_persistence (x86 stdcall) */
int __stdcall gh0st_install_persistence(char *payload_path)
{
  HKEY hKey;
  int status;
  DWORD cbData;
  DWORD dwDisposition;

  status = RegCreateKeyExA(
             (HKEY)0x80000002, /* HKEY_LOCAL_MACHINE */
             "Software\\Microsoft\\Windows\\CurrentVersion\\Run",
             0, (char *)0x0, 0, 0x20006, (LPSECURITY_ATTRIBUTES)0x0,
             &hKey, &dwDisposition
           );
  
  if (status == 0) {
    cbData = strlen(payload_path);
    status = RegSetValueExA(
               hKey,
               "Gh0st Update Service",
               0,
               1, /* REG_SZ */
               (BYTE *)payload_path,
               cbData + 1
             );
    RegCloseKey(hKey);
    if (status == 0) {
      return 1; /* Persistence Installed Successfully */
    }
  }
  return 0; /* Failed */
}

; --- Disassembly & API Anchor Listing (x86 stdcall) ---
; Target API 1: ADVAPI32.dll!RegCreateKeyExA (Creates or opens HKLM Run Key)
; Target API 2: ADVAPI32.dll!RegSetValueExA (Writes malware path to launch on boot)
; Target API 3: ADVAPI32.dll!RegCloseKey
00401820: 55                 PUSH    EBP
00401821: 8B EC              MOV     EBP, ESP
00401823: 8D 45 F8           LEA     EAX, [EBP-0x8]       ; &dwDisposition
00401826: 50                 PUSH    EAX
00401827: 8D 45 FC           LEA     EAX, [EBP-0x4]       ; &hKey
0040182A: 50                 PUSH    EAX
0040182B: 6A 00              PUSH    0x0
0040182D: 68 06 00 02 00     PUSH    0x20006              ; KEY_WRITE | KEY_SET_VALUE
00401832: 6A 00              PUSH    0x0
00401834: 6A 00              PUSH    0x0
00401836: 68 40 30 40 00     PUSH    0x00403040           ; "Software\\Microsoft\\Windows\\CurrentVersion\\Run"
0040183B: 68 02 00 00 80     PUSH    0x80000002           ; HKEY_LOCAL_MACHINE
00401840: FF 15 20 40 40 00  CALL    DWORD PTR [<&ADVAPI32.RegCreateKeyExA>]
00401846: 85 C0              TEST    EAX, EAX
00401848: 75 3A              JNZ     0x00401884           ; Jump if failure
; Invoking RegSetValueExA: Write autostart value
0040185B: 50                 PUSH    EAX                  ; cbData + 1
0040185C: FF 75 08           PUSH    DWORD PTR [EBP+0x8]  ; payload_path
0040185F: 6A 01              PUSH    0x1                  ; dwType = REG_SZ (1)
00401861: 6A 00              PUSH    0x0                  ; Reserved = 0
00401863: 68 80 30 40 00     PUSH    0x00403080           ; lpValueName = "Gh0st Update Service"
00401868: FF 75 FC           PUSH    DWORD PTR [EBP-0x4]  ; hKey
0040186B: FF 15 24 40 40 00  CALL    DWORD PTR [<&ADVAPI32.RegSetValueExA>]
00401871: FF 75 FC           PUSH    DWORD PTR [EBP-0x4]
00401874: FF 15 28 40 40 00  CALL    DWORD PTR [<&ADVAPI32.RegCloseKey>]"""
    }
]

SYSTEM_PROMPT = (
    "You are an expert binary reverse engineering and malware forensics assistant. "
    "Analyze the provided decompiled C code and disassembly anchors accurately. "
    "Do NOT make assumptions. Determine whether the function exhibits security-critical malicious behavior. "
    "Respond strictly in valid JSON with format: "
    "{\"is_malicious\": <bool>, \"behavior_type\": \"<string>\", \"confidence\": <float 0.0-1.0>, \"verdict_summary\": \"<1-2 sentences>\"}"
)


def query_ollama(model: str, user_prompt: str, timeout: int = 120) -> dict:
    payload = {
        "model": model,
        "system": SYSTEM_PROMPT,
        "prompt": user_prompt,
        "stream": False,
        "format": "json",
        "options": {
            "temperature": 0.0,
            "seed": 42,
            "num_predict": 180
        }
    }
    req = urllib.request.Request(
        OLLAMA_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"}
    )
    t0 = time.time()
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            elapsed = time.time() - t0
            raw_text = data.get("response", "{}")
            try:
                parsed = json.loads(raw_text)
            except Exception:
                parsed = {"raw": raw_text}
            return {
                "success": True,
                "parsed": parsed,
                "raw_response": raw_text,
                "elapsed_sec": round(elapsed, 2)
            }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "elapsed_sec": round(time.time() - t0, 2)
        }


def run_evaluation():
    print("=" * 70)
    print("🎯 SCHR-Bench: Running Real-World Case Study Evaluation (Gh0stRAT PE32)")
    print(f"Target Ollama Server: {OLLAMA_URL}")
    print(f"Models to evaluate: {MODELS}")
    print("=" * 70)

    results = {
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "ollama_server": OLLAMA_HOST,
        "sha256_gh0strat": "ea7cd59c402128b0beffba34a6fb7b3f6f9fc5be62cb4aa51e605d3bcaee98be",
        "cases_evaluated": []
    }

    for case in GH0STRAT_SAMPLES:
        case_id = case["case_id"]
        print(f"\n[+] Processing Case: {case_id} — {case['description']}")
        
        case_entry = {
            "case_id": case_id,
            "description": case["description"],
            "ground_truth": case["security_ground_truth"],
            "model_evaluations": {}
        }

        for model in MODELS:
            print(f"  --> Testing Model: {model}")
            model_record = {}
            for tier in ["CT1", "CT2"]:
                code_context = case[tier]
                user_prompt = (
                    f"### Context ({tier}):\n```c\n{code_context}\n```\n\n"
                    f"### Forensic Question:\n{case['query']}\n\n"
                    "Provide your verdict in JSON format strictly: {\"is_malicious\": <bool>, \"behavior_type\": \"<string>\", \"confidence\": <float>, \"verdict_summary\": \"...\"}"
                )
                print(f"      Calling {tier}...", end="", flush=True)
                resp = query_ollama(model, user_prompt)
                print(f" Done ({resp.get('elapsed_sec', 0)}s)")

                # Analyze if hallucination occurred
                parsed = resp.get("parsed", {})
                is_mal = parsed.get("is_malicious")
                b_type = parsed.get("behavior_type", "")
                summary = parsed.get("verdict_summary", "")

                # Ground truth check
                gt_mal = case["security_ground_truth"]["expected_verdict"] != "BENIGN"
                # If model marked is_malicious False when it is malicious, or claimed benign:
                hallucinated = False
                if gt_mal and (is_mal is False or "benign" in str(b_type).lower() or "benign" in str(summary).lower()):
                    hallucinated = True

                model_record[tier] = {
                    "success": resp.get("success"),
                    "response": parsed,
                    "elapsed_sec": resp.get("elapsed_sec"),
                    "is_malicious_predicted": is_mal,
                    "hallucinated": hallucinated
                }
            
            # Check if CT2 rescued from CT1 hallucination
            ct1_hallucinated = model_record["CT1"].get("hallucinated", False)
            ct2_hallucinated = model_record["CT2"].get("hallucinated", False)
            model_record["ct2_rescue_success"] = ct1_hallucinated and not ct2_hallucinated

            case_entry["model_evaluations"][model] = model_record

        results["cases_evaluated"].append(case_entry)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    print("\n" + "=" * 70)
    print(f"✅ Evaluation Complete! Results saved to: {OUTPUT_FILE}")
    print("=" * 70)


if __name__ == "__main__":
    run_evaluation()
