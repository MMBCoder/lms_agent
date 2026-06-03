import sqlite3

conn = sqlite3.connect("data/progress.db")

rows = conn.execute("""
SELECT
    lecture_id,
    title
FROM lectures
WHERE absent = 1
AND lecture_id NOT IN (
    SELECT lecture_id
    FROM processed_queue
)
ORDER BY lecture_id
""").fetchall()

print(f"\nRemaining: {len(rows)}\n")

for row in rows:
    print(row)

conn.close()