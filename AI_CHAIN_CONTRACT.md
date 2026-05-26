# AI Chain Contract — AppForge AI
> **Version:** 1.0 | **Authors:** Amritansu + Prateeksha (filled in Day 1-2 session)
> This file defines every LangChain chain's input type, output type, owner, and wiring points.
> **Neither contributor may change a chain's input/output signature without updating this file and notifying the other.**

---

## Chain: `overviewChain`

| Field | Value |
|-------|-------|
| **File** | `server/ai/chains/overviewChain.js` |
| **Owner** | Prateeksha |
| **Called by** | `overviewNode.js` (Amritansu) |
| **Prompt file** | `server/ai/prompts/overviewPrompt.js` (Prateeksha) |
| **Parser file** | `server/ai/parsers/overviewParser.js` (Prateeksha) |

**Input:**
```typescript
{
  ideaText: string,           // Raw user input, min 20 words
  formatInstructions: string  // From overviewParser.getFormatInstructions()
}
```

**Output:**
```typescript
{
  appName: string,          // Short app name, 2-4 words
  oneLiner: string,         // One sentence description
  targetUsers: string,      // Who will use the app
  coreFeatures: string[],   // Array of 4-6 feature strings
  complexity: "simple" | "standard" | "complex",
  techNotes: string,        // Any technical constraints detected
  dataEntities: string[]    // Array of entity names e.g. ["User","Task","Project"]
}
```

**Export:** `export const overviewChain` — a `RunnableSequence` invokable via `.invoke(input)`

---

## Chain: `questionsChain`

| Field | Value |
|-------|-------|
| **File** | `server/ai/chains/questionsChain.js` |
| **Owner** | Prateeksha |
| **Called by** | `questionsNode.js` (Amritansu) |
| **Prompt file** | `server/ai/prompts/questionsPrompt.js` (Prateeksha) |
| **Parser file** | `server/ai/parsers/questionsParser.js` (Prateeksha) |

**Input:**
```typescript
{
  overviewJson: string,   // JSON.stringify() of OverviewOutput above
  questionCount: number   // 8 | 12 | 16 based on complexity
}
```

**Output:**
```typescript
Array<{
  question_id: string,    // "q1", "q2", ... "q16"
  category: "Users & Roles" | "Core Data" | "Workflow" | "UI/UX" | "Notifications" | "Integrations",
  question: string,       // Display text shown to user
  type: "text" | "choice",
  options?: string[]      // Present only when type === "choice", 3-5 items
}>
```

**Export:** `export const questionsChain` — a `RunnableSequence` invokable via `.invoke(input)`

---

## Function: `streamDoc`

| Field | Value |
|-------|-------|
| **File** | `server/ai/chains/documentationChain.js` |
| **Owner** | Prateeksha |
| **Called by** | `docsNode.js` (Amritansu) |
| **Prompt files** | `srsPrompt.js`, `sddPrompt.js`, `briefPrompt.js` (all Prateeksha) |
| **Parser** | `StringOutputParser` — raw markdown streaming, no structured parse |

**Input:**
```typescript
{
  docType: "srs" | "sdd" | "brief",
  sessionContext: {
    appName: string,
    oneLiner: string,
    targetUsers: string,
    coreFeatures: string[],
    complexity: string,
    techNotes: string,
    dataEntities: string[],
    questions: Array<{ question_id: string, question: string }>,
    answers: Array<{ question_id: string, answer_text: string }>,
    diagrams: {
      useCaseDiagram: string,
      architectureDiagram: string,
      erDiagram: string
    }
  },
  onToken: (chunk: string) => void,   // Called per streamed token
  onComplete: (fullText: string) => void  // Called when stream ends
}
```

**Output:** `void` — all data delivered via callbacks

**Export:** `export async function streamDoc(input)`

---

## Function: `generateDiagrams`

| Field | Value |
|-------|-------|
| **File** | `server/ai/chains/diagramChain.js` |
| **Owner** | Amritansu |
| **Called by** | `diagramsNode.js` (Amritansu) |
| **Prompt file** | `server/ai/prompts/diagramsPrompt.js` (Prateeksha writes prompt) |
| **Parser file** | `server/ai/parsers/diagramsParser.js` (Amritansu) |
| **MCP tools used** | `validateMermaid` × 3 |

**Input:**
```typescript
{
  overviewJson: object,   // Full OverviewOutput object (not stringified)
  answers: Array<{ question_id: string, answer_text: string }>
}
```

**Output:**
```typescript
{
  useCaseDiagram: string,       // Valid Mermaid string
  architectureDiagram: string,  // Valid Mermaid string
  erDiagram: string             // Valid Mermaid string
}
```

**Export:** `export async function generateDiagrams({ overviewJson, answers })`

**Self-correction:** Up to 2 retries. On failure, validation error is injected as `previousError` into the prompt.

---

## Function: `runCodegenChain`

| Field | Value |
|-------|-------|
| **File** | `server/ai/chains/codegenChain.js` |
| **Owner** | Amritansu |
| **Called by** | `codegenNode.js` (Amritansu) |
| **Prompt file** | `server/ai/prompts/codegenPrompts.js` (Prateeksha writes prompts) |
| **Parser file** | `server/ai/parsers/codegenParser.js` (Amritansu) |
| **MCP tools used** | `validateSQLSchema`, `validateJSSyntax`, `validateJSXSyntax` |

**Input:**
```typescript
{
  state: AppForgeState,   // Full LangGraph state object (see appforgeState.js)
  emit: (event: {
    type: "step",
    step: string,           // filename e.g. "schema.sql"
    status: "generating" | "validating" | "validated" | "retrying" | "failed",
    message: string
  }) => void
}
```

**Output:**
```typescript
Array<{
  path: string,     // Relative path in generated app e.g. "server/routes/task.js"
  content: string,  // Full file content as string
  source: "ai" | "template"
}>
```

**Export:** `export async function runCodegenChain({ state, emit })`

---

## MCP Client Interface

| Field | Value |
|-------|-------|
| **File** | `server/ai/mcp/mcpClient.js` |
| **Owner** | Amritansu |
| **Used by** | `diagramChain.js`, `codegenChain.js` |

**API:**
```typescript
mcpClient.callTool(
  name: "validateMermaid" | "validateJSSyntax" | "validateJSXSyntax" | "validateSQLSchema",
  args: object
): Promise<{ valid: boolean, error?: string, line?: number }>
```

---

## LangGraph Graph Interface

| Field | Value |
|-------|-------|
| **File** | `server/ai/graph/appforgeGraph.js` |
| **Owner** | Amritansu |
| **Export** | `compiledGraph` |

**Invocation pattern (used in every AI route):**
```javascript
import { compiledGraph } from "../ai/graph/appforgeGraph.js";

const result = await compiledGraph.invoke(
  { sessionId, userId, currentPhase: "overview", ideaText },
  { configurable: { thread_id: sessionId } }
);
// result is the full updated AppForgeState
```

**Checkpoint:** Every node invocation auto-checkpoints to `langgraph_checkpoints` table via `SqliteSaver`.

---

*End of AI Chain Contract v1.0*