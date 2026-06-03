from adapters.custom_adapter import CustomAdapter

class MoodleAdapter(CustomAdapter):
    async def login(self, page):
        await page.goto('about:blank')

    async def get_courses(self, page):
        return []

    async def get_content(self, page, course_url):
        return []

    async def extract_transcript(self, page):
        return ''
