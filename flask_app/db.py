import sqlite3
import os

DATABASE = os.path.join(os.path.dirname(__file__), 'campustocareer.db')

def get_db():
    """Return a SQLite connection. Rows accessible like dicts."""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn
