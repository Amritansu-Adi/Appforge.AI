# API Contract — AppForge AI
> **Version:** 1.0 | **Authors:** Amritansu (backend) + Prateeksha (frontend consumer)
> All endpoints are prefixed `/api`. All protected routes require `Authorization: Bearer <JWT>`.
> All error responses follow `{ "error": "human readable message" }` with the correct HTTP status.

---

## Auth Routes — `/api/auth`

### POST `/api/auth/register`
**Auth:** None
**Request:**
```json
{ "email": "string (valid email)", "password": "string (min 8 chars)" }
```
**Success `201`:**
```json
{ "token": "string (JWT, 24h)", "user": { "id": "uuid", "email": "string" } }
```
**Errors:** `400` email invalid | `400` password too short | `409` email already registered

---

### POST `/api/auth/login`
**Auth:** None
**Request:**
```json
{ "email": "string", "password": "string" }
```
**Success `200`:**
```json
{ "token": "string (JWT, 24h)", "user": { "id": "uuid", "email": "string" } }
```
**Errors:** `400` missing fields | `401` invalid credentials

---

### POST `/api/auth/logout`
**Auth:** Required
**Request:** Empty body
**Success `200`:** `{ "message": "Logged out" }`

---

### GET `/api/auth/me`
**Auth:** Required
**Success `200`:**
```json
{ "id": "uuid", "email": "string", "created_at": "ISO datetime" }
```
**Errors:** `401` invalid/missing token

---

## Session Routes — `/api/session`

### POST `/api/session/create`
**Auth:** Required
**Request:** Empty body
**Success `201`:**
```json
{ "sessionId": "uuid", "status": "idea", "created_at": "ISO datetime" }
```
**Rate limit:** 10 per user per minute → `429`

---

### GET `/api/session/:id`
**Auth:** Required
**Success `200`:**
```json
{
  "id": "uuid",
  "user_id": "uuid",
  "status": "idea|overview|questions|diagrams|docs|codegen|complete",
  "idea_text": "string|null",
  "overview_json": "object|null",
  "complexity": "simple|standard|complex|null",
  "app_name": "string|null",
  "created_at": "ISO datetime",
  "updated_at": "ISO datetime"
}
```
**Errors:** `403` not owner | `404` not found

---

### GET `/api/session/list`
**Auth:** Required
**Success `200`:**
```json
[
  {
    "id": "uuid",
    "app_name": "string|null",
    "status": "string",
    "created_at": "ISO datetime",
    "updated_at": "ISO datetime"
  }
]
```

---

### PATCH `/api/session/:id/status`
**Auth:** Required
**Request:**
```json
{ "status": "idea|overview|questions|diagrams|docs|codegen|complete" }
```
**Success `200`:** `{ "updated": true }`
**Errors:** `400` invalid status | `403` not owner

---

### DELETE `/api/session/:id`
**Auth:** Required
**Success `200`:** `{ "deleted": true }`
**Note:** Cascades to questions, answers, diagrams, documents, generated_files, and langgraph_checkpoints for this thread_id.

---

## AI Routes — `/api/ai`

### POST `/api/ai/overview`
**Auth:** Required
**Request:**
```json
{ "sessionId": "uuid", "ideaText": "string (min 20 words)" }
```
**Success `200`:**
```json
{
  "appName": "string",
  "oneLiner": "string",
  "targetUsers": "string",
  "coreFeatures": ["string"],
  "complexity": "simple|standard|complex",
  "techNotes": "string",
  "dataEntities": ["string"]
}
```
**Errors:** `400` ideaText too short | `422` AI parser failed after retry | `403` not session owner

---

### POST `/api/ai/questions`
**Auth:** Required
**Request:**
```json
{ "sessionId": "uuid" }
```
**Success `200`:**
```json
[
  {
    "question_id": "q1",
    "category": "Users & Roles|Core Data|Workflow|UI/UX|Notifications|Integrations",
    "question": "string",
    "type": "text|choice",
    "options": ["string"] 
  }
]
```
**Note:** Array length = 8 (simple) | 12 (standard) | 16 (complex). `options` present only when `type === "choice"`.
**Errors:** `400` overview not yet generated | `403` not session owner

