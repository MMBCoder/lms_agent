import sqlite3

conn = sqlite3.connect("data/progress.db")

conn.execute("""
CREATE TABLE IF NOT EXISTS lecture_progress (
    lecture_id TEXT PRIMARY KEY,
    started_at TEXT,
    finished_at TEXT,
    status TEXT
)
""")

conn.commit()
conn.close()

print("lecture_progress table created")