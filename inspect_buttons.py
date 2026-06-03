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

    buttons = page.locator("button")

    print("Total Buttons:", buttons.count())

    for i in range(buttons.count()):

        try:

            text = buttons.nth(i).inner_text()

            print(f"{i}: {repr(text)}")

        except Exception as e:

            print(f"{i}: ERROR")

    input("Press Enter...")