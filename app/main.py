from fastapi import FastAPI
from app.modules.registry import router as module_router

app = FastAPI(title="Kit Middleware")

@app.get("/")
async def root():
    return {"message": "Kit is purring. Atomic Era Middleware Active."}

app.include_router(module_router, prefix="/modules")
