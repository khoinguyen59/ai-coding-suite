import io
import os
import sys

# Fix console encoding for Windows
if sys.platform == "win32":
    try:
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")
    except Exception:
        pass

def configure_dsh(tunnel_url: str = "https://your-colab-tunnel.trycloudflare.com/v1"):
    if tunnel_url.endswith("/"):
        tunnel_url = tunnel_url[:-1]
    if not tunnel_url.endswith("/v1"):
        tunnel_url += "/v1"

    dsh_dir = os.path.expanduser("~/.dsh")
    os.makedirs(dsh_dir, exist_ok=True)
    settings_file = os.path.join(dsh_dir, "settings.yaml")

    yaml_content = f"""ui-onboarding:
  welcomeNoticeVersion: 2026-08-13.1

llm-pi-ai:
  providers:
    colab-coding-suite:
      displayName: "Colab AI Coding Suite (Heretic + Unsloth)"
      api: openai-completions
      baseURL: {tunnel_url}
      headers:
        Authorization: Bearer colab-key
      models:
        - id: Qwen/Qwen2.5-Coder-7B-Instruct
          name: Qwen 2.5 Coder 7B (Code Generator)
          contextWindow: 32768
          maxTokens: 4096
        - id: deepseek-ai/DeepSeek-R1-Distill-Qwen-7B
          name: DeepSeek-R1 Distill 7B (Architect & Logic)
          contextWindow: 32768
          maxTokens: 4096
        - id: deepseek-ai/DeepSeek-Coder-V2-Lite-Instruct
          name: DeepSeek-Coder-V2 Lite (Reviewer & Security)
          contextWindow: 65536
          maxTokens: 4096
"""

    with open(settings_file, "w", encoding="utf-8") as f:
        f.write(yaml_content)

    print("[+] Da cap nhat settings.yaml thanh cong!")

if __name__ == "__main__":
    url = sys.argv[1] if len(sys.argv) > 1 else "https://your-colab-tunnel.trycloudflare.com/v1"
    configure_dsh(url)
