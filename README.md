# 🚀 AI Coding Suite (DeepSeek Harness + Heretic + Unsloth + Google Colab T4)

Hệ sinh thái công cụ hỗ trợ lập trình AI toàn diện, kết hợp sức mạnh của **DeepSeek Harness** (Agent Runtime & Web UI trên máy cục bộ) với hạ tầng tính toán **Google Colab** (chạy Heretic bóc kiểm duyệt, Unsloth fine-tuning trên L4/A100 và phục vụ API hàng ngày trên GPU T4 16GB VRAM).

---

## 🌟 1. Tổng quan Kiến trúc

```
┌────────────────────────────────────────────────────────────────────────┐
│                        GOOGLE COLAB (Cloud Compute)                    │
│                                                                        │
│  [Giai đoạn 1: L4/A100] ──► Heretic Uncensoring (Triệt tiêu Refusal)   │
│                                   │                                    │
│                                   ▼                                    │
│  [Giai đoạn 2: L4/A100] ──► Unsloth Fine-tuning (QLoRA 4-bit)          │
│                                   │                                    │
│                                   ▼ (Lưu Google Drive / Hub)           │
│  [Giai đoạn 3: T4 16GB]  ──► Serving OpenAI-compatible API Server      │
│                                   │                                    │
│                                   ▼                                    │
│                         [Cloudflare Tunnel] (HTTPS URL)                │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │ https://xxxx.trycloudflare.com/v1
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│                    MÁY TÍNH CỦA BẠN (Windows Local)                     │
│                                                                        │
│  [DeepSeek Harness] (`deepseek-ai/deepseek-harness`)                   │
│  ├── Giao diện Web tương tác hiện đại (`dsh web` tại port 3080)        │
│  ├── File & Workspace Tools: Đọc, viết, sửa đổi trực tiếp code dự án  │
│  ├── Terminal / Command Execution: Tự động chạy test, build, lint     │
│  └── Multi-Model Smart Router: Tự động chọn model tối ưu theo tác vụ   │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 🧠 2. Ba Model Code Cốt Lõi

| # | Model | Vai trò chuyên trách | Cấu hình VRAM T4 |
| :--- | :--- | :--- | :--- |
| **1** | **`Qwen2.5-Coder-7B-Instruct`** | **Sinh mã & Refactor chính:** Viết code hàm, refactor, auto-complete tốc độ cao (>40 tokens/s). | ~5GB (4-bit) / ~14GB (FP16) |
| **2** | **`DeepSeek-R1-Distill-Qwen-7B`** | **Kiến trúc & Suy luận logic:** Giải thuật khó, thiết kế hệ thống, phân tích logic chuỗi tư duy (CoT). | ~5GB (4-bit) / ~14GB (FP16) |
| **3** | **`DeepSeek-Coder-V2-Lite-Instruct`** | **Reviewer & Đa ngôn ngữ:** Review bảo mật, tối ưu hóa mã, hỗ trợ hơn 300+ ngôn ngữ lập trình. | ~10GB (4-bit MoE) |

---

## 📋 3. Hướng Dẫn Sử Dụng Chi Tiết (A - Z)

### 🔹 Bước 1: Uncensor Model với Heretic (Chạy 1 lần trên Colab L4/A100)
1. Mở [Google Colab](https://colab.research.google.com/).
2. Chọn menu `Runtime` -> `Change runtime type` -> Chọn **L4** hoặc **A100 GPU**.
3. Upload và mở file [`colab/1_heretic_uncensor.ipynb`](colab/1_heretic_uncensor.ipynb).
4. Chọn model muốn uncensor (ví dụ `Qwen/Qwen2.5-Coder-7B-Instruct`).
5. Chạy tuần tự các ô lệnh để Heretic tự động tìm tham số abliteration và lưu model đã bóc bỏ kiểm duyệt vào Google Drive của bạn (`/content/drive/MyDrive/ai_coding_models_uncensored`).

---

### 🔹 Bước 2 (Tùy chọn): Fine-tune với Unsloth (Colab L4/A100)
1. Trên Colab L4/A100, upload và mở file [`colab/2_unsloth_finetune.ipynb`](colab/2_unsloth_finetune.ipynb).
2. Nạp model đã uncensor ở Bước 1 từ Google Drive.
3. Huấn luyện siêu tốc với QLoRA 4-bit trên tập dữ liệu code tùy chỉnh.
4. Merge model và lưu lại Google Drive.

---

### 🔹 Bước 3: Phục vụ Model hàng ngày (Chạy trên Colab GPU T4 16GB)
1. Trên Google Colab, chọn `Runtime` -> Chọn GPU **T4** (GPU miễn phí).
2. Upload và mở file [`colab/3_serve_model.ipynb`](colab/3_serve_model.ipynb).
3. Chọn model bạn muốn nạp vào VRAM (từ Google Drive hoặc trực tiếp từ Hugging Face).
4. Nhấn **Run All**. Server sẽ khởi chạy và Cloudflare Tunnel sẽ in ra một đường link công khai dạng:
   ```
   🎉 BACKEND SERVER ĐÃ KHỞI CHẠY THÀNH CÔNG!
   👉 OPENAI BASE URL: https://abc-xyz-123.trycloudflare.com/v1
   ```
5. Giữ tab Colab này chạy trong khi bạn lập trình.

---

### 🔹 Bước 4: Khởi chạy DeepSeek Harness trên máy tính của bạn
1. Trên máy tính Windows, mở thư mục `ai-coding-suite` và nhấp đúp vào **`start.bat`**.
2. **Lần đầu tiên:** Chọn `[1]` để cài đặt tự động Node.js, pnpm và DeepSeek Harness.
3. **Khi bắt đầu code:** Chọn `[2]` -> Dán đường link Cloudflare Tunnel từ Colab (ở Bước 3) vào.
4. Trình duyệt sẽ tự động mở giao diện **DeepSeek Harness Web UI** tại `http://127.0.0.1:3080`.
5. Bạn có thể chọn workspace thư mục dự án của bạn và yêu cầu AI đọc code, viết tính năng mới, tạo test cases hoặc sửa lỗi hoàn toàn tự động!

---

## ⚙️ 4. Cấu trúc Thư mục

```
ai-coding-suite/
├── colab/
│   ├── 1_heretic_uncensor.ipynb   # Uncensor model với Heretic (Colab L4/A100)
│   ├── 2_unsloth_finetune.ipynb   # Fine-tune model với Unsloth (Colab L4/A100)
│   ├── 3_serve_model.ipynb        # Serving API hàng ngày (Colab T4 16GB)
│   └── shared/
│       ├── api_server.py          # FastAPI Server chuẩn OpenAI với Streaming SSE
│       └── tunnel.py              # Cloudflare Tunnel Manager
├── local/
│   ├── setup_harness.bat          # Script tự động cài đặt Node.js & DeepSeek Harness
│   ├── start_harness.bat          # Script khởi động Web UI
│   └── harness_config/
│       ├── single_model.json      # Config 1 Model - 1 Colab T4
│       └── multi_model.json       # Config 3 Models - 3 Colab T4 instances
├── plugins/
│   └── model_router/              # Plugin phân loại prompt và định tuyến 3 model
├── data/
│   └── sample_coding_data.jsonl   # Tập dữ liệu code mẫu cho Unsloth
├── start.bat                      # Menu điều khiển 1 chạm cho Windows
└── README.md                      # Tài liệu hướng dẫn toàn diện
```
