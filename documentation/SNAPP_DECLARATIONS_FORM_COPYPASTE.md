# HƯỚNG DẪN COPY-PASTE KHAI BÁO DECLARATIONS TRÊN CỔNG SNAPP (SPRINGER NATURE)
## (Chuẩn bị sẵn sàng 100% theo đúng yêu cầu tại Trang 8 file `G7_Gop_y_sua_nop_SNAPP_V2.pdf`)

Khi nhóm mở cổng nộp bài **SNAPP** của Springer Nature đến bước **Declarations & Metadata**, hãy copy chính xác từng đoạn văn bản tiếng Anh chuẩn mực dưới đây dán vào từng ô tương ứng:

---

### 1. Competing Interests (Xung đột lợi ích)
> **Dán đoạn sau vào ô Competing Interests:**
```text
The authors declare that they have no competing financial or non-financial interests that are directly or indirectly related to the work submitted for publication.
```

---

### 2. Data & Artifact Availability Statement (Khả dụng dữ liệu & Mã nguồn)
> **Dán đoạn sau vào ô Data Availability:**
```text
All experimental code, C source pairs, compiled stripped PE64 binaries, disassembly files, the 240-item paired multiple-choice question gold set, and complete raw evaluation logs generated during this study are openly available in the anonymized research repository at:
https://anonymous.4open.science/r/SCHR-Bench-Anon-827B

To maintain strict operational safety and prevent the proliferation of live malware, the real-world Gh0stRAT PE32 executable is not distributed in the repository; only its public cryptographic identifier (SHA-256: ea7cd59c402128b0beffba34a6fb7b3f6f9fc5be62cb4aa51e605d3bcaee98be) and extracted static decompiler snippets are provided.
```

---

### 3. Ethics Approval & Responsible Security Research Statement (Đạo đức nghiên cứu)
> **Dán đoạn sau vào ô Ethics / Responsible Conduct:**
```text
This research strictly adheres to standard defensive cybersecurity research ethics. All primary quantitative benchmark evaluations were conducted on self-contained, synthetic C functions designed solely to evaluate program comprehension. The qualitative case study on the in-the-wild Gh0stRAT Trojan was conducted strictly via static disassembly (NSA Ghidra 11.2) in an isolated, air-gapped sandbox environment with zero live binary execution, zero memory unpacking, and zero network egress. This work is intended exclusively to improve the reliability and safety of automated binary analysis and reverse engineering tools.
```

---

### 4. Disclosure of AI Usage (Tuyên bố sử dụng AI)
> **Dán đoạn sau vào ô AI Usage Statement:**
```text
During the preparation of this work, the authors used local open-weight Large Language Models (LLaMA-3.1 8B and Qwen2.5-Coder 14B hosted via Ollama) strictly as the empirical subjects of scientific evaluation. Generative AI assistance was employed solely for LaTeX code formatting, script refactoring, and English language polishing. All experimental scripts, C source functions, evaluation pipelines, and statistical tables were conceptualized, implemented, and verified by the authors.
```

---

### 5. Author Contributions Statement (CREdiT Taxonomy)
> **Dán đoạn sau vào ô Author Contributions (Điền theo chuẩn CRediT quốc tế):**
```text
- Tan-Phat Nguyen: Conceptualization, Methodology, Software, Formal Analysis, Data Curation, Writing – Original Draft, Visualization.
- Thien-Nhan Do: Software, Validation, Investigation, Data Curation, Resources.
- Trong-Duy Nguyen: Validation, Formal Analysis, Software, Writing – Review & Editing.
- Hong-Phuc Vo: Investigation, Validation, Data Curation, Writing – Review & Editing.
- Mai-Hoang Dinh: Conceptualization, Methodology, Supervision, Project Administration, Writing – Review & Editing (Corresponding Author).
```

---

### 6. Funding Statement (Tài trợ)
> **Dán đoạn sau vào ô Funding:**
```text
The authors declare that no specific funding, grants, or commercial sponsorships were received for this research project.
```

---

### 7. Suggested Reviewers (Gợi ý phản biện nếu hệ thống yêu cầu)
Nếu hệ thống SNAPP yêu cầu đề xuất 2 Reviewer chuyên ngành (Security / LLM for Code), nhóm có thể điền:
1. **Reviewer 1:**  
   - *Name:* Prof./Dr. Benjamin Tan  
   - *Institution:* University of Calgary, Canada  
   - *Email:* `benjamin.tan1@ucalgary.ca`  
   - *Reason:* Expert in empirical evaluation of LLMs in binary reverse engineering and software security.
2. **Reviewer 2:**  
   - *Name:* Prof./Dr. Hanzhuo Tan  
   - *Institution:* Southern University of Science and Technology (SUSTech), China  
   - *Email:* `hanzhuo.tan@gmail.com`  
   - *Reason:* Lead author of LLM4Decompile (EMNLP 2024), expert in neural decompilation and binary program synthesis.
