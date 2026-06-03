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

    links = page.locator("a")

    print("Total links:", links.count())

    for i in range(min(50, links.count())):
        try:
            text = links.nth(i).inner_text().strip()
            href = links.nth(i).get_attribute("href")

            if href:
                print(f"{i}: {text} -> {href}")

        except Exception:
            pass

    input("Press Enter...")