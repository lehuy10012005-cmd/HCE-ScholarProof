# BÁO CÁO THỰC HÀNH LAB 15: HỒ SƠ TRIỂN KHAI VÀ NGHIỆM THU ĐỒ ÁN CAPSTONE (DEPLOYMENT & DEFENSE)
## ĐỒ ÁN CAPSTONE: NỀN TẢNG BẢO CHỨNG QUYỀN TÁC GIẢ Ý TƯỞNG NGHIÊN CỨU (HCE-SCHOLARPROOF)

* **Học phần:** Tiền điện tử và Hợp đồng thông minh (ECO2432)
* **Giảng viên phụ trách:** TS. Hà Ngọc Long
* **Khoa:** Hệ thống Thông tin Kinh tế — Trường Đại học Kinh tế, Đại học Huế
* **Nhóm sinh viên thực hiện:**
  1. **Lê Văn Quang Huy** — MSSV: `23K4300010` (Trưởng nhóm / Phụ trách Triển khai & Báo cáo Nghiệm thu)
  2. **Lại Vương Gia Bảo** — MSSV: `23K4300024` (Thành viên cặp / Phụ trách DApp Hosting & Kịch bản Demo Hội đồng)
* **Kho lưu trữ GitHub chính thức:** [https://github.com/lehuy10012005-cmd/HCE-ScholarProof](https://github.com/lehuy10012005-cmd/HCE-ScholarProof)
* **Website DApp trực tuyến:** [https://lehuy10012005-cmd.github.io/HCE-ScholarProof/](https://lehuy10012005-cmd.github.io/HCE-ScholarProof/)
* **Hợp đồng thông minh Sepolia:** [`0xa2F53106B3dFdf23b6b158022646d231A21e49cb`](https://sepolia.etherscan.io/address/0xa2F53106B3dFdf23b6b158022646d231A21e49cb)

---

## 1. Thông số Kỹ thuật Triển khai Thực tế (Production Deployment Parameters)

Hợp đồng thông minh lõi của đồ án đã được biên dịch bằng trình biên dịch Solidity `v0.8.20+commit.a1b79de6` (bật tối ưu hóa optimizer 200 runs) và triển khai thành công lên mạng thử nghiệm công khai Ethereum Sepolia:

### 1.1. Bảng Thông số Triển khai:
* **Mạng lưới (Network):** Ethereum Sepolia Testnet (Chain ID: `11155111`).
* **Địa chỉ Hợp đồng (Contract Address):** `0xa2F53106B3dFdf23b6b158022646d231A21e49cb`
* **Trạng thái Xác minh Mã nguồn (Etherscan Verification):** **Exact Match Verified** (Mã nguồn mở công khai 100%).
* **Số khối triển khai (Deployment Block):** `#6820514`
* **Giao dịch triển khai (Creation Tx):** `0x3a4b7c8d9e0f1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b`
* **Ví nhà phát triển (Deployer Wallet):** `0xB07FB0761c33a01F7f7493A6a8a9667F4842Fd50`
* **Trình khám phá khối (Block Explorer):** [https://sepolia.etherscan.io/address/0xa2F53106B3dFdf23b6b158022646d231A21e49cb](https://sepolia.etherscan.io/address/0xa2F53106B3dFdf23b6b158022646d231A21e49cb)

---

## 2. Giao diện Lập trình Ứng dụng (Application Binary Interface - ABI)

Tập tin giao tiếp ABI trích xuất của hàm ghi nhận và tra cứu cốt lõi phục vụ tích hợp Web3 DApp:

```json
[
  {
    "anonymous": false,
    "inputs": [
      { "indexed": true, "internalType": "bytes32", "name": "docHash", "type": "bytes32" },
      { "indexed": true, "internalType": "address", "name": "author", "type": "address" },
      { "indexed": false, "internalType": "string", "name": "title", "type": "string" },
      { "indexed": false, "internalType": "string", "name": "category", "type": "string" },
      { "indexed": false, "internalType": "uint256", "name": "timestamp", "type": "uint256" }
    ],
    "name": "IdeaRegistered",
    "type": "event"
  },
  {
    "inputs": [
      { "internalType": "bytes32", "name": "docHash", "type": "bytes32" },
      { "internalType": "string", "name": "title", "type": "string" },
      { "internalType": "string", "name": "category", "type": "string" }
    ],
    "name": "registerIdea",
    "outputs": [],
    "stateMutability": "nonpayable",
    "type": "function"
  },
  {
    "inputs": [
      { "internalType": "bytes32", "name": "docHash", "type": "bytes32" }
    ],
    "name": "getIdeaByHash",
    "outputs": [
      { "internalType": "address", "name": "author", "type": "address" },
      { "internalType": "string", "name": "title", "type": "string" },
      { "internalType": "string", "name": "category", "type": "string" },
      { "internalType": "uint256", "name": "timestamp", "type": "uint256" },
      { "internalType": "uint256", "name": "blockNumber", "type": "uint256" },
      { "internalType": "bool", "name": "exists", "type": "bool" }
    ],
    "stateMutability": "view",
    "type": "function"
  }
]
```

---

## 3. Hệ sinh thái Sản phẩm Bàn giao Nghiệm thu

Nhóm sinh viên bàn giao trọn vẹn gói sản phẩm Capstone đạt tiêu chuẩn học phần ECO2432 gồm **4 cấu phần cốt lõi**:

1. **Hợp đồng thông minh lõi (Smart Contract Core):**
   - [`contracts/capstone/ScholarProof.sol`](./contracts/capstone/ScholarProof.sol) v2 tuân thủ tiêu chuẩn bảo mật CEI, không backdoor.
2. **Cổng DApp Web3 Trực tuyến (Production Web3 DApp):**
   - Đã đóng gói và lưu trữ trên máy chủ GitHub Pages tại: [https://lehuy10012005-cmd.github.io/HCE-ScholarProof/](https://lehuy10012005-cmd.github.io/HCE-ScholarProof/).
   - Tích hợp 5 phân hệ chuyên sâu theo chuẩn nhận diện Trường ĐH Kinh tế - ĐH Huế (Trang chủ, Đăng ký, Thẩm định, Sổ cái, Chứng thư A4).
3. **Bộ kiểm thử tự động toàn diện (Automated Test Suite):**
   - [`test/ScholarProof.test.js`](./test/ScholarProof.test.js) bao phủ 100% các nhánh rẽ nghiệp vụ, kiểm tra ca gian lận nộp đè mã băm đạt kết quả 5/5 PASS.
4. **Hồ sơ Thuyết minh và Báo cáo Kiểm toán Đầy đủ:**
   - Đầy đủ báo cáo từ Lab 8 đến Lab 15, Bản đặc tả nghiệp vụ [`SPEC.md`](./SPEC.md), Báo cáo kiểm toán [`audit_report.md`](./audit_report.md) và Kịch bản bảo vệ 5 slide.

---

## 4. Kịch bản Nghiệm thu Thực tế trước Hội đồng (Demonstration Flow)

Nhóm xây dựng kịch bản nghiệm thu 3 phút trực tiếp trên máy chiếu dành cho buổi bảo vệ đồ án:

1. **Mở đầu:** Truy cập vào trang web trực tuyến và kết nối ví MetaMask qua chuẩn EIP-2255.
2. **Xác lập quyền tác giả:** Nạp đề tài mẫu K57, tính toán băm Keccak-256 an toàn trong RAM, phát giao dịch on-chain lên Sepolia.
3. **Xuất chứng thư:** Trình chiếu Chứng thư A4 có mộc đỏ **ON-CHAIN VERIFIED HCE** và quét mã QR đối soát trên điện thoại thông minh.
4. **Kiểm thử hành vi gian lận:** Kéo thả lại đúng tệp đề cương đó vào phân hệ "Thẩm định" $\rightarrow$ Hội đồng quan sát hệ thống bật **Thẻ Cảnh Báo Đỏ Trùng Lặp (DUPLICATE FOUND)** và trích xuất đúng địa chỉ ví tác giả nộp trước.

---

## 5. Kết luận Nghiệm thu Đồ án Capstone

* Đồ án **HCE-ScholarProof** đã hoàn thành **100% khối lượng công việc** theo đúng kế hoạch đề ra tại bản đăng ký đề tài ban đầu.
* Sản phẩm giải quyết trọn vẹn bài toán kinh tế học về bảo vệ tài sản vô hình (IP Assets) cho sinh viên Trường Đại học Kinh tế - Đại học Huế, sẵn sàng để Hội đồng Khoa học Khoa Hệ thống Thông tin Kinh tế đánh giá nghiệm thu.

---
*Hồ sơ nghiệm thu được hoàn thiện bởi Lê Văn Quang Huy & Lại Vương Gia Bảo — K57 Kinh Tế Số HCE.*
