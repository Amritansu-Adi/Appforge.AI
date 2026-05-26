"""
ai-service/mcp/server.py
Owner: Amritansu

FastMCP server exposing all 4 AppForge validation tools.
Tools are also callable in-process via mcp_client.py (no HTTP overhead).
"""
from mcp.server.fastmcp import FastMCP
from ai_service.mcp.tools.validate_mermaid import validate_mermaid
from ai_service.mcp.tools.validate_js import validate_js_syntax
from ai_service.mcp.tools.validate_jsx import validate_jsx_syntax
from ai_service.mcp.tools.validate_sql import validate_sql_schema

mcp = FastMCP("appforge-validator")

# Register all 4 tools on the FastMCP instance
mcp.tool()(validate_mermaid)
mcp.tool()(validate_js_syntax)
mcp.tool()(validate_jsx_syntax)
mcp.tool()(validate_sql_schema)
