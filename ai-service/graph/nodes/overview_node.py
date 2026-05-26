"""
ai-service/graph/nodes/overview_node.py
Owner: Amritansu
Status: STUB — wired in Phase 2.4 once overview_chain (Prateeksha) is merged.
"""

async def overview_node(state: dict) -> dict:
    """
    Calls overview_chain with idea_text, returns partial state update.
    Full implementation in Phase 2.4.
    """
    # TODO Phase 2.4: uncomment after Prateeksha merges feat/ai-overview-chain
    # from ai_service.chains.overview_chain import overview_chain
    # from ai_service.parsers.overview_parser import overview_parser
    # result = await overview_chain.ainvoke({
    #     "idea_text": state["idea_text"],
    #     "format_instructions": overview_parser.get_format_instructions(),
    # })
    # return {"overview_json": result.model_dump(), "current_phase": "questions"}
    raise NotImplementedError("overview_node not yet implemented — Phase 2.4")
