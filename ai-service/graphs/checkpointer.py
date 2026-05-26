"""
ai-service/graphs/checkpointer.py
Owner: Amritansu

SqliteSaver singleton for LangGraph state persistence.

v4.0 Architecture:
  - LangGraph writes to its OWN file: data/langgraph.db
  - Node.js owns data/appforge.db exclusively
  - These are TWO SEPARATE database files. Python NEVER touches appforge.db.

check_same_thread=False is REQUIRED for FastAPI async context where
the same connection may be accessed from different threads via the executor.
"""

import sqlite3
import os
from pathlib import Path
from langgraph.checkpoint.sqlite import SqliteSaver

_LG_DB_PATH = os.environ.get("LG_DB_PATH", "./data/langgraph.db")

# Ensure data/ directory exists
Path(_LG_DB_PATH).parent.mkdir(parents=True, exist_ok=True)

# check_same_thread=False required for FastAPI async context
_conn = sqlite3.connect(_LG_DB_PATH, check_same_thread=False)

checkpointer = SqliteSaver(_conn)
