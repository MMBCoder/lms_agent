import csv
import sqlite3
import re

conn = sqlite3.connect("data/progress.db")

conn.execute("""
CREATE TABLE IF NOT EXISTS lectures (
    lecture_id TEXT PRIMARY KEY,
    page_no INTEGER,
    title TEXT,
    lecture_url TEXT,
    mandatory INTEGER,
    absent INTEGER,
    present INTEGER
)
""")

with open(
    "all_lectures.csv",
    encoding="utf-8"
) as f:

    reader = csv.DictReader(f)

    for row in reader:

        href = row["href"]

        match = re.search(
            r"/lectures/(\d+)",
            href
        )

        lecture_id = (
            match.group(1)
            if match
            else None
        )

        text = row["text"]

        title = (
            text.split("\n")[0]
            if text
            else ""
        )

        mandatory = (
            1 if "Mandatory" in text else 0
        )

        absent = (
            1 if "Absent" in text else 0
        )

        present = (
            1 if "Present" in text else 0
        )

        conn.execute(
            """
            INSERT OR REPLACE
            INTO lectures
            VALUES
            (
                ?, ?, ?, ?, ?, ?, ?
            )
            """,
            (
                lecture_id,
                row["page"],
                title,
                href,
                mandatory,
                absent,
                present
            )
        )

conn.commit()
conn.close()

print(
    "Inventory database created."
)