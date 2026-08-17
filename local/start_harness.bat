@echo off
chcp 65001 >nul
title DeepSeek Harness - Coding Agent UI
echo ================================================================
echo ⚡ DEEPSEEK HARNESS - AGENT CODING RUNTIME (Local Web UI)
echo ================================================================
echo.
echo [V] Node.js và pnpm đã có sẵn trên máy.
echo.

set /p COLAB_URL="👉 Nhập Cloudflare Tunnel URL từ Colab (VD: https://xyz.trycloudflare.com/v1): "

if "%COLAB_URL%"=="" (
    echo [!] Chưa nhập URL mới, dùng cấu hình mặc định...
) else (
    echo [*] Đang cấu hình endpoint Colab: %COLAB_URL%
    set "OPENAI_BASE_URL=%COLAB_URL%"
    set "OPENAI_API_KEY=colab-dummy-key"
)

echo.
echo 🚀 Đang khởi động DeepSeek Harness Web UI tại http://127.0.0.1:3080...
echo 💡 Nhấn Ctrl+C để dừng server.
echo.

:: Kiểm tra nếu có repo deepseek-harness cục bộ thì chạy trực tiếp
if exist "%~dp0..\..\deepseek-harness" (
    cd /d "%~dp0..\..\deepseek-harness"
    call npx @deepseek-ai/dsh web --port 3080
) else (
    call npx @deepseek-ai/dsh web --port 3080
)

pause
