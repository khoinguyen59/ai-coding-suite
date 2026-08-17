@echo off
title AI Coding Suite - DeepSeek Harness
cd /d "%~dp0"

where python >nul 2>nul
if %errorlevel% equ 0 (
    python launcher.py
) else (
    echo [!] Python not found, launching directly with npx...
    npx -y @deepseek-ai/dsh web --port 3080
)

pause
