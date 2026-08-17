@echo off
title AI Coding Suite - Master Launcher
cd /d "%~dp0"

:MENU
cls
echo ================================================================
echo    AI CODING SUITE (HERETIC + UNSLOTH + DEEPSEEK HARNESS)
echo    GitHub: https://github.com/khoinguyen59/ai-coding-suite
echo ================================================================
echo.
echo [1] Mo Web UI Lap trinh (Giao dien Web truc quan + 1-Click Colab)
echo [2] Chay Local Agent CLI (AI tu dong DOC / GHI / SUA file truc tiep)
echo [3] Mo Google Colab Server tren trinh duyet (Chay GPU T4 mien phi)
echo [0] Thoat
echo.
echo ================================================================
set /p CHOICE="Lua chon cua ban (0-3): "

if "%CHOICE%"=="1" (
    python launcher.py
    goto MENU
)
if "%CHOICE%"=="2" (
    python agent_cli.py
    pause
    goto MENU
)
if "%CHOICE%"=="3" (
    start https://colab.research.google.com/github/khoinguyen59/ai-coding-suite/blob/main/colab/3_serve_model.ipynb
    goto MENU
)
if "%CHOICE%"=="0" (
    exit /b 0
)

goto MENU
