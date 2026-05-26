"""
ai-service/routers/ai_router.py
Owner: Amritansu
Status: STUB — implement in Phase 2.4 (overview), 3.2 (questions), 4.2 (diagrams)

Exposes: POST /internal/ai/overview
         POST /internal/ai/questions
         POST /internal/ai/diagrams
"""
from fastapi import APIRouter

router = APIRouter(prefix="/internal/ai", tags=["ai"])

# TODO Phase 2.4: implement /overview endpoint
# TODO Phase 3.2: implement /questions endpoint
# TODO Phase 4.2: implement /diagrams endpoint
