# 🚀 AI Coding Suite (Heretic + Unsloth + DeepSeek Harness)

[![GitHub Repo](https://img.shields.io/badge/GitHub-khoinguyen59%2Fai--coding--suite-blue?logo=github)](https://github.com/khoinguyen59/ai-coding-suite)
[![Open In Colab: Serve Model](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/khoinguyen59/ai-coding-suite/blob/main/colab/3_serve_model.ipynb)

Hệ sinh thái công cụ hỗ trợ lập trình AI toàn diện, kết hợp sức mạnh của **Local Autonomous Coding Agent & Web UI** với hạ tầng tính toán đám mây **Google Colab** (chạy Heretic bóc kiểm duyệt, Unsloth fine-tuning trên L4/A100 và phục vụ API hàng ngày trên GPU T4 16GB VRAM).

---

## ⚡ 1-Click Mở Google Colab (Không cần upload file thủ công)

| Nhiệm vụ | GPU Colab | Nút mở nhanh 1 chạm |
| :--- | :--- | :---: |
| **1. Phục vụ Coding hàng ngày** | **T4 (Miễn phí)** | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/khoinguyen59/ai-coding-suite/blob/main/colab/3_serve_model.ipynb) |
| **2. Bóc kiểm duyệt (Heretic)** | **L4 / A100** | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/khoinguyen59/ai-coding-suite/blob/main/colab/1_heretic_uncensor.ipynb) |
| **3. Huấn luyện QLoRA (Unsloth)** | **L4 / A100** | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/khoinguyen59/ai-coding-suite/blob/main/colab/2_unsloth_finetune.ipynb) |

---

## 🤖 2. Khả Năng Thao Tác File Cục Bộ (Local File Operations)

Hệ thống cung cấp **Autonomous Local Coding Agent (`agent_cli.py`)** cho phép AI trực tiếp tương tác với mã nguồn trên máy tính của bạn:
* 📂 **`list_dir`**: Quét và hiển thị cây thư mục dự án.
* 📖 **`read_file`**: Đọc nội dung mã nguồn của bất kỳ file nào.
* ✍️ **`write_file`**: Tự động tạo file mới trên ổ cứng.
* 🔧 **`replace_in_file`**: Sửa đổi, refactor và vá lỗi trực tiếp trong file.
* 🔍 **`search_files`**: Tìm kiếm hàm, biến, class trong toàn bộ dự án.
* 💻 **`run_command`**: Chạy lệnh shell (chạy test, build, linting) và tự sửa lỗi nếu test fail.

---

## 📋 3. Cách Sử Dụng Nhanh

1. **Khởi động Colab Backend:**
   * Bấm vào nút [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/khoinguyen59/ai-coding-suite/blob/main/colab/3_serve_model.ipynb).
   * Nhấn **Runtime** -> **Run All**.
   * Copy đường link Cloudflare Tunnel (dạng `https://xxxx.trycloudflare.com/v1`).

2. **Khởi chạy trên máy tính:**
   * Nhấp đúp vào **`start.bat`**:
     * Chọn **`[1]`** để mở **Web UI** trực quan tại `http://127.0.0.1:3080`.
     * Chọn **`[2]`** để chạy **Local Agent CLI** tự động đọc/ghi/sửa file mã nguồn trực tiếp trong thư mục dự án của bạn!
