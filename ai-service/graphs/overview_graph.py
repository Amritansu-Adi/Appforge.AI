"""
ai-service/graphs/overview_graph.py
Owner: Amritansu

Mini-graph for the overview phase: START → overview_node → END.

v4.0 Architecture: Each phase has its OWN compiled StateGraph.
- All 5 share the same AppForgeState TypedDict and SqliteSaver (langgraph.db).
- thread_id = session_id ties checkpoints across all 5 graphs.
- Each graph is invoked exactly ONCE per HTTP request; no single ainvoke() runs all phases.

Usage:
    from ai_service.graphs.overview_graph import overview_graph
    result = await overview_graph.ainvoke(
        {"session_id": session_id, ...},
        config={"configurable": {"thread_id": session_id}},
    )
"""

from langgraph.graph import StateGraph, START, END
from ai_service.state.appforge_state import AppForgeState
from ai_service.nodes.overview_node import overview_node
from ai_service.graphs.checkpointer import checkpointer

_builder = StateGraph(AppForgeState)
_builder.add_node("overview", overview_node)
_builder.add_edge(START, "overview")
_builder.add_edge("overview", END)

overview_graph = _builder.compile(checkpointer=checkpointer)
