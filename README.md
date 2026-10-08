# HCE-ScholarProof — Nền tảng Ghi nhận & Bảo chứng Quyền tác giả Ý tưởng Nghiên cứu Khoa học trên Blockchain

> **Đồ án Capstone môn học:** Tiền điện tử và Hợp đồng thông minh (ECO2432)  
> **Khoa:** Hệ thống Thông tin Kinh tế — Trường Đại học Kinh tế, Đại học Huế  
> **Giảng viên hướng dẫn:** TS. Hà Ngọc Long  
> **Kho lưu trữ chính thức:** [https://github.com/lehuy10012005-cmd/HCE-ScholarProof](https://github.com/lehuy10012005-cmd/HCE-ScholarProof)  
> **Website DApp trực tuyến (Live Demo):** [https://lehuy10012005-cmd.github.io/HCE-ScholarProof/](https://lehuy10012005-cmd.github.io/HCE-ScholarProof/)

---

## 👥 Nhóm sinh viên thực hiện (Cặp 2 sinh viên)

| STT | Họ và tên sinh viên | Mã sinh viên | Lớp | Vai trò dự án | Email |
| :---: | :--- | :---: | :---: | :--- | :--- |
| 1 | **Lê Văn Quang Huy** | `23K4300010` | K57 Kinh Tế Số | **Trưởng nhóm** / Kỹ sư Hợp đồng Thông minh & Đặc tả Nghiệp vụ | `lehuy10012005@gmail.com` |
| 2 | **Lại Vương Gia Bảo** | `23K4300024` | K57 Kinh Tế Số | **Thành viên cặp** / Kỹ sư Kiểm thử Tự động & Giao diện Web3 DApp | `bao9d4tpsh@gmail.com` |

---

## 🎯 Giới thiệu Đề tài Đồ án Capstone

* **Chủ đề lựa chọn:** **Chủ đề 8 — Ghi nhận quyền tác giả của ý tưởng nghiên cứu khoa học (Proof of Authorship & Idea Timestamping)**  
  *(Căn cứ theo danh mục 10 chủ đề tại Phần N, Trang 48–49 — Sổ tay thực hành ECO2432)*
* **Tên sản phẩm:** **HCE-ScholarProof**
* **Tuyên ngôn định vị giá trị (Value Proposition):**
  > *“Nhóm xây dựng HCE-ScholarProof cho sinh viên, giảng viên và các nhà nghiên cứu trẻ Trường Đại học Kinh tế để xác lập bằng chứng ưu tiên quyền sở hữu trí tuệ bất biến (Proof of Existence) cho các ý tưởng nghiên cứu, đề cương khoa học và tập dữ liệu ban đầu trên blockchain với chi phí vi mô, ngăn chặn hoàn toàn nguy cơ bị chiếm đoạt ý tưởng (Scooping) mà không cần bộc lộ nội dung bí mật ra công chúng.”*
* **Hồ sơ đăng ký chi tiết:** Xem tệp [`TOPIC_REGISTRATION.md`](./TOPIC_REGISTRATION.md)

---

## 📂 Danh mục sản phẩm & Lộ trình triển khai Đồ án (Lab 8 – 15)

| Giai đoạn | Sản phẩm bàn giao | Mô tả nghiệp vụ & Kỹ thuật | Trạng thái |
| :---: | :--- | :--- | :---: |
| **Lab 8** | [`TOPIC_REGISTRATION.md`](./TOPIC_REGISTRATION.md)<br>[`lab08.md`](./lab08.md)<br>[`ScholarProof.sol`](./contracts/capstone/ScholarProof.sol) | Khởi động đồ án Chủ đề 8, thiết lập cơ chế Proof of Existence, băm mật mã client-side, thiết kế Smart Contract & bộ 3 ca kiểm thử | ✅ **Hoàn thành** |
| **Lab 9** | [`SPEC.md`](./SPEC.md)<br>[`lab09.md`](./lab09.md)<br>[`contracts/training/TimeLockVault.sol`](./contracts/training/TimeLockVault.sol) | Đặc tả nghiệp vụ BA chi tiết cho nền tảng ScholarProof, máy trạng thái xác thực ý tưởng và ma trận rủi ro | ✅ **Hoàn thành** |
| **Lab 10** | [`lab10.md`](./lab10.md)<br>[`contracts/capstone/ScholarProof.sol`](./contracts/capstone/ScholarProof.sol) (v2)<br>[`contracts/project/ProjectCore.sol`](./contracts/project/ProjectCore.sol) | Rà soát mã nguồn do AI sinh ra, giải mã Storage Slot 2 (VaultBuggy), kiểm toán & nâng cấp ScholarProof v2 | ✅ **Hoàn thành** |
| **Lab 11** | [`web/index.html`](./web/index.html)<br>[`lab11.md`](./lab11.md) | Xây dựng giao diện Web3 DApp: Băm file client-side (Keccak-256), kết nối MetaMask Ethers.js v6, tra cứu và xuất chứng thư số | ✅ **Hoàn thành** |
| **Lab 12** | [`test/ScholarProof.test.js`](./test/ScholarProof.test.js)<br>[`contracts/test/ScholarProof_test.sol`](./contracts/test/ScholarProof_test.sol)<br>[`lab12.md`](./lab12.md) | Bộ kịch bản kiểm thử tự động toàn diện: Luồng chuẩn, chống gian lận nộp đè mã băm, xử lý ngoại lệ biên | ✅ **Hoàn thành** |
| **Lab 13** | [`web/index.html`](./web/index.html) (Tích hợp Sepolia Testnet)<br>[`lab13.md`](./lab13.md)<br>[`AI_JOURNAL.md`](./AI_JOURNAL.md) | Tích hợp địa chỉ hợp đồng deploy Sepolia, xác thực mã nguồn Etherscan, kiểm thử luồng ký ví và đối soát sự kiện on-chain | ✅ **Hoàn thành** |
| **Lab 14** | [`audit_report.md`](./audit_report.md)<br>[`lab14.md`](./lab14.md)<br>[`scripts/gas_benchmark.py`](./scripts/gas_benchmark.py) | Kiểm toán an toàn hợp đồng, đo lường chi phí Gas thực nghiệm trên Layer 2 Base/Arbitrum vs Sepolia Testnet | ✅ **Hoàn thành** |
| **Lab 15** | [`DEPLOYMENT.md`](./DEPLOYMENT.md)<br>[`SLIDES.md`](./SLIDES.md)<br>[`lab15.md`](./lab15.md) | Tài liệu hướng dẫn vận hành hệ thống, slide thuyết trình nghiệm thu trước hội đồng, bảo vệ thành công đồ án | ✅ **Hoàn thành (Đồ án 100%)** |

---

## 🛠️ Cấu trúc kho lưu trữ mã nguồn Đồ án
```text
HCE-ScholarProof/
├── contracts/
│   ├── capstone/
│   │   └── ScholarProof.sol     # Hợp đồng thông minh ghi nhận quyền tác giả ý tưởng (v2)
│   ├── project/
│   │   └── ProjectCore.sol      # Hợp đồng lõi theo định danh quy định của học phần
│   └── training/                # Thư viện hợp đồng mẫu tham chiếu (TimeLockVault, VaultBuggy)
├── web/
│   └── index.html               # Giao diện Web3 DApp băm file và tra cứu on-chain
├── AGENTS.md                    # Quy ước lập trình và chuẩn mực bảo mật dự án
├── AI_JOURNAL.md                # Nhật ký làm việc, phản biện và giám sát AI (Lab 1 - 10)
├── SPEC.md                      # Bản đặc tả nghiệp vụ BA và máy trạng thái hệ thống
├── TOPIC_REGISTRATION.md        # Bản đăng ký đề tài Capstone chính thức của cặp sinh viên
├── lab08.md                     # Báo cáo kỹ thuật và kinh tế khởi động đồ án (Lab 8)
├── lab10.md                     # Báo cáo rà soát mã AI và kiểm toán hợp đồng lõi (Lab 10)
├── package.json                 # Cấu hình phụ thuộc OpenZeppelin Contracts v5
└── README.md                    # Tài liệu giới thiệu tổng quan đồ án HCE-ScholarProof
```

---
*Dự án được xây dựng và phát triển theo chuẩn quy ước [AGENTS.md](./AGENTS.md) của học phần ECO2432.*
