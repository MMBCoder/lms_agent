from playwright.sync_api import sync_playwright
import sqlite3
import time

DB = "data/progress.db"

BASE_URL = "https://students.masaischool.com"

conn = sqlite3.connect(DB)

row = conn.execute("""
SELECT
    lecture_id,
    title,
    lecture_url
FROM lectures
WHERE absent = 1
ORDER BY lecture_id
LIMIT 1
""").fetchone()

if not row:
    print("No absent lectures found")
    conn.close()
    exit()

lecture_id, title, lecture_url = row

print(f"\nLecture: {title}")
print(f"ID: {lecture_id}")

conn.close()

with sync_playwright() as p:

    browser = p.chromium.launch_persistent_context(
        user_data_dir="./browser_profile",
        headless=False
    )

    page = browser.new_page()

    page.goto(
        BASE_URL + lecture_url
    )

    page.wait_for_selector(
        "video",
        timeout=60000
    )

    page.evaluate("""
    () => {
        const v = document.querySelector('video');

        v.playbackRate = 2;

        v.play();
    }
    """)

    print("\nVideo Started")

    while True:

        stats = page.evaluate("""
        () => {

            const v =
                document.querySelector('video');

            return {
                currentTime: v.currentTime,
                duration: v.duration,
                paused: v.paused,
                playbackRate: v.playbackRate,
                ended: v.ended,
                percent:
                    (
                        v.currentTime /
                        v.duration
                    ) * 100
            };
        }
        """)

        print(
            f"{stats['percent']:.2f}%"
        )

        conn = sqlite3.connect(DB)

        conn.execute("""
        INSERT OR REPLACE
        INTO playback_progress
        (
            lecture_id,
            title,
            current_time,
            duration,
            percent
        )
        VALUES
        (
            ?, ?, ?, ?, ?
        )
        """,
        (
            lecture_id,
            title,
            stats["currentTime"],
            stats["duration"],
            stats["percent"]
        ))

        conn.commit()
        conn.close()

        if stats["ended"]:

            conn = sqlite3.connect(DB)

            conn.execute("""
            INSERT OR REPLACE
            INTO lecture_progress
            (
                lecture_id,
                started_at,
                finished_at,
                status
            )
            VALUES
            (
                ?,
                datetime('now'),
                datetime('now'),
                'completed'
            )
            """,
            (lecture_id,)
            )

            conn.commit()
            conn.close()

            print(
                "\nLecture Finished"
            )

            break

        time.sleep(60)

    browser.close()