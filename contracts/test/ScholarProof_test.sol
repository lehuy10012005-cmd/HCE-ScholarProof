// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "../capstone/ScholarProof.sol";

// Giao diện Assert chuẩn cho môi trường Remix IDE và Foundry
interface IAssert {
    function equal(uint256 a, uint256 b, string memory message) external returns (bool);
    function equal(address a, address b, string memory message) external returns (bool);
    function equal(bool a, bool b, string memory message) external returns (bool);
    function ok(bool a, string memory message) external returns (bool);
}

/**
 * @title ScholarProofTest (Bộ kiểm thử On-Chain Solidity)
 * @author Nhóm sinh viên ECO2432: Lê Văn Quang Huy (23K4300010) & Lại Vương Gia Bảo (23K4300024)
 * @notice Tệp kiểm thử đơn vị On-chain tương thích với Remix IDE (Solidity Unit Testing Plugin)
 *         và Hardhat/Foundry, xác thực các bất biến kinh tế và luồng phòng vệ gian lận.
 */
contract ScholarProofTest {
    ScholarProof private _contract;

    bytes32 private constant SAMPLE_DOC_HASH_1 = keccak256("HCE_RESEARCH_PAPER_TEST_01");
    bytes32 private constant SAMPLE_DOC_HASH_2 = keccak256("HCE_RESEARCH_PAPER_TEST_02");

    // Khởi tạo hợp đồng mới trước mỗi ca kiểm thử
    function beforeEach() public {
        _contract = new ScholarProof();
    }

    /**
     * @notice Ca 1: Luồng chuẩn - Đăng ký ý tưởng và xác lập dấu thời gian thành công
     */
    function testRegisterIdeaSuccess() public {
        string memory title = "He thong xac thuc quyen tac gia Web3";
        string memory category = "Fintech";

        _contract.registerIdea(SAMPLE_DOC_HASH_1, title, category);

        require(_contract.totalIdeas() == 1, "Tong so y tuong tren so cai phai la 1");
        require(_contract.isIdeaRegistered(SAMPLE_DOC_HASH_1) == true, "DocHash phai duoc danh dau exists");

        (
            address author,
            uint256 timestamp,
            uint256 blockNumber,
            string memory resTitle,
            string memory resCategory
        ) = _contract.verifyIdea(SAMPLE_DOC_HASH_1);

        require(author == address(this), "Tac gia phai la dia chi hop dong kiem thu");
        require(timestamp > 0, "Timestamp phai hop le");
        require(blockNumber > 0, "Block number phai lon hon 0");
        require(keccak256(bytes(resTitle)) == keccak256(bytes(title)), "Tieu de khong khop");
        require(keccak256(bytes(resCategory)) == keccak256(bytes(category)), "Linh vuc khong khop");
    }

    /**
     * @notice Ca 2: Chống gian lận nộp đè (Anti-Scooping) - Nộp trùng hash bắt buộc Revert
     */
    function testRegisterDuplicateHashShouldFail() public {
        _contract.registerIdea(SAMPLE_DOC_HASH_1, "Ban thao goc", "Kinh te so");

        // Thử nộp lại cùng docHash với tiêu đề khác
        try _contract.registerIdea(SAMPLE_DOC_HASH_1, "Dao van tieu de", "AI") {
            revert("Loi: Hop dong khong duoc phep cho nop trung ma bam");
        } catch {
            // Chặn thành công
            require(_contract.totalIdeas() == 1, "So cai khong duoc tang khi bi revert");
        }
    }

    /**
     * @notice Ca 3: Kiểm soát dữ liệu biên - Chặn mã băm rỗng bytes32(0)
     */
    function testEmptyDocHashShouldFail() public {
        try _contract.registerIdea(bytes32(0), "Tieu de hop le", "Fintech") {
            revert("Loi: Khong duoc chap nhan bytes32(0)");
        } catch {
            // Chặn thành công
        }
    }

    /**
     * @notice Ca 4: Kiểm soát độ dài dữ liệu - Chặn tiêu đề vượt quá 200 ký tự (Storage Bloat)
     */
    function testOversizedTitleShouldFail() public {
        // Tạo chuỗi 205 ký tự
        bytes memory longBytes = new bytes(205);
        for (uint256 i = 0; i < 205; i++) {
            longBytes[i] = "A";
        }
        string memory longTitle = string(longBytes);

        try _contract.registerIdea(SAMPLE_DOC_HASH_2, longTitle, "Fintech") {
            revert("Loi: Phai chan tieu de qua 200 ky tu de tiet kiem Storage");
        } catch {
            // Chặn thành công
        }
    }
}
