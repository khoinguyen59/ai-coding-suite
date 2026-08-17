@echo off
chcp 65001 >nul
echo ================================================================
echo 🚀 HỆ THỐNG CÀI ĐẶT DEEPSEEK HARNESS (Agent Coding Environment)
echo ================================================================
echo.

:: 1. Kiểm tra Node.js
where node >nul 2>nul
if %errorlevel% neq 0 (
    echo [!] Chưa tìm thấy Node.js trên máy tính của bạn.
    echo [*] Đang tải và cài đặt Node.js tự động qua winget...
    winget install OpenJS.NodeJS.LTS -e --silent
    if %errorlevel% neq 0 (
        echo [X] Cài đặt tự động không thành công. Vui lòng tải Node.js tại: https://nodejs.org/
        pause
        exit /b 1
    )
    echo [V] Cài đặt Node.js thành công. Vui lòng khởi động lại CMD nếu cần.
) else (
    echo [V] Đã tìm thấy Node.js:
    node -v
)

:: 2. Kiểm tra pnpm
where pnpm >nul 2>nul
if %errorlevel% neq 0 (
    echo [*] Đang cài đặt pnpm toàn cục qua npm...
    call npm install -g pnpm
) else (
    echo [V] Đã tìm thấy pnpm:
    pnpm -v
)

:: 3. Khởi tạo DeepSeek Harness Runtime
echo.
echo [*] Đang kiểm tra DeepSeek Harness CLI (@deepseek-ai/dsh)...
call npm install -g @deepseek-ai/dsh
if %errorlevel% equ 0 (
    echo [V] DeepSeek Harness CLI đã sẵn sàng!
) else (
    echo [!] Đang fallback sang phiên bản clone từ source...
)

echo.
echo ================================================================
echo 🎉 CÀI ĐẶT HOÀN TẤT!
echo 👉 Để khởi chạy Web UI, hãy chạy: local\start_harness.bat
echo ================================================================
pause
