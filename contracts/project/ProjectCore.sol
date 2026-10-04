// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "../capstone/ScholarProof.sol";

/**
 * @title ProjectCore (Hợp đồng lõi Đồ án Capstone HCE-ScholarProof)
 * @author Nhóm sinh viên ECO2432: Lê Văn Quang Huy & Lại Vương Gia Bảo
 * @notice Tệp định danh chuẩn contracts/project/ProjectCore.sol theo quy định của học phần ECO2432.
 *         Kế thừa toàn bộ logic nghiệp vụ cốt lõi đã được kiểm toán từ ScholarProof v2.
 */
contract ProjectCore is ScholarProof {
    // Kế thừa toàn bộ logic, sự kiện và cấu trúc lỗi của ScholarProof.
    // Sẵn sàng tích hợp thêm các quy tắc kinh tế (thu phí vi mô, chứng chỉ NFT/SBT) ở Lab 11.
}
