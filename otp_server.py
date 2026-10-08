#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
================================================================================
  COPYCHAIN - MÁY CHỦ GỬI MÃ OTP XÁC THỰC QUA GMAIL THẬT (SMTP GMAIL SERVICE)
  Dự án: Hệ thống Quản trị & Xác thực Bản quyền Tác giả On-chain ECO2432
  Tác giả: Lê Huy (ECO2432)
================================================================================
  Mô tả:
  - Máy chủ cục bộ (Local Server) sử dụng thư viện chuẩn của Python.
  - Tự động đọc biến môi trường GMAIL_USER và GMAIL_APP_PASSWORD từ tệp .env (bảo mật theo chuẩn AGENTS.md).
  - Kết nối trực tiếp đến máy chủ Google (smtp.gmail.com:587 qua TLS) để gửi thư từ chính hộp thư Gmail của bạn.
  - Hỗ trợ CORS đầy đủ để trang web COPYCHAIN (kể cả trên GitHub Pages hay localhost) gửi yêu cầu mượt mà.
================================================================================
"""

import os
import sys
import json
import ssl
import smtplib
from http.server import HTTPServer, BaseHTTPRequestHandler
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Đảm bảo UTF-8 an toàn trên Windows Console
if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass
if hasattr(sys.stderr, 'reconfigure'):
    try:
        sys.stderr.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

def safe_print(*args, **kwargs):
    try:
        print(*args, **kwargs, flush=True)
    except Exception:
        pass

# ==============================================================================
# HÀM NẠP BIẾN MÔI TRƯỜNG TỪ TỆP .env (TUÂN THỦ AGENTS.md - KHÔNG LỘ MẬT KHẨU)
# ==============================================================================
def load_env_file(filepath=".env"):
    """Đọc tệp .env và nạp vào os.environ."""
    candidates = [
        filepath,
        os.path.join(os.path.dirname(__file__), filepath),
        os.path.join(os.path.dirname(__file__), "..", filepath)
    ]
    for p in candidates:
        if os.path.isfile(p):
            try:
                with open(p, "r", encoding="utf-8") as f:
                    for line in f:
                        line = line.strip()
                        if line and not line.startswith("#") and "=" in line:
                            k, v = line.split("=", 1)
                            k = k.strip()
                            v = v.strip().strip('"').strip("'")
                            os.environ[k] = v
                break
            except Exception as e:
                safe_print(f"[CẢNH BÁO] Không đọc được tệp {p}: {e}")

# Tải cấu hình
load_env_file()

def get_gmail_credentials():
    load_env_file()
    email = os.environ.get("GMAIL_USER", "").strip()
    password = os.environ.get("GMAIL_APP_PASSWORD", "").replace(" ", "").strip()
    return email, password

# ==============================================================================
# HÀM GỬI EMAIL THẬT QUA SMTP GOOGLE
# ==============================================================================
def send_otp_email(to_email, to_name, otp_code):
    sender_email, app_password = get_gmail_credentials()

    if not sender_email or not app_password:
        return False, "Chưa cấu hình GMAIL_USER hoặc GMAIL_APP_PASSWORD trong tệp .env!"

    subject = f"[COPYCHAIN] Mã xác thực OTP đăng ký tài khoản: {otp_code}"
    
    # Nội dung văn bản thuần
    text_content = f"""Xin chào {to_name or 'Quý tác giả'},

Mã OTP xác thực đăng ký tài khoản trên Hệ thống Bản quyền COPYCHAIN của bạn là: {otp_code}

