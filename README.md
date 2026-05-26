# AppForge AI

> **AI-powered app builder for non-technical users** — go from a plain-English idea to a fully deployable codebase in five guided steps.

AppForge AI is a guided, multi-step web application that lets anyone — without writing a single line of code — turn an app idea into a working React + Node + SQLite project, complete with architecture diagrams, professional documentation, and a live deployment guide. 

**v3.0 Architecture Update:** The application relies on a robust microservice architecture. A **Node.js/Express** backend handles platform state, authentication, and database operations, acting as a secure proxy to a standalone **Python AI Service** powered by **FastAPI, LangChain, and LangGraph**.

---

## Table of Contents

- [AppForge AI](#appforge-ai)
  - [Table of Contents](#table-of-contents)
  - [Overview](#overview)
  - [Features](#features)
  - [The Five-Phase Pipeline](#the-five-phase-pipeline)
  - [Tech Stack](#tech-stack)
    - [AppForge Platform](#appforge-platform)
    - [Generated App Stack (Fixed)](#generated-app-stack-fixed)
  - [What You Can Build](#what-you-can-build)
    - [Supported App Types](#supported-app-types)
    - [Not Supported](#not-supported)
  - [Project Structure](#project-structure)

---

## Overview

Non-technical founders, students, and small business owners have ideas for software but face an enormous communication gap with developers and development tools. AppForge fills the gap **upstream** — translating a human idea into complete technical artefacts before any code is written.

The system uses a sequential AI pipeline powered by **Groq (llama-3.3-70b)** with a **Google Gemini Flash 2.0** fallback. AI orchestration is managed via **LangGraph**, ensuring stateful, resumable generation of structured overviews, clarifying questions, architecture diagrams, full technical documentation, and ultimately a working codebase. Code and diagram syntax are validated mid-generation via a **Model Context Protocol (MCP)** server.

**100% free to run.** Every service, library, and tool is either open source or free-tier.

---

## Features

- **Zero tech vocabulary** — the user never sees words like API, schema, or endpoint.
- **Sequential approval gates** — nothing advances without the user confirming each step.
- **Python-powered AI Layer** — State-of-the-art orchestration using LangChain and LangGraph.
- **MCP Validation** — Diagrams (Mermaid.js) and code (JS/JSX/SQL) are validated via a local MCP server with self-correction loops before the user ever sees them.
- **Real document output** — Downloadable `.docx` SRS and SDD, plus a streamed Markdown project brief.
- **Live code generation** — React + Node + SQLite codebase generated file-by-file with Server-Sent Events (SSE) streaming progress.
- **Fully resumable sessions** — Checkpointed via LangGraph's `SqliteSaver` and synced with the Node.js backend; refresh the browser anytime and pick up exactly where you left off.

---

## The Five-Phase Pipeline

| Phase | Name | Input | Output | User Action |
|-------|------|-------|--------|-------------|
| 1 | Idea & Overview | Plain-text idea | Structured app overview + complexity tier | Review & confirm |
| 2 | Questions & Answers | App overview | 8–16 targeted Q&A | Answer all questions |
| 3 | Diagram Generation | All answers | 3 Mermaid.js diagrams | Approve or regenerate each |
| 4 | Documentation | Approved diagrams | SRS + SDD (`.docx`) + project brief | Download & approve |
| 5 | Code & Deploy | All docs + answers | Full codebase (`.zip`) + Deploy guide | One-click download |

---

## Tech Stack

### AppForge Platform

| Layer | Technology |
|-------|-----------|
| Frontend | React 18 + Vite 5 + Tailwind CSS 3 |
| Client State | Zustand (Auth) + TanStack Query v5 |
| Node.js Backend | Node.js 20 LTS + Express 4 (Auth, Session, API Proxy) |
| Platform Database | SQLite via `better-sqlite3` |
| **AI Service Backend** | **Python 3.11+ + FastAPI** |
| **AI Orchestration** | **LangChain + LangGraph (Python)** |
| **Output Validation** | **Pydantic v2 + FastMCP (Python SDK)** |
| AI (primary) | Groq API — `llama-3.3-70b` |
| AI (fallback) | Google Gemini Flash 2.0 |
| Tracing | LangSmith |
| Hosting | Render (free tier) |

### Generated App Stack (Fixed)

| Layer | Technology |
|-------|-----------|
| Frontend | React 18 + Vite + Tailwind CSS |
| Backend | Node.js 20 + Express 4 |
| Database | SQLite via `better-sqlite3` |
| Auth | JWT + bcrypt |

---

## What You Can Build

### Supported App Types

- Personal productivity tools (todo apps, habit trackers, journals)
- Small business tools (invoicing, inventory, appointment booking)
- Data collection tools (surveys, feedback forms, waiting lists)
- Admin dashboards with charts and filtering
- Internal tools (leave trackers, expense loggers, directories)

### Not Supported

- Real-time features (chat, live updates)
- Payment processing
- Mobile apps (iOS/Android)
- Complex AI/ML inside generated apps

---

## Project Structure

```text
appforge-ai/
├── client/                     # React frontend (Vite)
│   └── src/
│       ├── pages/              
│       ├── components/         
│       └── hooks/              
├── server/                     # Node.js backend (Express)
│   ├── routes/                 # Auth, Session, and AI Proxy routes
│   ├── middleware/             # aiProxy.js (JWT validation & internal forwarding)
│   └── db/                     
│       ├── schema.sql          # Full SQLite schema (includes langgraph_checkpoints)
│       └── database.js         # better-sqlite3 singleton
├── ai-service/                 # Python AI Microservice (FastAPI)
│   ├── main.py                 # FastAPI application and internal auth verification
│   ├── chains/                 # LangChain LCEL pipes (overview, codegen, etc.)
│   ├── graph/                  # LangGraph StateGraph (appforge_graph.py)
│   ├── mcp/                    # FastMCP server + Python validation tools
│   ├── prompts/                # ChatPromptTemplates
│   ├── parsers/                # Pydantic and JSON Output Parsers
│   └── routers/                # FastAPI internal endpoints (SSE streaming support)
├── .env.example
├── package.json                # Monorepo root (npm workspaces)
└── README.md

