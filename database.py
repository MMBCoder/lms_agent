import sqlite3
import os

os.makedirs("data", exist_ok=True)

conn = sqlite3.connect("data/progress.db")

conn.execute("""
CREATE TABLE IF NOT EXISTS processed (
    lecture_id TEXT PRIMARY KEY,
    title TEXT,
    processed_at DATETIME DEFAULT CURRENT_TIMESTAMP
)
""")

conn.commit()
conn.close()

print("Database initialized successfully.")
