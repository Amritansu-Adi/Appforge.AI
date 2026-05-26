"""
ai-service/chains/documentation_chain.py
Owner: Prateeksha
Status: STUB — implement in Phase 5.1

Async streaming chain using chain.astream().
Exports stream_doc(doc_type, session_context, on_token, on_complete).
"""
from typing import Callable, Literal

async def stream_doc(
    doc_type: Literal["srs", "sdd", "brief"],
    session_context: dict,
    on_token: Callable[[str], None],
    on_complete: Callable[[str], None],
) -> None:
    """
    TODO Phase 5.1 (Prateeksha): implement using chain.astream()
    """
    raise NotImplementedError("stream_doc not yet implemented — Phase 5.1")
