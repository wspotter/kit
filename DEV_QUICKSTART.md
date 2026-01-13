# Kit — Dev Quickstart (reliable run)

This is the “no drama” way to run Kit locally on Linux.

## What you’re starting

- Backend (FastAPI): http://127.0.0.1:8000
- Frontend (Vite): http://127.0.0.1:5173
- Optional engine (Open WebUI via Docker): http://127.0.0.1:3000

The frontend dev server proxies:

- `/modules/*` → backend `:8000`
- `/proxy/*` → backend `:8000` (which then reverse-proxies to Open WebUI)

## 1) Backend

From repo root:

```bash
pip install -r requirements.txt
uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

Verify:

```bash
curl -s -o /dev/null -w "%{http_code}" http://127.0.0.1:8000/ && echo
curl -s -o /dev/null -w "%{http_code}" http://127.0.0.1:8000/modules/list && echo
```

## 2) Frontend

In a second terminal:

```bash
cd frontend
npm install
npm run dev -- --host 127.0.0.1 --port 5173
```

Open:

- http://127.0.0.1:5173

Verify the proxy works (this should return `200`):

```bash
curl -s -o /dev/null -w "%{http_code}" http://127.0.0.1:5173/modules/list && echo
```

## If a port is already in use

If you see “address already in use” it usually means Kit is *already running*.

See what’s listening:

```bash
lsof -i :5173 -sTCP:LISTEN -n -P || true
lsof -i :8000 -sTCP:LISTEN -n -P || true
```

If it’s stale and you want to stop it, kill the PID:

```bash
kill <PID>
```

## Optional: Run Open WebUI engine

If you want the `/proxy/*` routes to work against Open WebUI:

```bash
docker compose up -d
```

Then verify (optional):

```bash
curl -s -o /dev/null -w "%{http_code}" http://127.0.0.1:3000/ && echo
```
