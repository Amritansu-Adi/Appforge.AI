"""
ai-service/prompts/questions_prompt.py
Owner: Prateeksha
Status: STUB — implement in Phase 3.1
"""
from langchain_core.prompts import ChatPromptTemplate

questions_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are AppForge AI. Generate {question_count} clarifying questions for the given app overview.\nRespond ONLY with a raw JSON array. No markdown fences."),
    ("human", "App overview: {overview_json}"),
])
