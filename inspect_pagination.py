from playwright.sync_api import sync_playwright

URL = "https://students.masaischool.com/learn?tab=lectures&lectureTab=all&batch_id=199"

with sync_playwright() as p:

    browser = p.chromium.launch_persistent_context(
        user_data_dir="./browser_profile",
        headless=False
    )

    page = browser.new_page()

    page.goto(URL)

    page.wait_for_timeout(10000)

    page.evaluate("""
    window.scrollTo(0, document.body.scrollHeight)
    """)

    page.wait_for_timeout(3000)

    print("Current URL:")
    print(page.url)

    print("\nBottom Text:\n")

    body = page.locator("body").inner_text()

    print(body[-3000:])

    input("Press Enter...")