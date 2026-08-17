# 🚀 AI Coding Suite & DeepSeek Harness Ecosystem Overview

Tài liệu này mô tả toàn bộ **Cây thư mục tổng thể dự án (Outer Workspace)**, vai trò của từng thành phần, cơ sở kiến thức và quy trình vận hành hệ sinh thái **AI Coding Suite + DeepSeek Harness + Heretic + Unsloth**.

---

## 🌳 Cây Thư Mục Tổng Thể (Workspace Root)

```text
Vietsub/ (Workspace Root)
│
├── 📂 ai-coding-suite/                # 🎯 TRỌNG TÂM: Bộ Notebook Colab, Script 1-Click & Launcher
│   ├── colab/                         # 3 Notebook Colab chính + 3 Notebook 1-Click theo Model
│   │   ├── 1_heretic_uncensor.ipynb   #   - Bước 1: Heretic Uncensoring Pipeline
│   │   ├── 2_unsloth_finetune.ipynb   #   - Bước 2: Unsloth QLoRA Fine-tuning Pipeline
│   │   ├── 3_serve_model.ipynb        #   - Bước 3: Master Serving API + Cloudflare Tunnel
│   │   ├── 3_serve_qwen_coder.ipynb   #   - 1-Click Serve Qwen 2.5 Coder 7B
│   │   ├── 3_serve_deepseek_r1.ipynb  #   - 1-Click Serve DeepSeek-R1 Distill 7B
│   │   ├── 3_serve_deepseek_coder_v2.ipynb # 1-Click Serve DeepSeek-Coder-V2 Lite 16B
│   │   └── shared/                    #   - Code FastAPI Server dùng chung (api_server.py)
│   ├── configure_dsh_settings.py      # Script nạp cấu hình Provider vào ~/.dsh/settings.yaml
│   ├── open_colab.bat                 # Script 1-Click mở đúng Colab Notebook theo model
│   ├── start.bat                      # Script khởi chạy DeepSeek Harness Web UI (Port 3080)
│   └── PROJECT_OVERVIEW.md            # Tài liệu tổng quan dự án (File này)
│
├── 📂 deepseek-harness/               # 🖥️ DEEPSEEK HARNESS MONOREPO (Giao diện Web AI Agent)
│   ├── apps/web/                      # Web Client App (React / Vite)
│   ├── packages/client/               # UI Components (ModelSelect, ProviderEditor, etc.)
│   └── packages/llm/                  # Plugin kết nối các Provider LLM
│
├── 📂 heretic/                        # 🛡️ HERETIC LLM FRAMEWORK (Loại bỏ 100% Censorship)
│   ├── src/                           # Mã nguồn Heretic (Optuna optimization, direction removal)
│   ├── pyproject.toml                 # Cấu hình gói Heretic Python
│   └── README.md                      # Tài liệu hướng dẫn Heretic
│
├── 📂 unsloth/                        # 🦥 UNSLOTH FINETUNING FRAMEWORK (Huấn luyện QLoRA 2-5x)
│   ├── unsloth/                       # Core Triton kernels & FastLanguageModel engine
│   ├── scripts/                       # Script hỗ trợ huấn luyện và export GGUF/Merged 16-bit
│   └── pyproject.toml                 # Cấu hình gói Unsloth Python
│
├── 📂 .agents/                        # 🤖 AI AGENT SKILLS & KNOWLEDGE BASE
│   └── skills/
│       └── vietsub-translator/        # Skill dịch thuật và xử lý phụ đề SRT tự động
│
├── 🎬 File Dữ Liệu Phụ Đề & Tool Xử Lý (Vietsub Tools):
│   ├── clean_repeats_0811.py          # Script Python làm sạch lặp từ trong file SRT
│   ├── SKILL_VIETSUB_GUIDELINES.md    # Quy chuẩn dịch thuật phụ đề Việt hóa
│   └── *.srt                           # Các file phụ đề SRT (0725, 0811, 0812, 0817...)
│
└── ⚙️ Cấu hình Local người dùng (User Profile):
    └── C:\Users\Nguyen Trong Khoi\.dsh\settings.yaml # File cấu hình DeepSeek Harness kết nối Colab
```

