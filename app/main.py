import os
from typing import Dict

import requests
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, Response

from app.modules.registry import router as module_router

app = FastAPI(title="Kit Middleware")


@app.middleware("http")
async def atomic_error_middleware(request: Request, call_next):
    try:
        return await call_next(request)
    except requests.RequestException as exc:
        # Proxy/network failure
        return JSONResponse(
            status_code=502,
            content={
                "error": "Gee Whiz! Something went wrong!",
                "detail": "Couldn't reach the Kit Engine (Open WebUI).",
                "hint": "Is the Docker container running and reachable from this host?",
                "path": str(request.url.path),
                "exception": str(exc),
            },
        )
    except Exception as exc:
        # Catch-all
        return JSONResponse(
            status_code=500,
            content={
                "error": "Jumpin' Jupiter!",
                "detail": "Unexpected trouble in Kit Middleware.",
                "path": str(request.url.path),
                "exception": str(exc),
            },
        )

@app.get("/")
async def root():
    return {"message": "Kit is purring. Atomic Era Middleware Active."}


@app.api_route(
    "/proxy/{full_path:path}",
    methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
)
async def proxy_to_openwebui(request: Request, full_path: str):
    """Very small reverse-proxy to a local Open WebUI instance.

    Contract:
    - Input: any HTTP request to /proxy/*
    - Output: same response body/status from Open WebUI
    - Error: Atomic Era JSON message with helpful hints
    """

    base_url = os.getenv("OPENWEBUI_BASE_URL", "http://localhost:3000").rstrip("/")
    target_url = f"{base_url}/{full_path.lstrip('/')}"

    # Preserve query string
    if request.url.query:
        target_url = f"{target_url}?{request.url.query}"

    # Forward headers conservatively
    headers: Dict[str, str] = {
        k: v
        for k, v in request.headers.items()
        if k.lower() not in {"host", "content-length"}
    }

    body = await request.body()

    resp = requests.request(
        method=request.method,
        url=target_url,
        headers=headers,
        data=body if body else None,
        timeout=float(os.getenv("OPENWEBUI_PROXY_TIMEOUT", "30")),
    )

    return Response(
        content=resp.content,
        status_code=resp.status_code,
        media_type=resp.headers.get("content-type"),
    )

app.include_router(module_router, prefix="/modules")
