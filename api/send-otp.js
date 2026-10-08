const nodemailer = require('nodemailer');
const fs = require('fs');
const path = require('path');

// Nạp file .env nếu có (khi chạy local/dev)
function loadEnv() {
  const candidates = [
    path.join(process.cwd(), '.env'),
    path.join(__dirname, '..', '.env')
  ];
  for (const c of candidates) {
    if (fs.existsSync(c)) {
      try {
        const text = fs.readFileSync(c, 'utf8');
        for (const line of text.split('\n')) {
          const trimmed = line.trim();
          if (trimmed && !trimmed.startsWith('#') && trimmed.includes('=')) {
            const idx = trimmed.indexOf('=');
            const k = trimmed.slice(0, idx).trim();
            const v = trimmed.slice(idx + 1).trim().replace(/^["']|["']$/g, '');
            if (!process.env[k]) {
              process.env[k] = v;
            }
          }
        }
        break;
      } catch (e) {}
    }
  }
}

loadEnv();

module.exports = async function handler(req, res) {
  // CORS Headers cho phép gọi từ GitHub Pages và bất kỳ máy nào
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type, Authorization');

  if (req.method === 'OPTIONS') {
    return res.status(200).end();
  }

  if (req.method === 'GET') {
    const user = process.env.GMAIL_USER || '';
    const hasPass = Boolean(process.env.GMAIL_APP_PASSWORD);
    return res.status(200).json({
      status: 'online',
      service: 'HCE Ledger Vercel Cloud OTP Service',
      sender_configured: Boolean(user && hasPass)
    });
  }

  if (req.method !== 'POST') {
    return res.status(405).json({ success: false, error: 'Method Not Allowed' });
  }

  try {
    let body = req.body;
    if (typeof body === 'string') {
      try {
        body = JSON.parse(body);
      } catch (e) {}
    }
    body = body || {};

    const toEmail = (body.email || '').trim();
    const toName = (body.name || 'Tác giả').trim();
    const otpCode = String(body.otp || '').trim();

    if (!toEmail || !otpCode) {
      return res.status(400).json({ success: false, error: 'Thiếu địa chỉ email hoặc mã OTP' });
    }

    const gmailUser = (process.env.GMAIL_USER || '').trim();
    const gmailPass = (process.env.GMAIL_APP_PASSWORD || '').replace(/\s+/g, '').trim();

    if (!gmailUser || !gmailPass) {
      return res.status(500).json({
        success: false,
        error: 'Chưa cấu hình GMAIL_USER hoặc GMAIL_APP_PASSWORD trong Environment Variables của Vercel!'
      });
    }

    const transporter = nodemailer.createTransport({
      host: 'smtp.gmail.com',
      port: 587,
      secure: false, // STARTTLS
      auth: {
        user: gmailUser,
        pass: gmailPass
      },
      tls: {
        rejectUnauthorized: false
      }
    });

    const mailOptions = {
      from: `"HCE Ledger • Xác Thực Bản Quyền" <${gmailUser}>`,
      to: toEmail,
      subject: `Mã xác thực đăng ký tài khoản HCE Ledger: ${otpCode}`,
      text: `Xin chào ${toName},\n\nMã xác nhận đăng ký tài khoản trên hệ thống HCE Ledger của bạn là: ${otpCode}\n\nMã có hiệu lực trong vòng 5 phút.\n\nTrân trọng,\nLê Văn Quang Huy - Dự án HCE Ledger (ĐH Kinh tế Huế)`,
      html: `
        <!DOCTYPE html>
        <html>
        <head><meta charset="utf-8"></head>
        <body style="margin: 0; padding: 24px; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; background-color: #f9fafb; color: #111827;">
          <div style="max-width: 520px; margin: 0 auto; background: #ffffff; border: 1px solid #e5e7eb; border-radius: 8px; padding: 32px 28px; box-shadow: 0 1px 3px rgba(0,0,0,0.05);">
            <div style="border-bottom: 2px solid #2563eb; padding-bottom: 12px; margin-bottom: 20px;">
              <h2 style="margin: 0; font-size: 18px; color: #1e3a8a; font-weight: 700;">Hệ thống Bản quyền Số HCE Ledger</h2>
              <p style="margin: 4px 0 0; font-size: 12px; color: #6b7280;">Trường Đại học Kinh tế - Đại học Huế</p>
            </div>

            <p style="font-size: 14.5px; line-height: 1.6; margin: 0 0 16px;">Xin chào <strong>${toName}</strong>,</p>
            <p style="font-size: 14px; line-height: 1.6; color: #374151; margin: 0 0 20px;">
              Bạn vừa thực hiện đăng ký tài khoản trên cổng dịch vụ <strong>HCE Ledger</strong>. Dưới đây là mã số OTP xác nhận của bạn:
            </p>

            <div style="background: #f0fdf4; border: 1px solid #bbf7d0; border-radius: 6px; padding: 18px; text-align: center; margin: 0 0 24px;">
              <div style="font-size: 12px; color: #166534; font-weight: 600; text-transform: uppercase; margin-bottom: 6px;">Mã xác nhận tài khoản</div>
              <div style="font-size: 32px; font-weight: 800; letter-spacing: 6px; color: #15803d; font-family: 'Consolas', 'Courier New', monospace;">${otpCode}</div>
              <div style="font-size: 12px; color: #4b5563; margin-top: 6px;">Hiệu lực trong 5 phút</div>
            </div>

            <p style="font-size: 13px; line-height: 1.5; color: #6b7280; margin: 0 0 24px;">
              Nếu bạn không yêu cầu mã này, vui lòng bỏ qua email.
            </p>

            <div style="border-top: 1px solid #f3f4f6; padding-top: 16px; font-size: 12px; color: #9ca3af; line-height: 1.5;">
              Trân trọng,<br>
              <strong>Lê Văn Quang Huy</strong> • Phân hiệu Web3 / LegalTech<br>
              Khoa Hệ thống Thông tin Kinh tế, Trường Đại học Kinh tế - ĐH Huế
            </div>
          </div>
        </body>
        </html>
      `
    };

    await transporter.sendMail(mailOptions);
    return res.status(200).json({
      success: true,
      message: `Mã OTP đã được gửi thẳng tới Gmail: ${toEmail}`
    });

  } catch (error) {
    console.error('Lỗi khi gửi email:', error);
    return res.status(500).json({
      success: false,
      error: 'Lỗi gửi email: ' + (error.message || error)
    });
  }
};
