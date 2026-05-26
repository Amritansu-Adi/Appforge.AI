"""
ai-service/prompts/srs_prompt.py
Owner: Prateeksha
Status: STUB — implement in Phase 5.1
"""
from langchain_core.prompts import ChatPromptTemplate

srs_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are AppForge AI. Write a complete Software Requirements Specification (SRS) document in Markdown format."),
    ("human", "App: {app_name}\nOverview: {overview_json}\nDiagrams: {diagrams}\nAnswers: {answers}"),
])