---

### POST `/api/ai/diagrams`
**Auth:** Required
**Request:**
```json
{ "sessionId": "uuid" }
```
**Success `200`:**
```json
{
  "useCaseDiagram": "string (Mermaid src)",
  "architectureDiagram": "string (Mermaid src)",
  "erDiagram": "string (Mermaid src)"
}
```
**Errors:** `400` questions not fully answered | `422` diagram generation failed after retries

---

### POST `/api/ai/srs`
**Auth:** Required
**Request:**
```json
{ "sessionId": "uuid" }
```
**Response:** `text/event-stream` SSE
```
data: {"type":"token","content":"chunk of markdown text"}
data: {"type":"done","filePath":"/generated/session-uuid/srs.docx"}
```

---

### POST `/api/ai/sdd`
**Auth:** Required
**Request:** `{ "sessionId": "uuid" }`
**Response:** SSE — same format as `/api/ai/srs`

---

### POST `/api/ai/brief`
**Auth:** Required
**Request:** `{ "sessionId": "uuid" }`
**Response:** SSE — token stream only, no .docx file produced
```
data: {"type":"token","content":"chunk"}
data: {"type":"done"}
```

---

## Answers Routes — `/api/answers`

### POST `/api/answers/save`
**Auth:** Required
**Request:**
```json
{ "sessionId": "uuid", "questionId": "q1", "answerText": "string (min 5 chars)" }
```
**Success `200`:** `{ "saved": true }`
**Note:** Upserts — re-saving an answer overwrites the previous one.
**Errors:** `400` answerText too short | `403` not session owner | `404` questionId not found for session

---

### GET `/api/answers/:sessionId`
**Auth:** Required
**Success `200`:**
```json
[
  { "question_id": "q1", "answer_text": "string", "answered_at": "ISO datetime" }
]
```

---

## Diagram Routes — `/api/diagram`

### GET `/api/diagram/:sessionId`
**Auth:** Required
**Success `200`:**
```json
[
  {
    "id": 1,
    "diagram_type": "usecase|architecture|er",
    "mermaid_src": "string",
    "approved": 0,
    "version": 1,
    "created_at": "ISO datetime"
  }
]
```

---

### POST `/api/diagram/approve/:id`
**Auth:** Required
**Request:** Empty body
**Success `200`:** `{ "approved": true }`
**Errors:** `403` not session owner | `404` diagram not found

---

### POST `/api/diagram/regenerate/:id`
**Auth:** Required
**Request:** Empty body
**Success `200`:**
```json
{
  "id": 1,
  "diagram_type": "string",
  "mermaid_src": "string (new Mermaid src)",
  "version": 2
}
```
**Note:** Increments version, resets `approved` to 0.

---

## Docs Routes — `/api/docs`

### GET `/api/docs/:sessionId/srs`
**Auth:** Required
**Response:** File download (`application/vnd.openxmlformats-officedocument.wordprocessingml.document`)
**Errors:** `404` doc not yet generated

---

### GET `/api/docs/:sessionId/sdd`
**Auth:** Required
**Response:** File download `.docx`

---

## Codegen Routes — `/api/codegen`

### POST `/api/codegen/start`
**Auth:** Required
**Request:**
```json
{ "sessionId": "uuid" }
```
**Response:** `text/event-stream` SSE
```
data: {"type":"step","step":"schema.sql","status":"generating|validating|validated|retrying|failed","message":"string"}
data: {"type":"step","step":"server/routes/task.js","status":"validated","message":"task.js ready ✓"}
data: {"type":"done","zipPath":"/generated/session-uuid/app.zip"}
```

---

### GET `/api/codegen/download/:sessionId`
**Auth:** Required
**Response:** File download (`application/zip`)
**Errors:** `404` zip not yet generated

---

*End of API Contract v1.0*