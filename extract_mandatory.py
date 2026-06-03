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

            if not href:
                continue

            if "/lectures/" not in href:
                continue

            if not text:
                continue

            lectures.append({
                "href": href,
                "text": text
            })

        except:
            pass

    print("\nMANDATORY LECTURES\n")

    for lecture in lectures:

        if (
            "Mandatory" in lecture["text"]
        ):

            print("=" * 80)
            print(lecture["href"])
            print(lecture["text"])

    input("Press Enter...")