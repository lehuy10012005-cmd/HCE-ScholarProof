# NHẬT KÝ LÀM VIỆC VỚI AI - LAB 1: THIẾT LẬP MÔI TRƯỜNG & QUY ƯỚC AGENTS.MD

## Lần 1

**Prompt:**
> "Tôi đã mở thư mục hce-web3-starter làm Workspace. Bây giờ hãy giúp tôi hoàn thành dứt điểm toàn bộ bài Lab 1:
> 1. Hãy tự động đọc và tinh chỉnh lại tệp AGENTS.md, thêm quy tắc cá nhân chuẩn cho tôi.
> 2. Tự mở Terminal hướng dẫn và chạy các lệnh Git (add, commit, push) để đẩy kho mã nguồn này lên GitHub cá nhân của tôi và lấy link commit nộp bài.
> 3. Nhắc tôi kiểm tra địa chỉ ví để hoàn tất sản phẩm nộp của Lab 1."

**AI trả về:**
- Tinh chỉnh phần "Quy tắc cá nhân của sinh viên" trong tệp `AGENTS.md` thành 4 điều khoản chi tiết: Ngôn ngữ & Diễn giải, Quản trị rủi ro & Kế toán On-chain, Kiểm thử nghiêm ngặt, An toàn bảo mật tài sản số.
- Tự động tạo kho lưu trữ `ECO2432-Lab-2026` trên GitHub cá nhân (`lehuy10012005-cmd`), chạy các lệnh Git (`init`, `add`, `commit`, `remote add`, `push`).
- Cung cấp link commit kiểm chứng và checklist kiểm tra ví MetaMask mạng Sepolia.

**Đánh giá:** Dùng được.

**Chỗ sai:**
Phần quy tắc cá nhân mặc định trước đó chỉ có 2 dòng sơ sài, thiếu định danh sinh viên (Lê Huy - ECO2432), chưa có quy tắc bảo mật khóa riêng (Private Key) và chưa gắn chặt với góc nhìn kiểm toán on-chain. Kho mã nguồn trên GitHub chưa được tạo trước đó khiến lệnh đẩy ban đầu không có đích đến.

**Cách sửa:**
Sinh viên yêu cầu AI đối chiếu Sổ tay môn học ECO2432 để viết lại bộ quy tắc thành 4 điều chuẩn mực; đồng thời tạo repo trống trên GitHub trước khi push mã nguồn.

**Ai phát hiện:** Sinh viên phát hiện.

## Lần 2 (Lab 2: Ví và giao dịch đầu tiên)

**Prompt:**
> "địa chỉ ví : 0xB07FB0761c33a01F7f7493A6a8a9667F4842Fd50 mã băm của giao dịch thành công : 0x012b71a61a33cf554ffbda91ff2a2b679ef5339adb10fa21bc7fefc13b1c9440 mã băm giao dịch không thành công ( hoặc thành công) : 0xdfcb9f3cce3e8a8431af94d72b1641beb74c4aff514cd99a369cfcb2eb4c276c cố tình sửa 1 kí tự ở ví người nhận thì nó không cho chuyển qua trạng thái này ( cái này tôi chưa hiểu lắm mà đúng không)"

**AI trả về:**
- Giải thích bản chất kỹ thuật của giao dịch `0xdfcb...276c`: Đã thành công on-chain nhưng từng bị MetaMask cảnh báo đỏ "Đã bị đầu độc" (Address Poisoning).
- Giải thích lý do khi cố tình sửa 1 ký tự ví người nhận thì MetaMask lập tức khóa nút gửi: Do cơ chế mã kiểm tra EIP-55 Checksum tự động phát hiện lỗi chính tả ngay tại lớp ứng dụng (client-side), giúp người dùng không tốn phí gas vô ích.
- Tạo báo cáo `lab02.md` gồm bảng đối chiếu dữ liệu on-chain thực tế và đoạn giải trình 3 câu về tính bất biến (Immutability) của blockchain dưới góc nhìn kế toán và quản trị rủi ro.

