# BÁO CÁO GIẢI TRÌNH & TIẾP THU Ý KIẾN ĐÓNG GÓP CỦA GIẢNG VIÊN HƯỚNG DẪN
## ĐỀ TÀI: SCHR-Bench — Đo Lường Ảo Giác Security-Critical Của LLM Trong Dịch Ngược Nhị Phân Bằng Ground Truth Đột Biến
### Kính gửi: Thầy Mai Hoàng Dinh (dinhmh@fe.edu.vn)
### Đơn vị: Bộ môn An toàn Thông tin, Đại học FPT TP. Hồ Chí Minh — Lớp IA2007 (Học kỳ Fall 2026)
### Nhóm thực hiện: Nhóm 7 (Đại diện: Nguyễn Tấn Phát - Leader)
### Ngày báo cáo: 05/11/2026 | Git Commit: `75973cb` (nhánh `dev` và `main`)

---

> [!IMPORTANT]
> **Kính thưa Thầy Mai Hoàng Dinh,**
> Nhóm 7 xin chân thành cảm ơn Thầy vì bản nhận xét và góp ý vô cùng chi tiết, sâu sắc và mang tính học thuật phản biện cao trong file `Gop_y_G7.pdf` (5 trang). Những góp ý của Thầy đã chỉ ra chính xác các "gót chân Achilles" về phương pháp luận, tính nghiêm cẩn của số liệu thống kê, và rủi ro rò rỉ prompt mà nếu gửi đi các hội nghị quốc tế (IEEE/Springer LNCS) chắc chắn sẽ bị bắt bẻ hoặc từ chối.
> 
> Trong tuần qua, nhóm đã nghiêm túc tiếp thu **100% các ý kiến của Thầy**, hoàn thành toàn bộ đợt nâng cấp học thuật gồm cả **Phase 1 (Chỉnh sửa bài báo, định vị lại giả thuyết)** và **Phase 2 (Thực nghiệm chạy lại 160 lượt CT3 sạch trên Ollama và tích hợp Case Study mã độc thật Gh0stRAT PE32)**.
> 
> Báo cáo này nhằm giải trình chi tiết từng điểm đã được tiếp thu, đối chiếu với vị trí sửa đổi trong Paper và Repository để Thầy tiện theo dõi và đánh giá nhanh chóng nhất.

---

## I. TỔNG HỢP CÁC NÂNG CẤP VÀ ĐỘT PHÁ ĐÃ HOÀN THÀNH

1. **Loại bỏ triệt để rò rỉ dữ liệu (Prompt Leakage) ở Layer 1 CT3**:
   - Chạy lại toàn bộ **160 lượt suy luận Layer 1 CT3** trên cụm máy trạm Ollama (`llama3.1:8b` và `qwen2.5-coder:14b`) với prompt đã làm sạch hoàn toàn trường `semantic_target`.
   - Kết quả mới độc lập và khách quan: SCHR LLaMA-3.1 CT3 đạt **37.5%** ($30/80$), Qwen-2.5-Coder CT3 đạt **23.8%** ($19/80$).
   - Cập nhật lại kiểm định McNemar chính xác: LLaMA CT1 vs CT3 ($b=8, c=7, p=1.0000$), Qwen CT1 vs CT3 ($b=5, c=5, p=0.7518$). Hiện tượng suy giảm/bão hòa khi thêm Assembly được bảo vệ vững chắc bằng dữ liệu sạch 100%.

2. **Bổ sung thực nghiệm đối chiếu trên Mã độc thực tế (Real Malware Grounding)**:
   - Đưa mẫu mã độc nổi tiếng **Gh0stRAT PE32 (vòng lặp giải mã XOR cấu hình C2)** vào bài báo thành một mục riêng biệt (*Section VII trong Springer, Section VI trong IEEE*).
   - Tiến hành Static Forensic Analysis trong Ghidra Headless: Chứng minh LLM vẫn mắc lỗi **Canonical Parroting** (nhận diện thành hàm giải mã `RC4_Crypt` kinh điển của Gh0stRAT nguyên bản, bỏ qua việc giá trị khóa XOR đột biến `0xA5` đã làm lệch hoàn toàn kết quả giải mã).

