from playwright.sync_api import sync_playwright
import sqlite3
from datetime import datetime

BASE_URL = "https://students.masaischool.com"

conn = sqlite3.connect("data/progress.db")

row = conn.execute("""
SELECT
    lecture_id,
    title,
    lecture_url
FROM lectures
WHERE mandatory = 1
AND absent = 1
ORDER BY page_no
LIMIT 1
""").fetchone()

conn.close()

if not row:
    print("No lectures found")
    exit()

lecture_id, title, lecture_url = row

url = BASE_URL + lecture_url

print(f"Opening: {title}")
print(url)

with sync_playwright() as p:

    browser = p.chromium.launch_persistent_context(
        user_data_dir="./browser_profile",
        headless=False
    )

    page = browser.new_page()

    page.goto(url)

    page.wait_for_selector("video", timeout=60000)

    info = page.evaluate("""
    () => {
        const v = document.querySelector('video');

        return {
            duration: v.duration,
            currentTime: v.currentTime,
            paused: v.paused,
            playbackRate: v.playbackRate
        }
    }
    """)

    print("\nVideo Info")
    print(info)

    input("\nPress Enter to close")

    browser.close()