**Đánh giá:** Dùng được.

**Chỗ sai:**
Ban đầu sinh viên nhầm lẫn giao dịch `0xdfcb...276c` là giao dịch thất bại do nhìn thấy cảnh báo đỏ `⚠️ Đã bị đầu độc` trên MetaMask, và chưa phân biệt được giữa việc giao dịch thất bại on-chain (revert/out of gas) với việc bị ví chặn ngay từ giao diện do sai Checksum (chưa hề được phát sóng lên mạng nên không có Tx Hash).

**Cách sửa:**
AI tra cứu trực tiếp biên lai (receipt) từ mạng Sepolia RPC để chứng minh giao dịch thực tế đã Confirmed, đồng thời phân tích cơ chế bảo mật EIP-55 Checksum và thủ đoạn gian lận Address Poisoning theo đúng chuẩn nghiệp vụ tuân thủ AML.

**Ai phát hiện:** Sinh viên phát hiện hiện tượng bất thường và chủ động hỏi AI đối soát dữ liệu on-chain.

## Lần 3 (Lab 3: Đọc giao dịch và hợp đồng trên Etherscan)

**Prompt:**
> "rồi ok qua Lab 3 , cứ theo trình tự vậy"

**AI trả về:**
- Mổ xẻ chi tiết 8 trường dữ liệu on-chain của giao dịch `0x012b...9440` (Status, Block, Timestamp, From/To, Value, Tx Fee, Gas Price, Nonce) gắn với góc nhìn kế toán tài sản số và điều tra tuân thủ (AML/KYC).
- Thẩm định hợp đồng thực tế USDT trên Ethereum Mainnet (`0xdAC17F958D2ee523a2206206994597C13D831ec7`): phân biệt Bytecode và Verified Code, truy vấn trực tiếp tổng cung (~88.3 tỷ USDT) qua hàm `totalSupply()`.
- Phát hiện và phân tích quyền đóng băng tài khoản tập trung qua hàm `addBlackList()` và `destroyBlackFunds()`, trả lời sâu sắc về mức độ phi tập trung thực tế và rủi ro kiểm duyệt (Censorship Risk).
- Tạo tệp sản phẩm nộp `forensics.md` và đồng bộ lên kho GitHub.

**Đánh giá:** Dùng được.

**Chỗ sai:**
Nhiều người dùng lầm tưởng các token trên blockchain đều phi tập trung hoàn toàn và không ai có thể can thiệp số dư. Nếu không đọc tab Write Contract của hợp đồng USDT, sinh viên sẽ không phát hiện ra nhà phát hành Tether có đặc quyền đóng băng địa chỉ ví và tiêu hủy tiền trong ví của người khác.

**Cách sửa:**
AI trực tiếp tra cứu mã nguồn đã xác thực của hợp đồng Tether trên Etherscan, chỉ rõ tên các hàm quản trị danh sách đen (`addBlackList`, `destroyBlackFunds`) và phân tích bài học quản trị rủi ro dòng tiền cho doanh nghiệp.

**Ai phát hiện:** Sinh viên định hướng yêu cầu AI phân tích rủi ro kiểm duyệt on-chain theo khung Sổ tay thực hành.

## Lần 4 (Lab 4: Nhận diện hợp đồng có rủi ro)

**Prompt:**
> "Bạn là chuyên viên thẩm định rủi ro tài sản số. Dưới đây là mã nguồn một hợp đồng token trong contracts/lab04/ClubTokens.sol. Hãy liệt kê mọi quyền đặc biệt mà chủ sở hữu hợp đồng có thể thực hiện, và với mỗi quyền, nêu rõ: Tên hàm và số dòng; Người nắm giữ token chịu rủi ro gì. Chỉ trả lời dựa trên mã nguồn tôi cung cấp. Nếu không tìm thấy, nói là không tìm thấy."

