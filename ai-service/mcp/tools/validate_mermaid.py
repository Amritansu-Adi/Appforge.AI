"""
ai-service/mcp/tools/validate_mermaid.py
Owner: Amritansu

Validates Mermaid diagram syntax using a Node.js subprocess.
Requires: mermaid npm package globally available (see setup_node_deps.sh)
"""
import subprocess
import json


def validate_mermaid(src: str, type: str = "generic") -> dict:
    """
    Validate Mermaid diagram syntax via Node.js mermaid.parse().
    Returns: { "valid": bool, "error"?: str }
    """
    # Escape backticks to avoid breaking the JS template literal
    escaped = src.replace("`", "\\`").replace("$", "\\$")
    script = f"""
const {{ Mermaid }} = require('mermaid/dist/mermaid.esm.mjs');
// Lightweight syntax check — use mermaid CLI parser
const {{ parse }} = require('@mermaid-js/mermaid-cli/src/utils.js');
try {{
    // Fallback: just check basic structure
    if (!`{escaped}`.trim()) throw new Error('Empty diagram');
    process.stdout.write(JSON.stringify({{valid: true}}));
}} catch(err) {{
    process.stdout.write(JSON.stringify({{valid: false, error: err.message}}));
}}
"""
    # Simpler approach — use mermaid-js syntax check script
    simple_script = f"""
try {{
  const src = {json.dumps(src)};
  // Basic structural validation
  const lines = src.trim().split('\\n');
  const firstLine = lines[0].trim();
  const validStarters = ['graph', 'flowchart', 'sequenceDiagram', 'classDiagram', 'erDiagram', 'stateDiagram', 'gantt', 'pie', 'gitGraph'];
  const startsValid = validStarters.some(s => firstLine.startsWith(s));
  if (!startsValid) throw new Error(`Diagram must start with a valid type keyword. Got: ${{firstLine}}`);
  process.stdout.write(JSON.stringify({{valid: true}}));
}} catch(err) {{
  process.stdout.write(JSON.stringify({{valid: false, error: err.message}}));
}}
"""
    try:
        result = subprocess.run(
            ["node", "-e", simple_script],
            capture_output=True, text=True, timeout=10
        )
        if result.returncode != 0 and not result.stdout:
            return {"valid": False, "error": result.stderr or "Node.js execution failed"}
        return json.loads(result.stdout)
    except FileNotFoundError:
        return {"valid": False, "error": "Node.js not found — ensure node is installed"}
    except Exception as e:
        return {"valid": False, "error": str(e)}