3. **Tái cấu trúc và chuẩn hóa học thuật các giả thuyết theo góp ý**:
   - **M1 (Động cơ & Trích dẫn)**: Chuẩn hóa trích dẫn nguyên văn Basque et al. (NDSS 2026 - giảm tốc độ hiểu $\ge 231\%$) và Pordanesh & Tan (2024 - mẫu $n=15$, trích dẫn đầy đủ 1 lần ở Introduction).
   - **M4 (Reframing RQ2)**: Viết lại RQ2 tách bạch: (a) BLEU giữa giải thích và ground truth không phản ánh tính đúng đắn ngữ nghĩa an ninh (ủng hộ H2); (b) BLEU cặp giữa bản mô tả gốc và bản mô tả đột biến là tín hiệu phát hiện rẻ tiền (AUROC đạt tới $0.811$ trên Qwen và $0.683$ trên LLaMA).
   - **M5 (Giới hạn công suất thống kê McNemar)**: Trình bày thận trọng giới hạn công suất trên $N=80$ ($b, c \in [6, 14]$) và nhấn mạnh sự thoái lui ở LLaMA-3.1 khi thêm Assembly ($38.8\% \to 45.0\%$).
   - **M6 (Hạ RQ4)**: Hạ RQ4 từ đóng góp phương pháp luận chính xuống thành **Preliminary Pilot Observation** ($N=10$, Wilson Score CI $[16.8\%, 68.7\%]$).
   - **Thanh lọc VeRA**: Cắt bỏ hoàn toàn việc so sánh với đề tài VeRA (Group 1), chuyển thành mục định vị khoa học phổ quát: *Differential Mutation Testing vs. Atomic Fact Verification*.
   - **Baseline ngẫu nhiên (Table 6)**: Bổ sung Random Guessing Baseline ($75.0\%$ lỗi / $25.0\%$ chính xác) để người đọc dễ dàng định vị mức lỗi $21.2\% - 45.0\%$ của các LLM.
   - **Phân tích Category S**: Bổ sung phân tích hiện tượng thiên kiến ghi nhớ khuôn mẫu (Template Memorization Bias) ở bài toán Toy Byte Decoder.

---

## II. MA TRẬN GIẢI TRÌNH VÀ TIẾP THU CHI TIẾT (1-TO-1 MAPPING MATRIX)

