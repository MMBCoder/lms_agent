import sqlite3

conn = sqlite3.connect("data/progress.db")

print("\nLECTURES")

count = conn.execute("""
SELECT COUNT(*)
FROM lectures
""").fetchone()[0]

print(count)

print("\nABSENT LECTURES")

rows = conn.execute("""
SELECT
    lecture_id,
    title
FROM lectures
WHERE absent = 1
ORDER BY lecture_id
""").fetchall()

for row in rows:
    print(row)

print("\nLECTURE_PROGRESS")

rows = conn.execute("""
SELECT *
FROM lecture_progress
""").fetchall()

print(rows)

print("\nPLAYBACK_PROGRESS")

rows = conn.execute("""
SELECT *
FROM playback_progress
""").fetchall()

print(rows)

conn.close()