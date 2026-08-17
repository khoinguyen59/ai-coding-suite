import asyncio
import json
import time
import uuid
from typing import Any, AsyncGenerator, Dict, List, Optional, Union

import torch
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field
from transformers import AutoModelForCausalLM, AutoTokenizer, TextIteratorStreamer
import threading

app = FastAPI(title="Colab AI Coding Backend - OpenAI Compatible", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global variables holding model & tokenizer
MODEL = None
TOKENIZER = None
MODEL_NAME = "Loaded-Code-Model"

class ChatMessage(BaseModel):
    role: str
    content: str

class ChatCompletionRequest(BaseModel):
    model: Optional[str] = "custom-model"
    messages: List[ChatMessage]
    temperature: Optional[float] = 0.2
    top_p: Optional[float] = 0.95
    max_tokens: Optional[int] = 2048
    stream: Optional[bool] = False

class ModelCard(BaseModel):
    id: str
    object: str = "model"
    created: int = Field(default_factory=lambda: int(time.time()))
    owned_by: str = "colab-local"

class ModelListResponse(BaseModel):
    object: str = "list"
    data: List[ModelCard]

def init_model(model_path_or_id: str, load_in_4bit: bool = True):
    global MODEL, TOKENIZER, MODEL_NAME
    print(f"🔄 Initializing Model: {model_path_or_id} (4-bit={load_in_4bit})...")
    
    TOKENIZER = AutoTokenizer.from_pretrained(model_path_or_id, trust_remote_code=True)
    if TOKENIZER.pad_token is None:
        TOKENIZER.pad_token = TOKENIZER.eos_token
    TOKENIZER.padding_side = "left"

    kwargs = {
        "device_map": "auto",
        "trust_remote_code": True,
        "torch_dtype": torch.float16,
    }
    
    if load_in_4bit:
        from transformers import BitsAndBytesConfig
        kwargs["quantization_config"] = BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_compute_dtype=torch.float16,
            bnb_4bit_quant_type="nf4",
            bnb_4bit_use_double_quant=True,
        )

    MODEL = AutoModelForCausalLM.from_pretrained(model_path_or_id, **kwargs)
    MODEL_NAME = model_path_or_id
    print(f"✅ Model {model_path_or_id} loaded successfully!")

@app.get("/v1/models", response_model=ModelListResponse)
async def list_models():
    return ModelListResponse(data=[ModelCard(id=MODEL_NAME)])

@app.post("/v1/chat/completions")
async def chat_completions(req: ChatCompletionRequest):
    global MODEL, TOKENIZER, MODEL_NAME
    if MODEL is None or TOKENIZER is None:
        raise HTTPException(status_code=503, detail="Model is not initialized on server.")

    # Convert messages to chat template
    messages_payload = [{"role": m.role, "content": m.content} for m in req.messages]
    
    try:
        prompt_text = TOKENIZER.apply_chat_template(
            messages_payload,
            tokenize=False,
            add_generation_prompt=True
        )
    except Exception as e:
        # Fallback simple template
        prompt_text = ""
        for m in req.messages:
            prompt_text += f"<|im_start|>{m.role}\n{m.content}<|im_end|>\n"
        prompt_text += "<|im_start|>assistant\n"

    inputs = TOKENIZER([prompt_text], return_tensors="pt").to(MODEL.device)
    completion_id = f"chatcmpl-{uuid.uuid4().hex[:12]}"
    created_time = int(time.time())

    generation_kwargs = dict(
        inputs,
        max_new_tokens=req.max_tokens or 2048,
        do_sample=req.temperature > 0 if req.temperature is not None else False,
        temperature=req.temperature if req.temperature and req.temperature > 0 else None,
        top_p=req.top_p if req.temperature and req.temperature > 0 else None,
        pad_token_id=TOKENIZER.pad_token_id,
    )

    if req.stream:
        async def event_generator() -> AsyncGenerator[str, None]:
            streamer = TextIteratorStreamer(TOKENIZER, skip_prompt=True, skip_special_tokens=True)
            generation_kwargs["streamer"] = streamer
            
            thread = threading.Thread(target=MODEL.generate, kwargs=generation_kwargs)
            thread.start()

            # First chunk: role
            first_chunk = {
                "id": completion_id,
                "object": "chat.completion.chunk",
                "created": created_time,
                "model": MODEL_NAME,
                "choices": [{"index": 0, "delta": {"role": "assistant", "content": ""}, "finish_reason": None}]
            }
            yield f"data: {json.dumps(first_chunk)}\n\n"

            for new_text in streamer:
                if new_text:
                    chunk = {
                        "id": completion_id,
                        "object": "chat.completion.chunk",
                        "created": created_time,
                        "model": MODEL_NAME,
                        "choices": [{"index": 0, "delta": {"content": new_text}, "finish_reason": None}]
                    }
                    yield f"data: {json.dumps(chunk)}\n\n"
                await asyncio.sleep(0.001)

            # Final chunk
            final_chunk = {
                "id": completion_id,
                "object": "chat.completion.chunk",
                "created": created_time,
                "model": MODEL_NAME,
                "choices": [{"index": 0, "delta": {}, "finish_reason": "stop"}]
            }
            yield f"data: {json.dumps(final_chunk)}\n\n"
            yield "data: [DONE]\n\n"

        return StreamingResponse(event_generator(), media_type="text/event-stream")

    else:
        with torch.no_grad():
            outputs = MODEL.generate(**generation_kwargs)
        
        # Decode only newly generated tokens
        input_len = inputs["input_ids"].shape[1]
        response_text = TOKENIZER.decode(outputs[0][input_len:], skip_special_tokens=True)

        return {
            "id": completion_id,
            "object": "chat.completion",
            "created": created_time,
            "model": MODEL_NAME,
            "choices": [
                {
                    "index": 0,
                    "message": {
                        "role": "assistant",
                        "content": response_text,
                    },
                    "finish_reason": "stop"
                }
            ],
            "usage": {
                "prompt_tokens": input_len,
                "completion_tokens": len(outputs[0]) - input_len,
                "total_tokens": len(outputs[0])
            }
        }

if __name__ == "__main__":
    import uvicorn
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--model", type=str, required=True, help="Hugging Face ID or local path")
    parser.add_argument("--port", type=int, default=8000)
    parser.add_argument("--4bit", dest="load_4bit", action="store_true", default=True)
    args = parser.parse_args()

    init_model(args.model, load_in_4bit=args.load_4bit)
    uvicorn.run(app, host="0.0.0.0", port=args.port)
