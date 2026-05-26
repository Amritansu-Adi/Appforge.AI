"""
ai-service/tests/test_mcp_tools.py
Owner: Amritansu
Status: PARTIALLY IMPLEMENTED — SQL tests work immediately; JS/Mermaid need node installed.
"""
import pytest
from ai_service.mcp.tools.validate_sql import validate_sql_schema
from ai_service.mcp.tools.validate_mermaid import validate_mermaid


def test_validate_sql_valid():
    result = validate_sql_schema(
        "CREATE TABLE users (id TEXT PRIMARY KEY, email TEXT UNIQUE NOT NULL);"
    )
    assert result["valid"] is True


def test_validate_sql_invalid():
    result = validate_sql_schema("CREATE TABLE (no name here);")
    assert result["valid"] is False
    assert "error" in result


def test_validate_mermaid_valid():
    result = validate_mermaid("graph TD\n    A --> B", type="generic")
    assert result["valid"] is True


def test_validate_mermaid_invalid():
    result = validate_mermaid("not a valid mermaid diagram at all $$$$", type="generic")
    assert result["valid"] is False


@pytest.mark.asyncio
async def test_mcp_client_validate_sql():
    from ai_service.mcp.mcp_client import mcp_client
    result = await mcp_client.call_tool("validate_sql_schema", {
        "sql": "CREATE TABLE tasks (id INTEGER PRIMARY KEY, title TEXT NOT NULL);"
    })
    assert result["valid"] is True
