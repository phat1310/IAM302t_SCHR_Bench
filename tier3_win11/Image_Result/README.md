# 📸 MỤC LỤC & BÁO CÁO PHÂN TÍCH HÌNH ẢNH MẪU GH0STRAT PE32 (TIER 3 SANDBOX)

> **Mẫu phân tích:** Gh0stRAT PE32  
> **SHA256:** `ea7cd59c402128b0beffba34a6fb7b3f6f9fc5be62cb4aa51e605d3bcaee98be`  
> **Kích thước:** 16.45 MB (PE32 GUI Executable)  
> **Công cụ thực hiện:** Detect It Easy (DIE) v3.21 & PE-bear v0.7.2  
> **Mục tiêu đồ án:** Bằng chứng thực nghiệm Mốc D4 & Section 5 Bài báo khoa học Springer LNICST (EAI INISCOM 2027)

---

## 📑 Danh Mục Bằng Chứng Thực Nghiệm

| STT | Tên Tệp Minh Chứng | Công Cụ | Nội Dung & Phát Hiện Kỹ Thuật | Ý Nghĩa Trong Bài Báo Springer |
|:---:|:---|:---:|:---|:---|
| **01** | `01_die_overview_vprotect_packed.png` | DIE v3.21 | Giao diện tổng quan: PE32 GUI, Entry Point `0x010b0703`, 9 Sections, phát hiện **Protector: VXiProtect (new)**, **Packer: Generic Imports like VMProtect (v3.6.0+)**. | Bằng chứng mã độc thực tế được bảo vệ bởi kỹ thuật obfuscation/packing phức tạp, gây khó khăn cho decompiler. |
| **02** | `02_die_entropy_sections_graph.png` | DIE v3.21 | Đồ thị Entropy biểu diễn mức độ ngẫu nhiên/nén của toàn bộ 9 sections. Section `.O#J` đạt entropy cực đại gần 7.9 bit/byte. | Minh chứng trực quan sự tồn tại của payload mã hóa/nén trong binary, làm méo mó cấu trúc điều khiển. |
| **03** | `03_die_sections_table_entropy.png` | DIE v3.21 | Bảng chi tiết Entropy và trạng thái packed của từng section: Section `.O#J` (Size `0x01071c00`, Entropy `7.89095`, Status: **packed**). | Cung cấp số liệu chính xác để lập Table trong Section 5 của Paper. |
| **04** | `04_die_strings_search_empty.png` | DIE v3.21 | Tìm kiếm chuỗi tĩnh `Software\Microsoft` trả về **0 strings found**. | Chứng minh các chuỗi IOC nhạy cảm (Registry Run Key Persistence) đã bị mã hóa trong runtime, static analysis thông thường thất bại. |
| **05** | `05_die_strings_raw_filtered.png` | DIE v3.21 | Danh mục chuỗi thô bóc tách từ overlay và các section không nén (59,178 chuỗi). | Thể hiện mức độ làm rối chuỗi (string encryption/obfuscation). |
| **06** | `06_pebear_dos_file_header.png` | PE-bear v0.7.2 | Cấu trúc DOS Header & PE File Header: Machine `IMAGE_FILE_MACHINE_I386` (32-bit), TimeDateStamp, Characteristics. | Xác thực cấu trúc tệp PE32 chuẩn. |
| **07** | `07_pebear_section_headers_map.png` | PE-bear v0.7.2 | Bản đồ phân bổ 9 Section Headers trong bộ nhớ: Virtual Address, Virtual Size, Raw Address, Raw Size. | Định vị ranh giới các section phục vụ trích xuất Ghidra. |
| **08** | `08_pebear_section_characteristics.png` | PE-bear v0.7.2 | Thuộc tính phân quyền Section (`IMAGE_SCN_MEM_READ`, `WRITE`, `EXECUTE`) của các section làm rối. | Phát hiện section có đồng thời cờ Write và Execute (W+X) — dấu hiệu packer unpack vào RAM. |
| **09** | `09_pebear_imports_iat_analysis.png` | PE-bear v0.7.2 | Bảng Import Address Table (IAT): Các hàm nạp động tối thiểu do VMProtect/VXiProtect để lại để load payload vào bộ nhớ. | Cung cấp địa chỉ hàm nạp và offset đầu vào cho Tier 2 (Kali) chạy Ghidra trích xuất Assembly. |
| **10** | `10_pebear_exports_resources_analysis.png` | PE-bear v0.7.2 | Phân tích thư mục Resources (.rsrc) và Manifest nhúng của mã độc. | Xác nhận các thành phần hỗ trợ thực thi của Gh0stRAT. |

---

## 📊 Tệp Dữ Liệu & Nhật Ký Kèm Theo
* `gh0strat_die_entropy_sections.log`: Nhật ký ghi lại chỉ số entropy chi tiết từng section từ DIE.
* `gh0strat_pe_sections_layout.json`: Bản đồ offset và kích thước raw binary của 9 sections.
* `gh0strat_strings_all.txt`: Toàn bộ 59,178 chuỗi thô trích xuất từ mẫu phục vụ đối chiếu IOC.
