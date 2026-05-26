"""
ai-service/prompts/diagrams_prompt.py
Owner: Prateeksha
Status: STUB — implement in Phase 4.2
Must produce JSON with keys: use_case_diagram, architecture_diagram, er_diagram
"""
from langchain_core.prompts import ChatPromptTemplate

diagrams_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are AppForge AI. Generate 3 Mermaid diagrams (use case, architecture, ER) for the app.\nReturn JSON with keys: use_case_diagram, architecture_diagram, er_diagram.\nNo markdown fences.\n{previous_error}"),
    ("human", "Overview: {overview_json}\nAnswers: {answers}"),
])
