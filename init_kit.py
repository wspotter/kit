import os

# Define the project structure
project_name = "Kit"
structure = {
    "KIT_BLUEPRINT.md": """# Project Blueprint: Kit (The Atomic Assistant)

## 1. Vision & Identity
- **Name:** Kit
- **Vibe:** "Atomic Era" (1950s-60s) Advertising.
- **Style:** Starbursts, Boomerangs, Teal (#008080), Tangerine (#FF8C00), and Mustard (#E1AD01).
- **Avatar:** Mid-century minimalist black cat.

## 2. Technical Stack
- **Engine:** Open WebUI (Headless)
- **Brain:** AMD MI50 Cluster (llama.cpp ROCm)
- **Senses:** Nvidia RTX 3060/3070 (Faster-Whisper & Kokoro TTS)
- **Logic:** "Ralph Loop" (Self-correcting automation)

## 3. The Ralph Loop Definition
Tools must:
1. **Observe**: Check status (e.g., list emails).
2. **Execute**: Run action (e.g., delete email).
3. **Verify**: Check status again to confirm success.
4. **Self-Correct**: If verification fails, retry with new logic (max 3 times).""",

    "docker-compose.yml": """version: '3.8'
services:
  kit-engine:
    image: ghcr.io/open-webui/open-webui:main
    container_name: kit-engine
    ports:
      - "3000:8080"
    environment:
      - 'WEBUI_NAME=Kit'
      - 'OPENAI_API_BASE_URL=http://[AMD_SERVER_IP]:8080/v1'
      - 'OPENAI_API_KEY=none'
      - 'AUDIO_STT_ENGINE=openai'
      - 'AUDIO_STT_OPENAI_API_BASE_URL=http://[NVIDIA_SERVER_IP]:5001/v1'
      - 'AUDIO_TTS_ENGINE=openai'
      - 'AUDIO_TTS_OPENAI_API_BASE_URL=http://[NVIDIA_SERVER_IP]:5002/v1'
    volumes:
      - kit_data:/app/backend/data
    restart: always

volumes:
  kit_data:""",

    "app/main.py": """from fastapi import FastAPI
from app.modules.registry import router as module_router

app = FastAPI(title="Kit Middleware")

@app.get("/")
async def root():
    return {"message": "Kit is purring. Atomic Era Middleware Active."}

app.include_router(module_router, prefix="/modules")
""",

    "app/modules/registry.py": """from fastapi import APIRouter

router = APIRouter()

@app.get("/list")
async def list_modules():
    return [
        {"id": "inbox", "name": "Inbox Cleaner", "icon": "envelope"},
        {"id": "ebay", "name": "eBay Watcher", "icon": "shopping-cart"},
        {"id": "social", "name": "Social Manager", "icon": "camera"}
    ]
""",

    "app/modules/inbox_cleaner.py": """# Implementation of the Ralph Loop for Email
def clean_inbox():
    # 1. Observe
    # 2. Execute
    # 3. Verify
    # 4. Self-Correct
    pass
""",

    "frontend/theme.css": """:root {
  --atomic-teal: #008080;
  --atomic-tangerine: #FF8C00;
  --atomic-mustard: #E1AD01;
  --atomic-beige: #F1E4B7;
}

body {
  background-color: var(--atomic-beige);
  font-family: 'Futura', 'Gill Sans', sans-serif;
}""",

    "requirements.txt": "fastapi\\nuvicorn\\nrequests\\npython-multipart"
}

def setup_project():
    for path, content in structure.items():
        os.makedirs(os.path.dirname(path), exist_ok=True) if os.path.dirname(path) else None
        with open(path, "w") as f:
            f.write(content)
    print("✨ Kit has been initialized! Open this folder in VS Code and start vibe coding.")

if __name__ == "__main__":
    setup_project()
