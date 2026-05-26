# AI Chain Contract — AppForge AI Service
> **Version:** v4.0 | **Status:** Authoritative — any change requires both Amritansu + Prateeksha to approve.
> **Purpose:** Specifies every Python chain: its input/output types, owner, which graph node calls it, and which prompt/parser files it uses. The corresponding Node→Python HTTP contract is in `INTERNAL_API_CONTRACT.md`.

---

## Contract Rules
1. Input and output types below are the **law** — node files and router files consume exactly these shapes.
2. All chains are **async** and must be invoked with `await chain.ainvoke({...})` or iterated with `async for chunk in chain.astream({...})`.
3. All chains import `llm` from `ai_service.models.llm` (real) or `ai_service.models.llm_mock` (tests only).
4. No chain file imports from `graphs/`, `nodes/`, or `routers/` — chains are pure LCEL pipes.

---

## Chain 1: `overview_chain`
| Field | Value |
|-------|-------|
| **Owner** | Prateeksha |
| **File** | `ai_service/chains/overview_chain.py` |
| **Phase** | 2.3 (build) → 2.4 (wired into node) |
| **Called by** | `ai_service/nodes/overview_node.py` → `overview_graph` |
| **Prompt file** | `ai_service/prompts/overview_prompt.py` → `overview_prompt` |
| **Parser file** | `ai_service/parsers/overview_parser.py` → `overview_parser` |
| **LCEL pipe** | `overview_prompt \| llm \| overview_parser` |

### Input
```python
{
    "idea_text": str,              # Raw user idea — min 20 words
    "format_instructions": str,    # From overview_parser.get_format_instructions()
}
```
### Output
```python
# OverviewOutput — Pydantic model instance (call .model_dump() to get dict)
OverviewOutput(
    app_name="TaskMaster Pro",          # str
    one_liner="A task app for teams.",  # str — max 20 words
    target_users=["Team leads", ...],   # list[str]
    core_features=["Create tasks", ...],# list[str] — min 3, max 8
    complexity="standard",              # Literal["simple", "standard", "complex"]
    tech_notes="Needs auth...",         # str
    data_entities=["User", "Task"],     # list[str]
)
```

---

## Chain 2: `questions_chain`
| Field | Value |
|-------|-------|
| **Owner** | Prateeksha |
| **File** | `ai_service/chains/questions_chain.py` |
| **Phase** | 3.1 (build) → 3.2 (wired into node) |
| **Called by** | `ai_service/nodes/questions_node.py` → `questions_graph` |
| **Prompt file** | `ai_service/prompts/questions_prompt.py` → `questions_prompt` |
| **Parser** | `JsonOutputParser()` inline — no separate parser file |
| **LCEL pipe** | `questions_prompt \| llm \| JsonOutputParser()` |

### Input
```python
{
    "overview_json": str,      # JSON.dumps() of OverviewOutput dict
    "question_count": int,     # 8 (simple) | 12 (standard) | 16 (complex)
}
```
### Output
```python
# list[dict] — each dict matches Question TypedDict
[
    {
        "question_id": "q1",                    # str — sequential
        "category": "Users & Roles",            # str — from category list
        "question": "What roles do you need?",  # str
        "type": "choice",                       # "text" | "choice"
        "options": ["Admin", "Member", "Guest"],# list[str] | None
    },
    # ... question_count items total
]
```
### Prompt requirements (for Prateeksha)
- Include one-shot example of a question JSON object
- Inject `{question_count}` for count control
- Category list: Users & Roles, Core Data, Workflows, UI & Design, Integrations, Constraints
- End with: "Respond ONLY with a raw JSON array. No markdown fences. No explanation."

---

## Chain 3: `stream_document` (documentation_chain)
| Field | Value |
|-------|-------|
| **Owner** | Prateeksha |
| **File** | `ai_service/chains/documentation_chain.py` |
| **Phase** | 5.1 (build) → 5.2 (wired into node + router) |
| **Called by** | `ai_service/nodes/docs_node.py` → `docs_graph` |
| **Prompt files** | `srs_prompt.py`, `sdd_prompt.py`, `brief_prompt.py` |
| **Parser** | `StrOutputParser()` inline |
| **Pattern** | async generator — NOT a simple chain.ainvoke() |

