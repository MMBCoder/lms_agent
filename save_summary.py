import sqlite3

def save_summary(
    lecture_id,
    title,
    summary
):

    conn = sqlite3.connect(
        "data/progress.db"
    )

    conn.execute("""
    INSERT OR REPLACE
    INTO lecture_summary
    (
        lecture_id,
        title,
        summary
    )
    VALUES
    (
        ?, ?, ?
    )
    """,
    (
        lecture_id,
        title,
        summary
    ))

    conn.commit()
    conn.close()