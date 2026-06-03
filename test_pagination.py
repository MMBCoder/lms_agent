from playwright.sync_api import sync_playwright

URL = "https://students.masaischool.com/learn?tab=lectures&lectureTab=all&batch_id=199"

with sync_playwright() as p:

    browser = p.chromium.launch_persistent_context(
        user_data_dir="./browser_profile",
        headless=False
    )

    page = browser.new_page()

    page.goto(URL)

    page.wait_for_timeout(5000)

    print("Before:")
    print(page.url)

    page.get_by_text("2", exact=True).click()

    page.wait_for_timeout(5000)

    print("\nAfter:")
    print(page.url)

    titles = page.locator("h4")

    print("\nVisible Lectures:\n")

    for i in range(min(10, titles.count())):

        try:
            print(
                titles.nth(i).inner_text()
            )
        except:
            pass

    input("Press Enter")

    browser.close()