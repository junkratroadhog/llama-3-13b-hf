import json
from fastapi import FastAPI
from pydantic import BaseModel
from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import PeftModel, LoraConfig, get_peft_model
from pathlib import Path
import subprocess
import torch

app = FastAPI()

MODEL_PATH = "/workspace/Llama-3-13b-hf"
LORA_PATH = "/workspace/lora_weights"
LOG_FILE = Path("/workspace/logged_prompts.json")
LAST_COUNT_FILE = Path("/workspace/last_trained_count.txt")

# Load tokenizer and base model
tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
model = AutoModelForCausalLM.from_pretrained(
    MODEL_PATH,
    device_map="auto",
    load_in_4bit=True,
    torch_dtype=torch.float16
)

# Load LoRA weights if available
if Path(LORA_PATH).exists():
    model = PeftModel.from_pretrained(model, LORA_PATH, device_map="auto")

# Initialize log file
if not LOG_FILE.exists():
    LOG_FILE.write_text(json.dumps({"train": []}, indent=4))

if not LAST_COUNT_FILE.exists():
    LAST_COUNT_FILE.write_text("0")

class Request(BaseModel):
    prompt: str
    max_tokens: int = 200

@app.post("/generate")
def generate(req: Request):
    inputs = tokenizer(req.prompt, return_tensors="pt").to("cuda")
    output = model.generate(**inputs, max_new_tokens=req.max_tokens)
    result = tokenizer.decode(output[0])

    # Log prompt & completion
    with open(LOG_FILE, "r+") as f:
        data = json.load(f)
        data["train"].append({"prompt": req.prompt, "completion": result})
        f.seek(0)
        json.dump(data, f, indent=4)
        f.truncate()

    return {"text": result}

@app.post("/train_lora")
def train_lora():
    """
    Trigger incremental LoRA training manually
    """
    subprocess.run([
        "python3", "/workspace/train_lora.py",
        "--base_model", MODEL_PATH,
        "--data", str(LOG_FILE),
        "--output", LORA_PATH,
        "--batch_size", "1",
        "--epochs", "3",
        "--fp16",
        "--last_count_file", str(LAST_COUNT_FILE)
    ], check=True)

    return {"status": "LoRA training completed"}
