"""
ai-service/mcp/tools/validate_mermaid.py
Owner: Amritansu

v4.0 REWRITE: Replaced unreliable Node.js subprocess with a structural
Python regex check. Full semantic validation happens in the browser via
Mermaid.js — that is the correct architectural layer for it.

The previous implementation spawned a Node.js subprocess to run a mermaid
CLI parse. This was fragile (Node/npm not guaranteed in Python environment,
async subprocess issues). v4.0 fixes #1 from the revision log.

Tool signature matches mcp/client.py TOOL_MAP: validate_mermaid(src, diagram_type)
"""

import re

VALID_DIAGRAM_TYPES = [
    "flowchart",
    "graph",
    "erDiagram",
    "sequenceDiagram",
    "classDiagram",
    "stateDiagram-v2",
    "stateDiagram",
    "gantt",
    "pie",
    "gitGraph",
]


def validate_mermaid(src: str, diagram_type: str = "generic") -> dict:
    """
    Structural validation only — checks:
    1. Non-empty source
    2. Starts with a recognised Mermaid diagram type keyword
    3. Has at least 2 non-empty lines of content
    4. No unmatched double quotes (common LLM generation error)

    Returns: {"valid": bool, "error"?: str}
    """
    if not src or not src.strip():
        return {"valid": False, "error": "Empty diagram source"}

    lines = [line for line in src.strip().split("\n") if line.strip()]
    first_line = lines[0].strip()

    if not any(first_line.startswith(dt) for dt in VALID_DIAGRAM_TYPES):
        return {
            "valid": False,
            "error": (
                f"Diagram must start with a valid type keyword. "
                f"Got: '{first_line[:50]}'. "
                f"Expected one of: {', '.join(VALID_DIAGRAM_TYPES)}"
            ),
        }

    if len(lines) < 2:
        return {
            "valid": False,
            "error": "Diagram has no content — only a type declaration line",
        }

    # Count unescaped double quotes — odd count means unmatched pair (common LLM error)
    # Strip escaped quotes first, then count
    src_stripped = re.sub(r'\\"', "", src)
    if src_stripped.count('"') % 2 != 0:
        return {"valid": False, "error": "Unmatched double quotes in diagram source"}

    return {"valid": True}
