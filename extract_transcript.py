from playwright.sync_api import sync_playwright

URL = "https://students.masaischool.com/lectures/138358"

with sync_playwright() as p:

    browser = p.chromium.launch_persistent_context(
        user_data_dir="./browser_profile",
        headless=False
    )

    page = browser.new_page()

    page.goto(URL)

    page.wait_for_timeout(8000)

    try:
        page.get_by_text("Transcript", exact=True).click()
        page.wait_for_timeout(5000)

        print("\nTranscript tab clicked\n")

    except Exception as e:
        print("Could not click Transcript:", e)

    body = page.locator("body").inner_text()

    print(body[:10000])

    input("Press Enter")

    browser.close()