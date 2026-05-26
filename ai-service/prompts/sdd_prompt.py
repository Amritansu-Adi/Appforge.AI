"""
ai-service/prompts/sdd_prompt.py
Owner: Prateeksha
Status: STUB — implement in Phase 5.1
"""
from langchain_core.prompts import ChatPromptTemplate

sdd_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are AppForge AI. Write a complete Software Design Document (SDD) in Markdown format."),
    ("human", "App: {app_name}\nSRS: {srs_markdown}\nOverview: {overview_json}"),
])
