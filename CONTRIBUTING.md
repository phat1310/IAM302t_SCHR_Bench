# Contributing to SCHR-Bench (`CONTRIBUTING.md`)

We welcome contributions from the binary analysis, reverse engineering, and LLM security research communities—including new ground-truth C mutation pairs, additional compiler toolchains (Clang/LLVM, MSVC, ARM64), and evaluation logs for frontier or fine-tuned models.

---

## 1. Adding New Security-Critical Function Pairs

Each function pair in `dataset/SCHR_Bench_C_Functions/src/` must satisfy the **E0 Dynamic Behavioral Divergence Contract**:

1. **Function Signature:** Both `<ID>_original.c` and `<ID>_mutant.c` must implement `int target(int a, int b, int c)` without external dependencies or global mutable state.
2. **Single Controlled Mutation (`M1`–`M5`):**
   - `M1`: Relational Boundary Flip (`<` $\leftrightarrow$ `<=`, `>` $\leftrightarrow$ `>=`)
   - `M2`: Bitwise / Shift Mask Corruption (`>>` $\leftrightarrow$ `<<`, mask width shift)
   - `M3`: Arithmetic Sign / Modulo / Overflow Modification
   - `M4`: Equality / Polarity Inversion (`==` $\leftrightarrow$ `!=`, return polarity flip)
   - `M5`: Compound Guard / State-Reset Perturbation
3. **Discriminating Input Vector (`Vector 1`):** Must produce strictly different return values between Original and Mutant (`orig_out != mut_out`).
4. **Boundary-Preservation Input Vector (`Vector 2`):** Validates non-trivial execution along an unmutated or secondary path.

### Verification Command
After adding your pair to `dataset/SCHR_Bench_C_Functions/ground_truth_manifest.json`, run:
```bash
python dataset/SCHR_Bench_C_Functions/tools/check_suite.py
python code/step0_verify_e0_windows.py
```

---

## 2. Evaluating Additional LLMs (Local FP16, Quantized Ollama, or Cloud API)

- **Full 80-Variant Benchmark (`code/step3_mcp_server_and_benchmark.py`):**
  Supports local Ollama endpoints (`--mode return` and `--mode mcq`).
- **20-Pair Stratified FP16 / Cloud API Control Protocol (`code/step5_fp16_api_subset_ablation.py`):**
  To evaluate an unquantized FP16 vLLM server or OpenAI-compatible API endpoint against our 4-bit baseline on the stratified 20-pair ($N = 40$) subset:
  ```bash
  python code/step5_fp16_api_subset_ablation.py \
      --api-base http://localhost:11434/v1 \
      --model qwen2.5-coder:14b-fp16 \
      --output results/fp16_ablation_logs.json
  ```

---

## 3. Code & Dataset Licensing

By submitting a pull request, you agree that your code contributions are licensed under the **MIT License** and dataset contributions under **CC BY 4.0**.
