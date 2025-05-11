import sqlite3
from typing import Optional

DATABASE = "users.db"

def init_db():
    with sqlite3.connect(DATABASE) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE,
                hashed_password BLOB
            )
        """)
        conn.commit()

def get_db():
    return sqlite3.connect(DATABASE, check_same_thread=False)

def get_user(username: str) -> Optional[sqlite3.Row]:
    conn = get_db()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    return cursor.fetchone()

def create_user(username: str, hashed_password: bytes):
    with get_db() as conn:
        conn.execute("INSERT INTO users (username, hashed_password) VALUES (?, ?)", (username, hashed_password))
        conn.commit()
