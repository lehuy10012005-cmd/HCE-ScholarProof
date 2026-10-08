@echo off
chcp 65001 >nul
title HCE Ledger OTP Server
echo ===================================================
echo   Khoi dong May chu Gui OTP Gmail (HCE Ledger)
echo ===================================================
py otp_server.py
pause
