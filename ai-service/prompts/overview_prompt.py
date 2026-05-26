"""
ai-service/prompts/overview_prompt.py
Owner: Prateeksha
Status: STUB — implement in Phase 2.3

Build a ChatPromptTemplate.from_messages() with:
- system message: instructs LLM to extract structured app info, includes {format_instructions}
- human message: "App idea: {idea_text}"
"""
from langchain_core.prompts import ChatPromptTemplate

# TODO Phase 2.3 (Prateeksha): Replace stub with full prompt
overview_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are AppForge AI. Extract structured app information.\n\n{format_instructions}\n\nRespond ONLY with valid JSON. No markdown fences."),
    ("human", "App idea: {idea_text}"),
])
