@echo off
chcp 65001 >nul
title DeepSeek Harness - Coding Agent UI
echo ================================================================
echo   DEEPSEEK HARNESS - AGENT CODING RUNTIME (Local Web UI)
echo ================================================================
echo.
echo [V] Node.js va pnpm da co san tren may.
echo.

set /p COLAB_URL=">> Nhap Cloudflare Tunnel URL tu Colab (VD: https://xyz.trycloudflare.com/v1): "

if "%COLAB_URL%"=="" (
    echo [!] Chua nhap URL moi, dung cau hinh mac dinh...
) else (
    echo [*] Dang cau hinh endpoint Colab: %COLAB_URL%
    set "OPENAI_BASE_URL=%COLAB_URL%"
    set "OPENAI_API_KEY=colab-dummy-key"
)

echo.
echo [*] Dang khoi dong DeepSeek Harness Web UI tai http://127.0.0.1:3080...
echo [*] Nhan Ctrl+C de dung server.
echo.

if exist "%~dp0..\..\deepseek-harness" (
    cd /d "%~dp0..\..\deepseek-harness"
    call npx @deepseek-ai/dsh web --port 3080
) else (
    call npx @deepseek-ai/dsh web --port 3080
)

pause
