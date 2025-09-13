import subprocess
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

MODEL_PATH = "/workspace/models/Llama-3-8B/Meta-Llama-3-8B-Instruct.Q4_K_M.gguf"
LLAMA_CPP_BIN = "/workspace/llama.cpp/main"

class Request(BaseModel):
    prompt: str
    max_tokens: int = 200

@app.post("/generate")
def generate(req: Request):
    result = subprocess.run(
        [
            LLAMA_CPP_BIN,
            "-m", MODEL_PATH,
            "-p", req.prompt,
            "-n", str(req.max_tokens)
        ],
        capture_output=True,
        text=True
    )
    return {"text": result.stdout}
