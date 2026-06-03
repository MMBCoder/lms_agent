import sqlite3

conn = sqlite3.connect("data/progress.db")

conn.execute("""
CREATE TABLE IF NOT EXISTS lecture_summary (
    lecture_id TEXT PRIMARY KEY,
    title TEXT,
    transcript TEXT,
    summary TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
)
""")

conn.commit()
conn.close()

print("lecture_summary created")