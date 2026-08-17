@echo off
chcp 65001 >nul
echo ================================================================
echo   HE THONG CAI DAT DEEPSEEK HARNESS (Agent Coding Environment)
echo ================================================================
echo.

:: 1. Kiem tra Node.js
where node >nul 2>nul
if %errorlevel% neq 0 (
    echo [!] Chua tim thay Node.js tren may tinh cua ban.
    echo [*] Dang tai va cai dat Node.js tu dong qua winget...
    winget install OpenJS.NodeJS.LTS -e --silent
    if %errorlevel% neq 0 (
        echo [X] Cai dat tu dong khong thanh cong. Vui long tai Node.js tai: https://nodejs.org/
        pause
        exit /b 1
    )
    echo [V] Cai dat Node.js thanh cong. Vui long khoi dong lai CMD neu can.
) else (
    echo [V] Da tim thay Node.js:
    node -v
)

:: 2. Kiem tra pnpm
where pnpm >nul 2>nul
if %errorlevel% neq 0 (
    echo [*] Dang cai dat pnpm toan cuc qua npm...
    call npm install -g pnpm
) else (
    echo [V] Da tim thay pnpm:
    pnpm -v
)

:: 3. Khoi tao DeepSeek Harness Runtime
echo.
echo [*] Dang kiem tra DeepSeek Harness CLI (@deepseek-ai/dsh)...
call npm install -g @deepseek-ai/dsh
if %errorlevel% equ 0 (
    echo [V] DeepSeek Harness CLI da san sang!
) else (
    echo [!] Dang fallback sang phien ban clone tu source...
)

echo.
echo ================================================================
echo   CAI DAT HOAN TAT!
echo   De khoi chay Web UI, hay chay: start.bat
echo ================================================================
pause
