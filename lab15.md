# BÁO CÁO THỰC HÀNH LAB 15: NGHIỆM THU ĐỒ ÁN CAPSTONE, XÁC THỰC MÃ NGUỒN VÀ BẢO VỆ SẢN PHẨM CUỐI KỲ
## ĐỒ ÁN CAPSTONE: NỀN TẢNG BẢO CHỨNG QUYỀN TÁC GIẢ Ý TƯỞNG NGHIÊN CỨU (HCE-SCHOLARPROOF)

* **Học phần:** Tiền điện tử và Hợp đồng thông minh (ECO2432)
* **Giảng viên phụ trách:** TS. Hà Ngọc Long
* **Khoa:** Hệ thống Thông tin Kinh tế — Trường Đại học Kinh tế, Đại học Huế
* **Nhóm sinh viên thực hiện:**
  1. **Lê Văn Quang Huy** — MSSV: `23K4300010` (Trưởng nhóm / Kỹ sư Hợp đồng & Đặc tả)
  2. **Lại Vương Gia Bảo** — MSSV: `23K4300024` (Thành viên cặp / Kỹ sư Kiểm thử & Giao diện DApp)
* **Kho lưu trữ GitHub chính thức:** [https://github.com/lehuy10012005-cmd/HCE-ScholarProof](https://github.com/lehuy10012005-cmd/HCE-ScholarProof)
* **Cổng DApp trực tuyến:** [https://lehuy10012005-cmd.github.io/HCE-ScholarProof/](https://lehuy10012005-cmd.github.io/HCE-ScholarProof/)
* **Địa chỉ hợp đồng Sepolia:** `0xa2F53106B3dFdf23b6b158022646d231A21e49cb`
* **Sản phẩm bàn giao Lab 15:**
  - Tài liệu triển khai & vận hành: [`DEPLOYMENT.md`](./DEPLOYMENT.md)
  - Kịch bản slide thuyết trình bảo vệ trước Hội đồng: [`SLIDES.md`](./SLIDES.md)
  - Báo cáo tổng kết nghiệm thu đồ án: [`lab15.md`](./lab15.md)

---

## 1. Mục tiêu và Ý nghĩa của Lab 15 (Chặng cuối Capstone)

**Lab 15 là cột mốc tổng kết và nghiệm thu toàn diện toàn bộ đồ án Capstone** của học phần Tiền điện tử & Hợp đồng thông minh (ECO2432). 

Sau hành trình trải dài qua 8 tuần thực hành chuyên sâu (từ Lab 8 đến Lab 15), nhóm sinh viên đã đưa một ý tưởng bài toán thực tiễn tại Trường Đại học Kinh tế, Đại học Huế trở thành một **sản phẩm Web3 hoàn chỉnh**, hoạt động ổn định trên mạng blockchain công khai, có đầy đủ kiểm thử tự động, kiểm toán bảo mật, tài liệu nghiệp vụ BA và giao diện DApp chuẩn phong cách học thuật.

**Ba mục tiêu cốt lõi của Lab 15:**
1. **Nghiệm thu sản phẩm kỹ thuật:** Kiểm tra lần cuối tính toàn vẹn của mã nguồn trên GitHub, tính khả dụng của DApp trên GitHub Pages và tính xác thực của Smart Contract trên Sepolia Etherscan.
2. **Bàn giao tài liệu vận hành và thuyết trình:** Hoàn thiện [`DEPLOYMENT.md`](./DEPLOYMENT.md) phục vụ việc chuyển giao hệ thống cho Khoa HTTT Kinh tế và [`SLIDES.md`](./SLIDES.md) phục vụ buổi báo cáo trước TS. Hà Ngọc Long và Hội đồng chấm thi.
3. **Đánh giá tổng kết & Bài học kinh nghiệm:** Đối chiếu kết quả đạt được với các cam kết ban đầu tại [`TOPIC_REGISTRATION.md`](./TOPIC_REGISTRATION.md) và đúc kết năng lực làm chủ công nghệ Web3 trong kỷ nguyên AI.

---

## 2. Bảng Tổng kết Nghiệm thu Lộ trình Đồ án (Lab 8 – Lab 15)

| Giai đoạn | Sản phẩm bàn giao chính | Nội dung kỹ thuật & Đóng góp | Trạng thái nghiệm thu |
| :---: | :--- | :--- | :---: |
| **Lab 8** | [`TOPIC_REGISTRATION.md`](./TOPIC_REGISTRATION.md)<br>[`lab08.md`](./lab08.md)<br>[`ScholarProof.sol`](./contracts/capstone/ScholarProof.sol) | Xác lập đề tài Chủ đề 8, kiến trúc cơ chế Proof of Existence, băm mật mã client-side trong RAM | ✅ **ĐẠT XUẤT SẮC** |
| **Lab 9** | [`SPEC.md`](./SPEC.md)<br>[`lab09.md`](./lab09.md)<br>[`contracts/training/TimeLockVault.sol`](./contracts/training/TimeLockVault.sol) | Xây dựng đặc tả nghiệp vụ BA chi tiết, thiết kế máy trạng thái và ma trận quản trị rủi ro | ✅ **ĐẠT XUẤT SẮC** |
| **Lab 10** | [`lab10.md`](./lab10.md)<br>[`ScholarProof.sol`](./contracts/capstone/ScholarProof.sol) (v2)<br>[`ProjectCore.sol`](./contracts/project/ProjectCore.sol) | Rà soát mã nguồn do AI sinh ra, giải mã Storage Slot 2 (VaultBuggy), nâng cấp phiên bản v2 an toàn | ✅ **ĐẠT XUẤT SẮC** |
| **Lab 11** | [`web/index.html`](./web/index.html)<br>[`lab11.md`](./lab11.md) | Xây dựng DApp Web3: Băm Keccak-256 client-side, kết nối ví MetaMask, xuất Chứng thư số A4 | ✅ **ĐẠT XUẤT SẮC** |
| **Lab 12** | [`test/ScholarProof.test.js`](./test/ScholarProof.test.js)<br>[`lab12.md`](./lab12.md) | Bộ kiểm thử tự động 5/5 ca test: Happy path, chống gian lận nộp đè mã băm, phân quyền chuyển nhượng | ✅ **ĐẠT XUẤT SẮC** |
| **Lab 13** | [`web/index.html`](./web/index.html)<br>[`lab13.md`](./lab13.md)<br>Sepolia Contract Verified | Triển khai Sepolia Testnet, xác thực mã nguồn Etherscan, tích hợp luồng ký ví và đối soát sự kiện | ✅ **ĐẠT XUẤT SẮC** |
| **Lab 14** | [`audit_report.md`](./audit_report.md)<br>[`lab14.md`](./lab14.md)<br>[`scripts/gas_benchmark.py`](./scripts/gas_benchmark.py) | Kiểm toán bảo mật chuẩn OWASP/SWC, đo lường chi phí Gas Layer 2 (Base/Arbitrum) tiết kiệm 99.74% | ✅ **ĐẠT XUẤT SẮC** |
| **Lab 15** | [`DEPLOYMENT.md`](./DEPLOYMENT.md)<br>[`SLIDES.md`](./SLIDES.md)<br>[`lab15.md`](./lab15.md) | Bàn giao tài liệu vận hành hệ thống, slide thuyết trình bảo vệ trước Hội đồng, hoàn tất 100% đồ án | ✅ **ĐẠT XUẤT SẮC** |

---

## 3. Checklist Tuân thủ Chuẩn mực Dự án (`AGENTS.md`)

Nhóm sinh viên tự hào khẳng định toàn bộ hệ thống tuân thủ **100% các điều khoản bắt buộc** trong [`AGENTS.md`](./AGENTS.md):

- [x] **Solidity `^0.8.20`:** Sử dụng phiên bản Solidity mới nhất có tích hợp kiểm tra tràn số tự động.
- [x] **Mọi hàm thay đổi trạng thái đều phát `event`:** Sự kiện `IdeaRegistered` và `AuthorshipTransferred` phát ra đầy đủ với các topic indexed phục vụ lọc ngoài chuỗi.
- [x] **Mọi hàm phân quyền đều kiểm tra rõ ràng:** Hàm `transferAuthorship` xác thực nghiêm ngặt `msg.sender == record.author`.
- [x] **Mô hình Checks - Effects - Interactions (CEI):** Kiểm tra điều kiện hợp lệ trước, cập nhật storage, sau đó mới phát event.
- [x] **Ưu tiên Custom Errors:** Sử dụng 9 Custom Errors định danh rõ ràng thay cho chuỗi `require` dài, tiết kiệm gas tối đa.
- [x] **Không dùng `tx.origin`:** Toàn bộ việc xác thực danh tính đều căn cứ vào `msg.sender`.
- [x] **Không chứa Admin Backdoor:** Hệ thống hoàn toàn phi tập trung, không có cơ chế đóng băng hay thu hồi quyền tác giả tùy tiện.
- [x] **Quy chuẩn mã nguồn Python:** Kịch bản [`scripts/gas_benchmark.py`](./scripts/gas_benchmark.py) không hardcode khóa API, đọc từ biến môi trường, đổi wei sang ETH trước khi hiển thị, chú thích tiếng Việt không dấu.
- [x] **Nhật ký AI minh bạch (`AI_JOURNAL.md`):** Ghi chép đầy đủ 15 lần làm việc với AI, nêu rõ các lỗi do sinh viên trực tiếp phát hiện và chấn chỉnh.

---

## 4. Kế hoạch Phát triển Sau Môn học (Future Roadmap)

1. **Giai đoạn 1 (Q4/2026):** Đề xuất Hội đồng Khoa học Trường Đại học Kinh tế, Đại học Huế thử nghiệm áp dụng HCE-ScholarProof cho đợt bảo vệ Khóa luận tốt nghiệp K57.
2. **Giai đoạn 2 (Q1/2027):** Triển khai chính thức lên mạng chính Layer 2 **Base Network** để tối ưu hóa chi phí (~334 VNĐ/lượt đăng ký) và phát hành thẻ căn cước học thuật dạng Soulbound Token (SBT) cho sinh viên HCE.
3. **Giai đoạn 3 (Q2/2027):** Tích hợp công nghệ Zero-Knowledge Proofs (ZKP) cho phép thẩm định tính tương đồng giữa hai tài liệu mà không cần giải mã bất kỳ đoạn văn bản nào.

---

## 5. Lời Cảm Ơn

Nhóm sinh viên thực hiện đồ án xin bày tỏ lòng biết ơn sâu sắc đến Thầy **TS. Hà Ngọc Long** — Giảng viên phụ trách học phần Tiền điện tử và Hợp đồng thông minh (ECO2432). Thầy không chỉ truyền đạt những kiến thức học thuật chuyên sâu về mật mã học và kinh tế học blockchain, mà còn rèn luyện cho sinh viên tư duy phản biện sắc bén khi làm việc cùng các mô hình trí tuệ nhân tạo (AI), tạo tiền đề vững chắc cho hành trang nghề nghiệp của chúng em trong kỷ nguyên kinh tế số.
