# BẢN ĐĂNG KÝ CẶP VÀ CHỦ ĐỀ ĐỒ ÁN CAPSTONE (ECO2432)

* **Học phần:** Tiền điện tử & Hợp đồng thông minh (ECO2432)
* **Giảng viên phụ trách:** TS. Hà Ngọc Long
* **Khoa:** Hệ thống Thông tin Kinh tế — Trường Đại học Kinh tế, Đại học Huế
* **Hạn nộp đăng ký:** Học kỳ I — Năm học 2026
* **Kho lưu trữ nhóm chính thức:** [https://github.com/lehuy10012005-cmd/HCE-ScholarProof](https://github.com/lehuy10012005-cmd/HCE-ScholarProof)

---

## 1. Thông tin hai thành viên trong cặp
1. **Lê Văn Quang Huy**
   * Mã sinh viên: **23K4300010**
   * Lớp: K57 Kinh Tế Số
   * Email: `lehuy10012005@gmail.com`
   * Địa chỉ ví thử nghiệm Sepolia: `0xB07FB0761c33a01F7f7493A6a8a9667F4842Fd50`
   * Vai trò chính: Trưởng nhóm / Quản trị Repo GitHub / Kỹ sư Hợp đồng Thông minh & Đặc tả Nghiệp vụ
2. **Lại Vương Gia Bảo**
   * Mã sinh viên: **23K4300024**
   * Lớp: K57 Kinh Tế Số
   * Email: `bao9d4tpsh@gmail.com`
   * Vai trò chính: Thành viên cặp / Kỹ sư Kiểm thử Tự động & Giao diện Web3 DApp

---

## 2. Chủ đề đồ án lựa chọn
* **Chủ đề:** **Chủ đề 8 — Ghi nhận quyền tác giả của ý tưởng nghiên cứu khoa học (Proof of Authorship & Research Idea Timestamping)**
* *(Căn cứ theo danh mục 10 chủ đề phù hợp sinh viên năm 3 tại Phần N, Trang 48–49 — Sổ tay thực hành ECO2432)*
* **Mức độ:** Vừa

---

## 3. Tên chính thức của sản phẩm
* **Tên tiếng Anh:** **HCE-ScholarProof** *(Decentralized Research & Idea Provenance Platform)*
* **Tên tiếng Việt:** Nền tảng Ghi nhận và Bảo chứng Quyền tác giả Ý tưởng Nghiên cứu Khoa học trên Blockchain

---

## 4. Tuyên ngôn định vị sản phẩm (Value Proposition)
> **“Nhóm xây dựng HCE-ScholarProof cho sinh viên, giảng viên và các nhà nghiên cứu trẻ Trường Đại học Kinh tế để xác lập bằng chứng ưu tiên quyền sở hữu trí tuệ bất biến (Proof of Existence) cho các ý tưởng nghiên cứu, đề cương khoa học và tập dữ liệu ban đầu trên blockchain với chi phí vi mô, ngăn chặn hoàn toàn nguy cơ bị chiếm đoạt ý tưởng (Scooping) mà không cần bộc lộ nội dung bí mật ra công chúng.”**

---

## 5. Luồng nghiệp vụ cốt lõi cam kết demo
1. **Băm dữ liệu ngoài chuỗi & Giữ bí mật nội dung (Off-chain Hashing & Privacy-Preserving):**
   * Tác giả tải tệp đề cương nghiên cứu / tài liệu ý tưởng (PDF, DOCX, Code, CSV) lên giao diện Web3.
   * Trình duyệt tự động tính toán mã băm mật mã chuẩn **SHA-256 / Keccak-256** của tệp ngay tại máy client mà **không gửi nội dung tài liệu lên máy chủ** (bảo đảm an toàn tuyệt đối cho ý tưởng sơ khởi).
2. **Đăng ký bản quyền on-chain & Ghi dấu thời gian (On-chain Registration & Block Timestamping):**
   * Tác giả kết nối ví MetaMask và ký giao dịch gửi mã băm `bytes32 docHash` kèm siêu dữ liệu (Tiêu đề, Tóm tắt ngắn, Mã ngành nghiên cứu) vào Smart Contract `ScholarProof.sol`.
   * Hợp đồng kiểm tra tính duy nhất của mã băm:
     * Nếu mã băm chưa từng tồn tại: Ghi nhận quyền tác giả cho địa chỉ ví `msg.sender` cùng mốc thời gian khách quan bất biến của mạng lưới (`block.timestamp`, `block.number`), phát ra sự kiện `IdeaRegistered`.
     * Nếu mã băm đã được đăng ký trước đó: Giao dịch bị đảo ngược (`revert`) với lỗi `IdeaAlreadyRegistered`, trả về danh tính ví của tác giả nộp trước và mốc thời gian lịch sử để chứng minh quyền ưu tiên (Prior Art).
3. **Tra cứu & Thẩm định quyền tác giả (Public Verification & Dispute Resolution):**
   * Bất kỳ hội đồng khoa học hoặc bên thứ ba nào cũng có thể tải một tài liệu nghi vấn lên hệ thống để hệ thống tự động băm và tra cứu on-chain.
   * Nếu mã băm trùng khớp: Hệ thống xuất chứng thư số bảo chứng (Digital Certificate of Provenance) khẳng định tác giả đầu tiên đã ghi nhận ý tưởng vào ngày, giờ, khối giao dịch chính xác trên blockchain.

---

## 6. Kế hoạch phối hợp nhóm (Roadmap 4 Tuần)
* **Tuần 1 (Lab 8 - 9):** Hoàn tất hồ sơ đăng ký đề tài, thiết lập quy ước nhóm `AGENTS.md`, hoàn thiện bản đặc tả nghiệp vụ `SPEC.md` và máy trạng thái quản lý ý tưởng. *(Phụ trách: Lê Văn Quang Huy)*
* **Tuần 2 (Lab 10 - 11):** Lập trình hợp đồng thông minh `ScholarProof.sol` (Solidity ^0.8.20), áp dụng OpenZeppelin v5, CEI pattern, Custom Errors; xây dựng bộ kiểm thử tự động với tối thiểu 3 ca (chuẩn, gian lận tranh chấp, ca biên). *(Phụ trách: Lê Huy phối hợp Gia Bảo)*
* **Tuần 3 (Lab 12 - 13):** Xây dựng giao diện Web3 DApp kết nối Ethers.js v6: băm file client-side, kết nối MetaMask, nộp hash và tra cứu thẩm định. *(Phụ trách: Lại Vương Gia Bảo)*
* **Tuần 4 (Lab 14 - 15):** Triển khai hợp đồng lên Sepolia Testnet, thẩm định chi phí gas thực tế, xác thực mã nguồn trên Etherscan, hoàn thiện slide báo cáo và video demo. *(Cả hai thành viên)*
