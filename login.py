from playwright.sync_api import sync_playwright

with sync_playwright() as p:

    browser = p.chromium.launch_persistent_context(
        user_data_dir="./browser_profile",
        headless=False
    )

    page = browser.new_page()

    page.goto(
        "https://students.masaischool.com/learn?tab=lectures"
    )

    input("Login manually then press Enter")

    browser.close()
