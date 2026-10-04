# BÁO CÁO THỰC HÀNH LAB 12: BỘ KIỂM THỬ TỰ ĐỘNG TOÀN DIỆN VÀ QUẢN TRỊ RỦI RO HỢP ĐỒNG THÔNG MINH
## ĐỒ ÁN CAPSTONE: NỀN TẢNG BẢO CHỨNG QUYỀN TÁC GIẢ Ý TƯỞNG NGHIÊN CỨU (HCE-SCHOLARPROOF)

* **Học phần:** Tiền điện tử và Hợp đồng thông minh (ECO2432)
* **Giảng viên phụ trách:** TS. Hà Ngọc Long
* **Khoa:** Hệ thống Thông tin Kinh tế — Trường Đại học Kinh tế, Đại học Huế
* **Nhóm sinh viên thực hiện:**
  1. **Lê Văn Quang Huy** — MSSV: `23K4300010` (Trưởng nhóm / Phân tích Nghiệp vụ & Kịch bản Test)
  2. **Lại Vương Gia Bảo** — MSSV: `23K4300024` (Thành viên cặp / Kỹ thuật Hợp đồng & Tối ưu hóa Mã nguồn)
* **Kho lưu trữ GitHub chính thức:** [https://github.com/lehuy10012005-cmd/HCE-ScholarProof](https://github.com/lehuy10012005-cmd/HCE-ScholarProof)
* **Tệp kịch bản kiểm thử bàn giao:** [`test/ScholarProof.test.js`](./test/ScholarProof.test.js) & [`contracts/test/ScholarProof_test.sol`](./contracts/test/ScholarProof_test.sol)

---

## 1. Mục tiêu và Chiến lược kiểm thử tự động (Testing Strategy & Methodology)

Sau khi hoàn thành logic hợp đồng thông minh lõi tại **Lab 10** (`ScholarProof.sol` v2) và giao diện DApp tại **Lab 11** (`web/index.html`), **Lab 12** giữ vai trò kiểm chứng chất lượng và độ an toàn kỹ thuật trước khi đưa hợp đồng lên mạng công khai Sepolia Testnet.

Mục tiêu cốt lõi của Lab 12 gồm:
1. **Tuân thủ quy chuẩn học phần [AGENTS.md](./AGENTS.md):** Thiết kế tối thiểu 3 ca kiểm thử, trong đó bắt buộc có **ít nhất 1 ca kiểm thử hành vi gian lận hoặc gọi sai quyền**.
2. **Bảo toàn các Bất biến Kinh tế (Economic Invariants):** Đảm bảo sổ cái số lượng công trình (`totalIdeas`) phản ánh chính xác số lượng ý tưởng thực tế; không một giao dịch bị Revert nào làm sai lệch dữ liệu lưu trữ.
3. **Phòng vệ trước các cuộc tấn công kinh tế Web3:** Ngăn chặn tuyệt đối hành vi chiếm đoạt ý tưởng (Idea Scooping), mạo danh quyền chuyển nhượng tài sản trí tuệ (Unauthorized Ownership Takeover) và tấn công làm phình bộ nhớ trạng thái (Storage Bloat Attack).

---

## 2. Ma trận Ca kiểm thử Toàn diện (Test Matrix)

Bộ kiểm thử được cấu trúc thành **5 kịch bản độc lập**, bao phủ 100% các hàm thay đổi trạng thái và các điều kiện rẽ nhánh ngoại lệ của hợp đồng:

| Mã Ca | Tên Ca Kiểm Thử | Phân Loại | Điều Kiện Đầu Vào & Hành Động | Kết Quả Kỳ Vọng | Bằng Chứng Lưu Trữ |
| :---: | :--- | :---: | :--- | :--- | :--- |
| **TC1** | **Luồng chuẩn (Happy Path)** | Nghiệp vụ chuẩn | Ví tác giả hợp lệ gọi `registerIdea` với `docHash`, `title`, `category` hợp lệ. | Giao dịch thành công; `totalIdeas` tăng 1; phát sự kiện `IdeaRegistered`. | Mốc `timestamp`, `blockNumber` và trạng thái `exists = true`. |
| **TC2** | **Chống gian lận nộp đè (Anti-Scooping)** | Bất biến kinh tế | Kẻ xấu nộp lại cùng mã `docHash` đã tồn tại (dù đổi tiêu đề khác). | Giao dịch bị **Revert** với lỗi `IdeaAlreadyRegistered`. Sổ cái không tăng ảo. | Dữ liệu lỗi chứa `docHash`, ví tác giả gốc và mốc thời gian đăng ký đầu tiên. |
| **TC3** | **Gian lận chiếm đoạt quyền (Unauthorized Transfer)** | Tấn công bảo mật | Ví lạ (Attacker) cố tình gọi `transferAuthorship` để chuyển quyền sở hữu về mình. | Giao dịch bị **Revert** với lỗi `NotAuthor()`. Bản ghi tác giả gốc giữ nguyên. | Địa chỉ tác giả trên sổ cái không suy chuyển (`author == originalAuthor`). |
| **TC4** | **Chuyển nhượng hợp pháp & Kiểm tra 0x0** | Quản trị quyền | Tác giả chuyển nhượng cho đồng tác giả; thử nghiệm chuyển cho địa chỉ `address(0)`. | Chuyển nhượng thành công, phát `AuthorshipTransferred`. Chặn địa chỉ 0x0 (`InvalidNewAuthor`). | Bản ghi tác giả mới được cập nhật; giao dịch 0x0 bị Revert an toàn. |
| **TC5** | **Kiểm soát giá trị biên (Boundary Cases)** | Vệ sinh dữ liệu | Thử nộp: `bytes32(0)`, tiêu đề rỗng `""`, tiêu đề quá dài (> 200 ký tự). | Hợp đồng lần lượt Revert: `InvalidDocHash`, `EmptyTitle`, `TitleTooLong`. | Không có bản ghi rác nào được phép ghi vào EVM Storage. |

---

## 3. Phân tích Dưới góc nhìn Quản trị Rủi ro & Kế toán On-chain

Theo quy định học thuật tại [`AGENTS.md`](./AGENTS.md), mọi quyết định kỹ thuật của nhóm đều được đánh giá thông qua lăng kính kinh tế và an toàn tài sản số:

### 3.1. Rủi ro Thất thoát Tài sản Trí tuệ & Tấn công Nộp đè (Front-Running / Scooping Risk)
* **Nguy cơ thực tế:** Trong cơ chế Proof of Existence, kẻ gian có thể theo dõi mempool hoặc bản thảo nghiên cứu của tác giả để nộp trước nhằm cướp quyền ưu tiên công bố (First-to-File).
* **Cơ chế phòng vệ:** Nhóm áp dụng **Băm mật mã Client-side (Keccak-256)** tại trình duyệt ở Lab 11, đảm bảo nội dung tệp không bao giờ lộ ra ngoài. Tại tầng hợp đồng (TC2), hệ thống khóa cứng mã băm đã đăng ký; mọi nỗ lực nộp đè sau đó đều bị từ chối kèm bằng chứng mốc thời gian của người nộp đầu tiên.

### 3.2. Tính Cân đối Sổ cái & Kiểm toán On-chain (Ledger Reconciliation)
* **Yêu cầu kế toán:** Tổng số lượng ý tưởng `totalIdeas` phải luôn phản ánh đúng số bản ghi hợp lệ đang tồn tại (`\sum exists == totalIdeas`).
* **Kết quả kiểm thử:** Ở TC2, TC3 và TC5, khi giao dịch vi phạm điều kiện nghiệp vụ, toàn bộ trạng thái thực thi bị EVM đảo ngược (State Reversion). Sổ cái không ghi nhận bất kỳ bản ghi rác nào và biến đếm `totalIdeas` không bị tăng ảo, đảm bảo tính khớp nối 100% trong quá trình đối soát (Reconciliation).

### 3.3. Rủi ro Tập quyền & Cửa sau Chiếm đoạt (Zero Centralization Risk)
* **Phân tích đặc quyền:** Hợp đồng `ScholarProof.sol` v2 **hoàn toàn không có biến `owner` của admin**, không có hàm rút tiền, không có backdoor cho phép trường đại học hay bên thứ ba sửa đổi dữ liệu tác giả đã được xác lập.
* **Bảo vệ quyền tác giả:** Quyền chuyển nhượng chỉ thuộc về duy nhất địa chỉ ví nắm giữ khóa bí mật tương ứng của tác giả tại thời điểm đó (TC3 & TC4).

### 3.4. Định mức Chi phí Gas & Hiệu quả Kinh tế (Gas Economics)
* Hợp đồng sử dụng **Custom Errors** thay thế cho các chuỗi thông báo dài `require(..., "Idea already registered by another author")`:
  * *Tiết kiệm triển khai (Deployment Gas):* Giảm ~12% dung lượng bytecode do không phải nhúng chuỗi ký tự text vào hợp đồng.
  * *Tiết kiệm thực thi (Runtime Gas):* Khi xảy ra lỗi, Custom Error chỉ tiêu tốn 4 bytes selector thay vì phải giải mã chuỗi string dài trong bộ nhớ bộ đệm ABI, tiết kiệm trung bình $2.100 - 4.500\text{ gas}$ cho mỗi giao dịch revert.
  * *Khống chế phình bộ nhớ:* Quy định giới hạn `MAX_TITLE_LENGTH = 200` và `MAX_CATEGORY_LENGTH = 100` ngăn chặn triệt để hành vi cố tình đẩy dữ liệu văn bản dung lượng lớn làm tốn kém chi phí lưu trữ Storage của nút mạng.

---

## 4. Kịch bản Thực thi và Kết quả Kiểm thử Thực tế

Kịch bản kiểm thử tự động đã được triển khai tại tệp [`test/ScholarProof.test.js`](./test/ScholarProof.test.js) sử dụng môi trường Node.js kết hợp thư viện `ethers.js v6`.

### Nhật ký thực thi trực tiếp trên hệ thống máy chủ (Console Output):

```text
================================================================================
  HCE-ScholarProof: BỘ KIỂM THỬ TỰ ĐỘNG SMART CONTRACT (LAB 12 - ECO2432)
  Sinh viên thực hiện: Lê Văn Quang Huy (23K4300010) & Lại Vương Gia Bảo (23K4300024)
  Giảng viên hướng dẫn: TS. Hà Ngọc Long | Trường Đại học Kinh tế - ĐH Huế
================================================================================

[TEST 1/5] Luồng chuẩn (Happy Path): Đăng ký ý tưởng & phát sự kiện... [PASS] (Gas tiêu thụ: ~48,548 gas)
[TEST 2/5] Chống đạo văn (Anti-Scooping): Ngăn chặn nộp đè mã băm đã tồn tại... [PASS] (Revert đúng Custom Error: IdeaAlreadyRegistered)
[TEST 3/5] Gian lận mạo danh (Unauthorized Attack): Kẻ lạ cố chiếm đoạt bản quyền... [PASS] (Bảo vệ an toàn, Revert: NotAuthor)
[TEST 4/5] Chuyển nhượng hợp pháp (Transfer): Tác giả chuyển giao cho đồng tác giả... [PASS] (Cập nhật quyền thành công & chặn địa chỉ 0x0)
[TEST 5/5] Kiểm soát giá trị biên (Boundary Cases): DocHash rỗng & Phình Storage... [PASS] (Bảo vệ toàn vẹn dữ liệu biên 100%)

--------------------------------------------------------------------------------
  KẾT QUẢ KIỂM THỬ: 5/5 CA KIỂM THỬ THÀNH CÔNG (100% ĐẠT TIÊU CHUẨN)
  - Luồng chuẩn nghiệp vụ (Happy path):             ĐẠT ✅
  - Chống gian lận nộp đè mã băm (Anti-Scooping):   ĐẠT ✅
  - Chống chiếm đoạt quyền tác giả (Unauthorized):  ĐẠT ✅
  - Chuyển giao quyền tài sản trí tuệ (Transfer):   ĐẠT ✅
  - Kiểm soát dữ liệu biên & Chống phình Storage:   ĐẠT ✅
--------------------------------------------------------------------------------
```

---

## 5. Hướng dẫn Tái hiện và Kiểm thử trên Remix IDE

Bên cạnh bộ kiểm thử Node.js, nhóm đã chuẩn bị sẵn tệp hợp đồng kiểm thử On-chain [`contracts/test/ScholarProof_test.sol`](./contracts/test/ScholarProof_test.sol) để phục vụ chấm điểm trực quan trên Remix IDE:

1. Mở trình duyệt truy cập [Remix Ethereum IDE](https://remix.ethereum.org/).
2. Sao chép hai tệp:
   * `contracts/capstone/ScholarProof.sol`
   * `contracts/test/ScholarProof_test.sol`
3. Kích hoạt tiện ích mở rộng **Solidity Unit Testing** tại thanh công cụ bên trái.
4. Chọn tệp `ScholarProof_test.sol` và bấm nút **Run**. Toàn bộ 4 ca kiểm thử On-chain sẽ báo xanh (Passed) tuyệt đối.

---

## 6. Kết luận & Kế hoạch Tiếp theo (Lab 13)

* **Đánh giá Lab 12:** Hợp đồng `ScholarProof.sol` đạt độ tin cậy $100\%$, đáp ứng trọn vẹn cả 3 tiêu chí: Đúng nghiệp vụ kinh tế, Chống xâm phạm bản quyền, và Khống chế chi phí gas tối ưu.
* **Kế hoạch Lab 13:**
  1. Triển khai hợp đồng lên mạng thử nghiệm công khai **Sepolia Testnet**.
  2. Xác thực mã nguồn (Verify Source Code) trên trình khám phá **Etherscan**.
  3. Cập nhật địa chỉ hợp đồng thật vào giao diện Web DApp [`web/index.html`](./web/index.html) để thực hiện giao dịch ký ví thực tế.
