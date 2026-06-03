import sqlite3

conn = sqlite3.connect(
    "data/progress.db"
)

processed = conn.execute("""
SELECT COUNT(*)
FROM processed_queue
""").fetchone()[0]

remaining = conn.execute("""
SELECT COUNT(*)
FROM lectures
WHERE absent = 1
AND lecture_id NOT IN
(
    SELECT lecture_id
    FROM processed_queue
)
""").fetchone()[0]

print(
    f"Processed: {processed}"
)

print(
    f"Remaining: {remaining}"
)

conn.close()