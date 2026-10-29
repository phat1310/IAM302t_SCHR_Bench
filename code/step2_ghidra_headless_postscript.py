# -*- coding: utf-8 -*-
# ==============================================================================
# SCHR-Bench: Ghidra Headless Post-Script (Jython / PyGhidra compatible)
# Usage with Ghidra analyzeHeadless:
#   analyzeHeadless /tmp/ghidra_proj SCHRProj -import build/pe_x64_O0/*.exe \
#       -postScript step2_ghidra_headless_postscript.py -deleteProject
# ==============================================================================

import json
import os

try:
    from ghidra.app.decompiler import DecompInterface
    from ghidra.util.task import ConsoleTaskMonitor
    IN_GHIDRA = True
except ImportError:
    IN_GHIDRA = False


def extract_from_ghidra():
    program = currentProgram
    prog_name = program.getName()
    monitor = ConsoleTaskMonitor()

    decomp = DecompInterface()
    decomp.openProgram(program)

    fm = program.getFunctionManager()
    listing = program.getListing()

    target_func = None
    for func in fm.getFunctions(True):
        fname = func.getName()
        if fname in ("target", "_target") or "FUN_00401" in fname or "FUN_140001" in fname:
            if func.getBody().getNumAddresses() > 5 and fname not in ("main", "_main"):
                target_func = func
                if fname in ("target", "_target"):
                    break

    if target_func is None:
        print("[!] Target function not found in:", prog_name)
        return

    # 1. Extract CT1: Ghidra Decompiled Pseudocode
    res = decomp.decompileFunction(target_func, 30, monitor)
    pseudocode = res.getDecompiledFunction().getC() if res and res.decompileCompleted() else ""

    # Mask function name to prevent any leakage
    masked_pseudo = pseudocode.replace("target(", "FUN_00401120(")

    # 2. Extract CT2: Raw Assembly Instructions
    asm_lines = []
    addr_set = target_func.getBody()
    code_units = listing.getInstructions(addr_set, True)
    while code_units.hasNext():
        ins = code_units.next()
        asm_lines.append("  {}:  {}".format(ins.getAddress(), ins.toString()))

    # 3. Extract CT3: Callees / Referenced Functions
    called_funcs = []
    for callee in target_func.getCalledFunctions(monitor):
        called_funcs.append({
            "name": callee.getName(),
            "signature": callee.getPrototypeString(False, False)
        })

    out_dir = os.environ.get("SCHR_OUT_DIR", ".")
    out_file = os.path.join(out_dir, "{}_ghidra.json".format(prog_name))
    payload = {
        "binary": prog_name,
        "entry_address": str(target_func.getEntryPoint()),
        "ct1_pseudocode": masked_pseudo,
        "ct2_assembly": "\n".join(asm_lines),
        "ct3_callees": called_funcs
    }
    with open(out_file, "w") as f:
        json.dump(payload, f, indent=2)
    print("[+] Extracted Ghidra CT1-CT3 for:", prog_name)


if IN_GHIDRA:
    extract_from_ghidra()
