import sqlite3

conn = sqlite3.connect(
    "data/progress.db"
)

conn.execute("""
CREATE TABLE IF NOT EXISTS playback_progress (
    lecture_id TEXT PRIMARY KEY,
    title TEXT,
    current_time REAL,
    duration REAL,
    percent REAL,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
)
""")

conn.commit()
conn.close()

print("Table created")