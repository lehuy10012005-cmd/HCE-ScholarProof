# KỊCH BẢN THUYẾT TRÌNH BẢO VỆ ĐỒ ÁN CAPSTONE (PRESENTATION SLIDES)
## ĐỒ ÁN: NỀN TẢNG BẢO CHỨNG QUYỀN TÁC GIẢ Ý TƯỞNG NGHIÊN CỨU KHOA HỌC TRÊN BLOCKCHAIN (HCE-SCHOLARPROOF)

* **Học phần:** Tiền điện tử và Hợp đồng thông minh (ECO2432)
* **Giảng viên hướng dẫn:** TS. Hà Ngọc Long
* **Khoa:** Hệ thống Thông tin Kinh tế — Trường Đại học Kinh tế, Đại học Huế
* **Nhóm thuyết trình:**
  1. **Lê Văn Quang Huy** (MSSV: `23K4300010` - K57 Kinh tế số)
  2. **Lại Vương Gia Bảo** (MSSV: `23K4300024` - K57 Kinh tế số)
* **Thời lượng thuyết trình dự kiến:** 15 phút (10 phút trình bày + 5 phút demo & Q&A)

---

### SLIDE 1: TRANG TIÊU ĐỀ & GIỚI THIỆU
- **Tiêu đề lớn:** HCE-SCHOLARPROOF
- **Phụ đề:** Nền tảng Bảo chứng Quyền tác giả & Phòng chống Trùng lặp Đề tài Nghiên cứu Khoa học bằng Cơ chế Proof of Existence
- **Đơn vị:** Trường Đại học Kinh tế, Đại học Huế — Học phần ECO2432
- **Giảng viên hướng dẫn:** TS. Hà Ngọc Long
- **Sinh viên thực hiện:** Lê Văn Quang Huy & Lại Vương Gia Bảo

---

### SLIDE 2: BỐI CẢNH & VẤN ĐỀ THỰC TIỄN (PROBLEM STATEMENT)
- **Thực trạng học thuật:**
  1. Tranh chấp ý tưởng sơ khởi (Scooping): Sinh viên, nhà nghiên cứu chia sẻ đề cương nghiên cứu nhưng bị chiếm đoạt trước khi xuất bản chính thức.
  2. Cơ chế đăng ký quyền tác giả truyền thống tốn nhiều tháng và chi phí cao, không khả thi cho hàng nghìn đề cương sinh viên mỗi năm.
  3. Thiếu công cụ đối soát dấu vân tay số độc lập, bất biến giữa các Khoa chuyên môn tại trường đại học.
- **Câu hỏi nghiên cứu:** Làm sao để xác lập quyền ưu tiên (Prior-art) ngay tức thì với chi phí gần như bằng 0 mà vẫn giữ bí mật tuyệt đối nội dung tài liệu?

---

### SLIDE 3: CƠ SỞ KHOA HỌC: MẬT MÃ HỌC & PROOF OF EXISTENCE
- **Thuật toán Keccak-256 (Client-side Hashing):**
  - Tệp nghiên cứu (PDF/Docx) được băm trực tiếp trong bộ nhớ RAM trình duyệt của tác giả.
  - Tệp gốc **KHÔNG BAO GIỜ** tải lên máy chủ hoặc gửi lên blockchain (Bảo mật 100%).
  - Dấu vân tay số 32 bytes (`bytes32`) là độc bản: thay đổi dù chỉ 1 dấu chấm sẽ tạo ra mã băm hoàn toàn khác.
- **Tính chất Blockchain:**
  - Bất biến (Immutability): Không ai có thể chỉnh sửa thời gian đã đóng khối.
  - Dấu thời gian công khai (Decentralized Timestamping): Bằng chứng khách quan trước pháp luật về thời điểm ra đời của ý tưởng.

---

### SLIDE 4: KIẾN TRÚC HỆ THỐNG & ĐẶC TẢ NGHIỆP VỤ (SPEC.MD)
- **Mô hình 3 lớp Web3:**
  - **Client UI:** Web DApp (Ethers.js v6, QR Code Generator, Giao diện chuẩn phong cách học thuật HCE).
  - **Consensus & State:** Hợp đồng thông minh `ScholarProof.sol` v2.
  - **Network:** Sepolia Testnet & Layer 2 (Base/Arbitrum).
- **Máy trạng thái bản ghi (State Machine):**
  - `Non-Existent` ➔ `Registered (Immutably Timestamped)` ➔ `Transferred (Optional)`.

---

### SLIDE 5: THIẾT KẾ SMART CONTRACT AN TOÀN (`ScholarProof.sol` v2)
- **Tuân thủ triệt để chuẩn mực `AGENTS.md`:**
  - **Mô hình CEI (Checks-Effects-Interactions):** Kiểm tra điều kiện ➔ Cập nhật Storage ➔ Phát Event.
  - **Phòng thủ Storage Bloat:** Giới hạn cứng `MAX_TITLE_LENGTH = 200` ký tự ngăn tấn công phình bộ nhớ node mạng.
  - **9 Custom Errors định danh rõ ràng:** Thay thế chuỗi lỗi dài giúp tiết kiệm gas giao dịch tối đa.
  - **Phi tập trung tuyệt đối (No Admin Backdoor):** Không có quyền khóa ví hay tịch thu bản quyền của người dùng.