**AI trả về:**
- Thẩm định 3 hợp đồng mẫu `ClubTokenA`, `ClubTokenB`, `ClubTokenC` trong tệp `contracts/lab04/ClubTokens.sol`.
- Chỉ ra chính xác số dòng và cơ chế rủi ro:
  + `ClubTokenA` (dòng 7–11): Sạch, không có quyền đặc biệt.
  + `ClubTokenB` (dòng 18–20): Hàm `mint()` không có trần `MAX_SUPPLY`, rủi ro pha loãng vô hạn (Rug-pull).
  + `ClubTokenC` (dòng 30–32 và dòng 34–37): Hàm `setRestricted()` kết hợp logic chặn trong hàm `_update()`, tạo bẫy Honeypot (chỉ cho mua, không cho bán).
- Đưa ra đề xuất cải tiến mã nguồn và lập báo cáo chi tiết `lab04.md`.

**Đánh giá:** Dùng được.

**So sánh Đối chứng (Đọc thủ công vs AI) & Bắt lỗi AI:**
- **Đọc thủ công tìm ra gì:** Sinh viên đọc mã nguồn 15 phút đầu và phát hiện ngay hàm `mint` ở Token B có `onlyOwner` và biến `restricted` ở Token C dùng để chặn chuyển tiền.
- **AI tìm thêm được gì:** AI phân tích sâu hơn về mặt kỹ thuật: chỉ ra Token C vi phạm OpenZeppelin v5 ở chỗ can thiệp vào hàm `_update` nhưng không phát ra `event` khi gọi `setRestricted` (gây mù thông tin cho các bot cảnh báo on-chain), đồng thời chỉ ra thủ đoạn ngụy tạo lý do "bảo vệ cộng đồng" để che giấu bẫy Honeypot.
- **AI có nói sai chỗ nào không:** Ban đầu nếu không có câu ràng buộc *"Chỉ trả lời dựa trên mã nguồn tôi cung cấp"*, AI thường tự suy đoán hợp đồng có thể dính lỗi Reentrancy (dù đây là token ERC-20 thuần túy không có hàm chuyển ETH). Sinh viên đã dùng đúng mẫu prompt chuẩn trong `prompt_templates.md` để ép AI bám sát từng dòng mã cụ thể từ dòng 1 đến dòng 40.

**Ai phát hiện:** Sinh viên phát hiện và kiểm soát giới hạn suy diễn của AI.

## Lần 5 (Lab 5: Viết đặc tả cho công cụ phân tích dòng tiền)

**Prompt:**
> "Hãy giúp tôi hoàn thiện bản đặc tả nghiệp vụ SPEC.md cho công cụ phân tích dòng tiền ví on-chain trong 90 ngày theo đúng chuẩn BA Fintech (Sổ tay thực hành ECO2432, trang 15–16). Không viết code trong buổi này. Bổ sung đầy đủ 6 phần: Mục đích, Đầu vào, Quy tắc R1–R6, Đầu ra, Trường hợp ngoại lệ và Ngoài phạm vi, kèm quy tắc mở rộng cho tình huống tự chuyển tiền (Self-transfer)."

**AI trả về:**
- Bản đặc tả nghiệp vụ `SPEC.md` hoàn chỉnh gồm 6 phần cốt lõi và 7 quy tắc nghiệp vụ tài chính (R1–R7).
- Định nghĩa chặt chẽ cơ chế tính toán dòng tiền ra (`giá trị + phí gas`) và hạch toán phí gas của giao dịch thất bại.
- Bổ sung 4 ca biên ngoại lệ (Edge Cases E1–E4) về xử lý ví rỗng, lỗi xác thực API Etherscan, địa chỉ sai định dạng và cơ chế phân trang tự động khi vượt quá 10.000 giao dịch.

**Đánh giá:** Dùng được.

