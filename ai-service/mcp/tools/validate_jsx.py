"""
ai-service/mcp/tools/validate_jsx.py
Owner: Amritansu

Validates JSX syntax using @babel/parser via Node.js subprocess.
Requires: @babel/parser npm package globally available (see setup_node_deps.sh)
"""
import subprocess
import json


def validate_jsx_syntax(code: str, filename: str = "unknown.jsx") -> dict:
    """
    Validate JSX syntax via @babel/parser with jsx plugin.
    Returns: { "valid": bool, "error"?: str, "line"?: int }
    """
    script = f"""
const parser = require('@babel/parser');
try {{
    parser.parse({json.dumps(code)}, {{sourceType: 'module', plugins: ['jsx']}});
    process.stdout.write(JSON.stringify({{valid: true}}));
}} catch(err) {{
    process.stdout.write(JSON.stringify({{valid: false, error: err.message, line: err.loc ? err.loc.line : null}}));
}}
"""
    try:
        result = subprocess.run(
            ["node", "-e", script],
            capture_output=True, text=True, timeout=10
        )
        if result.returncode != 0 and not result.stdout:
            return {"valid": False, "error": result.stderr or "Node.js execution failed"}
        return json.loads(result.stdout)
    except FileNotFoundError:
        return {"valid": False, "error": "Node.js not found"}
    except Exception as e:
        return {"valid": False, "error": str(e)}
