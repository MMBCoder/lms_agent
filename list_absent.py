import sqlite3

conn = sqlite3.connect("data/progress.db")

rows = conn.execute("""
SELECT
    lecture_id,
    title,
    lecture_url
FROM lectures
WHERE mandatory = 1
AND absent = 1
ORDER BY page_no
""").fetchall()

print(f"\nFound {len(rows)} mandatory absent lectures\n")

for i, row in enumerate(rows, start=1):

    lecture_id, title, url = row

    print("=" * 80)
    print(f"{i}. {title}")
    print(f"ID: {lecture_id}")
    print(f"URL: https://students.masaischool.com{url}")

conn.close()