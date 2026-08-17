@echo off
title 1-Click Mo Colab GPU
cd /d "%~dp0"

:MENU
cls
echo ================================================================
echo 🚀 1-CLICK MO GOOGLE COLAB CHUYEN DUNG THEO TUNG MODEL
echo ================================================================
echo.
echo [1] ⚡ Mo Colab Qwen 2.5 Coder 7B (Chuyen Viet code, Refactor, T4 GPU)
echo [2] 🧠 Mo Colab DeepSeek-R1 Distill 7B (Chuyen Giai thuat, Kien truc, T4 GPU)
echo [3] 🔍 Mo Colab DeepSeek-Coder-V2 Lite (Chuyen Review ma nguon, Bao mat, T4 GPU)
echo.
echo [4] 🛡️ Mo Colab Heretic Uncensor (Chay 1 lan boc kiem duyet, L4/A100 GPU)
echo [5] 🦥 Mo Colab Unsloth Fine-tune (Chay 1 lan huan luyen QLoRA, L4/A100 GPU)
echo [0] Thoat
echo.
echo ================================================================
set /p C="👉 Chon model ban muon chay tren Colab (1-5): "

if "%C%"=="1" (
    echo [*] Dang mo Colab Qwen 2.5 Coder 7B tren trinh duyet...
    start https://colab.research.google.com/github/khoinguyen59/ai-coding-suite/blob/main/colab/3_serve_qwen_coder.ipynb
    exit /b 0
)
if "%C%"=="2" (
    echo [*] Dang mo Colab DeepSeek-R1 Distill 7B tren trinh duyet...
    start https://colab.research.google.com/github/khoinguyen59/ai-coding-suite/blob/main/colab/3_serve_deepseek_r1.ipynb
    exit /b 0
)
if "%C%"=="3" (
    echo [*] Dang mo Colab DeepSeek-Coder-V2 Lite tren trinh duyet...
    start https://colab.research.google.com/github/khoinguyen59/ai-coding-suite/blob/main/colab/3_serve_deepseek_coder_v2.ipynb
    exit /b 0
)
if "%C%"=="4" (
    echo [*] Dang mo Colab Heretic Uncensor tren trinh duyet...
    start https://colab.research.google.com/github/khoinguyen59/ai-coding-suite/blob/main/colab/1_heretic_uncensor.ipynb
    exit /b 0
)
if "%C%"=="5" (
    echo [*] Dang mo Colab Unsloth Fine-tune tren trinh duyet...
    start https://colab.research.google.com/github/khoinguyen59/ai-coding-suite/blob/main/colab/2_unsloth_finetune.ipynb
    exit /b 0
)
if "%C%"=="0" (
    exit /b 0
)
goto MENU
