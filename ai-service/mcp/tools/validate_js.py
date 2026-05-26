"""
ai-service/mcp/tools/validate_js.py
Owner: Amritansu

Validates JavaScript syntax using acorn via Node.js subprocess.
Requires: acorn npm package globally available (see setup_node_deps.sh)
"""
import subprocess
import json


def validate_js_syntax(code: str, filename: str = "unknown.js") -> dict:
    """
    Validate JS syntax via Node.js acorn.parse().
    Returns: { "valid": bool, "error"?: str, "line"?: int }
    """
    script = f"""
const acorn = require('acorn');
try {{
    acorn.parse({json.dumps(code)}, {{ecmaVersion: 2022, sourceType: 'module'}});
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
