import http.server
import io
import os
import socketserver
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

PORT = 3080
DIRECTORY = os.path.join(os.path.dirname(os.path.abspath(__file__)), "web_ui")

class CustomHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def log_message(self, format, *args):
        pass

def start_server():
    socketserver.TCPServer.allow_reuse_address = True
    try:
        with socketserver.TCPServer(("", PORT), CustomHandler) as httpd:
            print(f"[+] Web Server da lang nghe tai: http://127.0.0.1:{PORT}")
            httpd.serve_forever()
    except Exception as e:
        print(f"[!] Server status: {e}")

def main():
    print("=" * 68)
    print("AI CODING SUITE (HERETIC + UNSLOTH + DEEPSEEK HARNESS)")
    print("=" * 68)
    print("\n[V] Moi truong Web UI Lap trinh da san sang tren may cua ban!\n")
    print("HUONG DAN KET NOI:")
    print("   1. Mo notebook colab/3_serve_model.ipynb tren Google Colab T4.")
    print("   2. Chay xong ban se nhan duoc link dang: https://xxxx.trycloudflare.com/v1\n")
    print("-" * 68)

    # Khởi chạy Web Server cục bộ
    server_thread = threading.Thread(target=start_server, daemon=True)
    server_thread.start()
    time.sleep(0.5)

    print("\n" + "=" * 68)
    print(f"[*] Dang mo Web UI Lap trinh tai: http://127.0.0.1:{PORT}")
    print("[*] Dan Cloudflare Tunnel URL truc tiep tren giao dien Web de bat dau code!")
    print("[*] Nhan Ctrl+C de dung server khi khong dung nua.")
    print("=" * 68 + "\n")

    try:
        webbrowser.open(f"http://127.0.0.1:{PORT}")
    except Exception:
        pass

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n[!] Da dong giao dien AI Coding Suite.")

if __name__ == "__main__":
    main()