Mã có hiệu lực trong vòng 60 giây. Tuyệt đối không chia sẻ mã này cho bất kỳ ai.
Trân trọng,
COPYCHAIN LegalTech Security Team
"""

    # Nội dung HTML định dạng sang trọng
    html_content = f"""<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <style>
    body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #f8fafc; margin: 0; padding: 20px; color: #1e293b; }}
    .container {{ max-width: 540px; margin: 0 auto; background: #ffffff; border-radius: 12px; border: 1px solid #e2e8f0; overflow: hidden; box-shadow: 0 4px 12px rgba(0,0,0,0.05); }}
    .header {{ background: linear-gradient(135deg, #1e3a8a, #2563eb); padding: 24px; text-align: center; color: #ffffff; }}
    .header h1 {{ margin: 0; font-size: 22px; font-weight: 800; letter-spacing: 1px; }}
    .header p {{ margin: 6px 0 0; font-size: 13px; opacity: 0.9; }}
    .body-content {{ padding: 28px 24px; }}
    .otp-card {{ background: #f1f5f9; border: 2px dashed #3b82f6; border-radius: 8px; text-align: center; padding: 18px; margin: 20px 0; }}
    .otp-code {{ font-size: 32px; font-weight: 800; letter-spacing: 8px; color: #1e40af; font-family: 'Consolas', monospace; }}
    .footer {{ background: #f8fafc; border-top: 1px solid #e2e8f0; padding: 16px; text-align: center; font-size: 11.5px; color: #64748b; }}
  </style>
</head>
<body>
  <div class="container">
    <div class="header">
      <h1>🛡️ COPYCHAIN LEGALTECH</h1>
      <p>Hệ thống Đăng ký & Xác thực Bản quyền Tác giả On-Chain</p>
    </div>
    <div class="body-content">
      <p style="font-size: 15px;">Xin chào <strong>{to_name or 'Quý tác giả'}</strong>,</p>
      <p style="font-size: 14px; line-height: 1.6; color: #475569;">
        Bạn đang tiến hành đăng ký tài khoản tác giả trên cổng dịch vụ <strong>COPYCHAIN</strong>. Dưới đây là mã xác thực một lần (OTP) của bạn:
      </p>
      
      <div class="otp-card">
        <div style="font-size: 12px; color: #64748b; text-transform: uppercase; font-weight: 700; margin-bottom: 6px;">Mã OTP Xác Thực (6 Chữ Số)</div>
        <div class="otp-code">{otp_code}</div>
        <div style="font-size: 12px; color: #dc2626; margin-top: 6px; font-weight: 600;">⏱️ Mã có hiệu lực trong 60 giây</div>
      </div>

      <p style="font-size: 13px; color: #64748b; line-height: 1.5;">
        ⚠️ <strong>Cảnh báo an toàn:</strong> Không cung cấp mã OTP này cho bất kỳ ai để đảm bảo an toàn danh tính và quyền sở hữu trí tuệ tác phẩm của bạn trên Blockchain.
      </p>
    </div>
    <div class="footer">
      Email này được gửi tự động từ hệ thống COPYCHAIN theo yêu cầu của bạn.<br>
      © 2026 COPYCHAIN • Đại học Kinh tế (HCE) • Phân hiệu Web3/LegalTech.
    </div>
  </div>
</body>
</html>
"""

    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = f"COPYCHAIN LegalTech <{sender_email}>"
    msg["To"] = to_email

    part1 = MIMEText(text_content, "plain", "utf-8")
    part2 = MIMEText(html_content, "html", "utf-8")
    msg.attach(part1)
    msg.attach(part2)

    try:
        context = ssl.create_default_context()
        with smtplib.SMTP("smtp.gmail.com", 587, timeout=15) as server:
            server.ehlo()
            server.starttls(context=context)
            server.ehlo()
            server.login(sender_email, app_password)
            server.send_message(msg)
        return True, "Thành công"
    except smtplib.SMTPAuthenticationError:
        return False, "Lỗi đăng nhập Google: Sai email hoặc Mật khẩu ứng dụng (App Password) chưa chính xác!"
    except Exception as e:
        return False, f"Lỗi gửi email: {str(e)}"

# ==============================================================================
# BỘ XỬ LÝ HTTP VỚI CORS ĐẦY ĐỦ
# ==============================================================================
class OtpRequestHandler(BaseHTTPRequestHandler):
    def _send_cors_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization")

    def do_OPTIONS(self):
        self.send_response(200)
        self._send_cors_headers()
        self.end_headers()

    def do_GET(self):
        sender_email, app_password = get_gmail_credentials()
        self.send_response(200)
        self._send_cors_headers()
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.end_headers()

        response = {
            "status": "online",
            "service": "COPYCHAIN Local OTP Server",
            "sender_email": sender_email if sender_email else "CHƯA CẤU HÌNH",
            "is_configured": bool(sender_email and app_password)
        }
        self.wfile.write(json.dumps(response, ensure_ascii=False).encode("utf-8"))

    def do_POST(self):
        if self.path != "/send-otp":
            self.send_response(404)
            self._send_cors_headers()
            self.end_headers()
            return

        content_length = int(self.headers.get("Content-Length", 0))
        raw_body = self.rfile.read(content_length)

        try:
            data = json.loads(raw_body.decode("utf-8"))
            to_email = data.get("email", "").strip()
            to_name = data.get("name", "Tác giả").strip()
            otp_code = str(data.get("otp", "")).strip()

            if not to_email or not otp_code:
                self.send_response(400)
                self._send_cors_headers()
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.end_headers()
                self.wfile.write(json.dumps({"success": False, "error": "Thiếu email hoặc mã OTP"}, ensure_ascii=False).encode("utf-8"))
                return

            safe_print(f"\n[YÊU CẦU GỬI OTP] Gửi tới: {to_email} | OTP: {otp_code}")
            success, message = send_otp_email(to_email, to_name, otp_code)

            status_code = 200 if success else 500
            self.send_response(status_code)
            self._send_cors_headers()
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()

            if success:
                safe_print(f" -> ✓ Gửi email thành công tới {to_email}!")
                res_payload = {"success": True, "message": f"Mã OTP đã được gửi thẳng tới Gmail: {to_email}"}
            else:
                safe_print(f" -> ✗ Thất bại: {message}")
                res_payload = {"success": False, "error": message}

            self.wfile.write(json.dumps(res_payload, ensure_ascii=False).encode("utf-8"))

        except Exception as err:
            safe_print(f" -> ✗ Ngoại lệ: {err}")
            self.send_response(500)
            self._send_cors_headers()
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(json.dumps({"success": False, "error": str(err)}, ensure_ascii=False).encode("utf-8"))

    def log_message(self, format, *args):
        return

# ==============================================================================
# HÀM KHỞI CHẠY CHÍNH
# ==============================================================================
def main():
    port = int(os.environ.get("OTP_PORT", 5000))
    sender_email, app_password = get_gmail_credentials()

    safe_print("=" * 68)
    safe_print("      🚀 COPYCHAIN - MÁY CHỦ GỬI MÃ OTP GMAIL TRỰC TIẾP")
    safe_print("=" * 68)
    safe_print(f" [✓] Cổng lắng nghe (Port)   : http://127.0.0.1:{port}")
    if sender_email and app_password:
        masked_pwd = app_password[:2] + "****" + app_password[-2:] if len(app_password) >= 4 else "****"
        safe_print(f" [✓] Email người gửi         : {sender_email}")
        safe_print(f" [✓] Mật khẩu ứng dụng (App): {masked_pwd} (Đã sẵn sàng)")
        safe_print("\n -> Trạng thái: ĐANG LẮNG NGHE YÊU CẦU TỪ TRANG WEB COPYCHAIN...")
    else:
        safe_print(" [!] CẢNH BÁO: CHƯA CẤU HÌNH THÔNG TIN GMAIL TRONG TỆP .env!")
        safe_print("     Vui lòng mở tệp .env và thêm 2 dòng sau:")
        safe_print("     GMAIL_USER=email_cua_ban@gmail.com")
        safe_print("     GMAIL_APP_PASSWORD=xxxx xxxx xxxx xxxx")
    safe_print("=" * 68)

    server = HTTPServer(("127.0.0.1", port), OtpRequestHandler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        safe_print("\n[ĐÃ DỪNG] Máy chủ OTP đã tắt an toàn.")
        server.server_close()

if __name__ == "__main__":
    main()
