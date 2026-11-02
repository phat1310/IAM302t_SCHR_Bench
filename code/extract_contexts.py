# -*- coding: utf-8 -*-
"""
SCHR-Bench: Step 1B / Step 2 — Extract & Generate Normalized Stripped Contexts (CT1-CT4)
and OLLVM-Style Structural Transformation Templates (Obf0 - Obf3) for all 80 variants (40 pairs).
Also attaches real `objdump -d -M intel` disassembly from `disassembly_objdump_80.json`
when available, so both source-derived templates and compiled PE64 disassembly are linked.
"""

import json
import re
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_DIR = SCRIPT_DIR.parent
DATASET_DIR = (
    PROJECT_DIR / "dataset" / "SCHR_Bench_C_Functions"
    if (PROJECT_DIR / "dataset" / "SCHR_Bench_C_Functions").exists()
    else PROJECT_DIR / "Dataset_SCHR_Bench" / "SCHR_Bench_C_Functions"
)
RESULTS_DIR = (
    PROJECT_DIR / "results"
    if (PROJECT_DIR / "results").exists()
    else PROJECT_DIR / "Results"
)
RESULTS_DIR.mkdir(parents=True, exist_ok=True)


def extract_c_body(c_path: Path):
    lines = c_path.read_text(encoding="utf-8").splitlines()
    helpers = []
    target_line = ""
    for line in lines:
        s = line.strip()
        if not s or s.startswith("/*") or s.startswith("#"):
            continue
        if "KEEP int target" in s:
            target_line = s
        else:
            helpers.append(s)
    return helpers, target_line


def to_ghidra_stripped_pseudocode(sid: str, variant: str, helpers: list, target_line: str, obf_level: int = 0) -> str:
    """
    Transform C source into a normalized Ghidra-style stripped pseudocode representation (CT1).
    - Strips function name `target` -> `FUN_140001140`
    - Strips parameter names `a, b, c` -> `param_1, param_2, param_3`
    - Strips static helper names (`mock_add` -> `FUN_140001100`, `mock_remove` -> `FUN_140001110`)
    """
    body_match = re.search(r"target\s*\([^)]*\)\s*\{\s*(.*)\s*\}", target_line)
    raw_body = body_match.group(1) if body_match else target_line
    raw_body = re.sub(r"\(void\)\s*[abc]\s*;", "", raw_body).strip()

    raw_body_stripped = raw_body.replace("mock_add", "FUN_140001100").replace("mock_remove", "FUN_140001110")

    def repl_param(m):
        tok = m.group(0)
        return {"a": "param_1", "b": "param_2", "c": "param_3"}.get(tok, tok)

    body_p = re.sub(r"\b[abc]\b", repl_param, raw_body_stripped)

    if obf_level == 0:
        return (
            "/* Normalized Stripped Decompiler Representation: FUN_140001140 (PE64) */\n"
            "ulong FUN_140001140(int param_1, int param_2, int param_3)\n"
            "{\n"
            "  int iVar1;\n"
            "  uint uVar2;\n\n"
            f"  {body_p}\n"
            "}"
        )
    elif obf_level == 1:
        return (
            "/* Structural Obfuscation Template Obf1_CFF: Control-Flow Flattening Dispatcher */\n"
            "ulong FUN_140001140(int param_1, int param_2, int param_3)\n"
            "{\n"
            "  int local_state = 0x37a1;\n"
            "  while (1) {\n"
            "    if (local_state == 0x37a1) { local_state = 0x59b2; }\n"
            "    else if (local_state == 0x59b2) {\n"
            f"      {body_p}\n"
            "      break;\n"
            "    }\n"
            "  }\n"
            "  return 0;\n"
            "}"
        )
    elif obf_level == 2:
        body_mba = body_p.replace("!= 0", "^ 0x0 != ((param_2 & ~param_2))")
        body_mba = body_mba.replace("== 0", "== ((param_3 ^ param_3) & 0xff)")
        return (
            "/* Structural Obfuscation Template Obf2_Sub: Mixed Boolean-Arithmetic Substitution */\n"
            "ulong FUN_140001140(int param_1, int param_2, int param_3)\n"
            "{\n"
            f"  {body_mba}\n"
            "}"
        )
    else:
        body_mba = body_p.replace("!= 0", "^ 0x0 != ((param_2 & ~param_2))")
        return (
            "/* Structural Obfuscation Template Obf3_Combined: CFF + MBA + Opaque Predicate */\n"
            "ulong FUN_140001140(int param_1, int param_2, int param_3)\n"
            "{\n"
            "  uint local_dispatch = ((param_1 * (param_1 + 1)) & 1) ^ 0x7f01;\n"
            "  while (local_dispatch != 0x0) {\n"
            "    if (local_dispatch == 0x7f01) {\n"
            f"      {body_mba}\n"
            "    }\n"
            "    local_dispatch = 0x0;\n"
            "  }\n"
            "  return 0;\n"
            "}"
        )


