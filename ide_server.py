import asyncio
import io
import json
import os
import re
import subprocess
import sys
import threading
import time
import urllib.request
import webbrowser
from typing import Any, AsyncGenerator, Dict, List, Optional

# Console UTF-8 Fix for Windows
if sys.platform == "win32":
    try:
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")
    except Exception:
        pass

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, HTMLResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

app = FastAPI(title="AI Coding IDE Server", version="2.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global State
WORKSPACE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
COLAB_ENDPOINT = ""
ACTIVE_MODEL = "Qwen/Qwen2.5-Coder-7B-Instruct"

# ----------------- Models -----------------
class WorkspaceSetRequest(BaseModel):
    path: str

class FileReadRequest(BaseModel):
    path: str

class FileWriteRequest(BaseModel):
    path: str
    content: str

class FileCreateRequest(BaseModel):
    path: str
    is_dir: bool = False

class TerminalRunRequest(BaseModel):
    command: str

class ConfigUpdateRequest(BaseModel):
    endpoint_url: str
    model_name: Optional[str] = None

class AgentChatRequest(BaseModel):
    messages: List[Dict[str, str]]
    active_file: Optional[str] = None
    active_code: Optional[str] = None
    temperature: Optional[float] = 0.2

# ----------------- File System APIs -----------------
def get_file_tree(dir_path: str, max_depth: int = 4, current_depth: int = 0) -> List[Dict[str, Any]]:
    if current_depth > max_depth or not os.path.exists(dir_path):
        return []
    items = []
    try:
        entries = sorted(os.listdir(dir_path))
        for entry in entries:
            if entry in [".git", "__pycache__", "node_modules", ".venv", ".gemini", "dist", "build"]:
                continue
            full_path = os.path.join(dir_path, entry)
            is_dir = os.path.isdir(full_path)
            item = {
                "name": entry,
                "path": os.path.relpath(full_path, WORKSPACE_DIR).replace("\\", "/"),
                "is_dir": is_dir,
            }
            if is_dir:
                item["children"] = get_file_tree(full_path, max_depth, current_depth + 1)
            items.append(item)
    except Exception:
        pass
    return items

@app.get("/api/workspace")
async def get_workspace():
    return {"workspace": WORKSPACE_DIR, "tree": get_file_tree(WORKSPACE_DIR)}

@app.post("/api/workspace/set")
async def set_workspace(req: WorkspaceSetRequest):
    global WORKSPACE_DIR
    target = os.path.abspath(req.path)
    if not os.path.exists(target):
        raise HTTPException(status_code=400, detail="Thư mục không tồn tại.")
    WORKSPACE_DIR = target
    return {"status": "ok", "workspace": WORKSPACE_DIR, "tree": get_file_tree(WORKSPACE_DIR)}

@app.post("/api/fs/read")
async def read_file(req: FileReadRequest):
    full_path = os.path.normpath(os.path.join(WORKSPACE_DIR, req.path))
    if not os.path.exists(full_path) or os.path.isdir(full_path):
        raise HTTPException(status_code=404, detail="File không tồn tại.")
    try:
        with open(full_path, "r", encoding="utf-8", errors="replace") as f:
            content = f.read()
        return {"path": req.path, "content": content}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/fs/write")
async def write_file(req: FileWriteRequest):
    full_path = os.path.normpath(os.path.join(WORKSPACE_DIR, req.path))
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    try:
        with open(full_path, "w", encoding="utf-8") as f:
            f.write(req.content)
        return {"status": "ok", "path": req.path, "bytes": len(req.content)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/fs/create")
async def create_file(req: FileCreateRequest):
    full_path = os.path.normpath(os.path.join(WORKSPACE_DIR, req.path))
    try:
        if req.is_dir:
            os.makedirs(full_path, exist_ok=True)
        else:
            os.makedirs(os.path.dirname(full_path), exist_ok=True)
            if not os.path.exists(full_path):
                with open(full_path, "w", encoding="utf-8") as f:
                    f.write("")
        return {"status": "ok", "path": req.path, "tree": get_file_tree(WORKSPACE_DIR)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/terminal/run")
async def run_terminal_command(req: TerminalRunRequest):
    try:
        res = subprocess.run(
            req.command,
            shell=True,
            cwd=WORKSPACE_DIR,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            timeout=60,
        )
        return {"exit_code": res.returncode, "output": res.stdout or "(No output)"}
    except subprocess.TimeoutExpired:
        return {"exit_code": -1, "output": "Command timed out after 60s."}
    except Exception as e:
        return {"exit_code": 1, "output": str(e)}

@app.post("/api/config/set")
async def update_config(req: ConfigUpdateRequest):
    global COLAB_ENDPOINT, ACTIVE_MODEL
    url = req.endpoint_url.strip()
    if url.endswith("/"):
        url = url[:-1]
    if url and not url.endswith("/v1"):
        url += "/v1"
    COLAB_ENDPOINT = url
    if req.model_name:
        ACTIVE_MODEL = req.model_name
    return {"status": "ok", "endpoint": COLAB_ENDPOINT, "model": ACTIVE_MODEL}

@app.get("/api/config")
async def get_config():
    return {
        "endpoint": COLAB_ENDPOINT,
        "model": ACTIVE_MODEL,
        "workspace": WORKSPACE_DIR,
        "github_repo": "https://github.com/khoinguyen59/ai-coding-suite",
        "colab_serve_url": "https://colab.research.google.com/github/khoinguyen59/ai-coding-suite/blob/main/colab/3_serve_model.ipynb",
    }

# ----------------- Agent Streaming Loop -----------------
@app.post("/api/agent/stream")
async def agent_stream(req: AgentChatRequest):
    global COLAB_ENDPOINT, ACTIVE_MODEL, WORKSPACE_DIR
    if not COLAB_ENDPOINT:
        raise HTTPException(status_code=400, detail="Chưa cấu hình Colab Endpoint URL.")

    # System instruction tailored for IDE agent
    system_prompt = f"""You are the AI Coding Assistant embedded in a full IDE.
Workspace Directory: '{WORKSPACE_DIR}'
Active File: '{req.active_file or 'None'}'

When answering, you can write code, explain, or perform ACTIONS on the user's workspace.
To perform direct file actions or shell commands, output structured blocks:

```tool:write_file
filepath: path/to/file.py
content:
<code here>
```

```tool:replace_in_file
filepath: path/to/file.py
target:
<exact lines to find>
replacement:
<exact replacement lines>
```

```tool:run_command
command: python -m pytest
```

Always provide clean, production-ready code with complete logic."""

    prompt_messages = [{"role": "system", "content": system_prompt}] + req.messages

    # Forward to Colab API
    async def sse_generator() -> AsyncGenerator[str, None]:
        payload = {
            "model": ACTIVE_MODEL,
            "messages": prompt_messages,
            "temperature": req.temperature or 0.2,
            "stream": True,
        }
        try:
            req_data = json.dumps(payload).encode("utf-8")
            url = f"{COLAB_ENDPOINT}/chat/completions"
            cl_req = urllib.request.Request(
                url,
                data=req_data,
                headers={"Content-Type": "application/json"},
                method="POST",
            )
            resp = urllib.request.urlopen(cl_req, timeout=120)

            for line in resp:
                line_str = line.decode("utf-8", errors="replace")
                if line_str.startswith("data: "):
                    yield line_str
                    if line_str.strip() == "data: [DONE]":
                        break
        except Exception as e:
            err_obj = {"error": str(e)}
            yield f"data: {json.dumps(err_obj)}\n\n"
            yield "data: [DONE]\n\n"

    return StreamingResponse(sse_generator(), media_type="text/event-stream")

# Serve Web IDE Static Files
IDE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "web_ide")
os.makedirs(IDE_DIR, exist_ok=True)

@app.get("/")
async def root():
    index_path = os.path.join(IDE_DIR, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return HTMLResponse("<h1>AI Coding IDE is loading...</h1>")

app.mount("/static", StaticFiles(directory=IDE_DIR), name="static")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=3080)
