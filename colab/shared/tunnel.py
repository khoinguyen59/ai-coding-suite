import os
import re
import subprocess
import time
import urllib.request

def install_and_start_cloudflare(port: int = 8000) -> str:
    """
    Downloads cloudflared binary (if not present) and starts a tunnel pointing to `port`.
    Returns the public URL (https://*.trycloudflare.com).
    """
    cloudflared_path = "./cloudflared"
    if not os.path.exists(cloudflared_path):
        print("📥 Downloading cloudflared binary...")
        url = "https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64"
        urllib.request.urlretrieve(url, cloudflared_path)
        os.chmod(cloudflared_path, 0o755)
        print("✅ cloudflared downloaded successfully.")

    print(f"🚀 Starting Cloudflare Tunnel on port {port}...")
    log_file = "cloudflared.log"
    with open(log_file, "w") as f:
        process = subprocess.Popen(
            [cloudflared_path, "tunnel", "--url", f"http://127.0.0.1:{port}"],
            stdout=f,
            stderr=subprocess.STDOUT
        )

    tunnel_url = None
    max_retries = 30
    for _ in range(max_retries):
        time.sleep(1)
        if os.path.exists(log_file):
            with open(log_file, "r") as f:
                content = f.read()
                matches = re.findall(r"https://[a-zA-Z0-9-]+\.trycloudflare\.com", content)
                if matches:
                    tunnel_url = matches[0]
                    break

    if tunnel_url:
        print(f"\n" + "="*60)
        print(f"🎉 TUNNEL SẴN SÀNG:")
        print(f"👉 Public API Base URL: {tunnel_url}/v1")
        print(f"👉 Dùng URL này để cấu hình vào DeepSeek Harness!")
        print("="*60 + "\n")
        return tunnel_url
    else:
        raise RuntimeError("❌ Không thể lấy Cloudflare Tunnel URL. Vui lòng kiểm tra cloudflared.log.")

if __name__ == "__main__":
    install_and_start_cloudflare(8000)
