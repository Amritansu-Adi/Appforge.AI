"""
ai-service/prompts/codegen_prompts.py
Owner: Prateeksha
Status: STUB — implement in Phase 6.1

Must export 5 ChatPromptTemplate instances:
  schema_prompt, route_prompt, auth_prompt, page_prompt, component_prompt

CRITICAL: every system message must end with:
  "Output only the file contents. No explanation. No markdown fences. No preamble."
"""
from langchain_core.prompts import ChatPromptTemplate

_NO_PREAMBLE = "Output only the file contents. No explanation. No markdown fences. No preamble."

schema_prompt = ChatPromptTemplate.from_messages([
    ("system", f"You are AppForge AI. Generate a complete SQLite SQL schema file.\n{_NO_PREAMBLE}"),
    ("human", "Overview: {{overview_json}}\nSDD: {{sdd_markdown}}\nPrevious error: {{previous_error}}"),
])

route_prompt = ChatPromptTemplate.from_messages([
    ("system", f"You are AppForge AI. Generate an Express.js router file for the given entity.\n{_NO_PREAMBLE}"),
    ("human", "Entity: {{entity}}\nSchema SQL: {{schema_sql}}\nSDD: {{sdd_markdown}}\nPrevious error: {{previous_error}}"),
])

auth_prompt = ChatPromptTemplate.from_messages([
    ("system", f"You are AppForge AI. Generate Express.js auth middleware and routes.\n{_NO_PREAMBLE}"),
    ("human", "Overview: {{overview_json}}\nSchema SQL: {{schema_sql}}\nPrevious error: {{previous_error}}"),
])

page_prompt = ChatPromptTemplate.from_messages([
    ("system", f"You are AppForge AI. Generate a React page component using Tailwind CSS.\n{_NO_PREAMBLE}"),
    ("human", "Page: {{page_name}}\nOverview: {{overview_json}}\nPrevious error: {{previous_error}}"),
])

component_prompt = ChatPromptTemplate.from_messages([
    ("system", f"You are AppForge AI. Generate a shared React component using Tailwind CSS.\n{_NO_PREAMBLE}"),
    ("human", "Component: {{component_name}}\nContext: {{context}}\nPrevious error: {{previous_error}}"),
])
