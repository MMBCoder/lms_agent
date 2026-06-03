import sqlite3

conn = sqlite3.connect(
    "data/progress.db"
)

count = conn.execute(
    """
    SELECT COUNT(*)
    FROM lectures
    """
).fetchone()[0]

print(
    f"Total lectures: {count}"
)

mandatory = conn.execute(
    """
    SELECT COUNT(*)
    FROM lectures
    WHERE mandatory = 1
    """
).fetchone()[0]

print(
    f"Mandatory lectures: {mandatory}"
)

absent = conn.execute(
    """
    SELECT COUNT(*)
    FROM lectures
    WHERE absent = 1
    """
).fetchone()[0]

print(
    f"Absent lectures: {absent}"
)

conn.close()