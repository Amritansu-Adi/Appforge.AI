"""
ai-service/routers/docs_router.py
Owner: Amritansu
Status: STUB — implement in Phase 5.2

Exposes: POST /internal/docs/stream/{doc_type}  (StreamingResponse SSE)
"""
from fastapi import APIRouter

router = APIRouter(prefix="/internal/docs", tags=["docs"])

# TODO Phase 5.2: implement SSE streaming endpoint calling stream_doc()
