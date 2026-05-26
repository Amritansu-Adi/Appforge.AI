"""
ai-service/routers/codegen_router.py
Owner: Amritansu
Status: STUB — implement in Phase 6.2

Exposes: POST /internal/codegen/start  (StreamingResponse SSE)
"""
from fastapi import APIRouter

router = APIRouter(prefix="/internal/codegen", tags=["codegen"])

# TODO Phase 6.2: implement SSE streaming endpoint calling run_codegen_chain()
