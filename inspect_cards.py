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

    titles = page.locator("h4")

    print("Found:", titles.count(), "h4 elements")

    for i in range(min(20, titles.count())):
        try:
            text = titles.nth(i).inner_text()
            print(i, "=>", text)
        except:
            pass

    input("Press Enter...")