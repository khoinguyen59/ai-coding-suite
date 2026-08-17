import io
import os
import sys
import threading
import time
import webbrowser

# Fix Windows console UTF-8 output encoding for emojis and Vietnamese
if sys.platform == "win32":
    try:
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")
    except Exception:
        pass

import uvicorn
from ide_server import app

PORT = 3080

def start_server():
    try:
        uvicorn.run(app, host="127.0.0.1", port=PORT, log_level="warning")
    except Exception as e:
        print(f"[!] Server status: {e}")

def main():
    print("=" * 68)
    print("🚀 AI CODING STUDIO - INTEGRATED DEVELOPMENT ENVIRONMENT (IDE)")
    print("=" * 68)
    print("\n[✓] Môi trường IDE (Monaco Editor + File Explorer + AI Agent) sẵn sàng!\n")
    print("💡 HƯỚNG DẪN:")
    print("   1. Mở Colab T4: https://colab.research.google.com/github/khoinguyen59/ai-coding-suite/blob/main/colab/3_serve_model.ipynb")
    print("   2. Chạy Run All trên Colab để lấy link Cloudflare Tunnel (https://xxx.trycloudflare.com/v1)")
    print("   3. Dán link đó vào thanh Header của IDE để bắt đầu lập trình!\n")
    print("-" * 68)

    # Khởi chạy IDE Backend Server
    server_thread = threading.Thread(target=start_server, daemon=True)
    server_thread.start()
    time.sleep(1.2)

    ide_url = f"http://127.0.0.1:{PORT}"
    print(f"\n🌐 Đang mở AI Coding Studio IDE tại: {ide_url}")
    print("💡 Nhấn Ctrl+C trong cửa sổ này để tắt khi không dùng nữa.")
    print("=" * 68 + "\n")

    try:
        webbrowser.open(ide_url)
    except Exception:
        pass

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n👋 Đã đóng AI Coding Studio.")

if __name__ == "__main__":
    main()
