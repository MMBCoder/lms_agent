import sqlite3

conn = sqlite3.connect("data/progress.db")

conn.execute("""
CREATE TABLE IF NOT EXISTS reviewed_lectures (
    lecture_id TEXT PRIMARY KEY,
    reviewed_at DATETIME DEFAULT CURRENT_TIMESTAMP
)
""")

conn.commit()
conn.close()

print("reviewed_lectures table created")