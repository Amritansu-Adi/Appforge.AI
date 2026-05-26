"""
ai-service/graph/appforge_state.py
Owner: Amritansu

LangGraph state schema for the AppForge pipeline.
TypedDict — LangGraph merges partial dicts returned from nodes into this shape.
"""

from typing import TypedDict, Optional
from typing_extensions import Literal


class OverviewOutput(TypedDict):
    app_name: str
    one_liner: str
    target_users: list[str]
    core_features: list[str]
    complexity: Literal["simple", "standard", "complex"]
    tech_notes: str
    data_entities: list[str]


class Question(TypedDict):
    question_id: str
    category: str
    question: str
    type: Literal["text", "choice"]
    options: Optional[list[str]]


class Answer(TypedDict):
    question_id: str
    answer_text: str


class DiagramSet(TypedDict):
    use_case_diagram: str
    architecture_diagram: str
    er_diagram: str


class GeneratedFile(TypedDict):
    path: str
    content: str
    source: Literal["ai", "template"]


class AppForgeState(TypedDict):
    # Session metadata
    session_id: str
    user_id: str
    current_phase: Literal["overview", "questions", "diagrams", "docs", "codegen", "complete"]

    # Phase 1 — Overview
    idea_text: str
    overview_json: Optional[OverviewOutput]

    # Phase 2 — Questions
    questions: list[Question]
    answers: list[Answer]
    complexity: Optional[Literal["simple", "standard", "complex"]]

    # Phase 3 — Diagrams
    diagrams: Optional[DiagramSet]
    diagram_errors: list[str]

    # Phase 4 — Docs
    srs_markdown: str
    sdd_markdown: str
    brief_markdown: str

    # Phase 5 — Codegen
    generated_files: list[GeneratedFile]
    zip_path: Optional[str]

    # Retry tracking
    retry_count: int
    last_error: Optional[str]