def format_hex_annotations(expr: str) -> str:
    """Extract all 0x... hex constants in expression and annotate their exact decimal values."""
    hexes = re.findall(r"0x[0-9a-fA-F]+", expr)
    if not hexes:
        return "none"
    notes = [f"{h} = {int(h, 16)} (decimal)" for h in sorted(set(hexes))]
    return ", ".join(notes)


def generate_x64_assembly(sid: str, variant: str, helpers: list, target_line: str) -> str:
    """
    Generate Register-Mapped x86-64 Pseudo-Assembly Context (CT2)
    under the Win64 fastcall convention (ECX=param_1, EDX=param_2, R8D=param_3).
    """
    body_match = re.search(r"target\s*\([^)]*\)\s*\{\s*(.*)\s*\}", target_line)
    raw_body = body_match.group(1) if body_match else target_line
    raw_body = re.sub(r"\(void\)\s*[abc]\s*;", "", raw_body).strip()

    def repl_reg(m):
        tok = m.group(0)
        return {"a": "ECX(param_1)", "b": "EDX(param_2)", "c": "R8D(param_3)"}.get(tok, tok)

    reg_body = re.sub(r"\b[abc]\b", repl_reg, raw_body)
    imm_notes = format_hex_annotations(raw_body)

    asm_lines = [
        "; --- Win64 Fastcall Register-Mapped Listing (ECX=param_1, EDX=param_2, R8D=param_3) ---",
        "FUN_140001140:",
        "  140001140: 55                 PUSH    RBP",
        "  140001141: 48 89 e5           MOV     RBP, RSP",
        f"  ; Immediate Constants : {imm_notes}",
        f"  ; Register Expression : {reg_body}",
    ]
    if "mock_add" in raw_body:
        asm_lines += [
            "  140001148: e8 b3 ff ff ff     CALL    FUN_140001100",
            "  ; Callee FUN_140001100: MOV EAX, ECX ; OR EAX, 0x1 ; RET",
        ]
    elif "mock_remove" in raw_body:
        asm_lines += [
            "  140001148: e8 c3 ff ff ff     CALL    FUN_140001110",
            "  ; Callee FUN_140001110: MOV EAX, ECX ; AND EAX, 0xfffffffe ; RET",
        ]
    asm_lines += [
        "  140001160: 5d                 POP     RBP",
        "  140001161: c3                 RET"
    ]
    return "\n".join(asm_lines)