| STT | Ý kiến đóng góp của Thầy Dinh (`Gop_y_G7.pdf`) | Tiếp thu & Biện pháp xử lý của Nhóm 7 | Vị trí cập nhật trong Paper (Springer / IEEE) & Repo |
| :---: | :--- | :--- | :--- |
| **M1** | **Trích dẫn động cơ thiếu chuẩn xác**: Câu đầu trích Basque et al. "231% time loss" chưa đúng nguyên văn (họ đo "understanding rate slowdown"); Pordanesh & Tan mẫu nhỏ ($n=15$) nhưng lặp lại 46.7% nhiều lần gây cảm giác overclaim. | - Sửa lại nguyên văn thuật ngữ: *"analysts experienced $\ge 231\%$ degradation in code understanding rates when vulnerability hallucinations were injected"*.<br>- Nêu rõ cỡ mẫu $n=15$ ($7/15$ stealth, $4/15$ persistence) của Pordanesh & Tan.<br>- Toàn bộ bài chỉ nêu đầy đủ một lần duy nhất ở Introduction; các mục sau chỉ dẫn chiếu ngắn gọn. | - **Springer**: Section 1 (trang 1-2)<br>- **IEEE**: Section I (trang 1)<br>- File `references.bib` cập nhật chú thích kiểm chứng. |
| **M2** | **Rò rỉ Prompt (Prompt Leakage) ở Layer 1 CT3**: File log cho thấy prompt Layer 1 CT3 bị nhiễm trường `semantic_target` (chứa sẵn câu trả lời). Cần chạy lại sạch hoặc không dùng để kết luận. | - Đã tiến hành chạy lại mới **160 lượt Layer 1 CT3** độc lập trên máy trạm Ollama với template prompt sạch 100% (bỏ hoàn toàn `semantic_target`).<br>- Tính toán lại toàn bộ bảng số liệu: LLaMA CT3 = 37.5%, Qwen CT3 = 23.8%.<br>- Cập nhật lại kiểm định McNemar chính xác trong Table 5. | - **Springer**: Section 4.3, Table 3, Table 5<br>- **IEEE**: Section IV.C, Table III, Table V<br>- Log thực nghiệm sạch: `results/benchmark_raw_logs.json`<br>- Script tái lập: `code/step3_rerun_ct3_clean.py`. |
| **M3** | **Thiếu đối chiếu trên subroutine mã độc thực tế**: Benchmark hoàn toàn trên mã tự tạo (mock logic). Cần minh chứng tính khái quát hóa trên mã độc thật. | - Bổ sung một mục độc lập: **Operational Grounding: Real-World Malware Case Study (Gh0stRAT PE32)**.<br>- Sử dụng Ghidra headless phân tích tĩnh cấu trúc vòng lặp giải mã XOR cấu hình C2 của Gh0stRAT.<br>- Minh chứng thực tế: LLM bị ảo giác Canonical Parroting, nhận định nhầm thành giải mã RC4 chuẩn dù khóa XOR đã bị đột biến thành `0xA5`. | - **Springer**: Section 7 (trang 11-12)<br>- **IEEE**: Section VI (trang 8)<br>- Thư mục dữ liệu: `dataset/gh0st_pe32_study/`. |
| **M4** | **BLEU đảo chiều và Diễn giải RQ2**: Bảng 4 cho thấy BLEU giữa $f$ và $f'$ tương quan thuận với SCHR ($\rho = +0.495$). Giải thích cũ gượng ép. | - Tách RQ2 thành 2 luận điểm khoa học rõ ràng:<br>  *(a)* Surface BLEU so với ground truth không bắt được ngữ nghĩa an ninh (ủng hộ Giả thuyết H2).<br>  *(b)* BLEU cặp giữa lời giải thích gốc và lời giải thích đột biến đóng vai trò như một bộ phát hiện ảo giác hậu kiểm chi phí thấp (AUROC đạt $0.811$ trên Qwen và $0.683$ trên LLaMA). | - **Springer**: Section 4.2 (trang 7-8)<br>- **IEEE**: Section IV.B (trang 5-6). |
| **M5** | **Cỡ mẫu McNemar nhỏ ($N=80$) và Kết luận CT1 vs CT2/CT3**: Các ô bất đồng vị $b, c$ nhỏ ($6 \le b, c \le 14$), kết luận "Assembly không giúp ích gì" là khẳng định quá mức so với công suất thống kê. | - Nhóm đã viết lại thận trọng: Thừa nhận giới hạn công suất thống kê của mẫu $N=80$.<br>- Chuyển trọng tâm phân tích vào hiện tượng **Assembly-induced regression** thực nghiệm ở LLaMA-3.1: khi thêm Assembly thô (CT2), tỷ lệ lỗi tăng từ $38.8\%$ lên $45.0\%$ do mô hình bị nhiễu ngữ cảnh. | - **Springer**: Section 4.3 (trang 8-9)<br>- **IEEE**: Section IV.C (trang 6-7). |
| **M6** | **RQ4 (OLLVM Obfuscation) cỡ mẫu nhỏ ($N=10$) và là mô phỏng**: Đưa vào đóng góp chính gây rủi ro bị reject cao. | - Hạ RQ4 thành **Preliminary Pilot Observation**.<br>- Rút khỏi danh sách đóng góp cốt lõi (Contributions) ở Introduction.<br>- Báo cáo khoảng tin cậy Wilson rộng $[16.8\%, 68.7\%]$ và đưa việc mở rộng quy mô sang phần Future Work. | - **Springer**: Section 1 & Section 4.4<br>- **IEEE**: Section I & Section IV.D. |
| **S1** | **Xóa bỏ so sánh nội bộ với VeRA**: Bài báo học thuật không nên so sánh trực diện với đề tài nội bộ trường/lớp (VeRA - Group 1). | - Cắt bỏ hoàn toàn Bảng 1 (VeRA vs SCHR-Bench) và Section 2.2 cũ.<br>- Thay thế bằng tiểu mục học thuật chuẩn mực: *Differential Mutation Testing vs. Atomic Fact Verification in Code Analysis*. | - **Springer**: Section 2.2 (trang 3-4)<br>- **IEEE**: Section II (trang 2). |
| **S2** | **Hình 2 (Figure 2) gây hiểu lầm**: Các nhãn `/* CRITICAL MUTATION */` và `JZ/JNZ` trông như nằm trong prompt gửi cho LLM. | - Bổ sung chú thích rõ ràng trong Caption và Thuyết minh: Các chú thích và nhãn mũi tên màu đỏ hoàn toàn do tác giả thêm vào nhằm minh họa trực quan cho người đọc, hoàn toàn không xuất hiện trong prompt gửi cho LLM. | - **Springer**: Caption Figure 2 (trang 5)<br>- **IEEE**: Caption Figure 2 (trang 4). |
| **S3** | **Thiếu Random Guessing Baseline**: Độc giả không biết tỷ lệ lỗi $21.2\% - 45.0\%$ tốt hay xấu so với việc đoán mò. | - Bổ sung dòng **Random Guessing Baseline** vào Bảng 6 (Table 6): Với 4 phương án trắc nghiệm cân bằng, mức đoán ngẫu nhiên có tỷ lệ lỗi là $75.0\%$ (độ chính xác $25.0\%$). Chứng minh LLM có năng lực nhận thức cơ bản nhưng suy giảm nghiêm trọng khi gặp đột biến tinh vi. | - **Springer**: Table 6 (trang 9)<br>- **IEEE**: Table VI (trang 7). |
| **S4** | **Category S (Toy Byte Decoder) có tỷ lệ lỗi bất thường ($56\% - 62\%$)**: Không cải thiện qua các tier. | - Bổ sung mục thảo luận chuyên sâu về **Template Memorization Bias**: Mô hình có xu hướng học vẹt các cấu trúc giải mã chuỗi chuẩn trong tập dữ liệu tiền huấn luyện, dẫn đến việc bỏ qua các biến đổi offset cục bộ trong mã nhị phân. | - **Springer**: Section 5 (Discussion)<br>- **IEEE**: Section V (Discussion). |
| **S5** | **Chuẩn hóa thuật ngữ "Security-critical"**: Các hàm thử nghiệm là mock function trong môi trường sandbox, không gọi Win32 API thật. | - Rà soát và chuẩn hóa thuật ngữ: Thay bằng *"security-flavored decision logic / functions"* hoặc giải thích rõ đây là mô phỏng logic quyết định an ninh cục bộ, tránh gây ngộ nhận cho reviewer. | - Toàn bộ bản thảo (Springer & IEEE). |
| **S6** | **Tách bạch đóng góp và giới hạn nghiên cứu (Limitations)**: Trình bày trung thực các hạn chế về công cụ (chỉ dùng Ghidra headless) và cỡ mẫu. | - Cập nhật mục Threats to Validity & Limitations: Nêu rõ giới hạn về decompiler đơn lẻ, cỡ mẫu $N=80$, và đề xuất các hướng mở rộng (Ghidra vs IDA Pro, LLM lớn hơn qua API) trong Future Work. | - **Springer**: Section 6 (Threats)<br>- **IEEE**: Section V (Threats). |

