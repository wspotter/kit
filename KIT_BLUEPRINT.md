# Project Blueprint: Kit (The Atomic Assistant)

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
4. **Self-Correct**: If verification fails, retry with new logic (max 3 times).