# Security & Artifact Safety Policy (`SECURITY.md`)

## 1. Benchmark Binary Safety (`dataset/SCHR_Bench_C_Functions/`)

All **40 C function pairs ($N = 80$ compiled 64-bit Windows PE executables)** located in `dataset/SCHR_Bench_C_Functions/` are **100% synthetic, deterministic, pure arithmetic/bitwise routines** (`int target(int a, int b, int c)`):

- **Zero System/Network Side Effects:** None of the 80 C source files invoke network sockets, file system modification APIs, registry operations, process spawning, or dynamic memory allocation.
- **Deterministic Execution Harness:** The test driver (`dataset/SCHR_Bench_C_Functions/tools/runner.c`) only parses three command-line integers `(a, b, c)`, invokes `target(a, b, c)`, and prints the integer result to `stdout`.
- **Antivirus False-Positive Notice:** Because the 80 binaries in `dataset/SCHR_Bench_C_Functions/bin/pe_x64_O2/` are compiled with MinGW-w64 (`x86_64-w64-mingw32-gcc -O2`) and stripped of symbol tables (`strip --strip-all`) to simulate realistic reverse-engineering targets, heuristic endpoint scanners may occasionally flag stripped MinGW executables. You can inspect every C source file in `dataset/SCHR_Bench_C_Functions/src/` and recompile all 80 binaries from scratch using `python dataset/SCHR_Bench_C_Functions/tools/build_pe.py`.

## 2. Ecological Case Study Policy (No Live Malware in Repository)

- **Strictly No Live Malware Binaries:** In full compliance with GitHub Terms of Service and academic artifact safety standards, **no live malware executables (`.exe`, `.dll`, `.bin`) from the ecological Gh0stRAT case study are tracked or distributed in this repository** (enforced via `.gitignore`).
- **Static Text & Metadata Only:** Only sanitized static analysis outputs (PE section entropy tables, import address table summaries, and decompiled/disassembled text snippets in `results/GH0STRAT_EVALUATION.json` and `tier3_win11/Image_Result/`) are included for reproducibility of the ecological triage case study.

## 3. Reporting Issues

If you discover any security or reproducibility issue in the benchmark harness, please open an issue on GitHub or contact the authors via the institutional emails listed in `CITATION.cff`.
