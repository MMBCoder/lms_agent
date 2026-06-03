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

    print("Links containing page numbers:\n")

    for i in range(links.count()):

        try:

            text = links.nth(i).inner_text().strip()

            href = links.nth(i).get_attribute("href")

            if text in [
                "1","2","3","4","5",
                "6","7","8","9","10",
                "11","12"
            ]:
                print(
                    f"{text} -> {href}"
                )

        except:
            pass

    input("Press Enter...")