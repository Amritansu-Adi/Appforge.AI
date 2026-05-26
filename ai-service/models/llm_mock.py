"""
ai-service/models/llm_mock.py
Owner: Amritansu

Deterministic mock LLM for development — avoids burning API quota.
Prateeksha uses this to build and test chains without real API keys.

Usage (swap into any chain file during dev):
    from ai_service.models.llm_mock import llm_mock as llm
"""

import json
from langchain_core.runnables import RunnableLambda
from langchain_core.messages import AIMessage, BaseMessage

# ── Mock response payloads (mirrors JS llm.mock.js) ────────────────────

MOCK_OVERVIEW = json.dumps({
    "app_name": "TaskMaster Pro",
    "one_liner": "A simple task management app for small teams to track work and deadlines.",
    "target_users": ["Team leads", "Project managers", "Individual contributors"],
    "core_features": [
        "Create and assign tasks",
        "Set due dates and priorities",
        "Mark tasks complete",
        "View team member workload",
        "Send deadline reminders",
    ],
    "complexity": "standard",
    "tech_notes": "Needs user authentication and role-based access. Email notifications implied.",
    "data_entities": ["User", "Task", "Project", "Comment"],
})

MOCK_QUESTIONS = json.dumps([
    {"question_id": "q1", "category": "Users & Roles", "question": "What user roles should the app support?", "type": "choice", "options": ["Admin only", "Admin + Members", "Admin + Managers + Members"]},
    {"question_id": "q2", "category": "Core Data", "question": "Should tasks support subtasks?", "type": "choice", "options": ["Yes", "No"]},
    {"question_id": "q3", "category": "Workflow", "question": "How should task status work?", "type": "choice", "options": ["Simple done/not done", "Kanban columns", "Custom statuses"]},
    {"question_id": "q4", "category": "UI/UX", "question": "Describe the main dashboard view you envision.", "type": "text"},
    {"question_id": "q5", "category": "Notifications", "question": "Should users receive email notifications?", "type": "choice", "options": ["Yes", "No", "Optional per user"]},
    {"question_id": "q6", "category": "Integrations", "question": "Any third-party integrations needed?", "type": "choice", "options": ["None", "Slack", "Google Calendar", "Multiple"]},
    {"question_id": "q7", "category": "Core Data", "question": "Should tasks have file attachment support?", "type": "choice", "options": ["Yes", "No"]},
    {"question_id": "q8", "category": "Users & Roles", "question": "Should the app support multiple separate workspaces?", "type": "choice", "options": ["Yes", "No — single workspace"]},
])

MOCK_DIAGRAMS = json.dumps({
    "use_case_diagram": "graph TD\n    User -->|Login| AuthSystem\n    User -->|Create Task| TaskSystem\n    Admin -->|Manage Users| UserSystem",
    "architecture_diagram": "graph LR\n    Client[React Frontend] -->|REST API| Server[Express Backend]\n    Server -->|SQL Queries| DB[(SQLite DB)]",
    "er_diagram": 'erDiagram\n    USER {\n      text id PK\n      text email\n    }\n    TASK {\n      integer id PK\n      text title\n      text assignee_id FK\n    }\n    USER ||--o{ TASK : "is assigned"',
})

MOCK_SRS = "# Software Requirements Specification — TaskMaster Pro\n\n## 1. Introduction\nThis document describes the requirements for TaskMaster Pro...\n\n## 2. Functional Requirements\n- Users shall register and log in\n- Users shall create, assign, and track tasks\n"
MOCK_SDD = "# Software Design Document — TaskMaster Pro\n\n## 1. Architecture Overview\nThree-tier architecture: React frontend, Express REST API, SQLite persistence...\n"
MOCK_BRIEF = "## TaskMaster Pro — Project Brief\n\nA task management app for small teams.\n\n**Stack:** React + Express + SQLite\n"

RESPONSE_MAP = {
    "overview": MOCK_OVERVIEW,
    "questions": MOCK_QUESTIONS,
    "diagrams": MOCK_DIAGRAMS,
    "srs": MOCK_SRS,
    "sdd": MOCK_SDD,
    "brief": MOCK_BRIEF,
}


def _detect_type(messages: list) -> str:
    """Inspect message content to pick the right mock response."""
    combined = " ".join(
        m.content if isinstance(m.content, str) else ""
        for m in messages
    ).lower()
    if "overview" in combined or "app name" in combined:
        return "overview"
    if "question" in combined or "clarif" in combined:
        return "questions"
    if "diagram" in combined or "mermaid" in combined:
        return "diagrams"
    if "srs" in combined or "requirements specification" in combined:
        return "srs"
    if "sdd" in combined or "design document" in combined:
        return "sdd"
    if "brief" in combined:
        return "brief"
    return "overview"


def _mock_invoke(messages) -> AIMessage:
    """Core mock invoke — works for both list-of-messages and prompt-value inputs."""
    if not isinstance(messages, list):
        # Could be a ChatPromptValue — convert to message list
        try:
            messages = messages.to_messages()
        except AttributeError:
            messages = []
    response_type = _detect_type(messages)
    return AIMessage(content=RESPONSE_MAP.get(response_type, MOCK_OVERVIEW))


llm_mock = RunnableLambda(_mock_invoke)
