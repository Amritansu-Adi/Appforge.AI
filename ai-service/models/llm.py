"""
ai-service/models/llm.py
Owner: Amritansu

Exports a single `llm` object: ChatGroq (primary) with ChatGoogleGenerativeAI
as automatic fallback on 429 / 5xx errors.

Usage in any chain:
    from ai_service.models.llm import llm
    chain = prompt | llm | parser
"""

import os
from langchain_groq import ChatGroq
from langchain_google_genai import ChatGoogleGenerativeAI

if not os.environ.get("GROQ_API_KEY"):
    print("⚠️  GROQ_API_KEY not set. LLM calls will fail unless using mock.")
if not os.environ.get("GEMINI_API_KEY"):
    print("⚠️  GEMINI_API_KEY not set. Fallback LLM unavailable.")

# ── Primary: Groq llama-3.3-70b ─────────────────────────────────────────
groq_model = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0.3,
    max_tokens=4096,
    api_key=os.environ.get("GROQ_API_KEY", ""),
)

# ── Fallback: Gemini Flash 2.0 ───────────────────────────────────────────
gemini_model = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    temperature=0.3,
    max_output_tokens=4096,
    google_api_key=os.environ.get("GEMINI_API_KEY", ""),
)

# `llm` fires Gemini automatically when Groq returns 429 or any retriable error
llm = groq_model.with_fallbacks([gemini_model])
