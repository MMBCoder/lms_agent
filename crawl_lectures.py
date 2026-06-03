from playwright.sync_api import sync_playwright
import csv

BASE_URL = (
    "https://students.masaischool.com/"
    "learn?tab=lectures&lectureTab=all&batch_id=199"
)

all_lectures = []

with sync_playwright() as p:

    browser = p.chromium.launch_persistent_context(
        user_data_dir="./browser_profile",
        headless=False
    )

    page = browser.new_page()

    page.goto(BASE_URL)

    page.wait_for_timeout(5000)

    TOTAL_PAGES = 12

    for page_no in range(1, TOTAL_PAGES + 1):

        print(f"\n{'='*80}")
        print(f"Processing Page {page_no}")
        print(f"{'='*80}")

        page.wait_for_timeout(3000)

        links = page.locator("a")

        page_lectures = 0

        for i in range(links.count()):

            try:

                text = links.nth(i).inner_text().strip()

                href = links.nth(i).get_attribute("href")

                if (
                    href
                    and "/lectures/" in href
                    and text
                ):

                    all_lectures.append({
                        "page": page_no,
                        "href": href,
                        "text": text
                    })

                    page_lectures += 1

            except Exception:
                pass

        print(
            f"Found {page_lectures} lectures on page {page_no}"
        )

        # Move to next page
        if page_no < TOTAL_PAGES:

            next_page = str(page_no + 1)

            print(
                f"Moving to page {next_page}"
            )

            pagination_links = page.locator(
                "a[rel='nofollow']"
            )

            found = False

            for j in range(pagination_links.count()):

                try:

                    txt = (
                        pagination_links
                        .nth(j)
                        .inner_text()
                        .strip()
                    )

                    if txt == next_page:

                        pagination_links.nth(j).click()

                        page.wait_for_timeout(5000)

                        found = True

                        break

                except Exception:
                    pass

            if not found:

                print(
                    f"Could not find page {next_page}"
                )

                break

    browser.close()

# Remove duplicates
unique = {}

for row in all_lectures:

    unique[row["href"]] = row

all_lectures = list(unique.values())

# Save CSV
with open(
    "all_lectures.csv",
    "w",
    newline="",
    encoding="utf-8"
) as f:

    writer = csv.DictWriter(
        f,
        fieldnames=[
            "page",
            "href",
            "text"
        ]
    )

    writer.writeheader()

    writer.writerows(all_lectures)

print("\n")
print("=" * 80)
print(f"Saved {len(all_lectures)} unique lectures")
print("Output file: all_lectures.csv")
print("=" * 80)