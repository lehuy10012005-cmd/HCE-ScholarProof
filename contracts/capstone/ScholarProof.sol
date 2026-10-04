// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

/**
 * @title HCE-ScholarProof (v2 - Phiên bản tối ưu & an toàn sau kiểm toán Lab 10)
 * @author Nhóm sinh viên ECO2432: Lê Văn Quang Huy (23K4300010) & Lại Vương Gia Bảo (23K4300024)
 * @notice Hợp đồng thông minh xác lập bằng chứng ưu tiên (Proof of Existence) và dấu thời gian (Timestamping)
 *         cho các ý tưởng nghiên cứu khoa học, đề cương và dữ liệu sơ bộ tại Trường Đại học Kinh tế, Đại học Huế.
 * @dev Tuân thủ chuẩn mực AGENTS.md:
 *      1. Áp dụng nghiêm ngặt mô hình Checks-Effects-Interactions (CEI).
 *      2. Mọi hàm thay đổi trạng thái đều phát Event có indexed để truy vấn ngoài chuỗi.
 *      3. Sử dụng Custom Errors thay cho chuỗi require dài giúp tiết kiệm gas giao dịch.
 *      4. Giới hạn độ dài dữ liệu chuỗi (title, category) ngăn chặn tấn công làm phình bộ nhớ Storage (Storage Bloat).
 *      5. Hỗ trợ chuyển nhượng quyền tác giả/sở hữu trí tuệ (Authorship Transfer) với kiểm tra phân quyền chặt chẽ.
 */
