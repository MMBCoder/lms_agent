from playwright.sync_api import sync_playwright

URL = "https://students.masaischool.com/lectures/152501?tab=notes"

with sync_playwright() as p:

    browser = p.chromium.launch_persistent_context(
        user_data_dir="./browser_profile",
        headless=False
    )

    page = browser.new_page()

    page.goto(URL)

    page.wait_for_selector("video")

    page.wait_for_timeout(5000)

    page.evaluate("""
    () => {
    const v = document.querySelector('video');
    v.playbackRate = 2;
    v.play();
    }
    """)

    t1 = page.evaluate("""
    () => document.querySelector('video').currentTime
    """)

    page.wait_for_timeout(10000)

    t2 = page.evaluate("""
    () => document.querySelector('video').currentTime
    """)

    print("Time1:", t1)
    print("Time2:", t2)

    input("Press Enter")