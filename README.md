# AppForge AI

> **AI-powered app builder for non-technical users** — go from a plain-English idea to a fully deployable codebase in five guided steps.

AppForge AI is a guided, multi-step web application that lets anyone — without writing a single line of code — turn an app idea into a working React + Node + SQLite project, complete with architecture diagrams, professional documentation, and a live GitHub deployment.

---

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [The Five-Phase Pipeline](#the-five-phase-pipeline)
- [Tech Stack](#tech-stack)
- [What You Can Build](#what-you-can-build)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
- [Environment Variables](#environment-variables)
- [API Reference](#api-reference)
- [Deployment](#deployment)
- [Testing](#testing)
- [Known Limitations](#known-limitations)

---

## Overview

Non-technical founders, students, and small business owners have ideas for software but face an enormous communication gap with developers and development tools. AppForge fills the gap **upstream** — translating a human idea into complete technical artefacts before any code is written.

The system uses a sequential AI pipeline powered by **Groq (llama-3.3-70b)** with a **Google Gemini Flash** fallback to generate structured overviews, clarifying questions, architecture diagrams, full technical documentation, and ultimately a working codebase — all committed to a GitHub repository automatically.

**100% free to run.** Every service, library, and tool is either open source or free-tier.

---

## Features

- **Zero tech vocabulary** — the user never sees words like API, schema, or endpoint
- **Sequential approval gates** — nothing advances without the user confirming each step
- **AI with fallback** — Groq as primary LLM; Gemini Flash if rate-limited
- **Mermaid.js diagrams** — server-validated before the user ever sees them
- **Real document output** — downloadable `.docx` SRS and SDD, plus a streamed project brief
- **Live code generation** — React + Node + SQLite codebase generated file-by-file
- **GitHub + Render deployment** — one-click push to a live URL
- **Fully resumable sessions** — refresh the browser anytime, pick up exactly where you left off

---

## The Five-Phase Pipeline

| Phase | Name | Input | Output | User Action |
|-------|------|-------|--------|-------------|
| 1 | Idea & Overview | Plain-text idea | Structured app overview + complexity tier | Review & confirm |
| 2 | Questions & Answers | App overview | 8–16 targeted Q&A | Answer all questions |
| 3 | Diagram Generation | All answers | 3 Mermaid.js diagrams | Approve or regenerate each |
| 4 | Documentation | Approved diagrams | SRS + SDD (`.docx`) + project brief | Download & approve |
| 5 | Code & Deploy | All docs + answers | Full codebase + GitHub repo + live URL | One-click deploy |

Each phase makes exactly **one AI API call**. All calls are sequential — the next call only starts after the user approves the previous output. This keeps the system within Groq's free-tier rate limits (30 req/min) and makes every step debuggable in isolation.

---

## Tech Stack

### AppForge Platform

| Layer | Technology |
|-------|-----------|
| Frontend | React 18 + Vite 5 + Tailwind CSS 3 |
| State management | TanStack Query (React Query) v5 |
| Diagram rendering | Mermaid.js 10 |
| Backend | Node.js 20 LTS + Express 4 |
| Database | SQLite via `better-sqlite3` |
| AI (primary) | Groq API — `llama-3.3-70b` |
| AI (fallback) | Google Gemini Flash 2.0 |
| Document generation | `docx` npm package |
| Version control output | GitHub REST API v3 |
| Hosting | Render (free tier) |

### Generated App Stack (fixed — all users get this)

| Layer | Technology |
|-------|-----------|
| Frontend | React 18 + Vite + Tailwind CSS |
| Backend | Node.js 20 + Express 4 |
| Database | SQLite via `better-sqlite3` |
| Auth | JWT + bcrypt |
| File uploads | Multer (if required) |
| Deployment | Render free tier + Docker |

---

## What You Can Build

### Supported App Types

- Personal productivity tools (todo apps, habit trackers, journals)
- Small business tools (invoicing, inventory, appointment booking)
- Community platforms (forums, event boards, Q&A sites)
- Portfolio and CMS-style sites with admin panels
- Data collection tools (surveys, feedback forms, waiting lists)
- Simple e-commerce (catalogue + cart, no live payments)
- Admin dashboards with charts and filtering
- Education tools (quizzes, flashcard systems, course trackers)
- Booking and scheduling systems
- Internal tools (leave trackers, expense loggers, directories)

### Not Supported

| Feature | Reason |
|---------|--------|
| Real-time features (chat, live updates) | SQLite + REST doesn't support WebSockets natively |
| Payment processing | Requires domain verification, webhooks, compliance |
| Mobile apps (iOS/Android) | React Native is a separate codebase |
| AI/ML inside generated apps | Requires GPU resources not available on free tier |
| Email sending | SMTP/SendGrid setup must be done manually post-generation |
| Third-party OAuth (Google, GitHub login) | Requires OAuth app registration |
| Custom domains | Render free tier uses `.onrender.com` subdomain |

---

## Project Structure

```
appforge-ai/
├── client/                     # React frontend (Vite)
│   └── src/
│       ├── pages/              # One file per screen
│       ├── components/         # Reusable UI components
│       ├── hooks/              # useSession, useStream
│       └── api/                # API call wrappers
├── server/
│   ├── routes/                 # Express route handlers
│   ├── services/               # Business logic
│   │   ├── groqService.js      # Groq SDK wrapper + retry
│   │   ├── geminiService.js    # Gemini fallback
│   │   ├── promptBuilder.js    # All prompt templates
│   │   ├── docGenerator.js     # .docx generation
│   │   ├── codeGenerator.js    # Code file generation
│   │   └── githubService.js    # GitHub API wrapper
│   ├── db/
│   │   ├── schema.sql          # Full SQLite schema
│   │   └── migrate.js          # Migration runner
│   ├── templates/              # Base app scaffolds (not AI-generated)
│   └── prompts/                # LLM prompt text files
├── .env.example
├── package.json                # Monorepo root (npm workspaces)
└── README.md
```

---

## Getting Started

### Prerequisites

- Node.js v20+
- npm v9+
- Git

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/yourusername/appforge-ai.git
cd appforge-ai

# 2. Install all dependencies (client + server)
npm install

# 3. Set up environment variables
cp .env.example .env
# Edit .env and add your API keys (see Environment Variables below)

# 4. Run database migrations
npm run db:migrate

# 5. Start the development servers
npm run dev
```

The app will be available at `http://localhost:5173`. The API server runs on port `3001`.

---

## Environment Variables

| Variable | Required | Description | Where to get |
|----------|----------|-------------|--------------|
| `GROQ_API_KEY` | Yes | Primary LLM provider | [console.groq.com](https://console.groq.com) |
| `GEMINI_API_KEY` | Yes | Fallback LLM provider | [aistudio.google.com](https://aistudio.google.com) |
| `GITHUB_PAT` | Yes (Phase 5) | Personal Access Token with `repo` scope | GitHub Settings → Developer Settings |
| `RENDER_API_KEY` | Optional | Triggers Render deploys via API | [render.com/docs/api](https://render.com/docs/api) |
| `NODE_ENV` | Yes (prod) | Set to `production` on Render | Render dashboard |
| `PORT` | No | Express port — defaults to `3001` | Set automatically by Render |
| `DB_PATH` | No | SQLite file path — defaults to `./data/appforge.db` | Override for custom path |

---

## API Reference

### Session Management

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/session/create` | Create a new session, returns UUID |
| `GET` | `/api/session/:id` | Get complete session state |
| `GET` | `/api/session/list` | List all sessions (history page) |
| `PATCH` | `/api/session/:id/status` | Update session status |
| `DELETE` | `/api/session/:id` | Delete session and all related data |

### AI Pipeline

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/ai/overview` | Phase 1 — idea text → overview JSON |
| `POST` | `/api/ai/questions` | Phase 2 — overview → question array |
| `POST` | `/api/ai/diagrams` | Phase 3 — answers → Mermaid diagrams |
| `POST` | `/api/ai/srs` | Phase 4a — SRS document (SSE stream) |
| `POST` | `/api/ai/sdd` | Phase 4b — SDD document (SSE stream) |
| `POST` | `/api/ai/brief` | Phase 4c — project brief (SSE stream) |

### Documents & Code

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/docs/:sessionId/srs` | Download SRS `.docx` |
| `GET` | `/api/docs/:sessionId/sdd` | Download SDD `.docx` |
| `GET` | `/api/docs/:sessionId/brief` | Download project brief `.md` |
| `POST` | `/api/codegen/start` | Start Phase 5 — SSE stream of generation progress |
| `GET` | `/api/codegen/download/:sessionId` | Download generated app as `.zip` |
| `GET` | `/api/deploy/status/:sessionId` | Get GitHub repo URL and Render deploy status |

---

## Deployment

### Deploy to Render

1. Push all code to GitHub (`main` branch)
2. Log in at [render.com](https://render.com) → **New > Web Service**
3. Connect your GitHub repository
4. Set the following:
   - **Build command:** `npm install && cd client && npm run build`
   - **Start command:** `node server/index.js`
5. Add environment variables: `GROQ_API_KEY`, `GEMINI_API_KEY`, `GITHUB_PAT`, `NODE_ENV=production`
6. Deploy — Render provides a free `*.onrender.com` subdomain

> **Note:** The Render free tier spins down after 15 minutes of inactivity. The first request after a cold start takes ~30 seconds. This is expected for a free-tier deployment.

---

## Testing

| Test Type | Tool | What is Tested |
|-----------|------|----------------|
| Unit tests | Jest | Prompt builders, JSON parser, Markdown→docx mapper |
| Integration tests | Jest + Supertest | All API endpoints with mock AI responses |
| AI output tests | Custom runner | 5 fixed app ideas run through full pipeline — outputs checked for schema validity |
| Frontend component tests | Vitest + React Testing Library | QuestionCard, DiagramViewer, StepBar, BriefViewer |
| End-to-end tests | Manual (Playwright optional) | Full user journey: idea → deploy for 3 test apps |
| Syntax validation | Jest | Generated JS/JSX/SQL passes parsers for 10 sample outputs |

```bash
# Run all tests
npm test

# Run only unit tests
npm run test:unit

# Run integration tests
npm run test:integration
```

---

## Known Limitations

- **Groq free tier:** 30 requests/minute. A full session (all 5 phases) uses ~10 requests. Rate limits are handled automatically with a Gemini fallback — the user sees a loading spinner, not an error.
- **SQLite:** Suitable for demos and student-scale usage. Not suitable for production with concurrent users at scale.
- **GitHub PAT:** Uses a developer-owned Personal Access Token. In a production version, users would authenticate via GitHub OAuth.
- **Generated code quality:** Code is syntax-validated before commit but not functionally tested. Complex apps may require minor manual adjustments.
- **Render cold starts:** ~30 second delay after 15 minutes of inactivity on the free tier.

---

## References

- [Groq API Documentation](https://console.groq.com/docs/openai)
- [Google Gemini API](https://ai.google.dev/gemini-api/docs)
- [Mermaid.js Documentation](https://mermaid.js.org/intro/)
- [better-sqlite3](https://github.com/WiseLibs/better-sqlite3)
- [React 18 Documentation](https://react.dev)
- [Express.js Guide](https://expressjs.com/en/guide/routing.html)
- [docx npm package](https://docx.js.org)
- [Render Documentation](https://render.com/docs)
- [GitHub REST API](https://docs.github.com/en/rest)
- [TanStack Query](https://tanstack.com/query/latest)

---

*Student Final Year Project — AppForge AI v1.0 — 2025*
