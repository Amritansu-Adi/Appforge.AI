"""
ai-service/graph/appforge_graph.py
Owner: Amritansu

LangGraph StateGraph — wires all 5 phase nodes into a sequential pipeline.
SqliteSaver checkpointer writes to the same appforge.db used by Node.js
(langgraph_checkpoints + langgraph_writes tables).

The graph is NOT invoked end-to-end automatically. Each FastAPI endpoint
invokes only the relevant node by resuming the graph at the correct phase
using thread_id = session_id for checkpoint continuity.

Usage:
    from ai_service.graph.appforge_graph import compiled_graph

    result = await compiled_graph.ainvoke(
        partial_state_dict,
        config={"configurable": {"thread_id": session_id}},
    )
"""

import os
import sqlite3
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.sqlite import SqliteSaver
from ai_service.graph.appforge_state import AppForgeState

# ── Node imports (stub functions — filled per phase) ────────────────────
from ai_service.graph.nodes.overview_node import overview_node
from ai_service.graph.nodes.questions_node import questions_node
from ai_service.graph.nodes.diagrams_node import diagrams_node
from ai_service.graph.nodes.docs_node import docs_node
from ai_service.graph.nodes.codegen_node import codegen_node

# ── SQLite checkpointer — shares the same DB file as Node.js ────────────
DB_PATH = os.environ.get("DB_PATH", "../data/appforge.db")
_conn = sqlite3.connect(DB_PATH, check_same_thread=False)
checkpointer = SqliteSaver(_conn)

# ── Build the graph ──────────────────────────────────────────────────────
builder = StateGraph(AppForgeState)

builder.add_node("overview",  overview_node)
builder.add_node("questions", questions_node)
builder.add_node("diagrams",  diagrams_node)
builder.add_node("docs",      docs_node)
builder.add_node("codegen",   codegen_node)

builder.add_edge(START,       "overview")
builder.add_edge("overview",  "questions")
builder.add_edge("questions", "diagrams")
builder.add_edge("diagrams",  "docs")
builder.add_edge("docs",      "codegen")
builder.add_edge("codegen",   END)

compiled_graph = builder.compile(checkpointer=checkpointer)
