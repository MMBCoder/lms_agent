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

    tabs = page.get_by_role("tab")

    print("Tabs Found:\n")

    for i in range(tabs.count()):

        try:
            print(
                i,
                tabs.nth(i).inner_text()
            )
        except:
            pass

    input("Press Enter")

    browser.close()