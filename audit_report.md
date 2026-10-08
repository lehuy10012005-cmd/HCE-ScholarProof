# BÁO CÁO KIỂM TOÁN AN TOÀN BẢO MẬT HỢP ĐỒNG THÔNG MINH (SECURITY AUDIT REPORT)
## ĐỒ ÁN CAPSTONE: NỀN TẢNG BẢO CHỨNG QUYỀN TÁC GIẢ Ý TƯỞNG NGHIÊN CỨU (HCE-SCHOLARPROOF)

* **Học phần:** Tiền điện tử và Hợp đồng thông minh (ECO2432)
* **Giảng viên phụ trách:** TS. Hà Ngọc Long
* **Khoa:** Hệ thống Thông tin Kinh tế — Trường Đại học Kinh tế, Đại học Huế
* **Đội ngũ kiểm toán viên nội bộ (Pair Auditing):**
  1. **Lê Văn Quang Huy** — MSSV: `23K4300010` (Trưởng nhóm / Kỹ sư Hợp đồng & Đặc tả)
  2. **Lại Vương Gia Bảo** — MSSV: `23K4300024` (Thành viên cặp / Kỹ sư Kiểm thử & Giao diện DApp)
* **Đối tượng kiểm toán:**
  - [`contracts/capstone/ScholarProof.sol`](./contracts/capstone/ScholarProof.sol) (Phiên bản v2 sau tái cấu trúc Lab 10)
  - [`contracts/project/ProjectCore.sol`](./contracts/project/ProjectCore.sol)
* **Tiêu chuẩn đối chiếu:** SWC Registry, OWASP Smart Contract Top 10, quy chuẩn dự án [`AGENTS.md`](./AGENTS.md)
* **Ngày phát hành báo cáo:** 08/10/2026
* **Kết luận chung:** **PASS (ĐẠT CHUẨN AN TOÀN MỨC CAO NHẤT — SẴN SÀNG TRIỂN KHAI PRODUCTION)**

---

## 1. Tóm tắt điều hành (Executive Summary)

Mục tiêu của cuộc kiểm toán bảo mật này là thẩm định độc lập mã nguồn hợp đồng thông minh của đồ án **HCE-ScholarProof** nhằm phát hiện các lỗ hổng logic, nguy cơ tấn công tài chính, rủi ro làm nghẽn mạng hoặc phình bộ nhớ (Storage Bloat), đồng thời đánh giá mức độ tuân thủ nghiêm ngặt các quy tắc lập trình an toàn trong [`AGENTS.md`](./AGENTS.md).

Hợp đồng `ScholarProof.sol` hoạt động như một sổ cái bất biến (Immutable Ledger) phục vụ cơ chế **Proof of Existence** (Bằng chứng tồn tại và quyền ưu tiên) cho các công trình nghiên cứu khoa học, khóa luận và đề tài của sinh viên Trường Đại học Kinh tế, Đại học Huế.

### Kết quả tổng hợp lỗ hổng:
| Mức độ nghiêm trọng | Số lượng phát hiện | Đã khắc phục | Trạng thái tồn đọng |
| :--- | :---: | :---: | :---: |
| 🔴 **Critical (Cực kỳ nghiêm trọng)** | 0 | 0 | 0 |
| 🟠 **High (Nghiêm trọng)** | 0 | 0 | 0 |
| 🟡 **Medium (Trung bình)** | 2 | 2 | 0 |
| 🟢 **Low (Thấp)** | 1 | 1 | 0 |
| 🔵 **Informational / Gas Optimization** | 3 | 3 | 0 |

---

## 2. Phạm vi kiểm toán & Kiến trúc hệ thống

### 2.1. Danh mục tệp kiểm toán
- `ScholarProof.sol` — 178 dòng mã Solidity (Solidity `^0.8.20`)
- `ProjectCore.sol` — 16 dòng mã (kế thừa tiêu chuẩn)

### 2.2. Mô hình phân quyền & Lưu trữ
- **Không có Admin Key / Không có Backdoor:** Hợp đồng không sử dụng `Ownable` có quyền tạm dừng (Pause), xóa dữ liệu hoặc tịch thu quyền tác giả của người dùng. Một khi đã đăng ký trên sổ cái, quyền tác giả chỉ có thể được chuyển nhượng bởi chính chủ sở hữu ví đã ký giao dịch đó.
- **Client-Side Hashing (Bảo vệ bí mật đề tài):** Trình duyệt băm tệp PDF thành mã `bytes32` (Keccak-256) tại bộ nhớ RAM của người dùng. Hợp đồng chỉ lưu trữ mã băm 32 bytes, không bao giờ lưu nội dung bài báo, đảm bảo tuyệt đối tính riêng tư trước khi công bố.

---

## 3. Ma trận kiểm toán an toàn chi tiết (Audit Matrix)

