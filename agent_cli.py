import io
import json
import os
import re
import subprocess
import sys
import urllib.error
import urllib.request

# Fix console encoding for Windows
if sys.platform == "win32":
    try:
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")
    except Exception:
        pass

class LocalCodingAgent:
    def __init__(self, base_url: str, workspace_dir: str, model_name: str = "Qwen/Qwen2.5-Coder-7B-Instruct"):
        if base_url.endswith("/"):
            base_url = base_url[:-1]
        if not base_url.endswith("/v1"):
            base_url += "/v1"
        self.base_url = base_url
        self.workspace_dir = os.path.abspath(workspace_dir)
        self.model_name = model_name
        self.messages = []
        self.max_iterations = 15
        self.init_system_prompt()

    def init_system_prompt(self):
        system_instruction = f"""You are an expert Autonomous Coding AI Agent operating in the local workspace directory: '{self.workspace_dir}'.
You have direct access to read, write, edit files and execute shell commands on the user's computer.

To interact with the environment, you MUST output structured tool calls in your response inside XML tags like this:

<tool_call>
{{"name": "read_file", "arguments": {{"path": "path/to/file.py"}}}}
</tool_call>

<tool_call>
{{"name": "write_file", "arguments": {{"path": "path/to/file.py", "content": "file content here..."}}}}
</tool_call>

<tool_call>
{{"name": "replace_in_file", "arguments": {{"path": "path/to/file.py", "target": "old code string to replace", "replacement": "new code string"}}}}
</tool_call>

<tool_call>
{{"name": "list_dir", "arguments": {{"path": "."}}}}
</tool_call>

<tool_call>
{{"name": "search_files", "arguments": {{"query": "def my_func", "path": "."}}}}
</tool_call>

<tool_call>
{{"name": "run_command", "arguments": {{"command": "python test.py"}}}}
</tool_call>

RULES:
1. Always explore the workspace first: list files or read existing files before modifying them.
2. Edit files directly using 'replace_in_file' or 'write_file'. Do NOT ask the user to copy-paste code manually.
3. Verify your changes by running tests or scripts via 'run_command'.
4. Be concise and explain what files you modified.
"""
        self.messages = [{"role": "system", "content": system_instruction}]

    def resolve_path(self, rel_path: str) -> str:
        if os.path.isabs(rel_path):
            return rel_path
        return os.path.normpath(os.path.join(self.workspace_dir, rel_path))

    def execute_tool(self, name: str, args: dict) -> str:
        try:
            if name == "read_file":
                path = self.resolve_path(args["path"])
                if not os.path.exists(path):
                    return f"Error: File '{args['path']}' does not exist."
                with open(path, "r", encoding="utf-8", errors="replace") as f:
                    content = f.read()
                return f"[File: {args['path']}]\n" + content

            elif name == "write_file":
                path = self.resolve_path(args["path"])
                os.makedirs(os.path.dirname(path), exist_ok=True)
                with open(path, "w", encoding="utf-8") as f:
                    f.write(args["content"])
                return f"Successfully wrote {len(args['content'])} characters to '{args['path']}'."

            elif name == "replace_in_file":
                path = self.resolve_path(args["path"])
                if not os.path.exists(path):
                    return f"Error: File '{args['path']}' does not exist."
                with open(path, "r", encoding="utf-8", errors="replace") as f:
                    content = f.read()
                target = args["target"]
                replacement = args["replacement"]
                if target not in content:
                    return f"Error: Target text not found in '{args['path']}'. Please verify line contents."
                new_content = content.replace(target, replacement, 1)
                with open(path, "w", encoding="utf-8") as f:
                    f.write(new_content)
                return f"Successfully replaced target in '{args['path']}'."

            elif name == "list_dir":
                path = self.resolve_path(args.get("path", "."))
                if not os.path.exists(path):
                    return f"Error: Directory '{args.get('path')}' does not exist."
                entries = []
                for entry in os.listdir(path):
                    if entry in [".git", "__pycache__", "node_modules", ".venv"]:
                        continue
                    full = os.path.join(path, entry)
                    prefix = "[DIR] " if os.path.isdir(full) else "[FILE]"
                    entries.append(f"{prefix} {entry}")
                return "\n".join(entries) or "(Empty directory)"

            elif name == "search_files":
                query = args["query"]
                path = self.resolve_path(args.get("path", "."))
                matches = []
                for root, dirs, files in os.walk(path):
                    dirs[:] = [d for d in dirs if d not in [".git", "__pycache__", "node_modules", ".venv"]]
                    for file in files:
                        file_path = os.path.join(root, file)
                        try:
                            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                                for idx, line in enumerate(f, 1):
                                    if query.lower() in line.lower():
                                        rel = os.path.relpath(file_path, self.workspace_dir)
                                        matches.append(f"{rel}:{idx}: {line.strip()}")
                                        if len(matches) >= 30:
                                            break
                        except Exception:
                            pass
                return "\n".join(matches) if matches else "No matches found."

            elif name == "run_command":
                cmd = args["command"]
                result = subprocess.run(
                    cmd,
                    shell=True,
                    cwd=self.workspace_dir,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    text=True,
                    timeout=60,
                )
                output = result.stdout or "(No output)"
                return f"[Exit code {result.returncode}]\n{output}"

            else:
                return f"Unknown tool: '{name}'"
        except Exception as e:
            return f"Tool execution error: {str(e)}"

    def call_llm(self) -> str:
        req_body = {
            "model": self.model_name,
            "messages": self.messages,
            "temperature": 0.2,
            "max_tokens": 4096,
            "stream": False,
        }
        url = f"{self.base_url}/chat/completions"
        req = urllib.request.Request(
            url,
            data=json.dumps(req_body).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        try:
            with urllib.request.urlopen(req, timeout=120) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                return data["choices"][0]["message"]["content"]
        except urllib.error.HTTPError as e:
            err_msg = e.read().decode("utf-8", errors="ignore")
            raise RuntimeError(f"HTTP {e.code}: {err_msg}")
        except Exception as e:
            raise RuntimeError(f"Connection error to {url}: {str(e)}")

    def run_turn(self, user_prompt: str):
        self.messages.append({"role": "user", "content": user_prompt})
        iteration = 0

        while iteration < self.max_iterations:
            iteration += 1
            print(f"\n🧠 [Agent Thinking... Iteration {iteration}]")
            response = self.call_llm()
            self.messages.append({"role": "assistant", "content": response})

            # Check for tool calls
            tool_call_matches = re.findall(r"<tool_call>\s*(.*?)\s*</tool_call>", response, re.DOTALL)
            if not tool_call_matches:
                # No more tools needed, agent finished thinking and answered
                print("\n" + "=" * 60)
                print("🤖 [Agent Response]:")
                print(response)
                print("=" * 60)
                break

            # Execute tool calls
            tool_results = []
            for raw_json in tool_call_matches:
                try:
                    payload = json.loads(raw_json)
                    tool_name = payload["name"]
                    tool_args = payload.get("arguments", {})
                    print(f"🔧 [Executing Tool]: {tool_name} with {json.dumps(tool_args, ensure_ascii=False)}")
                    result = self.execute_tool(tool_name, tool_args)
                    print(f"📄 [Result]:\n{result[:300]}..." if len(result) > 300 else f"📄 [Result]:\n{result}")
                    tool_results.append(f"Tool '{tool_name}' result:\n{result}")
                except Exception as e:
                    tool_results.append(f"Tool parse error: {str(e)}")

            tool_feedback = "\n\n".join(tool_results)
            self.messages.append({"role": "user", "content": f"Observation:\n{tool_feedback}"})

def main():
    print("=" * 70)
    print("🚀 LOCAL AUTONOMOUS CODING AGENT (DIRECT FILE READ/WRITE/EXEC)")
    print("=" * 70)

    # 1. Base URL
    saved_url = os.environ.get("OPENAI_BASE_URL", "")
    prompt_url = f"👉 Nhập Cloudflare Tunnel URL từ Colab [{saved_url}]: " if saved_url else "👉 Nhập Cloudflare Tunnel URL từ Colab: "
    url_input = input(prompt_url).strip()
    base_url = url_input if url_input else saved_url

    if not base_url:
        print("❌ Lỗi: Bạn cần cung cấp URL Endpoint từ Colab (VD: https://xxx.trycloudflare.com/v1)")
        sys.exit(1)

    # 2. Workspace
    default_ws = os.getcwd()
    ws_input = input(f"📁 Thư mục Workspace làm việc [{default_ws}]: ").strip()
    workspace = ws_input if ws_input else default_ws

    print(f"\n[✓] Kết nối API: {base_url}")
    print(f"[✓] Workspace: {workspace}")
    print("\n💡 Gõ 'exit' hoặc 'quit' để thoát. Gõ yêu cầu lập trình để Agent tự động đọc & sửa file!\n")

    agent = LocalCodingAgent(base_url, workspace)

    while True:
        try:
            user_msg = input("\n👤 [Bạn]: ").strip()
            if not user_msg:
                continue
            if user_msg.lower() in ["exit", "quit"]:
                print("👋 Tạm biệt!")
                break
            agent.run_turn(user_msg)
        except KeyboardInterrupt:
            print("\n👋 Đã hủy thao tác.")
            break
        except Exception as e:
            print(f"\n❌ Lỗi: {e}")

if __name__ == "__main__":
    main()
