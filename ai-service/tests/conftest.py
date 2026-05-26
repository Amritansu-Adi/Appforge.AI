"""
ai-service/tests/conftest.py
Owner: Amritansu

Pytest fixtures shared across all test files.
Phase 0 deliverable — Prateeksha needs llm_mock and sample_state to build chains.
"""

import pytest
from ai_service.models.llm_mock import llm_mock
from ai_service.state.appforge_state import AppForgeState


@pytest.fixture
def mock_llm():
    """Drop-in replacement for llm in any chain. Returns deterministic responses."""
    return llm_mock


@pytest.fixture
def sample_session_state() -> AppForgeState:
    """Fully populated state for use in graph/node tests."""
    return AppForgeState(
        session_id="test-session-uuid-0001",
        user_id="test-user-uuid-0001",
        idea_text=(
            "I want to build a task management app for small teams "
            "where users can create tasks, assign them to team members, "
            "set due dates, and track progress on a dashboard."
        ),
        overview_json={
            "app_name": "TaskMaster Pro",
            "one_liner": "A simple task management app for small teams to track work and deadlines.",
            "target_users": ["Team leads", "Project managers", "Individual contributors"],
            "core_features": [
                "Create and assign tasks",
                "Set due dates and priorities",
                "Mark tasks complete",
                "View team member workload",
            ],
            "complexity": "standard",
            "tech_notes": "Needs user authentication and role-based access.",
            "data_entities": ["User", "Task", "Project", "Comment"],
        },
        complexity="standard",
        questions=[
            {
                "question_id": "q1",
                "category": "Users & Roles",
                "question": "What user roles should the app support?",
                "type": "choice",
                "options": ["Admin only", "Admin + Members", "Admin + Managers + Members"],
            }
        ],
        answers=[
            {"question_id": "q1", "answer_text": "Admin + Members"}
        ],
        diagrams=None,
        diagram_validation_errors=[],
        srs_markdown="",
        sdd_markdown="",
        brief_markdown="",
        srs_docx_base64="",
        sdd_docx_base64="",
        generated_files=[],
        zip_base64=None,
        retry_count=0,
        last_error=None,
    )


@pytest.fixture
def sample_overview_json() -> dict:
    """Standalone overview dict for chain-level tests."""
    return {
        "app_name": "TaskMaster Pro",
        "one_liner": "A simple task management app for small teams.",
        "target_users": ["Team leads", "Individual contributors"],
        "core_features": ["Create tasks", "Assign tasks", "Track progress"],
        "complexity": "standard",
        "tech_notes": "Needs auth and role-based access.",
        "data_entities": ["User", "Task", "Project"],
    }
