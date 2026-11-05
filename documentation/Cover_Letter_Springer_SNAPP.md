# COVER LETTER FOR SUBMISSION TO SPRINGER NATURE (SNAPP)

**To:** The Editor-in-Chief  
**Journal / Conference:** Springer Lecture Notes in Computer Science (LNCS) / Security & AI Track  
**Date:** November 5, 2026  

---

**Dear Editor-in-Chief,**

We are pleased to submit our original research manuscript entitled:

> **"SCHR-Bench: Evaluating Security-Critical Hallucinations in LLM-Assisted Binary Reverse Engineering via Ground-Truth Mutations"**

for consideration for publication in Springer LNCS.

### Research Motivation & Key Contributions
While Large Language Models (LLMs) are rapidly adopted by binary analysts to assist in decompiled code understanding, unverified hallucinations in security-critical routines (e.g., anti-debugging logic, persistence mechanisms, cryptographic keys) pose acute operational hazards. Existing benchmarks rely predominantly on surface n-gram similarity (BLEU) or syntactic recompilability, failing to detect whether an LLM notices localized semantic inversions in stripped binary code.

To address this foundational gap, our paper makes the following principal contributions:
1. **Differential Mutation Benchmark (SCHR-Bench):** We establish a controlled benchmark of 40 paired C security-decision functions ($N = 80$ stripped x86-64 PE binaries) across five functional families, execution-verified across 160 dynamic test assertions in Experiment E0 (100% behavioral divergence on discriminating inputs).
2. **Empirical Evaluation of LLM Hallucinations:** Across 1,020 rigorously logged evaluations under zero temperature ($\tau = 0.0, \text{seed} = 42$), we demonstrate that stripped pseudocode induces significant return-value error rates (38.8% on LLaMA-3.1 8B and 23.8% on Qwen2.5-Coder 14B), and that high syntactic recompilability (100.0%) and high surface BLEU mask complete logic inversions.
3. **Context Escalation & Obfuscation Insights:** We evaluate the limits of assembly context escalation (CT2/CT3) under McNemar’s paired tests and provide preliminary pilot observations on structural obfuscation templates (Obf0–Obf3).
4. **Operational Grounding on Real-World Malware:** We validate our functional taxonomy against authentic subroutines of the Gh0stRAT PE32 trojan under NSA Ghidra static analysis, demonstrating that LLMs excel at coarse-grained triage but exhibit persistent "canonical parroting" hallucinations on mutated operational subroutines.

### Declarations & Double-Anonymous Compliance
- **Double-Blind Peer Review Compliance:** In accordance with Springer Nature’s double-anonymous policy, all author names, institutional affiliations (FPT University), student identifiers, course references, and identifiable repository URLs have been removed from the submitted manuscript (`manuscript.pdf`). All experimental artifacts have been hosted on an anonymized repository: `https://anonymous.4open.science/r/SCHR-Bench-Anon`.
- **Exclusivity & Originality:** This manuscript represents original work that has not been previously published and is not under consideration for publication elsewhere in whole or in part.
- **Ethical & Safety Statement:** All quantitative benchmark evaluations were conducted strictly on synthetic, self-contained mock C routines. Real malware analysis was conducted strictly via static disassembly in an isolated, air-gapped environment with zero malware execution and zero network egress.
- **Author Approval:** All co-authors have reviewed and approved the manuscript and agree with this submission.

### Corresponding Author Contact Information:
- **Name:** Mai-Hoang Dinh
- **Affiliation:** Department of Information Assurance, FPT University, Ho Chi Minh City, Vietnam
- **Email:** dinhmh@fe.edu.vn

Thank you very much for your time and consideration of our work.

Sincerely,  
**The Authors**
