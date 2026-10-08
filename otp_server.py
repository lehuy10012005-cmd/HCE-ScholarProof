#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
================================================================================
  HCE Ledger - MÁY CHỦ GỬI MÃ OTP XÁC THỰC QUA GMAIL THẬT (SMTP GMAIL SERVICE)
  Dự án: Hệ thống Quản trị & Xác thực Bản quyền Tác giả On-chain ECO2432
  Tác giả: Lê Huy (ECO2432)
================================================================================
  Mô tả:
  - Máy chủ cục bộ (Local Server) sử dụng thư viện chuẩn của Python.
  - Tự động đọc biến môi trường GMAIL_USER và GMAIL_APP_PASSWORD từ tệp .env (bảo mật theo chuẩn AGENTS.md).
  - Kết nối trực tiếp đến máy chủ Google (smtp.gmail.com:587 qua TLS) để gửi thư từ chính hộp thư Gmail của bạn.
  - Hỗ trợ CORS đầy đủ để trang web HCE Ledger (kể cả trên GitHub Pages hay localhost) gửi yêu cầu mượt mà.
================================================================================
"""

import os
import sys
import json
import ssl
import smtplib
from http.server import HTTPServer, BaseHTTPRequestHandler
import email.utils
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

    subject = f"[HCE Ledger] Mã xác thực OTP đăng ký tài khoản: {otp_code}"
    
    # Nội dung văn bản thuần tự nhiên
    text_content = f"""Xin chào {to_name or 'bạn'},

Bạn vừa yêu cầu mã xác nhận đăng ký tài khoản trên hệ thống HCE Ledger.
Mã xác nhận của bạn là: {otp_code}

Mã có hiệu lực trong vòng 5 phút. Nếu bạn không gửi yêu cầu này, vui lòng bỏ qua email.

Trân trọng,
Lê Văn Quang Huy - Dự án HCE Ledger (ĐH Kinh tế Huế)
"""

    # Nội dung HTML tối giản chuẩn mực (không dùng emoji, không dùng màu đỏ cảnh báo)
    html_content = f"""<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
</head>
<body style="margin: 0; padding: 24px; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; background-color: #f9fafb; color: #111827;">
  <div style="max-width: 520px; margin: 0 auto; background: #ffffff; border: 1px solid #e5e7eb; border-radius: 8px; padding: 32px 28px; box-shadow: 0 1px 3px rgba(0,0,0,0.05);">
    <div style="border-bottom: 2px solid #2563eb; padding-bottom: 12px; margin-bottom: 20px;">
      <h2 style="margin: 0; font-size: 18px; color: #1e3a8a; font-weight: 700;">Hệ thống Bản quyền Số HCE Ledger</h2>
      <p style="margin: 4px 0 0; font-size: 12px; color: #6b7280;">Trường Đại học Kinh tế - Đại học Huế</p>
    </div>

    <p style="font-size: 14.5px; line-height: 1.6; margin: 0 0 16px;">Xin chào <strong>{to_name or 'bạn'}</strong>,</p>
    <p style="font-size: 14px; line-height: 1.6; color: #374151; margin: 0 0 20px;">
      Bạn vừa thực hiện đăng ký tài khoản trên cổng dịch vụ HCE Ledger. Dưới đây là mã số xác nhận của bạn:
    </p>

    <div style="background: #f0fdf4; border: 1px solid #bbf7d0; border-radius: 6px; padding: 18px; text-align: center; margin: 0 0 24px;">
      <div style="font-size: 12px; color: #166534; font-weight: 600; text-transform: uppercase; margin-bottom: 6px;">Mã xác nhận tài khoản</div>
      <div style="font-size: 32px; font-weight: 800; letter-spacing: 6px; color: #15803d; font-family: 'Consolas', 'Courier New', monospace;">{otp_code}</div>
      <div style="font-size: 12px; color: #4b5563; margin-top: 6px;">Hiệu lực trong 5 phút</div>
    </div>

    <p style="font-size: 13px; line-height: 1.5; color: #6b7280; margin: 0 0 24px;">
      Nếu bạn không yêu cầu mã này, có thể một ai đó đã nhập nhầm địa chỉ email của bạn. Bạn không cần làm gì thêm.
    </p>

    <div style="border-top: 1px solid #f3f4f6; padding-top: 16px; font-size: 12px; color: #9ca3af; line-height: 1.5;">
      Trân trọng,<br>
      <strong>Lê Văn Quang Huy</strong> • Phân hiệu Web3 / LegalTech<br>
      Khoa Hệ thống Thông tin Kinh tế, Trường Đại học Kinh tế - ĐH Huế
    </div>
  </div>
</body>
</html>"""

    msg = MIMEMultipart("alternative")
    msg["Subject"] = f"Mã xác nhận tài khoản HCE Ledger: {otp_code}"
    msg["From"] = f"Lê Văn Quang Huy <{sender_email}>"
    msg["To"] = to_email
    msg["Reply-To"] = sender_email
    msg["Date"] = email.utils.formatdate(localtime=True)
    msg["Message-ID"] = email.utils.make_msgid(domain="gmail.com")
    msg["MIME-Version"] = "1.0"

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
            "service": "HCE Ledger Local OTP Server",
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
    safe_print("      🚀 HCE Ledger - MÁY CHỦ GỬI MÃ OTP GMAIL TRỰC TIẾP")
    safe_print("=" * 68)
    safe_print(f" [✓] Cổng lắng nghe (Port)   : http://127.0.0.1:{port}")
    if sender_email and app_password:
        masked_pwd = app_password[:2] + "****" + app_password[-2:] if len(app_password) >= 4 else "****"
        safe_print(f" [✓] Email người gửi         : {sender_email}")
        safe_print(f" [✓] Mật khẩu ứng dụng (App): {masked_pwd} (Đã sẵn sàng)")
        safe_print("\n -> Trạng thái: ĐANG LẮNG NGHE YÊU CẦU TỪ TRANG WEB HCE Ledger...")
    else:
        safe_print(" [!] CẢNH BÁO: CHƯA CẤU HÌNH THÔNG TIN GMAIL TRONG TỆP .env!")
        safe_print("     Vui lòng mở tệp .env và thêm 2 dòng sau:")
        safe_print("     GMAIL_USER=email_cua_ban@gmail.com")
        safe_print("     GMAIL_APP_PASSWORD=xxxx xxxx xxxx xxxx")
    safe_print("=" * 68)

    try:
        server = HTTPServer(("127.0.0.1", port), OtpRequestHandler)
    except OSError as err:
        if "10048" in str(err) or "already in use" in str(err) or "Address already in use" in str(err):
            safe_print(f"\n [✓] MÁY CHỦ OTP HIỆN ĐANG CHẠY SẴN TRÊN CỔNG http://127.0.0.1:{port}!")
            safe_print("     Hệ thống đã sẵn sàng 100%. Bạn có thể mở web và bấm gửi OTP ngay mà không cần bật lại lệnh này!")
            return
        safe_print(f" [✗] Không thể mở cổng {port}: {err}")
        return

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        safe_print("\n[ĐÃ DỪNG] Máy chủ OTP đã tắt an toàn.")
        server.server_close()

if __name__ == "__main__":
    main()
