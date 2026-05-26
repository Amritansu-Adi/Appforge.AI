"""
ai-service/state/appforge_state.py
Owner: Amritansu

LangGraph state schema for the AppForge pipeline.
TypedDict — LangGraph merges partial dicts returned from nodes into this shape.

v4.0 Changes:
  - Moved from graph/appforge_state.py to state/appforge_state.py
  - Removed current_phase field (each mini-graph handles ONE phase; phase is implicit)
  - Removed zip_path (Python returns base64, no shared filesystem)
  - Added diagram_validation_errors (renamed from diagram_errors)
  - Added srs_docx_base64, sdd_docx_base64 (base64 encoded .docx — no shared filesystem)
  - Added zip_base64 (base64 encoded zip — no shared filesystem)
  - GeneratedFile: added status field to match DB schema
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
    status: Literal["pending", "generating", "validated", "packaged", "failed"]


class AppForgeState(TypedDict):
    # Session metadata
    session_id: str
    user_id: str

    # Phase 1 — Overview
    idea_text: str
    overview_json: Optional[OverviewOutput]
    complexity: Optional[Literal["simple", "standard", "complex"]]

    # Phase 2 — Questions
    questions: list[Question]
    answers: list[Answer]

    # Phase 3 — Diagrams
    diagrams: Optional[DiagramSet]
    diagram_validation_errors: list[str]  # v4: renamed from diagram_errors

    # Phase 4 — Docs
    srs_markdown: str
    sdd_markdown: str
    brief_markdown: str
    srs_docx_base64: str  # v4: base64-encoded .docx, returned in JSON response
    sdd_docx_base64: str  # v4: base64-encoded .docx, returned in JSON response

    # Phase 5 — Codegen
    generated_files: list[GeneratedFile]
    zip_base64: Optional[str]  # v4: base64-encoded zip (no shared filesystem)

    # Retry tracking
    retry_count: int
    last_error: Optional[str]
