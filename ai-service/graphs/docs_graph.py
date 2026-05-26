"""
ai-service/graphs/docs_graph.py
Owner: Amritansu

Mini-graph for the docs phase: START → docs_node → END.

v4.0 Architecture: Each phase has its OWN compiled StateGraph.
- All 5 share the same AppForgeState TypedDict and SqliteSaver (langgraph.db).
- thread_id = session_id ties checkpoints across all 5 graphs.
- Each graph is invoked exactly ONCE per HTTP request; no single ainvoke() runs all phases.

Usage:
    from ai_service.graphs.docs_graph import docs_graph
    result = await docs_graph.ainvoke(
        {"session_id": session_id, ...},
        config={"configurable": {"thread_id": session_id}},
    )
"""

from langgraph.graph import StateGraph, START, END
from ai_service.state.appforge_state import AppForgeState
from ai_service.nodes.docs_node import docs_node
from ai_service.graphs.checkpointer import checkpointer

_builder = StateGraph(AppForgeState)
_builder.add_node("docs", docs_node)
_builder.add_edge(START, "docs")
_builder.add_edge("docs", END)

docs_graph = _builder.compile(checkpointer=checkpointer)
