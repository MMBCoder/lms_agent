from playwright.sync_api import sync_playwright

URL = "https://students.masaischool.com/lectures/152501?tab=notes"

with sync_playwright() as p:

    browser = p.chromium.launch_persistent_context(
        user_data_dir="./browser_profile",
        headless=False
    )

    page = browser.new_page()

    page.goto(URL)

    page.wait_for_selector("video", timeout=60000)

    page.wait_for_timeout(10000)

    print(
        page.evaluate("""
        () => {
            const v = document.querySelector('video');

            return {
                duration: v.duration,
                currentTime: v.currentTime,
                readyState: v.readyState,
                paused: v.paused,
                src: v.currentSrc
            }
        }
        """)
    )

    input("Press Enter...")

    browser.close()
