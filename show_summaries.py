import sqlite3

conn = sqlite3.connect(
    "data/progress.db"
)

rows = conn.execute("""
SELECT
    lecture_id,
    title
FROM lecture_summary
""").fetchall()

for row in rows:
    print(row)

conn.close()