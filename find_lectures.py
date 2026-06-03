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

    lectures = []

    for i in range(links.count()):
        try:
            text = links.nth(i).inner_text().strip()
            href = links.nth(i).get_attribute("href")

            if href and "/lectures/" in href:
                lectures.append({
                    "href": href,
                    "text": text
                })

        except Exception:
            pass

    print(f"Found {len(lectures)} lecture links\n")

    for lecture in lectures:
        print("=" * 80)
        print(lecture["href"])
        print(lecture["text"])

    input("Press Enter...")