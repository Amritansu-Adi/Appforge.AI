"""
ai-service/tests/test_mcp_tools.py
Owner: Amritansu

v4.0 Updates:
  - validate_mermaid: now pure Python (no Node.js needed) — all tests run without Node.
  - mcp_client import: updated from mcp_client.py → client.py.
  - Added unmatched-quote test (new check in v4 validate_mermaid).
"""

import pytest
from ai_service.mcp.tools.validate_sql import validate_sql_schema
from ai_service.mcp.tools.validate_mermaid import validate_mermaid


# ─── validate_sql_schema ───────────────────────────────────────────────

def test_validate_sql_valid():
    result = validate_sql_schema(
        "CREATE TABLE users (id TEXT PRIMARY KEY, email TEXT UNIQUE NOT NULL);"
    )
    assert result["valid"] is True


def test_validate_sql_invalid():
    result = validate_sql_schema("CREATE TABLE (no name here);")
    assert result["valid"] is False
    assert "error" in result


def test_validate_sql_multi_table():
    result = validate_sql_schema(
        "CREATE TABLE a (id INTEGER PRIMARY KEY);"
        "CREATE TABLE b (id INTEGER PRIMARY KEY, a_id INTEGER REFERENCES a(id));"
    )
    assert result["valid"] is True


# ─── validate_mermaid (v4 pure Python — no Node.js required) ───────────

def test_validate_mermaid_flowchart_valid():
    result = validate_mermaid("flowchart TD\n    A --> B\n    B --> C", diagram_type="generic")
    assert result["valid"] is True


def test_validate_mermaid_graph_valid():
    result = validate_mermaid("graph TD\n    A --> B", diagram_type="generic")
    assert result["valid"] is True


def test_validate_mermaid_er_valid():
    src = 'erDiagram\n    USER {\n        text id PK\n        text email\n    }\n    TASK {\n        integer id PK\n    }\n    USER ||--o{ TASK : "assigns"'
    result = validate_mermaid(src, diagram_type="er")
    assert result["valid"] is True


def test_validate_mermaid_invalid_no_type():
    result = validate_mermaid("not a valid mermaid diagram at all $$$$", diagram_type="generic")
    assert result["valid"] is False
    assert "error" in result


def test_validate_mermaid_empty():
    result = validate_mermaid("", diagram_type="generic")
    assert result["valid"] is False


def test_validate_mermaid_only_declaration():
    result = validate_mermaid("flowchart TD", diagram_type="generic")
    assert result["valid"] is False
    assert "no content" in result["error"].lower()


def test_validate_mermaid_unmatched_quotes():
    result = validate_mermaid('graph TD\n    A -->|"broken| B', diagram_type="generic")
    assert result["valid"] is False
    assert "quote" in result["error"].lower()


# ─── McpClient (v4 path: mcp/client.py) ───────────────────────────────

@pytest.mark.asyncio
async def test_mcp_client_validate_sql():
    from ai_service.mcp.client import mcp_client
    result = await mcp_client.call_tool("validate_sql_schema", {
        "sql": "CREATE TABLE tasks (id INTEGER PRIMARY KEY, title TEXT NOT NULL);"
    })
    assert result["valid"] is True


@pytest.mark.asyncio
async def test_mcp_client_validate_mermaid():
    from ai_service.mcp.client import mcp_client
    result = await mcp_client.call_tool("validate_mermaid", {
        "src": "graph TD\n    A --> B",
        "diagram_type": "generic",
    })
    assert result["valid"] is True


@pytest.mark.asyncio
async def test_mcp_client_unknown_tool():
    from ai_service.mcp.client import mcp_client
    with pytest.raises(ValueError, match="Unknown MCP tool"):
        await mcp_client.call_tool("non_existent_tool", {})