**Chỗ sai & Phản biện của sinh viên:**
Nếu chỉ mô tả chung chung "viết tool phân tích ví", AI thường bỏ qua việc giao dịch thất bại vẫn làm giảm số dư ví do tốn phí gas (vi phạm nguyên tắc bảo toàn số dư sổ cái), hoặc quên chia đơn vị 10^18 từ `wei` sang `ETH`. Sinh viên đã yêu cầu chuẩn hóa từng quy tắc R1–R7 độc lập có thể kiểm thử được (testable assertion) trước khi chuyển sang bước sinh mã ở Lab 6.

**Ai phát hiện:** Sinh viên định hình yêu cầu nghiệp vụ và giám sát cấu trúc đặc tả.

## Lần 6 (Lab 6: Sinh mã bằng AI và kiểm tra kết quả)

**Prompt:**
> "Đọc tệp SPEC.md trong dự án và viết chương trình Python wallet_analyzer.py thực hiện đúng đặc tả đó. Tuân thủ các quy ước trong AGENTS.md. Trước khi viết mã, tóm tắt lại cách bạn hiểu yêu cầu để tôi xác nhận. Sau đó tiến hành kiểm tra checklist 6 điểm của Sổ tay thực hành trang 17–18."

**AI trả về:**
- Tóm tắt cách hiểu bản đặc tả `SPEC.md` và viết chương trình Python `wallet_analyzer.py`.
- Tự động kết nối Etherscan API V2, tính toán dòng tiền vào/ra theo quy tắc R1–R7, xử lý ngoại lệ E1–E4 và trích xuất bảng số liệu tài chính kèm tệp biểu đồ đường `balance_chart.png`.
- Tạo tệp cấu hình mẫu `.env.example` để bảo vệ khóa bí mật.

**Đánh giá:** Phải sửa (sau khi sinh viên thực hiện bài kiểm tra checklist 6 điểm).

**Checklist 6 điểm kiểm tra & Bắt 2 lỗi ngớ ngẩn do AI sinh ra:**
1. **Lỗi 1 (Phiên bản API - Mục 6 Checklist):** AI ban đầu sinh mã sử dụng endpoint cũ `api-sepolia.etherscan.io/api?...` (Etherscan V1). Khi chạy thử nghiệm, API trả về lỗi: `NOTOK: You are using a deprecated V1 endpoint, switch to Etherscan API V2`. Sinh viên đã phát hiện và yêu cầu AI cập nhật lên chuẩn **Etherscan API V2** (`https://api.etherscan.io/v2/api?chainid=11155111...`).
2. **Lỗi 2 (Hạch toán giao dịch thất bại - Mục 4 Checklist):** Trong bản nháp đầu tiên, AI chỉ lọc các giao dịch có `isError == "0"` và bỏ qua hoàn toàn các giao dịch thất bại. Sinh viên đã chỉ ra lỗi logic kế toán: Giao dịch thất bại thì người gửi (`from`) vẫn bị trừ phí gas, nếu bỏ qua thì số dư lũy kế sẽ bị lệch so với thực tế ví trên Etherscan. AI đã phải sửa lại hàm `process_cashflow` để ghi nhận phí gas của giao dịch lỗi vào dòng tiền RA (Quy tắc R4).
3. **Các điểm kiểm tra còn lại:**
   - *Đơn vị tiền:* Đã chia cho 10^18 (`WEI_IN_ETH`), không bị số 19 chữ số.
   - *Bảo mật API:* Khóa được đọc qua `os.getenv("ETHERSCAN_API_KEY")`, không ghi cứng vào mã nguồn, tệp `.env` được bảo vệ trong `.gitignore`.
   - *Xử lý lỗi:* Có cơ chế bắt ngoại lệ khi API lỗi hoặc địa chỉ ví sai cú pháp (Edge Case E2, E3).

**Ai phát hiện:** Sinh viên phát hiện (trực tiếp kiểm tra đối soát theo Checklist 6 điểm của Sổ tay thực hành).

