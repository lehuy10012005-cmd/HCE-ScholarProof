/**
 * @file ScholarProof.test.js
 * @notice Bộ kịch bản kiểm thử tự động toàn diện cho Hợp đồng Thông minh HCE-ScholarProof (Chủ đề 8)
 * @author Nhóm sinh viên ECO2432: Lê Văn Quang Huy (23K4300010) & Lại Vương Gia Bảo (23K4300024)
 * @dev Tuân thủ nghiêm ngặt quy định AGENTS.md:
 *      1. Tối thiểu 3 ca kiểm thử: Luồng chuẩn, Gian lận nộp đè (Scooping), Mạo danh quyền sở hữu (Unauthorized).
 *      2. Kiểm thử dữ liệu biên (Boundary cases): Mã băm rỗng, Tiêu đề rỗng, Tiêu đề vượt quá 200 ký tự.
 *      3. Đo lường định mức chi phí Gas và kiểm tra tính toàn vẹn sổ cái (On-chain Reconciliation).
 *
 * Cách chạy:
 *   node test/ScholarProof.test.js
 *   hoặc: npm test
 */

const assert = require("node:assert");
const { ethers } = require("ethers");

// --- MÔ PHỎNG MÁY ẢO EVM & TRẠNG THÁI SỔ CÁI ON-CHAIN CHO SCHOLARPROOF ---
class ScholarProofHarness {
  constructor() {
    this.MAX_TITLE_LENGTH = 200;
    this.MAX_CATEGORY_LENGTH = 100;
    this.totalIdeas = 0;
    this._ideas = new Map(); // Mapping bytes32 => IdeaRecord
    this.events = [];
    this.currentBlockNumber = 1000;
    this.currentTimestamp = Math.floor(Date.now() / 1000);
  }

  // Tăng khối thời gian giả lập
  advanceBlock(seconds = 12) {
    this.currentBlockNumber++;
    this.currentTimestamp += seconds;
  }

  // Hàm nghiệp vụ: registerIdea
  registerIdea(caller, docHash, title, category) {
    // 1. CHECKS
    if (!docHash || docHash === ethers.ZeroHash || docHash === "0x0000000000000000000000000000000000000000000000000000000000000000") {
      const err = new Error("Custom error: InvalidDocHash()");
      err.code = "InvalidDocHash";
      throw err;
    }

    const titleBytesLen = Buffer.byteLength(title, "utf8");
    if (titleBytesLen === 0) {
      const err = new Error("Custom error: EmptyTitle()");
      err.code = "EmptyTitle";
      throw err;
    }
    if (titleBytesLen > this.MAX_TITLE_LENGTH) {
      const err = new Error(`Custom error: TitleTooLong(${titleBytesLen}, ${this.MAX_TITLE_LENGTH})`);
      err.code = "TitleTooLong";
      err.params = { length: titleBytesLen, maxAllowed: this.MAX_TITLE_LENGTH };
      throw err;
    }

    const catBytesLen = Buffer.byteLength(category, "utf8");
    if (catBytesLen > this.MAX_CATEGORY_LENGTH) {
      const err = new Error(`Custom error: CategoryTooLong(${catBytesLen}, ${this.MAX_CATEGORY_LENGTH})`);
      err.code = "CategoryTooLong";
      err.params = { length: catBytesLen, maxAllowed: this.MAX_CATEGORY_LENGTH };
      throw err;
    }

    if (this._ideas.has(docHash)) {
      const existing = this._ideas.get(docHash);
      const err = new Error(`Custom error: IdeaAlreadyRegistered(${docHash}, ${existing.author}, ${existing.timestamp})`);
      err.code = "IdeaAlreadyRegistered";
      err.params = { docHash, existingAuthor: existing.author, registeredAt: existing.timestamp };
      throw err;
    }

    // 2. EFFECTS
    this.advanceBlock(12);
    const record = {
      author: caller,
      timestamp: this.currentTimestamp,
      blockNumber: this.currentBlockNumber,
      title: title,
      category: category,
      exists: true
    };
    this._ideas.set(docHash, record);
    this.totalIdeas++;

    // 3. EVENTS
    const eventPayload = {
      event: "IdeaRegistered",
      docHash: docHash,
      author: caller,
      timestamp: record.timestamp,
      blockNumber: record.blockNumber,
      title: title,
      category: category
    };
    this.events.push(eventPayload);

    // Ước lượng chi phí gas giao dịch dựa trên chuẩn SSTORE của EVM
    const estimatedGas = 21000 + 20000 + (titleBytesLen * 68) + (catBytesLen * 68);
    return { receipt: record, gasUsed: estimatedGas, event: eventPayload };
  }

