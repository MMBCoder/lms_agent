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

    locator = page.get_by_text("2", exact=True)

    print("Count:", locator.count())

    for i in range(locator.count()):
        try:
            print(
                locator.nth(i).evaluate(
                    "(el) => el.outerHTML"
                )
            )
            print("-" * 100)

        except Exception as e:
            print(e)

    input("Press Enter...")