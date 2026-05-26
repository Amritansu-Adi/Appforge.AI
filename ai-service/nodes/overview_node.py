"""
ai-service/nodes/overview_node.py
Owner: Amritansu
Status: STUB — wired in Phase 2.4 once overview_chain (Prateeksha) is merged.

v4.0: Moved from graph/nodes/ to nodes/. Imports from state/ (not graph/).
"""

from ai_service.state.appforge_state import AppForgeState


async def overview_node(state: AppForgeState) -> dict:
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
    # return {"overview_json": result.model_dump(), "complexity": result.complexity}
    raise NotImplementedError("overview_node not yet implemented — Phase 2.4")
