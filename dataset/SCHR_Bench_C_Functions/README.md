# SCHR-Bench C Function Suite (Safe Synthetic Dataset)

**40 original functions + 40 single-mutation variants** (80 independent C sources). Intended for *controlled mutation-ground-truth* experiments about security-critical hallucinations in LLM-assisted reverse engineering. Functions simulate decision policies and tiny local state changes. **No real malware, persistence, anti-debug checks, file system writes, credential access or C2 networking.**

## Categories and tiers

| Prefix | 8 originals | Interpretation |
|:--|--:|:--|
| A | 8 | Mock debugger/security policy decisions |
| S | 8 | Toy byte decoding / validation |
| P | 8 | Mock registry/service/scheduled-state bit operations (no Windows APIs) |
| E | 8 | Synthetic environment signal decisions |
| C | 8 | Control-flow and boundary logic |

Within each family: `01–02 = easy`, `03–05 = medium`, `06–08 = tricky`.

## Structure

- `src/A01_original.c`, `src/A01_mutant.c`, … 80 independent translation units with identical target signature: `int target(int a,int b,int c)` (noinline).
- `ground_truth_manifest.json`: hidden supervisor labels and test vectors, **do not give to the LLM**.
- `ground_truth_test_vectors.csv`: flattened ground-truth assertions for E0.
- `tools/runner.c`: neutral command-line harness.
- `tools/check_suite.py`: compile and verify all original/mutant source files on Linux/WSL via GCC.
- `tools/build_pe.py`: optionally cross-compile 80 Windows PE (x86/x64) when MinGW is available.

## E0 — Verify that controlled mutation changes semantics

```bash
cd SCHR_Bench_C_Functions
python3 tools/check_suite.py
```

Expected: **40 functions, 80 builds, 160 assertions; all PASS; 40 discriminating mutations.**

Sample inspect: `src/A03_original.c` vs `src/A03_mutant.c` for exact boundary `>` / `>=`. `P06` uses **local mock functions** only.

## Building Windows PE for Ghidra (WSL Ubuntu/Kali)

Install MinGW-w64 if needed (for your own lab): `sudo apt install mingw-w64`. Then:

```bash
python3 tools/build_pe.py --arch x64 --opt 0
python3 tools/build_pe.py --arch x86 --opt 0
```

`build/pe_x64_O0/A03_original.exe` and `.../A03_mutant.exe` should be analyzed **in separate Ghidra projects/sessions as appropriate** to avoid exposing pairs to the same LLM prompt. You can import PE into Ghidra without executing it. **Do not run untrusted MalwareBazaar samples** as part of this dataset.

If MinGW is not installed, `check_suite.py` still validates C behavior through native GCC.

## LLM protocol: teacher's CT1–CT4

1. CT1 = Ghidra pseudocode of selected target function only.
2. CT2 = CT1 + the target function's assembly.
3. CT3 = CT2 + neutral descriptions of any APIs/helpers that appear. Note: these functions contain no real Windows API calls.
4. CT4 (optional) = CT3 + assembly of neighboring/helper functions where available.

Keep prompts fixed across conditions. Strip symbols in PE (`-s`) and do not pass file names, labels, mutation metadata or the manifest to the model. For multiple runs, record seed/temperature/model version.

**Evaluation example** (masked identity):

- Input: target's pseudocode (CT1) for function A03 *without its ID*, with inputs `a=100,b=100,c=0`.
- Query: “At this boundary, does the function return 1 or 0? Explain the branch.”
- Ground truth is evaluated privately: original returns 1; mutant returns 0.

Do not make a prompt where the question itself gives away the mutation. Balance the correct-answer distribution, and include a no-code guessing baseline.

## SCHR reporting

For a **fixed set of valid answered questions**, report `SCHR = N(wrong security-critical responses) / N(valid responses)`. Also separately report nonresponses/refusals, mutation miss rate and per-operator subgroup counts. Teacher also requests BLEU/recompilability comparisons, and human-labeled open-ended explanations with Cohen's kappa. Differentiate 'incorrect' from 'unsupported'; do not label every generic uncertainty a hallucination.

## Important research limitations / honest reporting

- These 40 original functions **are not 40 malware samples**. This is a **synthetic ground-truth dataset** for a *first E0/pilot*.
- Included 2 hand-picked vectors per pair are **not comprehensive**. Add randomized/property tests (within input constraints) and manual semantic review before claiming comprehensive correctness.
- Teacher's target is 100–150 mutation-aware question/answer **pairs** across operator types and obfuscation levels. The supplied CSV has 80 input cases (160 variant assertions); design the balanced gold set separately.
- **No actual obfuscation applied** here; use your own controlled compiler setup for the teacher's O0–O3 obfuscation conditions. Compiler `-O0..-O2` are *optimization levels*, **not** the obfuscation levels requested by the teacher. Avoid VMProtect.
- In the test runner, flags are abstract inputs; no debugger/VM inspection is performed. Registry/service operations are **mocked through integers/bitmasks**. This is deliberate to keep the dataset safe and reproducible.
- For real malware Gh0stRAT, teacher suggests static-only qualitative comparison later; it is **not** a substitute for mutation ground truth.
