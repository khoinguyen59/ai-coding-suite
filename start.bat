@echo off
title DeepSeek Harness - Official Web UI
cd /d "%~dp0..\deepseek-harness"

echo ================================================================
echo 🚀 DANG KHOI CHAY OFFICIAL DEEPSEEK HARNESS WEB UI
echo ================================================================
echo.
echo 🌐 Dang mo DeepSeek Harness tai: http://127.0.0.1:3080
echo 💡 Nhan Ctrl+C de dung server.
echo.

start "" "http://127.0.0.1:3080"
call pnpm dsh web --port 3080

pause