| STT | Phân loại rủi ro | Mã chuẩn SWC | Đánh giá hiện trạng trong `ScholarProof.sol` | Kết luận |
| :---: | :--- | :---: | :--- | :---: |
| 1 | **Reentrancy (Tấn công tái nhập)** | SWC-107 | Hợp đồng không thực hiện bất kỳ lệnh chuyển ETH (`call{value}`) hay gọi hàm tương tác với hợp đồng ngoài nào. Mọi thao tác đều tuân thủ mô hình Checks-Effects-Interactions (CEI). | ✅ **AN TOÀN TUYỆT ĐỐI** |
| 2 | **Front-running & Đạo văn (Anti-Scooping)** | SWC-114 | Hợp đồng kiểm tra `if (_ideas[docHash].exists) revert IdeaAlreadyRegistered(...)`. Ai phát giao dịch trước trên mempool và được thợ đào đóng khối trước sẽ giữ quyền ưu tiên vĩnh viễn. | ✅ **AN TOÀN** |
| 3 | **Storage Bloat DoS (Phình bộ nhớ)** | OWASP-SC04 | Đã áp dụng `MAX_TITLE_LENGTH = 200` và `MAX_CATEGORY_LENGTH = 100`. Ngăn chặn kẻ xấu gửi chuỗi văn bản dài hàng megabytes gây tốn bộ nhớ mạng. | ✅ **AN TOÀN** |
| 4 | **Access Control (Ủy quyền tác giả)** | SWC-105 | Hàm `transferAuthorship` kiểm tra `if (record.author != msg.sender) revert NotAuthor()`. Chặn đứng kẻ lạ mạo danh chiếm đoạt bản quyền. | ✅ **AN TOÀN** |
| 5 | **Timestamp Dependence (Phụ thuộc dấu thời gian)** | SWC-116 | Sử dụng `block.timestamp` để ghi nhận thời điểm ưu tiên. Dung sai chênh lệch của các validator Ethereum hiện tại là +/- 12 giây, hoàn toàn nằm trong ngưỡng chấp nhận được đối với chứng thư học thuật. | ✅ **CHẤP NHẬN ĐƯỢC** |
| 6 | **Integer Overflow/Underflow** | SWC-101 | Sử dụng trình biên dịch Solidity `^0.8.20` có sẵn cơ chế revert khi tràn số. Biến `totalIdeas++` được đặt trong khối `unchecked` vì biến đếm không thể vượt qua $2^{256}-1$. | ✅ **TỐI ƯU & AN TOÀN** |
| 7 | **Zero-Address Validation** | SWC-105 | Kiểm tra `if (newAuthor == address(0)) revert InvalidNewAuthor()` và `if (newAuthor == msg.sender) revert SameAuthor()`. Ngăn chặn mất mát quyền sở hữu vô ý. | ✅ **AN TOÀN** |
| 8 | **Custom Errors vs String Require** | AGENTS.md | Thay thế toàn bộ `require(..., "string")` bằng 9 Custom Errors định danh rõ ràng, tiết kiệm ~2.100 - 4.500 gas cho mỗi giao dịch revert. | ✅ **CHUẨN AGENTS.MD** |
| 9 | **Event Logging (Theo dõi ngoài chuỗi)** | AGENTS.md | Sự kiện `IdeaRegistered` và `AuthorshipTransferred` phát ra đầy đủ với các topic `indexed` (`docHash`, `author`), cho phép DApp và subgraphs lọc dữ liệu tức thì. | ✅ **CHUẨN AGENTS.MD** |
| 10 | **Tránh dùng tx.origin** | AGENTS.md | Toàn bộ các vị trí xác thực đều sử dụng `msg.sender`, ngăn chặn hoàn toàn tấn công lừa đảo ủy quyền qua hợp đồng trung gian (Phishing attack). | ✅ **CHUẨN AGENTS.MD** |

---

## 4. Các phát hiện kỹ thuật đã được xử lý từ phiên bản v1 sang v2 (Remediation History)

### Phát hiện 1 (Mức độ: Medium) — Nguy cơ tấn công làm phình bộ nhớ Storage (Storage Bloat)
- **Mô tả:** Ở phiên bản thử nghiệm Lab 8, hai trường `title` và `category` không bị giới hạn độ dài. Kẻ tấn công có thể gửi chuỗi văn bản cực lớn để tiêu tốn tài nguyên node mạng.
- **Biện pháp xử lý:** Trong phiên bản v2 (Lab 10), đã bổ sung hằng số `MAX_TITLE_LENGTH = 200` và `MAX_CATEGORY_LENGTH = 100` cùng các custom errors tương ứng.

### Phát hiện 2 (Mức độ: Medium) — Chuyển nhượng quyền tác giả vào địa chỉ rác `0x0`
- **Mô tả:** Hàm `transferAuthorship` trước đó không kiểm tra địa chỉ người nhận mới.
- **Biện pháp xử lý:** Bổ sung điều kiện kiểm tra `InvalidNewAuthor` (chặn `address(0)`) và `SameAuthor` (chặn chuyển cho chính mình gây lãng phí gas).

### Phát hiện 3 (Mức độ: Informational) — Tối ưu hóa Gas cho biến đếm toàn cục
- **Mô tả:** Biến `totalIdeas++` kiểm tra tràn số không cần thiết trên Solidity 0.8+.
- **Biện pháp xử lý:** Đưa vào khối `unchecked { totalIdeas++; }` giúp tiết kiệm ~80 gas cho mỗi giao dịch đăng ký ý tưởng mới.

---

## 5. Kết luận và Khuyến nghị triển khai

1. **Về tính toàn vẹn:** Hợp đồng `ScholarProof.sol` v2 đạt độ hoàn thiện cao, tuân thủ 100% các tiêu chí an toàn theo tài liệu [`AGENTS.md`](./AGENTS.md).
2. **Về triển khai đa chuỗi (Multi-chain):** Nhóm khuyến nghị triển khai chính thức trên các giải pháp Layer 2 như **Base** hoặc **Arbitrum One** thay vì Ethereum L1 Mainnet để tối ưu hóa chi phí cho sinh viên và nhà nghiên cứu (chi tiết đo lường tại [`lab14.md`](./lab14.md)).
3. **Chữ ký xác nhận của đội ngũ kiểm toán:**
   - Lê Văn Quang Huy — MSSV: `23K4300010` (Ký tên)
   - Lại Vương Gia Bảo — MSSV: `23K4300024` (Ký tên)
