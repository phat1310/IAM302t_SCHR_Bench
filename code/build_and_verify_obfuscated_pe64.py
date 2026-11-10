#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build_and_verify_obfuscated_pe64.py
Compiles all 30 obfuscated pilot C variants (5 pairs: A01, S01, P01, E01, C01 x 2 variants x 3 modes:
Obf1_CFF, Obf2_Sub, Obf3_Combined) into stripped 64-bit Windows PE executables (.exe),
verifies 100% dynamic behavioral preservation across 60 execution assertions (Vector 1 & Vector 2),
and extracts real `objdump -d -M intel` disassembly into `disassembly_obfuscated_30.json`.
"""

import json
import os
import re
import shutil
import subprocess
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_DIR = SCRIPT_DIR.parent
DATASET_DIR = PROJECT_DIR / "dataset" / "SCHR_Bench_C_Functions"
SRC_DIR = DATASET_DIR / "src"
SRC_OBF_DIR = DATASET_DIR / "src_obf"
BIN_OBF_DIR = DATASET_DIR / "bin" / "pe_x64_obf"
RUNNER_C = DATASET_DIR / "tools" / "runner.c"
MANIFEST_PATH = DATASET_DIR / "ground_truth_manifest.json"
DISASM_OUT_PATH = DATASET_DIR / "disassembly_obfuscated_30.json"

PILOT_IDS = ["A01", "S01", "P01", "E01", "C01"]
OBF_MODES = ["Obf1_CFF", "Obf2_Sub", "Obf3_Combined"]


def find_c_compiler():
    candidates = [
        os.environ.get("CC", ""),
        "x86_64-w64-mingw32-gcc",
        "gcc",
        r"C:\Program Files\CodeBlocks\MinGW\bin\x86_64-w64-mingw32-gcc.exe",
        r"C:\Program Files\CodeBlocks\MinGW\bin\gcc.exe",
        r"C:\msys64\mingw64\bin\x86_64-w64-mingw32-gcc.exe",
        r"C:\msys64\ucrt64\bin\gcc.exe",
    ]
    for c in candidates:
        if not c:
            continue
        resolved = shutil.which(c) or (c if Path(c).exists() else None)
        if resolved:
            return str(resolved)
    return None


def find_objdump():
    candidates = [
        "x86_64-w64-mingw32-objdump",
        "objdump",
        r"C:\Program Files\CodeBlocks\MinGW\bin\objdump.exe",
        r"C:\Program Files\CodeBlocks\MinGW\bin\x86_64-w64-mingw32-objdump.exe",
        r"C:\msys64\mingw64\bin\objdump.exe",
    ]
    for c in candidates:
        resolved = shutil.which(c) or (c if Path(c).exists() else None)
        if resolved:
            return str(resolved)
    return None


def generate_obfuscated_c_source(orig_c_text: str, mode: str) -> str:
    """
    Transforms a standard SCHR-Bench C file into a compilable C source file
    implementing Obf1_CFF, Obf2_Sub, or Obf3_Combined with volatile dispatchers
    so the compiler preserves the structural transformation in the PE64 binary.
    """
    lines = orig_c_text.splitlines()
    header_and_helpers = []
    target_line = ""
    for line in lines:
        if "KEEP int target" in line:
            target_line = line.strip()
        else:
            header_and_helpers.append(line)

    m = re.search(r"target\s*\([^)]*\)\s*\{\s*(.*)\s*\}", target_line)
    raw_body = m.group(1) if m else target_line

    if mode == "Obf1_CFF":
        new_target = (
            "KEEP int target(int a, int b, int c) {\n"
            "    volatile int _cff_state = 0x37a1;\n"
            "    while (_cff_state != 0) {\n"
            "        if (_cff_state == 0x37a1) {\n"
            "            _cff_state = 0x59b2;\n"
            "        } else if (_cff_state == 0x59b2) {\n"
            f"            {raw_body}\n"
            "        }\n"
            "    }\n"
            "    return 0;\n"
            "}\n"
        )
    elif mode == "Obf2_Sub":
        body_mba = raw_body.replace("!= 0", "^ 0x0 != ((b & ~b))")
        body_mba = body_mba.replace("== 0", "== ((c ^ c) & 0xff)")
        new_target = (
            "KEEP int target(int a, int b, int c) {\n"
            "    volatile int _mba_mask = (b & ~b);\n"
            "    (void)_mba_mask;\n"
            f"    {body_mba}\n"
            "}\n"
        )
    elif mode == "Obf3_Combined":
        body_mba = raw_body.replace("!= 0", "^ 0x0 != ((b & ~b))")
        new_target = (
            "KEEP int target(int a, int b, int c) {\n"
            "    volatile unsigned int _dispatch = (((unsigned int)a * ((unsigned int)a + 1U)) & 1U) ^ 0x7f01U;\n"
            "    while (_dispatch != 0U) {\n"
            "        if (_dispatch == 0x7f01U) {\n"
            f"            {body_mba}\n"
            "        }\n"
            "        _dispatch = 0U;\n"
            "    }\n"
            "    return 0;\n"
            "}\n"
        )
    else:
        raise ValueError(f"Unknown obfuscation mode: {mode}")

    return "\n".join(header_and_helpers) + "\n" + new_target


def extract_target_objdump(objdump_bin: str, exe_path: Path) -> str:
    proc = subprocess.run(
        [objdump_bin, "-d", "-M", "intel", str(exe_path)],
        capture_output=True,
        text=True,
        check=True,
    )
    out = proc.stdout
    lines = out.splitlines()
    keep = []
    in_text = False
    for line in lines:
        if "section .text:" in line:
            in_text = True
            continue
        if in_text:
            if line.strip().startswith("Disassembly of section"):
                break
            if re.match(r"^\s*[0-9a-fA-F]+:\s+", line):
                keep.append(line)
                if len(keep) >= 35:
                    break
    return "\n".join(keep)


def main():
    cc = find_c_compiler()
    objdump = find_objdump()
    if not cc:
        raise SystemExit("ERROR: No C compiler found.")

    SRC_OBF_DIR.mkdir(parents=True, exist_ok=True)
    BIN_OBF_DIR.mkdir(parents=True, exist_ok=True)

    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    pilot_entries = [item for item in manifest if item["id"] in PILOT_IDS]

    total_built = 0
    total_assertions = 0
    passed_assertions = 0
    disasm_records = {}

    for entry in pilot_entries:
        sid = entry["id"]
        for variant in ("original", "mutant"):
            orig_src_path = SRC_DIR / f"{sid}_{variant}.c"
            orig_c_text = orig_src_path.read_text(encoding="utf-8")

            for mode in OBF_MODES:
                obf_key = f"{sid}_{variant}_{mode}"
                obf_c_path = SRC_OBF_DIR / f"{obf_key}.c"
                obf_exe_path = BIN_OBF_DIR / f"{obf_key}.exe"

                obf_c_code = generate_obfuscated_c_source(orig_c_text, mode)
                obf_c_path.write_text(obf_c_code, encoding="utf-8")

                subprocess.run(
                    [
                        cc,
                        "-std=c11",
                        "-O2",
                        "-fno-inline",
                        "-fno-lto",
                        "-fno-omit-frame-pointer",
                        "-s",
                        str(obf_c_path),
                        str(RUNNER_C),
                        "-o",
                        str(obf_exe_path),
                    ],
                    check=True,
                )
                total_built += 1

                for t in entry["tests"]:
                    args = [str(t["a"]), str(t["b"]), str(t["c"])]
                    expected = int(t[variant])
                    run_proc = subprocess.run(
                        [str(obf_exe_path), *args],
                        capture_output=True,
                        text=True,
                        check=True,
                    )
                    actual = int(run_proc.stdout.strip())
                    total_assertions += 1
                    if actual == expected:
                        passed_assertions += 1
                    else:
                        raise AssertionError(
                            f"MISMATCH on {obf_key} input {args}: expected {expected}, got {actual}"
                        )

                if objdump:
                    disasm_records[obf_key] = {
                        "pair_id": sid,
                        "variant": variant,
                        "obf_mode": mode,
                        "binary_path": f"dataset/SCHR_Bench_C_Functions/bin/pe_x64_obf/{obf_key}.exe",
                        "objdump_intel": extract_target_objdump(objdump, obf_exe_path),
                    }

    if disasm_records:
        DISASM_OUT_PATH.write_text(
            json.dumps(disasm_records, indent=2, ensure_ascii=False), encoding="utf-8"
        )

    print("==============================================================================")
    print("  SCHR-Bench: Obfuscated PE64 Build & Dynamic Execution Verification (E4)")
    print("==============================================================================")
    print(f"Compiler Used: {cc}")
    print(f"Pilot Pairs: {len(pilot_entries)} | Obfuscated PE64 Binaries Built: {total_built}")
    print(f"Dynamic Execution Assertions Verified: {passed_assertions}/{total_assertions} (100.0% PASS)")
    print(f"Disassembly Records Saved: {len(disasm_records)} -> {DISASM_OUT_PATH.name}")
    print("==============================================================================")


if __name__ == "__main__":
    main()