## Lần 7 (Lab 7: Tính chi phí vận hành thực tế — Gas)

**Prompt:**
> "Tôi đang làm Lab 7 môn ECO2432 về tính toán chi phí vận hành on-chain cho chương trình thẻ tích điểm câu lạc bộ (1.000 giao dịch/tháng, mỗi giao dịch tốn 50.000 gas, giá gas 20 Gwei, giá ETH 3.000 USD). Hãy lập bảng tính chi phí cho Ethereum Layer 1, so sánh với Layer 2 (rẻ hơn 100 lần), phân tích ai là người trả chi phí này (CLB hay sinh viên) và đề xuất các giải pháp kiến trúc kinh tế tối ưu."

**AI trả về:**
- Bảng tính chi tiết quy đổi từ Gas → Gwei → ETH → USD → VNĐ cho 1 giao dịch và cả tháng (1.000 giao dịch).
- So sánh chi phí giữa Ethereum Mainnet L1 (75 triệu VNĐ/tháng) và Layer 2 Arbitrum/Base (750k VNĐ/tháng).
- Phân tích kinh tế hành vi giữa hai đối tượng chịu phí và đề xuất 3 hướng kiến trúc tối ưu (Di chuyển L2, Gộp giao dịch Batching, và Mô hình hỗn hợp Hybrid).
- Mở rộng tính toán chi phí cho đề tài Đồ án Capstone: Két tiết kiệm có khóa thời gian sinh viên (`TimeLockVault.sol`).

**Đánh giá:** Phải sửa (sau khi sinh viên kiểm tra thứ nguyên toán học và phản biện tính khả thi kinh tế).

**Chỗ sai & Phản biện sắc bén của sinh viên:**
1. **Lỗi 1 (Sai lệch thứ nguyên & Quy đổi đơn vị Gwei):** Trong bản nháp đầu tiên, AI nhầm lẫn giữa Gwei và Wei. Thay vì nhân $10^{-9}$ để quy đổi Gwei ra ETH, AI lại nhân trực tiếp số gas với đơn giá Gwei rồi nhân với giá ETH ($50.000 \times 20 \times 3.000$), dẫn tới kết quả chi phí cho 1 giao dịch lên đến... **3.000.000.000 USD** (3 tỷ USD cho một lượt tích điểm!). Sinh viên phát hiện ngay lập tức nhờ kiểm tra thứ nguyên kế toán: $1\text{ ETH} = 10^9\text{ Gwei} = 10^{18}\text{ Wei}$. Công thức chuẩn xác phải là: $\text{Phí (ETH)} = 50.000 \times 20 \times 10^{-9} = 0,001\text{ ETH} = 3\text{ USD}$ ($\approx 75.000\text{ VNĐ}$).
2. **Lỗi 2 (Ngây thơ về kinh tế hành vi & Trải nghiệm người dùng):** AI đề xuất cho sinh viên tự trả phí gas trên mạng chính Ethereum với lập luận rằng "để người dùng trải nghiệm sự phi tập trung đích thực của Web3". Sinh viên phản biện ngay: Sinh viên đi mua ly cà phê $25.000\text{ VNĐ}$ mà phải bỏ thêm $75.000\text{ VNĐ}$ tiền phí gas (tỷ lệ Gas-to-Value lên tới $300\%$) thì không một người dùng có lý trí nào chấp nhận. Đây là bài học sống còn: *Nếu chi phí giao dịch lớn hơn giá trị giao dịch thì mô hình kinh doanh phá sản*.

**Ai phát hiện:** Sinh viên phát hiện và trực tiếp chấn chỉnh tư duy kinh tế của AI.

## Lần 8 (Lab 8: Khởi động Đồ án Capstone — Chủ đề 8: Ghi nhận quyền tác giả của ý tưởng nghiên cứu khoa học)

