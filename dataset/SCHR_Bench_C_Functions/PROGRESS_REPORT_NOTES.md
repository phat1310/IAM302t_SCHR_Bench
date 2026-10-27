# Progress Report 2 — Dataset Pilot Evidence

## What is already verified in this package

- 5 synthetic behavior classes and 40 original C functions.
- 40 controlled mutation variants in separate C files.
- 80 manual input vectors with expected result for both versions.
- Automated native compilation and execution of 160 expected-output assertions.
- An optional MinGW-w64 cross-compile script for Windows PE x86/x64.

## What is **not** yet verified

- Successful Ghidra headless decompilation on Windows PE (not run in this package).
- Obfuscation conditions 0–3 (not generated here).
- LLM CT1–CT4 prompts or experimental outputs.
- SCHR, BLEU/recompilability, confidence intervals, McNemar tests, or kappa.
- Naturalism/generalizability of these synthetic examples to Gh0stRAT or other malware families.

## Suggested screenshots for Report 2

- `check_suite.py` E0 PASS log.
- Three side-by-side minimal C diffs (boundary A03, mock API P06, state machine C08).
- Ghidra imports of one original and one mutant after cross-compiling PE.
- Manifest excerpt showing ID, mutation type, test vector, output but **not** leaking ground truth into the model query.

## Safe-handling statement

All code in this suite uses pure local decision logic, toy token transforms, or mock state operations. No real Windows APIs are called to create persistence, inspect debuggers, access sensitive data, or communicate with C2 infrastructure.
