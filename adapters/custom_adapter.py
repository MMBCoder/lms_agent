import yaml

from adapters.base_adapter import BaseLMSAdapter


class CustomAdapter(BaseLMSAdapter):

    def __init__(self, config_path="config/lms_config.yaml"):
        with open(config_path, "r", encoding="utf-8") as file:
            self.config = yaml.safe_load(file)

    async def login(self, page):
        login = self.config["login"]

        await page.fill(
            login["username_selector"],
            ""
        )

        await page.fill(
            login["password_selector"],
            ""
        )

        await page.click(
            login["submit_selector"]
        )

    async def get_courses(self, page):
        return []

    async def get_content(self, page, course_url):
        return []

    async def extract_transcript(self, page):
        return ""
