from playwright.sync_api import sync_playwright
import sqlite3
import time

DB = "data/progress.db"
BASE_URL = "https://students.masaischool.com"


def get_next_lecture():

    conn = sqlite3.connect(DB)

    row = conn.execute("""
    SELECT
        l.lecture_id,
        l.title,
        l.lecture_url
    FROM lectures l
    LEFT JOIN processed_queue p
        ON l.lecture_id = p.lecture_id
    WHERE l.absent = 1
      AND p.lecture_id IS NULL
    ORDER BY l.lecture_id
    LIMIT 1
    """).fetchone()

    conn.close()

    return row


def save_playback_progress(
    lecture_id,
    title,
    current_time,
    duration,
    percent
):

    conn = sqlite3.connect(DB)

    conn.execute("""
    INSERT OR REPLACE INTO playback_progress
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
        current_time,
        duration,
        percent
    ))

    conn.commit()
    conn.close()


def save_summary(
    lecture_id,
    title,
    summary
):

    conn = sqlite3.connect(DB)

    conn.execute("""
    INSERT OR REPLACE INTO lecture_summary
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


def mark_processed(
    lecture_id
):

    conn = sqlite3.connect(DB)

    conn.execute("""
    INSERT OR REPLACE INTO processed_queue
    (
        lecture_id
    )
    VALUES
    (?)
    """,
    (lecture_id,)
    )

    conn.commit()
    conn.close()


lecture = get_next_lecture()

if not lecture:
    print("No lectures remaining.")
    exit()

lecture_id, title, lecture_url = lecture

print(f"\nProcessing: {title}")
print(f"Lecture ID: {lecture_id}")

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

    print("Playback started")

    while True:

        stats = page.evaluate("""
        () => {

            const v =
                document.querySelector('video');

            return {
                currentTime: v.currentTime,
                duration: v.duration,
                paused: v.paused,
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
            f"Progress: {stats['percent']:.2f}%"
        )

        save_playback_progress(
            lecture_id,
            title,
            stats["currentTime"],
            stats["duration"],
            stats["percent"]
        )

        if stats["ended"]:
            break

        time.sleep(60)

    print("\nPlayback completed.")

    page.get_by_role(
        "tab",
        name="AI Summary"
    ).click()

    page.wait_for_timeout(8000)

    summary_text = page.locator(
        "body"
    ).inner_text()

    save_summary(
        lecture_id,
        title,
        summary_text
    )

    mark_processed(
        lecture_id
    )

    browser.close()

print("\nSummary saved.")
print("Lecture marked as processed.")