---

## 🏗️ Kiến Trúc Luồng Dữ Liệu & Kết Nối (Ecosystem Flow)

```mermaid
graph TD
    subgraph 1. Colab Cloud GPU Server
        H["heretic/<br>1_heretic_uncensor.ipynb"] -->|Model Uncensored| U["unsloth/<br>2_unsloth_finetune.ipynb"]
        U -->|Model Fine-tuned| S["ai-coding-suite/colab/<br>3_serve_*.ipynb"]
        S -->|FastAPI Server| CF["Cloudflare Tunnel<br>(HTTPS Endpoint)"]
    end

    subgraph 2. Máy Local (User Environment)
        CF -->|Base URL| DSH["deepseek-harness/<br>Web UI (Port 3080)"]
        DSH -->|Workspace Access| Code["Thư mục Mã Nguồn / Dự Án Local"]
        DSH -->|Read Config| CFG["C:\\Users\\...\\.dsh\\settings.yaml"]
    end
```

---

## 🧠 Danh Sách 3 Model Coding Cốt Lõi & Nhiệm Vụ

| Model | Thư mục / Notebook phục vụ | Vai trò & Nhiệm vụ |
|-------|----------------------------|-------------------|
| **Qwen 2.5 Coder 7B Instruct** | `colab/3_serve_qwen_coder.ipynb` | **Code Generator**: Sinh mã nguồn siêu tốc, viết hàm, refactor code |
| **DeepSeek-R1 Distill Qwen 7B** | `colab/3_serve_deepseek_r1.ipynb` | **Architect & Logic**: Phân tích kiến trúc hệ thống, tư duy logic cao cấp |
| **DeepSeek-Coder-V2 Lite Instruct** | `colab/3_serve_deepseek_coder_v2.ipynb` | **Reviewer & Security**: Rà soát lỗi bảo mật, review code 300+ ngôn ngữ |

---

## ⚡ Quy Trình Vận Hành 1-Click (Quick Start)

### 1️⃣ Khởi chạy Giao diện DeepSeek Harness
Vào thư mục `ai-coding-suite/`, nhấp đúp file **`start.bat`**. Trình duyệt mở tự động tại:
👉 `http://127.0.0.1:3080`

### 2️⃣ Mở Colab Server theo Model mong muốn
Nhấp đúp file **`open_colab.bat`**:
- Bấm `1` $\rightarrow$ Mở Notebook **Qwen 2.5 Coder 7B**
- Bấm `2` $\rightarrow$ Mở Notebook **DeepSeek-R1 Distill 7B**
- Bấm `3` $\rightarrow$ Mở Notebook **DeepSeek-Coder-V2 Lite 16B**

### 3️⃣ Chạy Server trên Colab
Trên trang Colab vừa mở, bấm **Runtime → Run all** (`Ctrl + F9`). Sau khoảng 1 phút sẽ xuất hiện link:
👉 `https://xxx.trycloudflare.com/v1`

### 4️⃣ Dán Link & Bắt đầu Code
Mở **Settings ⚙️** trên DeepSeek Harness, dán link vào **`Base URL`** và bấm **`Apply`**. Bạn đã sẵn sàng giao việc cho Agent!

---

## 📌 Bảng Tổng Kết Trạng Thái Các Thư Mục

| Thư mục | Trạng thái | Ghi chú |
|---------|------------|---------|
| `ai-coding-suite` | ✅ Ready | Chứa toàn bộ notebook Colab & script 1-click |
| `deepseek-harness` | ✅ Ready | Đã build Web UI & tích hợp Custom Provider |
| `heretic` | ✅ Ready | Tích hợp vào Notebook 1 để bóc bỏ kiểm duyệt |
| `unsloth` | ✅ Ready | Tích hợp vào Notebook 2 để fine-tune QLoRA |
| `.agents/skills` | ✅ Ready | Chứa skill dịch thuật Vietsub & quy chuẩn phụ đề |

---
*Tài liệu được cập nhật tự động vào 2026-08-17.*