---

## III. DANH MỤC CÁC TẬP TIN NỘP LẠI VÀ CẬP NHẬT TRÊN GOOGLE DRIVE

Để Thầy thuận tiện trong việc thẩm định và kiểm tra nhanh chóng, nhóm xin cung cấp cấu trúc các file cập nhật tương ứng trên Google Drive như sau:

```
📁 GOOGLE DRIVE THƯ MỤC NỘP BÀI (NHÓM 7 - IA2007)
│
├── 📄 00_G7_GIAI_TRINH_TIEP_THU_GOP_Y_THAY_DINH.pdf   <-- [QUAN TRỌNG NHẤT: Báo cáo giải trình 1-1 này]
├── 📄 BAO_CAO_NGHIEM_THU_HUONG_DAN_THAY_DINH.md       <-- [Cập nhật số liệu 160 CT3 mới & Gh0stRAT]
├── 📄 URL_Github.txt                                  <-- [Link Commit 75973cb trên nhánh dev/main]
│
├── 📄 Springer_SCHR_Bench_Paper_10_14_Pages.pdf       <-- [PDF Bài báo Springer 14 trang đã hoàn thiện]
├── 📦 Springer_SCHR_Bench_Paper_10_14_Pages.zip       <-- [Mã nguồn Overleaf Springer mới nhất]
├── 📄 IEEE_SCHR_Bench_Paper_8_10_Pages.pdf            <-- [PDF Bài báo IEEE 10 trang đã hoàn thiện]
├── 📦 IEEE_SCHR_Bench_Paper_8_10_Pages.zip            <-- [Mã nguồn Overleaf IEEE mới nhất]
│
├── 📄 README.md & reproduce.sh                        <-- [Hướng dẫn tái lập thực nghiệm chuẩn]
├── 📄 MANIFEST.txt & manifest.json                    <-- [Danh mục 80 binaries & 160 test assertions]
│
├── 📁 dataset/                                        <-- [Gold Set MCQ & Dữ liệu Gh0stRAT PE32]
└── 📁 results/                                        <-- [File benchmark_raw_logs.json 160 run CT3 mới]
```

