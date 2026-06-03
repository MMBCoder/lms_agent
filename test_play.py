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

    page.wait_for_timeout(30000)

    before = page.evaluate("""
    () => {
        const v = document.querySelector('video');
        return {
            paused: v.paused,
            currentTime: v.currentTime
        };
    }
    """)

    print("Before:", before)

    page.evaluate("""
    () => {
        const v = document.querySelector('video');
        if(v){
            v.play();
        }
    }
    """)

    page.wait_for_timeout(30000)

    after = page.evaluate("""
    () => {
        const v = document.querySelector('video');
        return {
            paused: v.paused,
            currentTime: v.currentTime
        };
    }
    """)

    print("After:", after)

    input("Press Enter to close")

    browser.close()
