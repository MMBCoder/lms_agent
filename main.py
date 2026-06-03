import sqlite3
import time
from playwright.sync_api import sync_playwright

DB = "data/progress.db"
BASE_URL = "https://students.masaischool.com"

def init_db():
    """Ensure all required tables exist before starting the loop."""
    conn = sqlite3.connect(DB)
    conn.execute("""
    CREATE TABLE IF NOT EXISTS playback_progress (
        lecture_id TEXT PRIMARY KEY,
        title TEXT,
        current_time REAL,
        duration REAL,
        percent REAL,
        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)
    conn.execute("""
    CREATE TABLE IF NOT EXISTS lecture_progress (
        lecture_id TEXT PRIMARY KEY,
        started_at TEXT,
        finished_at TEXT,
        status TEXT
    )
    """)
    conn.execute("""
    CREATE TABLE IF NOT EXISTS lecture_summary (
        lecture_id TEXT PRIMARY KEY,
        title TEXT,
        summary TEXT,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)
    conn.execute("""
    CREATE TABLE IF NOT EXISTS processed_queue (
        lecture_id TEXT PRIMARY KEY,
        processed_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)
    conn.commit()
    conn.close()

def get_next_lecture():
    """Fetch the next mandatory and absent lecture that hasn't been processed yet."""
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
      AND l.mandatory = 1
      AND p.lecture_id IS NULL
    ORDER BY l.page_no, l.lecture_id
    LIMIT 1
    """).fetchone()  #
    conn.close()
    return row

def save_playback_progress(lecture_id, title, current_time, duration, percent):
    conn = sqlite3.connect(DB)
    conn.execute("""
    INSERT OR REPLACE INTO playback_progress
    (lecture_id, title, current_time, duration, percent)
    VALUES (?, ?, ?, ?, ?)
    """, (lecture_id, title, current_time, duration, percent))  #
    conn.commit()
    conn.close()

def mark_lecture_completed(lecture_id):
    conn = sqlite3.connect(DB)
    conn.execute("""
    INSERT OR REPLACE INTO lecture_progress
    (lecture_id, started_at, finished_at, status)
    VALUES (?, datetime('now'), datetime('now'), 'completed')
    """, (lecture_id,))  #
    conn.commit()
    conn.close()

def save_summary(lecture_id, title, summary):
    conn = sqlite3.connect(DB)
    conn.execute("""
    INSERT OR REPLACE INTO lecture_summary
    (lecture_id, title, summary)
    VALUES (?, ?, ?)
    """, (lecture_id, title, summary))  #
    conn.commit()
    conn.close()

def mark_processed(lecture_id):
    conn = sqlite3.connect(DB)
    conn.execute("""
    INSERT OR REPLACE INTO processed_queue (lecture_id)
    VALUES (?)
    """, (lecture_id,))  #
    conn.commit()
    conn.close()

def clean_summary(text):
    start = text.find("Overview")
    end = text.find("Happy with the content?")
    if start != -1 and end != -1:
        return text[start:end].strip()
    return text  #

def main():
    init_db()
    
    with sync_playwright() as p:
        # Launch persistent context to maintain login session
        browser = p.chromium.launch_persistent_context(
            user_data_dir="./browser_profile",
            headless=False
        )  #

        while True:
            lecture = get_next_lecture()
            
            if not lecture:
                print("\n🎉 All mandatory and absent lectures have been fully processed!")
                break

            lecture_id, title, lecture_url = lecture
            
            print(f"\n{'='*80}")
            print(f"Processing Lecture: {title}")
            print(f"ID: {lecture_id}")
            print(f"{'='*80}")

            page = browser.new_page()
            
            try:
                page.goto(BASE_URL + lecture_url)
                
                # Wait for video element to load
                page.wait_for_selector("video", timeout=60000)  #
                
                # Start video and force 2x speed
                page.evaluate("""
                () => {
                    const v = document.querySelector('video');
                    if(v) {
                        v.playbackRate = 2.0;
                        v.play();
                    }
                }
                """)  #
                
                print("▶ Video Playback started at 2x speed...")

                # Monitor video progress loop
                while True:
                    stats = page.evaluate("""
                    () => {
                        const v = document.querySelector('video');
                        if (!v) return null;
                        return {
                            currentTime: v.currentTime,
                            duration: v.duration,
                            paused: v.paused,
                            ended: v.ended,
                            percent: v.duration > 0 ? (v.currentTime / v.duration) * 100 : 0
                        };
                    }
                    """)  #

                    if not stats:
                        print("Lost track of video element.")
                        break

                    print(f"Progress: {stats['percent']:.2f}%")
                    save_playback_progress(lecture_id, title, stats["currentTime"], stats["duration"], stats["percent"])

                    if stats["ended"]:
                        mark_lecture_completed(lecture_id)
                        print("✅ Video playback completed.")
                        break

                    time.sleep(30) # Poll every 30 seconds
                
                # Extract AI Summary
                print("Fetching AI Summary...")
                try:
                    page.get_by_role("tab", name="AI Summary").click(timeout=10000)
                    page.wait_for_timeout(8000)
                    summary_text = page.locator("body").inner_text()
                    summary_text = clean_summary(summary_text)
                    
                    save_summary(lecture_id, title, summary_text)
                    print("✅ Summary extracted and saved.")
                except Exception as e:
                    print(f"⚠️ Could not extract AI Summary: {e}")

                # Mark as entirely processed so the loop moves to the next video
                mark_processed(lecture_id)

            except Exception as e:
                print(f"Error processing lecture {lecture_id}: {e}")
            finally:
                page.close() # Close tab to clear memory before moving to next lecture

        browser.close()

if __name__ == "__main__":
    main()