### Function signature
```python
async def stream_document(
    doc_type: Literal["srs", "sdd", "brief"],
    session_context: dict,
) -> AsyncGenerator[tuple[str, str], None]:
    """
    Yields: ("token", "<text_chunk>")  — for each streamed token
            ("done",  "<full_text>")   — once, at the end
    """
```
### `session_context` input shape
```python
{
    "app_name": str,
    "idea_text": str,
    "overview_json": dict,   # OverviewOutput dict
    "answers": list[dict],   # list of Answer dicts
    "diagrams": dict,        # DiagramSet dict (srs/sdd only; None for brief)
}
```
### SSE event format (emitted by docs_router.py)
```
data: {"type": "token", "text": "<chunk>"}\n\n
data: {"type": "done", "full_text": "<accumulated markdown>"}\n\n
```

---

## Chain 4: `generate_diagrams` (diagram_chain)
| Field | Value |
|-------|-------|
| **Owner** | Amritansu |
| **File** | `ai_service/chains/diagram_chain.py` |
| **Phase** | 4.2 (prompt by Prateeksha) → 4.3 (chain + MCP loop by Amritansu) |
| **Called by** | `ai_service/nodes/diagrams_node.py` → `diagrams_graph` |
| **Prompt file** | `ai_service/prompts/diagrams_prompt.py` → `diagrams_prompt` |
| **Parser** | `JsonOutputParser()` inline |
| **MCP tools used** | `validate_mermaid` × 3 (one per diagram type) |

### Function signature
```python
async def generate_diagrams(overview_json: dict, answers: list[dict]) -> dict:
    """
    Returns DiagramSet dict. Raises ValueError after MAX_RETRIES=2 failures.
    """
```
### Output
```python
{
    "use_case_diagram": "flowchart TD\n    ...",     # str — Mermaid source
    "architecture_diagram": "graph LR\n    ...",    # str — Mermaid source
    "er_diagram": "erDiagram\n    ...",              # str — Mermaid source
}
```
### Self-correction loop (Amritansu implements)
```
attempt 1: chain.ainvoke({"overview_json": ..., "answers_json": ..., "previous_errors": ""})
           → validate all 3 with mcp_client.call_tool("validate_mermaid", ...)
           → if all valid: return DiagramSet
attempt 2: if any invalid: chain.ainvoke(..., "previous_errors": "<error list>")
           → validate again
attempt 3: raise ValueError("Diagram generation failed after 2 retries")
```

---

## Chain 5: `run_codegen_chain` (codegen_chain)
| Field | Value |
|-------|-------|
| **Owner** | Amritansu |
| **File** | `ai_service/codegen/codegen_chain.py` |
| **Phase** | 6.1 (prompts by Prateeksha) → 6.2 (chain by Amritansu) |
| **Called by** | `ai_service/nodes/codegen_node.py` → `codegen_graph` |
| **Prompt file** | `ai_service/prompts/codegen_prompts.py` → 6 named ChatPromptTemplate instances |
| **MCP tools used** | `validate_sql_schema`, `validate_js_syntax`, `validate_jsx_syntax` |
| **Output delivery** | zip_base64 in AppForgeState (no shared filesystem) |

### 6 Sub-steps (sequential)
```
1. schema.sql     → validate_sql_schema     → self-correct ≤2
2. server/index.js → validate_js_syntax     → self-correct ≤2
3. server/routes/*.js → validate_js_syntax  → self-correct ≤2 per file
4. client/src/App.jsx → validate_jsx_syntax → self-correct ≤2
5. client/src/pages/*.jsx → validate_jsx_syntax → self-correct ≤2 per file
6. DEPLOYMENT.md  → no validation needed
```

### SSE events (emitted by codegen_router.py during generation)
```json
{"step": "schema.sql", "status": "generating"}
{"step": "schema.sql", "status": "validated"}
{"step": "schema.sql", "status": "failed", "error": "near syntax error"}
{"step": "zip", "status": "packaging"}
{"step": "zip", "status": "done", "zip_base64": "<base64 string>"}
```

---

## Prompt File Ownership Summary
| File | Owner | Used by Chain |
|------|-------|---------------|
| `prompts/overview_prompt.py` | Prateeksha | overview_chain |
| `prompts/questions_prompt.py` | Prateeksha | questions_chain |
| `prompts/diagrams_prompt.py` | Prateeksha | diagram_chain (Amritansu wires) |
| `prompts/srs_prompt.py` | Prateeksha | stream_document |
| `prompts/sdd_prompt.py` | Prateeksha | stream_document |
| `prompts/brief_prompt.py` | Prateeksha | stream_document |
| `prompts/codegen_prompts.py` | Prateeksha | codegen_chain (Amritansu wires) — 6 templates |

## Parser File Ownership Summary
| File | Owner | Used by Chain |
|------|-------|---------------|
| `parsers/overview_parser.py` | Prateeksha | overview_chain |
| `parsers/questions_parser.py` | Prateeksha | questions_chain (JsonOutputParser — no file needed) |
