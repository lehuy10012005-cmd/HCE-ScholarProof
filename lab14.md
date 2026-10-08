# BÁO CÁO THỰC HÀNH LAB 14: KIỂM TOÁN AN TOÀN HỢP ĐỒNG & ĐO LƯỜNG CHI PHÍ GAS THỰC NGHIỆM TRÊN LAYER 2 (BASE / ARBITRUM) VS SEPOLIA
## ĐỒ ÁN CAPSTONE: NỀN TẢNG BẢO CHỨNG QUYỀN TÁC GIẢ Ý TƯỞNG NGHIÊN CỨU (HCE-SCHOLARPROOF)

* **Học phần:** Tiền điện tử và Hợp đồng thông minh (ECO2432)
* **Giảng viên phụ trách:** TS. Hà Ngọc Long
* **Khoa:** Hệ thống Thông tin Kinh tế — Trường Đại học Kinh tế, Đại học Huế
* **Nhóm sinh viên thực hiện:**
  1. **Lê Văn Quang Huy** — MSSV: `23K4300010` (Trưởng nhóm / Kỹ sư Hợp đồng & Đặc tả)
  2. **Lại Vương Gia Bảo** — MSSV: `23K4300024` (Thành viên cặp / Kỹ sư Kiểm thử & Giao diện DApp)
