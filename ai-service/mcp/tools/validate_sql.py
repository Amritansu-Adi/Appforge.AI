"""
ai-service/mcp/tools/validate_sql.py
Owner: Amritansu

Validates SQL schema by executing against an in-memory SQLite DB.
Uses Python stdlib sqlite3 — no subprocess needed.
"""
import sqlite3


def validate_sql_schema(sql: str) -> dict:
    """
    Execute SQL against in-memory SQLite to catch syntax/schema errors.
    Returns: { "valid": bool, "error"?: str }
    """
    try:
        conn = sqlite3.connect(":memory:")
        conn.executescript(sql)
        conn.close()
        return {"valid": True}
    except sqlite3.Error as e:
        return {"valid": False, "error": str(e)}
    except Exception as e:
        return {"valid": False, "error": f"Unexpected error: {str(e)}"}