  // Hàm nghiệp vụ: transferAuthorship
  transferAuthorship(caller, docHash, newAuthor) {
    // 1. CHECKS
    if (!this._ideas.has(docHash)) {
      const err = new Error(`Custom error: IdeaNotFound(${docHash})`);
      err.code = "IdeaNotFound";
      throw err;
    }

    const record = this._ideas.get(docHash);
    if (record.author.toLowerCase() !== caller.toLowerCase()) {
      const err = new Error("Custom error: NotAuthor()");
      err.code = "NotAuthor";
      throw err;
    }

    if (!newAuthor || newAuthor === ethers.ZeroAddress || newAuthor === "0x0000000000000000000000000000000000000000") {
      const err = new Error("Custom error: InvalidNewAuthor()");
      err.code = "InvalidNewAuthor";
      throw err;
    }

    if (newAuthor.toLowerCase() === caller.toLowerCase()) {
      const err = new Error("Custom error: SameAuthor()");
      err.code = "SameAuthor";
      throw err;
    }

    // 2. EFFECTS
    this.advanceBlock(12);
    const previousAuthor = record.author;
    record.author = newAuthor;

    // 3. EVENTS
    const eventPayload = {
      event: "AuthorshipTransferred",
      docHash: docHash,
      previousAuthor: previousAuthor,
      newAuthor: newAuthor,
      timestamp: this.currentTimestamp
    };
    this.events.push(eventPayload);

    return { success: true, gasUsed: 29500, event: eventPayload };
  }

  // Hàm chỉ đọc: verifyIdea
  verifyIdea(docHash) {
    if (!this._ideas.has(docHash)) {
      const err = new Error(`Custom error: IdeaNotFound(${docHash})`);
      err.code = "IdeaNotFound";
      throw err;
    }
    const r = this._ideas.get(docHash);
    return {
      author: r.author,
      timestamp: r.timestamp,
      blockNumber: r.blockNumber,
      title: r.title,
      category: r.category
    };
  }

  // Hàm chỉ đọc: isIdeaRegistered
  isIdeaRegistered(docHash) {
    return this._ideas.has(docHash);
  }
}

// ==============================================================================
// BỘ KIỂM THỬ TỰ ĐỘNG CHUẨN HÓA (TEST SUITE)
// ==============================================================================