**Prompt:**
> "Chủ đề 8: Ghi nhận quyền tác giả của ý tưởng nghiên cứu khoa học. Đây sẽ là chủ đề đồ án của nhóm tôi (Lê Văn Quang Huy & Lại Vương Gia Bảo). Hãy xây dựng trọn bộ sản phẩm cho Lab 8: Khảo sát bài toán kinh tế - kỹ thuật, cơ chế băm dữ liệu & Proof of Existence, thiết kế hợp đồng ScholarProof.sol, lập bảng đối chiếu kiểm thử tối thiểu 3 ca và hoàn thiện hồ sơ đăng ký đề tài."

**AI trả về:**
- Phân tích bối cảnh vấn nạn chiếm đoạt ý tưởng nghiên cứu (Idea Scooping), đánh giá hạn chế của cơ quan bản quyền truyền thống và xác lập mô hình Proof of Existence (bằng chứng tồn tại mật mã) trên blockchain.
- Đề xuất kiến trúc tách rời dữ liệu: Băm file phía client (SHA-256 / Keccak-256) để giữ bí mật tuyệt đối nội dung tài liệu, chỉ gửi chuỗi băm 32 bytes (`docHash`) lên Smart Contract để ghi dấu thời gian (`block.timestamp`).
- Thiết kế hợp đồng thông minh `ScholarProof.sol` tuân thủ nghiêm ngặt `AGENTS.md` (Solidity ^0.8.20, Custom Errors, CEI, Events).
- Thiết lập 3 ca kiểm thử bắt buộc: Luồng chuẩn, Ca gian lận mạo danh nộp lại cùng hash, và Ca biên dữ liệu rỗng.
- Hoàn thiện tệp báo cáo `lab08.md`, bản đăng ký đề tài `TOPIC_REGISTRATION.md` cho sản phẩm mang tên **HCE-ScholarProof**.

**Đánh giá:** Dùng được (sau khi sinh viên chấn chỉnh tư duy lưu trữ và thẩm định bản quyền).

**Chỗ sai & Phản biện sắc bén của sinh viên:**
1. **Lỗi 1 (Sai lầm chết người về lưu trữ dữ liệu - Storage Bloat):** Trong bản phác thảo ý tưởng ban đầu, AI từng gợi ý "lưu trữ toàn bộ nội dung tệp PDF đề cương nghiên cứu dạng chuỗi bytes hoặc chuỗi hex trực tiếp vào biến trạng thái của Smart Contract để đảm bảo tính bất biến". Sinh viên đã bác bỏ ngay lập tức: Dưới góc nhìn kế toán chi phí on-chain (đã chứng minh ở Lab 7), ghi 1 MB dữ liệu vào EVM Storage có thể ngốn hàng chục ngàn USD tiền gas, gây tắc nghẽn mạng và làm dự án phá sản ngay từ ngày đầu. Giải pháp chuẩn xác phải là **chỉ lưu mã băm 32 bytes (`docHash`) on-chain**, còn tệp gốc giữ nguyên off-chain.
2. **Lỗi 2 (Nguy cơ lộ bí mật ý tưởng sơ khởi):** AI đề xuất cho sinh viên công khai toàn bộ tài liệu nghiên cứu lên IPFS công khai ngay khi đăng ký. Sinh viên phản biện: Ý tưởng nghiên cứu khoa học ở giai đoạn sơ khởi cần được bảo mật tối đa để tránh bị đối thủ sao chép trước khi công bố bài báo. Bằng chứng sở hữu trí tuệ trên blockchain chỉ cần chứng minh *"Tôi đã sở hữu tài liệu tạo ra mã băm này vào thời điểm T"* (Proof of Existence). Tài liệu gốc chỉ cần xuất trình khi có tranh chấp bản quyền xảy ra.

**Ai phát hiện:** Sinh viên phát hiện và định hướng kiến trúc bảo mật kết hợp kinh tế on-chain.

## Lần 9 (Lab 9: Xác lập Đặc tả Nghiệp vụ BA SPEC.md cho Đồ án Capstone HCE-ScholarProof)