---

### SLIDE 6: BỘ KIỂM THỬ TỰ ĐỘNG TOÀN DIỆN (LAB 12)
- **100% Pass (5/5 ca kiểm thử khắt khe):**
  1. `[TEST 1]` Luồng chuẩn (Happy Path): Đăng ký ý tưởng thành công, phát sự kiện on-chain đầy đủ.
  2. `[TEST 2]` Chống đạo văn (Anti-Scooping): Kẻ gian nộp đè mã băm bị Revert ngay lập tức với lỗi `IdeaAlreadyRegistered`.
  3. `[TEST 3]` Mạo danh chiếm quyền (Unauthorized): Kẻ lạ cố chuyển nhượng bị chặn đứng với lỗi `NotAuthor`.
  4. `[TEST 4]` Chuyển nhượng tác quyền hợp pháp: Cập nhật chủ sở hữu mới và chặn địa chỉ rỗng `0x0`.
  5. `[TEST 5]` Xử lý dữ liệu biên: Chặn chuỗi rỗng và chuỗi vượt quá 200 ký tự.

---

### SLIDE 7: BÁO CÁO KIỂM TOÁN BẢO MẬT (AUDIT_REPORT.MD)
- **Đánh giá theo chuẩn OWASP Smart Contract Top 10 & SWC Registry:**
  - 0 lỗ hổng Critical / 0 lỗ hổng High.
  - Khắc phục hoàn toàn 2 nguy cơ Medium: Storage Bloat và chuyển nhượng ví 0x0.
  - Kiểm toán Reentrancy, Timestamp Dependence, Access Control: Đạt chuẩn xuất sắc.

---

### SLIDE 8: BÀI TOÁN KINH TẾ & ĐO LƯỜNG GAS LAYER 2 (LAB 14)
- **Thực nghiệm đo lường qua `scripts/gas_benchmark.py`:**
  - Phí đăng ký trên **Ethereum L1**: ~`130.688 VNĐ` ($5.15 USD) ➔ Quá đắt.
  - Phí đăng ký trên **Base Network (L2)**: ~`334 VNĐ` ($0.013 USD) ➔ **Tiết kiệm 99.74%**.
- **Quy mô 1.500 đề tài/năm tại ĐH Kinh tế Huế:**
  - Chạy trên Base Network chỉ tốn **~500.000 VNĐ cho TOÀN BỘ sinh viên cả trường trong suốt 1 năm**.

---

### SLIDE 9: TRÌNH DIỄN GIAO DIỆN WEB3 DAPP THỰC TẾ
- **5 phân hệ công năng hoàn chỉnh:**
  1. Kéo thả băm tệp PDF Keccak-256 tức thì trong RAM.
  2. Kết nối ví MetaMask an toàn hoặc Chế độ Thử nghiệm HCE dự phòng.
  3. Sổ cái Sơ bộ On-chain (Live Ledger) tìm kiếm và lọc theo Khoa.
  4. Phân hệ Thẩm định Độc bản / Phát hiện trùng lặp tự động.
  5. Xuất Chứng thư Bảo chứng Quyền tác giả A4 đầy đủ Quốc hiệu, Tiêu ngữ và Mã QR tra cứu Etherscan.

---

### SLIDE 10: MINH CHỨNG TRIỂN KHAI THỰC TẾ (LIVE DEPLOYMENT)
- **Hợp đồng trên Sepolia Testnet:** `0xa2F53106B3dFdf23b6b158022646d231A21e49cb`
- **Mã nguồn Verified 100% trên Etherscan Sepolia:** Minh bạch tuyệt đối, ai cũng có thể đọc và tương tác.
- **Cổng DApp trực tuyến:** [https://lehuy10012005-cmd.github.io/HCE-ScholarProof/](https://lehuy10012005-cmd.github.io/HCE-ScholarProof/)

---

### SLIDE 11: ĐÓNG GÓP THỰC TIỄN CHO ĐẠI HỌC KINH TẾ HUẾ
- **Đối với Sinh viên:** Tự tin công bố ý tưởng khởi nghiệp, đề cương NCKH mà không sợ bị sao chép; sở hữu chứng thư số để đưa vào CV học thuật.
- **Đối với Giảng viên & Nhà trường:** Công cụ minh bạch hóa quy trình nộp đề tài, chấm dứt tình trạng tranh chấp bản quyền nội bộ, nâng cao uy tín học thuật của Nhà trường trong thời đại kinh tế số.

---

### SLIDE 12: KẾT LUẬN & PHIÊN HỎI ĐÁP (Q&A)
- Đồ án hoàn thành **100% lộ trình từ Lab 8 đến Lab 15** theo chuẩn mực của học phần ECO2432.
- Nhóm sinh viên xin trân trọng cảm ơn Thầy **TS. Hà Ngọc Long** đã tận tình hướng dẫn và định hướng chuyên môn trong suốt quá trình thực hiện đồ án!
- **Kính mời Hội đồng đặt câu hỏi phản biện.**