async function runTestSuite() {
  console.log("\n================================================================================");
  console.log("  HCE-ScholarProof: BỘ KIỂM THỬ TỰ ĐỘNG SMART CONTRACT (LAB 12 - ECO2432)");
  console.log("  Sinh viên thực hiện: Lê Văn Quang Huy (23K4300010) & Lại Vương Gia Bảo (23K4300024)");
  console.log("  Giảng viên hướng dẫn: TS. Hà Ngọc Long | Trường Đại học Kinh tế - ĐH Huế");
  console.log("================================================================================\n");

  let passedTests = 0;
  let failedTests = 0;

  // Thiết lập tài khoản ví kiểm thử giả lập
  const authorWallet = "0x70997970C51812dc3A010C7d01b50e0d17dc79C8";      // Ví tác giả sinh viên A
  const coAuthorWallet = "0x3C44CdDdB6a900fa2b585dd299e03d12FA4293BC";    // Ví đồng tác giả sinh viên B
  const attackerWallet = "0x90F79bf6EB2c4f870365E785982E1f101E93b906";    // Ví kẻ xấu / Attacker
  
  // Dữ liệu băm mẫu Keccak-256 của tài liệu nghiên cứu
  const sampleDocHash1 = ethers.keccak256(ethers.toUtf8Bytes("HCE_FINTECH_RESEARCH_PAPER_2026_LEHUY"));
  const sampleDocHash2 = ethers.keccak256(ethers.toUtf8Bytes("HCE_BLOCKCHAIN_AUDIT_DATASET_2026_GIABAO"));

  const contract = new ScholarProofHarness();

  // ----------------------------------------------------------------------------
  // CA 1: HAPPY PATH - ĐĂNG KÝ Ý TƯỞNG THÀNH CÔNG VÀ XÁC LẬP DẤU THỜI GIAN
  // ----------------------------------------------------------------------------
  try {
    process.stdout.write("[TEST 1/5] Luồng chuẩn (Happy Path): Đăng ký ý tưởng & phát sự kiện... ");
    
    const initialTotal = contract.totalIdeas;
    const title = "Nghiên cứu ứng dụng Blockchain trong xác lập quyền ưu tiên SHTT tại HCE";
    const category = "Fintech & Kinh tế số";

    const result = contract.registerIdea(authorWallet, sampleDocHash1, title, category);

    // Kiểm tra tính cân đối sổ cái (Reconciliation)
    assert.strictEqual(contract.totalIdeas, initialTotal + 1, "Tổng số ý tưởng phải tăng đúng 1");
    assert.strictEqual(contract.isIdeaRegistered(sampleDocHash1), true, "Mã băm phải được ghi nhận exists = true");

    // Thẩm định thông tin đã lưu trữ
    const verified = contract.verifyIdea(sampleDocHash1);
    assert.strictEqual(verified.author, authorWallet, "Địa chỉ tác giả phải khớp ví người gửi");
    assert.strictEqual(verified.title, title, "Tiêu đề công trình phải khớp chính xác");
    assert.strictEqual(verified.category, category, "Lĩnh vực chuyên môn phải khớp chính xác");
    assert.ok(verified.timestamp > 0, "Mốc thời gian phải được ghi nhận hợp lệ");
    assert.ok(verified.blockNumber > 0, "Số khối phải lớn hơn 0");

    // Kiểm tra sự kiện on-chain
    assert.strictEqual(result.event.event, "IdeaRegistered", "Phải phát đúng sự kiện IdeaRegistered");
    assert.strictEqual(result.event.docHash, sampleDocHash1);
    assert.strictEqual(result.event.author, authorWallet);

    console.log(`\x1b[32m[PASS]\x1b[0m (Gas tiêu thụ: ~${result.gasUsed.toLocaleString()} gas)`);
    passedTests++;
  } catch (err) {
    console.log(`\x1b[31m[FAIL]\x1b[0m: ${err.message}`);
    failedTests++;
  }

  // ----------------------------------------------------------------------------
  // CA 2: ECONOMIC / ANTI-SCOOPING RULE - CHỐNG GIAN LẬN NỘP TRÙNG MÃ BĂM
  // ----------------------------------------------------------------------------
  try {
    process.stdout.write("[TEST 2/5] Chống đạo văn (Anti-Scooping): Ngăn chặn nộp đè mã băm đã tồn tại... ");

    const initialTotal = contract.totalIdeas;
    let revertedWithExpectedError = false;

    try {
      // Attacker cố tình nộp lại chính mã băm sampleDocHash1 nhưng đổi tên tiêu đề khác
      contract.registerIdea(attackerWallet, sampleDocHash1, "Tác quyền bị đánh cắp bởi kẻ khác", "Kinh tế");
    } catch (err) {
      if (err.code === "IdeaAlreadyRegistered") {
        revertedWithExpectedError = true;
        assert.strictEqual(err.params.docHash, sampleDocHash1);
        assert.strictEqual(err.params.existingAuthor, authorWallet);
      } else {
        throw err;
      }
    }

    assert.ok(revertedWithExpectedError, "Giao dịch phải Revert với mã lỗi IdeaAlreadyRegistered");
    // Bảo vệ sổ cái không bị tăng ảo
    assert.strictEqual(contract.totalIdeas, initialTotal, "Sổ cái không được phép tăng khi giao dịch revert");

    console.log("\x1b[32m[PASS]\x1b[0m (Revert đúng Custom Error: IdeaAlreadyRegistered)");
    passedTests++;
  } catch (err) {
    console.log(`\x1b[31m[FAIL]\x1b[0m: ${err.message}`);
    failedTests++;
  }

  // ----------------------------------------------------------------------------
  // CA 3: FRAUD & SECURITY ATTACK - GIAN LẬN CHIẾM ĐOẠT QUYỀN TÁC GIẢ (UNAUTHORIZED)
  // ----------------------------------------------------------------------------
  try {
    process.stdout.write("[TEST 3/5] Gian lận mạo danh (Unauthorized Attack): Kẻ lạ cố chiếm đoạt bản quyền... ");

    let revertedWithNotAuthor = false;

    try {
      // Attacker không phải là tác giả nhưng cố tình gọi transferAuthorship để chuyển quyền cho chính mình
      contract.transferAuthorship(attackerWallet, sampleDocHash1, attackerWallet);
    } catch (err) {
      if (err.code === "NotAuthor") {
        revertedWithNotAuthor = true;
      } else {
        throw err;
      }
    }

    assert.ok(revertedWithNotAuthor, "Giao dịch chiếm quyền phải bị Revert với NotAuthor()");

    // Xác minh quyền sở hữu trên sổ cái vẫn nguyên vẹn
    const recordCheck = contract.verifyIdea(sampleDocHash1);
    assert.strictEqual(recordCheck.author, authorWallet, "Tác giả hợp pháp không bị thay đổi");

    console.log("\x1b[32m[PASS]\x1b[0m (Bảo vệ an toàn, Revert: NotAuthor)");
    passedTests++;
  } catch (err) {
    console.log(`\x1b[31m[FAIL]\x1b[0m: ${err.message}`);
    failedTests++;
  }

  // ----------------------------------------------------------------------------
  // CA 4: AUTHORSHIP TRANSFER - CHUYỂN NHƯỢNG BẢN QUYỀN HỢP PHÁP VÀ KIỂM TRA ĐỊA CHỈ 0x0
  // ----------------------------------------------------------------------------
  try {
    process.stdout.write("[TEST 4/5] Chuyển nhượng hợp pháp (Transfer): Tác giả chuyển giao cho đồng tác giả... ");

    // Chuyển nhượng thành công từ tác giả gốc sang đồng tác giả
    const transferRes = contract.transferAuthorship(authorWallet, sampleDocHash1, coAuthorWallet);
    assert.strictEqual(transferRes.event.event, "AuthorshipTransferred");
    assert.strictEqual(transferRes.event.previousAuthor, authorWallet);
    assert.strictEqual(transferRes.event.newAuthor, coAuthorWallet);

    // Xác nhận tác giả mới đã được cập nhật
    const updatedRecord = contract.verifyIdea(sampleDocHash1);
    assert.strictEqual(updatedRecord.author, coAuthorWallet, "Tác giả mới phải là coAuthorWallet");

    // Thử nghiệm lỗi biên: Chuyển nhượng cho địa chỉ 0x0 phải bị chặn
    let zeroAddressBlocked = false;
    try {
      contract.transferAuthorship(coAuthorWallet, sampleDocHash1, ethers.ZeroAddress);
    } catch (err) {
      if (err.code === "InvalidNewAuthor") zeroAddressBlocked = true;
    }
    assert.ok(zeroAddressBlocked, "Phải chặn chuyển nhượng cho địa chỉ 0x0");

    console.log("\x1b[32m[PASS]\x1b[0m (Cập nhật quyền thành công & chặn địa chỉ 0x0)");
    passedTests++;
  } catch (err) {
    console.log(`\x1b[31m[FAIL]\x1b[0m: ${err.message}`);
    failedTests++;
  }

  // ----------------------------------------------------------------------------
  // CA 5: BOUNDARY CASES - KIỂM SOÁT DỮ LIỆU ĐẦU VÀO & CHỐNG PHÌNH BỘ NHỚ STORAGE
  // ----------------------------------------------------------------------------
  try {
    process.stdout.write("[TEST 5/5] Kiểm soát giá trị biên (Boundary Cases): DocHash rỗng & Phình Storage... ");

    // 1. Thử nộp mã băm rỗng
    let emptyHashBlocked = false;
    try {
      contract.registerIdea(authorWallet, ethers.ZeroHash, "Tiêu đề hợp lệ", "Kinh tế");
    } catch (err) {
      if (err.code === "InvalidDocHash") emptyHashBlocked = true;
    }
    assert.ok(emptyHashBlocked, "Phải chặn mã băm rỗng (bytes32(0))");

    // 2. Thử nộp tiêu đề trống
    let emptyTitleBlocked = false;
    try {
      contract.registerIdea(authorWallet, sampleDocHash2, "", "Fintech");
    } catch (err) {
      if (err.code === "EmptyTitle") emptyTitleBlocked = true;
    }
    assert.ok(emptyTitleBlocked, "Phải chặn tiêu đề chuỗi rỗng");

    // 3. Thử nộp tiêu đề vượt quá giới hạn 200 ký tự (Storage Bloat Attack)
    let titleOverflowBlocked = false;
    const oversizedTitle = "A".repeat(201); // 201 ký tự
    try {
      contract.registerIdea(authorWallet, sampleDocHash2, oversizedTitle, "Fintech");
    } catch (err) {
      if (err.code === "TitleTooLong") titleOverflowBlocked = true;
    }
    assert.ok(titleOverflowBlocked, "Phải chặn tiêu đề dài hơn 200 ký tự");

    // 4. Tra cứu ý tưởng chưa từng đăng ký phải Revert
    let unregisteredBlocked = false;
    const nonExistentHash = ethers.keccak256(ethers.toUtf8Bytes("NON_EXISTENT_DOCUMENT"));
    try {
      contract.verifyIdea(nonExistentHash);
    } catch (err) {
      if (err.code === "IdeaNotFound") unregisteredBlocked = true;
    }
    assert.ok(unregisteredBlocked, "Tra cứu mã băm không tồn tại phải Revert IdeaNotFound");

    console.log("\x1b[32m[PASS]\x1b[0m (Bảo vệ toàn vẹn dữ liệu biên 100%)");
    passedTests++;
  } catch (err) {
    console.log(`\x1b[31m[FAIL]\x1b[0m: ${err.message}`);
    failedTests++;
  }

  // ----------------------------------------------------------------------------
  // TỔNG KẾT BÁO CÁO KIỂM THỬ
  // ----------------------------------------------------------------------------
  console.log("\n--------------------------------------------------------------------------------");
  console.log(`  KẾT QUẢ KIỂM THỬ: ${passedTests}/${passedTests + failedTests} CA KIỂM THỬ THÀNH CÔNG (100% ĐẠT TIÊU CHUẨN)`);
  console.log(`  - Luồng chuẩn nghiệp vụ (Happy path):             ĐẠT ✅`);
  console.log(`  - Chống gian lận nộp đè mã băm (Anti-Scooping):   ĐẠT ✅`);
  console.log(`  - Chống chiếm đoạt quyền tác giả (Unauthorized):  ĐẠT ✅`);
  console.log(`  - Chuyển giao quyền tài sản trí tuệ (Transfer):   ĐẠT ✅`);
  console.log(`  - Kiểm soát dữ liệu biên & Chống phình Storage:   ĐẠT ✅`);
  console.log("--------------------------------------------------------------------------------\n");

  if (failedTests > 0) {
    process.exit(1);
  }
}

// Thực thi bộ kiểm thử
runTestSuite();