**Prompt:**
> "Hãy giúp tôi hoàn thiện bản đặc tả nghiệp vụ BA Fintech (SPEC.md) cho đề tài Capstone HCE-ScholarProof theo chuẩn học phần ECO2432 (Sổ tay thực hành). Không viết code trong buổi này. Xây dựng đầy đủ 6 phần: Mục đích, Đầu vào (Off-chain & On-chain), Quy tắc nghiệp vụ R1–R8, Đầu ra, Máy trạng thái và Ma trận rủi ro / Trường hợp ngoại lệ E1–E5, kèm bài toán chống Front-running trên Mempool."

**AI trả về:**
- Bản đặc tả nghiệp vụ BA hoàn chỉnh `SPEC.md` và báo cáo `lab09.md` chuyên sâu cho đề tài `HCE-ScholarProof`.
- Mô hình hóa cây máy trạng thái 4 nấc (`Unregistered` ➔ `Hashing` ➔ `Registered` ➔ `Verified/Disputed`).
- Định nghĩa 8 quy tắc nghiệp vụ on-chain (R1–R8) đảm bảo nguyên tắc First-to-File, băm Keccak-256 client-side, lấy dấu thời gian khối bất biến và tra cứu miễn phí gas.
- Phân tích 5 kịch bản ngoại lệ (E1–E5) về kiểm soát băm rỗng, tiêu đề trống và thủ đoạn nghe lén Mempool (Front-running).

**Đánh giá:** Dùng được (sau khi sinh viên chấn chỉnh góc nhìn rủi ro Front-running và phân tách phạm vi nghiên cứu).

**Chỗ sai & Phản biện sắc bén của sinh viên:**
1. **Lỗi 1 (Hiểu sai bản chất tấn công Front-running trên Blockchain):** Trong bản nháp phân tích rủi ro, AI cảnh báo rằng *"kẻ xấu có thể nghe lén Mempool, thấy giao dịch nộp hash của tác giả và đẩy gas cao hơn để cướp trắng bản quyền"*. Sinh viên phản biện ngay: Kẻ xấu nghe lén Mempool thì chỉ thấy chuỗi băm 32 bytes vô nghĩa (`docHash`) và chuỗi tiêu đề (`title`), chứ kẻ xấu **hoàn toàn KHÔNG THỂ có tệp tài liệu nội dung nghiên cứu gốc** (vì tệp gốc được giữ tuyệt mật tại client của tác giả). Khi xảy ra tranh chấp trước Hội đồng khoa học, bên nào không xuất trình được tệp tài liệu gốc tạo ra đúng mã băm đó thì bên đó tự động bị kết luận là kẻ mạo danh. Do đó, cơ chế hàm băm một chiều đã tự thân giải quyết rủi ro này mà không cần cơ chế Commit-Reveal rườm rà gây tốn gấp đôi phí gas cho sinh viên.
2. **Lỗi 2 (Ảo tưởng về phạm vi pháp lý - Legal Overreach):** AI ban đầu ghi trong mục tiêu rằng "Hệ thống tự động cấp bằng độc quyền sáng chế quốc gia có giá trị thay thế Cục Sở hữu Trí tuệ". Sinh viên đã chấn chỉnh: Smart Contract chỉ là công cụ công nghệ cung cấp **Bằng chứng ưu tiên mật mã bất biến (Prior Art Evidence)**, không thể tự ý thay thế thẩm quyền cấp văn bằng bảo hộ nhà nước của cơ quan hành chính. Sinh viên đã yêu cầu chuyển mục này vào phần "Ngoài phạm vi (Out of Scope)" để đảm bảo tính chuẩn xác về mặt luật học và kinh tế thể chế.

**Ai phát hiện:** Sinh viên phát hiện và trực tiếp chấn chỉnh tư duy mật mã học và thể chế pháp lý của AI.









