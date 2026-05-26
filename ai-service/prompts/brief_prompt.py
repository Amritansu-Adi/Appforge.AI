"""
ai-service/prompts/brief_prompt.py
Owner: Prateeksha
Status: STUB — implement in Phase 5.1
"""
from langchain_core.prompts import ChatPromptTemplate

brief_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are AppForge AI. Write a concise, plain-English project brief in Markdown. No jargon. Max 500 words."),
    ("human", "App: {app_name}\nOverview: {overview_json}"),
])