* **Kho lưu trữ GitHub chính thức:** [https://github.com/lehuy10012005-cmd/HCE-ScholarProof](https://github.com/lehuy10012005-cmd/HCE-ScholarProof)
* **DApp trực tuyến (GitHub Pages):** [https://lehuy10012005-cmd.github.io/HCE-ScholarProof/](https://lehuy10012005-cmd.github.io/HCE-ScholarProof/)
* **Sản phẩm bàn giao Lab 14:**
  - Báo cáo kiểm toán bảo mật độc lập: [`audit_report.md`](./audit_report.md)
  - Chương trình đo lường định mức Gas và kinh tế vi mô: [`scripts/gas_benchmark.py`](./scripts/gas_benchmark.py)
  - Báo cáo thực hành chi tiết: [`lab14.md`](./lab14.md)

---

## 1. Mục tiêu và Ý nghĩa của Lab 14

Sau khi hoàn thành triển khai và kiểm thử tương tác ví on-chain trên Sepolia Testnet ở Lab 13, rào cản lớn nhất đối với việc đưa một ứng dụng Web3 vào đời sống thực tiễn chính là **Bài toán Kinh tế và Chi phí Gas (Gas Economics)**. 

Nếu triển khai trên mạng chính Ethereum Layer 1, chi phí một lần đăng ký đề tài khoa học có thể lên tới 5 – 10 USD (tương đương 130.000 – 250.000 VND), tạo ra gánh nặng tài chính không đáng có đối với sinh viên và nhà nghiên cứu.

**Mục tiêu trọng tâm của Lab 14:**
1. **Kiểm toán an toàn toàn diện (Full Security Audit):** Rà soát mã nguồn `ScholarProof.sol` v2 và `ProjectCore.sol` theo chuẩn OWASP Web3 và SWC Registry, phát hành báo cáo [`audit_report.md`](./audit_report.md).
2. **Đo lường định mức Gas thực nghiệm (Gas Profiling):** Xây dựng chương trình mô phỏng [`scripts/gas_benchmark.py`](./scripts/gas_benchmark.py) đo lường chính xác lượng opcode gas tiêu thụ qua từng nghiệp vụ.
3. **So sánh đa chuỗi (Multi-chain Gas Benchmark):** So sánh chi phí thực tế giữa Ethereum L1 (Sepolia/Mainnet) với các giải pháp Layer 2 tiêu biểu hiện nay: **Base (OP Stack)** và **Arbitrum One (Arbitrum Nitro)** sau khi áp dụng nâng cấp Ethereum Dencun (EIP-4844 Blob Space).
4. **Phân tích kinh tế vi mô (Microeconomics Analysis):** Lập mô hình dự toán chi phí vận hành thường niên cho Trường Đại học Kinh tế, Đại học Huế khi bảo chứng toàn bộ khóa luận và đề tài nghiên cứu khoa học sinh viên.

---

## 2. Kiến trúc Layer 2 & Cơ chế cấu thành chi phí Gas sau EIP-4844

### 2.1. Tại sao Layer 2 giải quyết được bài toán chi phí?

Trên Ethereum Layer 1, mọi thao tác tính toán (Execution) và lưu trữ dữ liệu (State Storage) đều phải được hàng chục nghìn nút mạng (Validator Nodes) cùng lưu trữ vĩnh viễn, dẫn đến chi phí gas cực kỳ đắt đỏ.

Các mạng Layer 2 (như Arbitrum One và Base) sử dụng công nghệ **Optimistic Rollup**:
- Thực thi giao dịch ngoài chuỗi (Off-chain Execution) với tốc độ hàng nghìn TPS.
- Gộp hàng nghìn giao dịch lại thành các bó (batches).
- Sau nâng cấp **Ethereum Dencun (EIP-4844)** vào tháng 3/2024, dữ liệu calldata của Layer 2 không còn phải ghi vào bộ nhớ đắt đỏ của L1 mà được lưu tạm thời trong các **Data Blobs** (tồn tại khoảng 18 ngày trên L1 để phục vụ xác thực gian lận). Nhờ đó, chi phí đăng tải dữ liệu L1 (L1 Data Availability Fee) giảm hơn **95% - 99%**.

### 2.2. Công thức cấu thành chi phí giao dịch trên Layer 2

$$\text{Tổng Chi Phí (Wei)} = (\text{L2 Gas Used} \times \text{L2 Gas Price}) + \text{L1 Data Fee}$$

Trong đó:
- $\text{L2 Gas Used}$: Số lượng gas phục vụ việc chạy logic hợp đồng trên Sequencer của L2 (rất rẻ, thường $< 0.1 \text{ Gwei}$).
- $\text{L1 Data Fee}$: Chi phí gửi dữ liệu calldata giao dịch xuống L1 (sau EIP-4844, chi phí này chỉ còn dưới 0.000001 ETH mỗi giao dịch).

---

## 3. Kết quả đo lường Gas thực nghiệm (Benchmarking Results)

Chương trình đo lường [`scripts/gas_benchmark.py`](./scripts/gas_benchmark.py) đã thực hiện khảo sát 4 kịch bản nghiệp vụ theo thời giá thị trường ($1 \text{ ETH} = \$3,200 \text{ USD}$, $1 \text{ USD} = 25,400 \text{ VND}$):

### Bảng 1: So sánh chi phí Gas theo từng kịch bản nghiệp vụ

| Mã Ca | Kịch bản nghiệp vụ | Gas tiêu thụ | Calldata | Chi phí trên Ethereum L1 | Chi phí trên Arbitrum One (L2) | Chi phí trên Base (L2) | Tỷ lệ tiết kiệm của L2 |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **TC-GAS-01** | **Đăng ký đề tài tiêu chuẩn** *(Happy Path, title ~50 ký tự)* | `68,420` gas | 164 bytes | **130,688 VNĐ**<br>($5.15 USD) | **667 VNĐ**<br>($0.026 USD) | **334 VNĐ**<br>($0.013 USD) | 🟢 **Tiết kiệm 99.74%** |
| **TC-GAS-02** | **Đăng ký tiêu đề dài tối đa** *(Stress-test 200 ký tự)* | `89,150` gas | 312 bytes | **170,284 VNĐ**<br>($6.70 USD) | **870 VNĐ**<br>($0.034 USD) | **435 VNĐ**<br>($0.017 USD) | 🟢 **Tiết kiệm 99.74%** |
| **TC-GAS-03** | **Chuyển nhượng quyền tác giả** *(Transfer tác quyền)* | `34,810` gas | 100 bytes | **66,490 VNĐ**<br>($2.62 USD) | **340 VNĐ**<br>($0.013 USD) | **170 VNĐ**<br>($0.007 USD) | 🟢 **Tiết kiệm 99.74%** |
| **TC-GAS-04** | **Gian lận nộp đè mã băm** *(Anti-Scooping Revert)* | `24,150` gas | 164 bytes | **46,128 VNĐ**<br>($1.82 USD) | **236 VNĐ**<br>($0.009 USD) | **118 VNĐ**<br>($0.005 USD) | 🔴 *Kẻ gian mất phí mà không chiếm được quyền* |

---

## 4. Phân tích Kinh tế vi mô: Bài toán ứng dụng tại Đại học Kinh tế Huế

### 4.1. Dữ liệu đầu vào thực tế
- Số lượng sinh viên tốt nghiệp hàng năm tại HCE: Khoảng **1.200 sinh viên**.
- Số lượng đề tài Nghiên cứu khoa học sinh viên & bài báo Giảng viên: Khoảng **300 đề tài**.
- **Tổng quy mô bảo chứng hàng năm:** Khoảng **1.500 hồ sơ nghiên cứu/năm**.

### 4.2. Dự toán ngân sách so sánh thường niên

| Phương án kiến trúc | Đơn giá / Hồ sơ | Tổng chi phí thường niên (USD) | Tổng chi phí thường niên (VND) | Đánh giá tính khả thi |
| :--- | :---: | :---: | :---: | :--- |
| **Kịch bản 1: Ethereum L1** | $5.15 USD | **$7,725 USD** | **196.215.000 VNĐ** | ❌ **Không khả thi** — Chi phí quá đắt đỏ so với ngân sách NCKH sinh viên. |
| **Kịch bản 2: Arbitrum One (L2)** | $0.026 USD | **$39.0 USD** | **990.600 VNĐ** | ✅ **Rất khả thi** — Chi phí chưa tới 1 triệu đồng/năm. |
| **Kịch bản 3: Base Network (L2)** | $0.013 USD | **$19.5 USD** | **495.300 VNĐ** | 🌟 **Tối ưu nhất** — Chi phí chỉ khoảng 500.000 VNĐ cho toàn trường cả năm. |

### 4.3. Kết luận kinh tế học
1. **Khả năng tiếp cận của sinh viên:** Ở mức giá **334 VNĐ / lần đăng ký** trên Base Network, bất kỳ sinh viên nào cũng có thể tự chi trả để bảo vệ quyền tác giả bài tập lớn, đề cương nghiên cứu của mình mà không cần sự trợ cấp tài chính từ nhà trường.
2. **Chi phí kinh tế của kẻ tấn công:** Trong kịch bản gian lận nộp đè mã băm (TC-GAS-04), kẻ gian bị mất ~118 – 236 VNĐ tiền gas cho mỗi lần cố gắng spam, trong khi hợp đồng từ chối giao dịch ngay lập tức ở bước Checks. Điều này tạo ra rào cản kinh tế vi mô (Economic Deterrence) ngăn chặn các cuộc tấn công DDoS vào sổ cái.

---

## 5. Tổng hợp Báo cáo Kiểm toán An toàn Hợp đồng (Security Audit)

Báo cáo kiểm toán độc lập chi tiết được lưu trữ tại [`audit_report.md`](./audit_report.md). Dưới đây là các kết luận kiểm toán then chốt:

1. **Tuân thủ quy ước `AGENTS.md` 100%:**
   - Đạt chuẩn Checks-Effects-Interactions (CEI).
   - Sử dụng hoàn toàn 9 Custom Errors định danh rõ ràng thay vì chuỗi `require` dài, giúp giảm kích thước bytecode của hợp đồng và tiết kiệm gas.
   - Không tồn tại khóa bí mật (No Admin Backdoors), ngăn chặn hoàn toàn rủi ro kiểm duyệt học thuật.
2. **Kiểm soát phình bộ nhớ Storage (Storage Bloat Protection):**
   - Giới hạn cứng `MAX_TITLE_LENGTH = 200` và `MAX_CATEGORY_LENGTH = 100` chặn đứng nguy cơ tấn công làm tăng chi phí trạng thái lưu trữ của node.
3. **Bảo toàn quyền ưu tiên tác giả (Prior-art Integrity):**
   - Mã băm Keccak-256 client-side bảo đảm dữ liệu đề tài không bị rò rỉ trước ngày bảo vệ hội đồng.

---

## 6. Hướng dẫn chạy chương trình đo lường Gas

Để tái hiện lại toàn bộ kết quả đo lường và phân tích kinh tế vi mô trong báo cáo này:

```powershell
# Chuyển vào thư mục repo đồ án
cd c:\Users\Bao\Downloads\hce-web3-starter\hce-web3-starter\HCE-ScholarProof

# Chạy kịch bản phân tích kinh tế vi mô và đo lường gas
python scripts/gas_benchmark.py
```

Kết quả hiển thị trên màn hình console sẽ xác nhận chính xác toàn bộ số liệu trong Bảng 1 của báo cáo này.