contract ScholarProof {
    // --- HẰNG SỐ AN TOÀN VÀ ĐỊNH MỨC DỮ LIỆU ---
    uint256 public constant MAX_TITLE_LENGTH = 200;       // Giới hạn 200 ký tự cho tiêu đề
    uint256 public constant MAX_CATEGORY_LENGTH = 100;    // Giới hạn 100 ký tự cho lĩnh vực nghiên cứu

    // --- CẤU TRÚC DỮ LIỆU SỔ CÁI ON-CHAIN ---
    struct IdeaRecord {
        address author;        // Địa chỉ ví của tác giả / chủ sở hữu hợp pháp hiện tại
        uint256 timestamp;     // Mốc thời gian khối (block.timestamp) khi đăng ký ban đầu
        uint256 blockNumber;   // Thứ tự khối giao dịch xác nhận
        string title;          // Tiêu đề ý tưởng / công trình nghiên cứu
        string category;       // Lĩnh vực chuyên môn (Kinh tế số, Fintech, AI, ...)
        bool exists;           // Cờ đánh dấu đã xác lập trên sổ cái
    }

    // Ánh xạ từ vân tay số 32 bytes (docHash Keccak-256) sang bản ghi quyền tác giả
    mapping(bytes32 => IdeaRecord) private _ideas;

    // Tổng số lượng công trình nghiên cứu đã được bảo chứng trên hệ thống
    uint256 public totalIdeas;

    // --- SỰ KIỆN ON-CHAIN (EVENTS) ---
    event IdeaRegistered(
        bytes32 indexed docHash,
        address indexed author,
        uint256 timestamp,
        uint256 blockNumber,
        string title,
        string category
    );

    event AuthorshipTransferred(
        bytes32 indexed docHash,
        address indexed previousAuthor,
        address indexed newAuthor,
        uint256 timestamp
    );

    // --- CẤU TRÚC LỖI TÙY BIẾN (CUSTOM ERRORS) ---
    error InvalidDocHash();                                              // Mã băm rỗng (bytes32(0))
    error EmptyTitle();                                                  // Tiêu đề để trống
    error TitleTooLong(uint256 length, uint256 maxAllowed);              // Tiêu đề vượt quá giới hạn an toàn
    error CategoryTooLong(uint256 length, uint256 maxAllowed);           // Lĩnh vực vượt quá giới hạn an toàn
    error IdeaAlreadyRegistered(bytes32 docHash, address existingAuthor, uint256 registeredAt); // Ý tưởng đã có người đăng ký
    error IdeaNotFound(bytes32 docHash);                                 // Mã băm chưa từng tồn tại trên sổ cái
    error NotAuthor();                                                   // Người gọi không phải là tác giả hợp pháp
    error InvalidNewAuthor();                                            // Địa chỉ tác giả mới là địa chỉ 0x0
    error SameAuthor();                                                  // Chuyển nhượng cho chính mình

    // --- CÁC HÀM NGHIỆP VỤ CỐT LÕI ---

    /**
     * @notice Đăng ký quyền tác giả và xác lập bằng chứng ưu tiên (Prior Art) cho ý tưởng nghiên cứu
     * @dev Áp dụng mô hình Checks-Effects-Interactions (CEI). Không lưu trữ tệp gốc để tiết kiệm gas.
     * @param docHash Mã băm Keccak-256 (32 bytes) của tệp tài liệu nghiên cứu tính toán tại trình duyệt
     * @param title Tiêu đề công trình / ý tưởng nghiên cứu
     * @param category Lĩnh vực khoa học
     */
    function registerIdea(
        bytes32 docHash,
        string calldata title,
        string calldata category
    ) external {
        // 1. CHECKS: Kiểm tra tính hợp lệ và toàn vẹn của dữ liệu đầu vào
        if (docHash == bytes32(0)) revert InvalidDocHash();
        
        uint256 titleLen = bytes(title).length;
        if (titleLen == 0) revert EmptyTitle();
        if (titleLen > MAX_TITLE_LENGTH) revert TitleTooLong(titleLen, MAX_TITLE_LENGTH);

        uint256 catLen = bytes(category).length;
        if (catLen > MAX_CATEGORY_LENGTH) revert CategoryTooLong(catLen, MAX_CATEGORY_LENGTH);

        if (_ideas[docHash].exists) {
            revert IdeaAlreadyRegistered(docHash, _ideas[docHash].author, _ideas[docHash].timestamp);
        }

        // 2. EFFECTS: Cập nhật trạng thái bộ nhớ lưu trữ bền vững (Storage)
        _ideas[docHash] = IdeaRecord({
            author: msg.sender,
            timestamp: block.timestamp,
            blockNumber: block.number,
            title: title,
            category: category,
            exists: true
        });

        unchecked {
            totalIdeas++;
        }

        // Phát sự kiện on-chain thông báo cho mạng lưới và ứng dụng Web3 client
        emit IdeaRegistered(
            docHash,
            msg.sender,
            block.timestamp,
            block.number,
            title,
            category
        );
    }

    /**
     * @notice Chuyển nhượng quyền tác giả / quyền sở hữu trí tuệ của ý tưởng cho cá nhân/tổ chức mới
     * @dev Chỉ tác giả hiện tại mới có quyền thực hiện giao dịch này. Tuân thủ CEI.
     * @param docHash Mã băm của tài liệu nghiên cứu cần chuyển nhượng
     * @param newAuthor Địa chỉ ví Web3 của người nhận quyền tác giả mới
     */
    function transferAuthorship(bytes32 docHash, address newAuthor) external {
        // 1. CHECKS
        IdeaRecord storage record = _ideas[docHash];
        if (!record.exists) revert IdeaNotFound(docHash);
        if (record.author != msg.sender) revert NotAuthor();
        if (newAuthor == address(0)) revert InvalidNewAuthor();
        if (newAuthor == msg.sender) revert SameAuthor();

        // 2. EFFECTS
        address previousAuthor = record.author;
        record.author = newAuthor;

        // Phát sự kiện chuyển giao quyền tài sản trí tuệ
        emit AuthorshipTransferred(docHash, previousAuthor, newAuthor, block.timestamp);
    }

    /**
     * @notice Tra cứu và thẩm định quyền tác giả của một tài liệu nghiên cứu
     * @dev Hàm view chỉ đọc, không tốn gas khi gọi từ bên ngoài chuỗi
     * @param docHash Mã băm của tài liệu cần kiểm chứng
     * @return author Địa chỉ ví của tác giả/chủ sở hữu hiện tại
     * @return timestamp Mốc thời gian khối khi đăng ký lần đầu
     * @return blockNumber Số thứ tự khối giao dịch xác nhận
     * @return title Tiêu đề công trình
     * @return category Lĩnh vực nghiên cứu
     */
    function verifyIdea(bytes32 docHash) external view returns (
        address author,
        uint256 timestamp,
        uint256 blockNumber,
        string memory title,
        string memory category
    ) {
        IdeaRecord memory record = _ideas[docHash];
        if (!record.exists) revert IdeaNotFound(docHash);

        return (
            record.author,
            record.timestamp,
            record.blockNumber,
            record.title,
            record.category
        );
    }

    /**
     * @notice Kiểm tra nhanh xem mã băm tài liệu đã từng được đăng ký hay chưa
     * @param docHash Mã băm tài liệu
     * @return isRegistered true nếu đã đăng ký, false nếu chưa
     */
    function isIdeaRegistered(bytes32 docHash) external view returns (bool isRegistered) {
        return _ideas[docHash].exists;
    }
}
