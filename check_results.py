import sqlite3

conn = sqlite3.connect("data/progress.db")

print("\nPROCESSED")

for row in conn.execute("""
SELECT * FROM processed_queue
"""):
    print(row)

print("\nSUMMARIES")

for row in conn.execute("""
SELECT lecture_id, title
FROM lecture_summary
"""):
    print(row)

conn.close()