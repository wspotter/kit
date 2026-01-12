# Kit — Atomic Era AI Assistant

Kit is a 1950s/60s Atomic Era-themed assistant.

- Backend: FastAPI “middleware”
- Engine: Open WebUI (typically via Docker)
- Frontend: Vite + React + Tailwind

## Quickstart

### 1) Backend (FastAPI)

Install deps:

```bash
pip install -r requirements.txt
```

Run the server:

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

Endpoints:
- `GET /` health
- `GET /modules/list` list discovered tools
- `POST /modules/run/{tool_id}` run a tool
- `/{proxy}/...` via `GET|POST /proxy/{full_path:path}` to Open WebUI

### 2) Frontend (Vite)

```bash
cd frontend
npm install
npm run dev
```

Then open:
- http://localhost:5173

The dev server proxies these paths to the backend:
- `/modules/*` → `http://localhost:8000`
- `/proxy/*` → `http://localhost:8000`

## Open WebUI proxy configuration

The backend proxy defaults to `http://localhost:3000`.

Override with:

```bash
export OPENWEBUI_BASE_URL=http://localhost:3000
export OPENWEBUI_PROXY_TIMEOUT=30
```

## Atomic Era palette

- Teal: `#008080`
- Tangerine: `#FF8C00`
- Mustard: `#E1AD01`
- Beige: `#F1E4B7`