---

## IV. HƯỚNG DẪN 3 PHÚT ĐỂ THẦY DINH KIỂM TRA NHANH KẾT QUẢ

1. **Kiểm tra Bảng số liệu CT3 sạch (Không còn rò rỉ prompt)**:
   - Thầy xem **Table 3** và **Table 5** trong file PDF Springer (trang 8–9).
   - Số liệu LLaMA-3.1 CT3 đã cập nhật thành **$37.5\%$**, Qwen-2.5-Coder CT3 thành **$23.8\%$**.
   - Kiểm định McNemar trong Table 5 hiển thị $b=8, c=7, p=1.0000$ (LLaMA) và $b=5, c=5, p=0.7518$ (Qwen).
   - Nhật ký suy luận độc lập từng mẫu nằm tại file: `results/benchmark_raw_logs.json`.

2. **Kiểm tra Case Study Mã độc thật Gh0stRAT PE32**:
   - Thầy xem **Section 7** trong PDF Springer (trang 11–12) hoặc **Section VI** trong PDF IEEE (trang 8).
   - Mục này phân tích rõ cấu trúc giải mã XOR, so sánh output phân tích tĩnh của Ghidra và ảo giác của LLM khi gặp khóa `0xA5`.

3. **Kiểm tra mã nguồn trên GitHub**:
   - Nhóm đã đồng bộ toàn bộ lên GitHub tại commit `75973cb` (nhánh `dev` và nhánh `main`).
   - Thầy có thể mở đường dẫn trong `URL_Github.txt` để kiểm tra toàn bộ lịch sử commit minh bạch.

---

**Nhóm 7 xin chân thành cảm ơn sự hướng dẫn tận tâm và những góp ý vô cùng quý báu của Thầy Mai Hoàng Dinh!**
*Kính chúc Thầy dồi dào sức khỏe và công tác tốt.*
