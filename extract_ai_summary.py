from playwright.sync_api import sync_playwright

def extract_ai_summary(
    lecture_url
):

    with sync_playwright() as p:

        browser = p.chromium.launch_persistent_context(
            user_data_dir="./browser_profile",
            headless=False
        )

        page = browser.new_page()

        page.goto(lecture_url)

        page.wait_for_timeout(8000)

        page.get_by_role(
            "tab",
            name="AI Summary"
        ).click()

        page.wait_for_timeout(8000)

        text = page.locator(
            "body"
        ).inner_text()

        browser.close()

        return text