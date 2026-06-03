from playwright.sync_api import sync_playwright
import time

URL = "https://students.masaischool.com/lectures/138360"

with sync_playwright() as p:

    browser = p.chromium.launch_persistent_context(
        user_data_dir="./browser_profile",
        headless=False
    )

    page = browser.new_page()

    page.goto(URL)

    page.wait_for_selector("video")

    page.evaluate("""
    () => {
        const v = document.querySelector('video');

        v.playbackRate = 2;
        v.play();
    }
    """)

    print("Monitoring video...\n")

    for _ in range(10):

        stats = page.evaluate("""
        () => {
            const v = document.querySelector('video');

            return {
                currentTime: v.currentTime,
                duration: v.duration,
                paused: v.paused,
                playbackRate: v.playbackRate,
                percent:
                    (
                        v.currentTime /
                        v.duration
                    ) * 100
            }
        }
        """)

        print(stats)

        time.sleep(10)

    input("Press Enter")

    browser.close()