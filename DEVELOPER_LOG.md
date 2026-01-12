# Developer Log — Kit

Date: 2026-01-12

## What I built

### ✅ Repo hygiene (monorepo)
- Converted the workspace into a single git repo rooted at `/home/stacy/kit`.
- Added root `.gitignore` to keep `frontend/node_modules/` and build artifacts out of git.
- Pushed everything to `main` on GitHub.

### ✅ Frontend scaffolding (Vite + React + Tailwind)
Location: `frontend/`

- Vite + React + TypeScript wiring:
  - `frontend/index.html`
  - `frontend/vite.config.ts`
  - `frontend/tsconfig.json`
  - `frontend/src/main.tsx`
  - `frontend/src/App.tsx`
- Tailwind v4 setup for Vite:
  - `frontend/tailwind.config.js`
  - `frontend/postcss.config.js` (uses `@tailwindcss/postcss`)
  - `frontend/src/styles/index.css` (Atomic Era tokens + components)
- UI components:
  - `frontend/src/components/Sidebar.tsx` (Boomerang motif + Atomic palette)
  - `frontend/src/components/ChatWindow.tsx`

### ✅ Animated Mascot
- Uses `frontend/src/assets/kit/kit-cat.svg`.
- Component: `frontend/src/components/Mascot.tsx`
- States:
  - `idle`: gentle breathing
  - `thinking`: twitch/tilt loop
  - `success`: quick shake/purr effect

### ✅ Backend middleware (FastAPI)
Location: `app/main.py`

- Added an HTTP middleware that returns Atomic Era flavored error payloads:
  - 502 for upstream/proxy issues: “Gee Whiz! Something went wrong!”
  - 500 for unexpected errors: “Jumpin' Jupiter!”
- Added a lightweight proxy endpoint:
  - `/{proxy}/{path}` style: `/proxy/{full_path:path}`
  - Defaults to `OPENWEBUI_BASE_URL=http://localhost:3000`
  - Timeout tunable via `OPENWEBUI_PROXY_TIMEOUT`

### ✅ Module discovery system
Location: `app/modules/registry.py`

- Fixes the previous bug (`@app.get` without `app`).
- Implements auto-discovery of `app/modules/*.py` via `pkgutil`.
- Tool contract:
  - `TOOL_DEFINITION = { id, name, icon, description }`
  - optional `run(payload: dict) -> Any`
- API:
  - `GET /modules/list` returns discovered tools
  - `POST /modules/run/{tool_id}` runs the tool

### ✅ Tooling note: no mock tools

Kit deliberately avoids demo/mock tools. If a capability isn't real enough to
ship, it shouldn't be discoverable or runnable.

### Minor cleanup
- `app/modules/inbox_cleaner.py` now has a `TOOL_DEFINITION` and a placeholder `run()` so it shows up in discovery.

## How to run (quick)

### Frontend
- Install already done in `frontend/package-lock.json`.
- Build was verified with `npm run build`.

### Backend
- Depends on `fastapi`, `uvicorn`, `requests` (already in `requirements.txt`).

## Next steps
- Wire the frontend chat input to call the backend proxy and/or tool routes.
- Decide the stable tool schema (inputs/outputs) and add per-tool validation.
- Add real integrations for tools (no mocks) or keep tools marked "not implemented".
- Add tests:
  - unit tests for `registry.discover_tools()`
