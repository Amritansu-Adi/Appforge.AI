"""
ai-service/mcp/mcp_client.py
Owner: Amritansu

In-process async MCP client — calls tool handler functions directly
without any HTTP/socket overhead. All handlers are sync; run_in_executor
prevents blocking the async FastAPI event loop.

Usage:
    from ai_service.mcp.mcp_client import mcp_client
    result = await mcp_client.call_tool("validate_mermaid", {"src": "...", "type": "er"})
    # result: { "valid": bool, "error"?: str }
"""
import asyncio
from ai_service.mcp.tools.validate_mermaid import validate_mermaid
from ai_service.mcp.tools.validate_js import validate_js_syntax
from ai_service.mcp.tools.validate_jsx import validate_jsx_syntax
from ai_service.mcp.tools.validate_sql import validate_sql_schema

TOOL_MAP = {
    "validate_mermaid":    validate_mermaid,
    "validate_js_syntax":  validate_js_syntax,
    "validate_jsx_syntax": validate_jsx_syntax,
    "validate_sql_schema": validate_sql_schema,
}


class McpClient:
    async def call_tool(self, name: str, args: dict) -> dict:
        handler = TOOL_MAP.get(name)
        if not handler:
            raise ValueError(f"Unknown MCP tool: {name}")
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, lambda: handler(**args))


mcp_client = McpClient()