def build_ct3_api_and_callee_spec(sid: str, category: str, helpers: list, target_line: str) -> str:
    """
    Build Context Tier 3 (CT3): Enriched Instruction, Constant & Callee Specifications.
    Strictly excludes any pair-level target descriptor or mutation description (P0-5).
    """
    body_match = re.search(r"target\s*\([^)]*\)\s*\{\s*(.*)\s*\}", target_line)
    raw_body = body_match.group(1) if body_match else target_line
    raw_body = re.sub(r"\(void\)\s*[abc]\s*;", "", raw_body).strip()
    imm_notes = format_hex_annotations(raw_body)

    specs = [
        "[Context Tier 3 — Enriched Register, Constant & Callee Specifications]",
        f"- Functional Category: {category}",
        f"- Win64 Register Mapping: `param_1` = `ECX` (arg 1), `param_2` = `EDX` (arg 2), `param_3` = `R8D` (arg 3)",
        f"- Hex-to-Decimal Immediate Table: {imm_notes}",
    ]
    if helpers:
        specs.append("- Static Callee Specifications:")
        specs.append("  * `FUN_140001100(int state)` -> `return state | 1;`")
        specs.append("  * `FUN_140001110(int state)` -> `return state & ~1;`")
    return "\n".join(specs)


def build_ct4_neighborhood(sid: str, helpers: list) -> str:
    lines = [
        "[Context Tier 4 — Caller Harness & Cross-Reference Neighborhood]",
        "Caller `main` (0x140001200):",
        "  int a = strtol(argv[1], NULL, 0);",
        "  int b = strtol(argv[2], NULL, 0);",
        "  int c = strtol(argv[3], NULL, 0);",
        "  int res = FUN_140001140(a, b, c);",
        "  printf(\"%d\\n\", res);"
    ]
    return "\n".join(lines)


def main():
    manifest_path = DATASET_DIR / "ground_truth_manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    objdump_path = DATASET_DIR / "disassembly_objdump_80.json"
    objdump_map = json.loads(objdump_path.read_text(encoding="utf-8")) if objdump_path.exists() else {}

    records = []
    for item in manifest:
        sid = item["id"]
        for variant in ("original", "mutant"):
            skey = f"{sid}_{variant}"
            c_path = DATASET_DIR / "src" / f"{skey}.c"
            helpers, target_line = extract_c_body(c_path)

            ct1 = to_ghidra_stripped_pseudocode(sid, variant, helpers, target_line, obf_level=0)
            ct2_asm = generate_x64_assembly(sid, variant, helpers, target_line)
            ct3_spec = build_ct3_api_and_callee_spec(sid, item["category"], helpers, target_line)
            ct4_neigh = build_ct4_neighborhood(sid, helpers)

            obf1 = to_ghidra_stripped_pseudocode(sid, variant, helpers, target_line, obf_level=1)
            obf2 = to_ghidra_stripped_pseudocode(sid, variant, helpers, target_line, obf_level=2)
            obf3 = to_ghidra_stripped_pseudocode(sid, variant, helpers, target_line, obf_level=3)

            real_objdump = objdump_map.get(skey, {}).get("objdump_intel_O2", "")

            records.append({
                "sample_key": skey,
                "id": sid,
                "variant": variant,
                "category": item["category"],
                "difficulty": item["difficulty"],
                "mutation_operator": item["mutation_operator"],
                "question": item["question"],
                "tests": item["tests"],
                "contexts": {
                    "CT1": ct1,
                    "CT2": f"{ct1}\n\n{ct2_asm}",
                    "CT2_Objdump": f"{ct1}\n\n; --- Compiled PE64 objdump -d -M intel (-O2) ---\n{real_objdump}" if real_objdump else f"{ct1}\n\n{ct2_asm}",
                    "CT3": f"{ct1}\n\n{ct2_asm}\n\n{ct3_spec}",
                    "CT4": f"{ct1}\n\n{ct2_asm}\n\n{ct3_spec}\n\n{ct4_neigh}",
                },
                "obfuscated_ct1": {
                    "Obf0": ct1,
                    "Obf1_CFF": obf1,
                    "Obf2_Sub": obf2,
                    "Obf3_Combined": obf3,
                }
            })

    out_path = RESULTS_DIR / "decompiled_contexts_80.json"
    out_path.write_text(json.dumps(records, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"[+] Built {len(records)} context records (zero target-label fields) at: {out_path}")


if __name__ == "__main__":
    main()
