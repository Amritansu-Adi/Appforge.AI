"""
ai-service/main.py
Owner: Amritansu

FastAPI entry point for the AppForge Python AI Service.
- Runs on port 8000 (uvicorn)
- Only accepts requests from Node.js backend (X-Internal-Secret middleware)
- All LangSmith tracing is activated here at startup

Start with:
    uvicorn main:app --reload --port 8000
"""

import os
from dotenv import load_dotenv

load_dotenv()

# ── LangSmith Tracing Setup (must be set BEFORE any langchain import) ──
if os.environ.get("LANGSMITH_API_KEY"):
    os.environ["LANGCHAIN_TRACING_V2"] = "true"
    os.environ["LANGCHAIN_API_KEY"] = os.environ["LANGSMITH_API_KEY"]
    os.environ["LANGCHAIN_PROJECT"] = os.environ.get("LANGSMITH_PROJECT", "appforge-dev")

from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware

# Routers — registered once all phase modules are implemented
# from ai_service.routers import ai_router, codegen_router, docs_router

app = FastAPI(
    title="AppForge AI Service",
    version="3.0.0",
    description="Internal Python AI microservice. Not exposed to browser.",
)

AI_SERVICE_SECRET = os.environ.get("AI_SERVICE_SECRET", "")

if not AI_SERVICE_SECRET:
    print("⚠️  AI_SERVICE_SECRET not set — all non-health requests will be rejected.")


@app.middleware("http")
async def verify_internal_secret(request: Request, call_next):
    """
    Reject any request that doesn't carry the correct shared internal secret.
    /health is exempt so Docker/Render can ping it without a secret.
    """
    if not request.url.path.startswith("/health"):
        secret = request.headers.get("X-Internal-Secret")
        if secret != AI_SERVICE_SECRET:
            raise HTTPException(status_code=403, detail="Forbidden — invalid internal secret")
    return await call_next(request)


# ── Register Routers (uncomment as phases are implemented) ──────────────
# app.include_router(ai_router.router)      # Phase 2-4
# app.include_router(docs_router.router)    # Phase 5
# app.include_router(codegen_router.router) # Phase 6


@app.get("/health")
def health():
    """Health check — called by Node.js on startup and by Render."""
    return {"status": "ok", "service": "appforge-ai", "version": "3.0.0"}
