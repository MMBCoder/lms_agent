from config.settings import LMS_USERNAME, LMS_PASSWORD

class LoginAgent:
    async def login(self, page, adapter):
        await adapter.login(page)
