"""
ai-service/graphs/questions_graph.py
Owner: Amritansu

Mini-graph for the questions phase: START → questions_node → END.

v4.0 Architecture: Each phase has its OWN compiled StateGraph.
- All 5 share the same AppForgeState TypedDict and SqliteSaver (langgraph.db).
- thread_id = session_id ties checkpoints across all 5 graphs.
- Each graph is invoked exactly ONCE per HTTP request; no single ainvoke() runs all phases.

Usage:
    from ai_service.graphs.questions_graph import questions_graph
    result = await questions_graph.ainvoke(
        {"session_id": session_id, ...},
        config={"configurable": {"thread_id": session_id}},
    )
"""

from langgraph.graph import StateGraph, START, END
from ai_service.state.appforge_state import AppForgeState
from ai_service.nodes.questions_node import questions_node
from ai_service.graphs.checkpointer import checkpointer

_builder = StateGraph(AppForgeState)
_builder.add_node("questions", questions_node)
_builder.add_edge(START, "questions")
_builder.add_edge("questions", END)

questions_graph = _builder.compile(checkpointer=checkpointer)
