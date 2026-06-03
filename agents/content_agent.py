class ContentAgent:
    async def discover_content(self, page, adapter, course_url):
        return await adapter.get_content(page, course_url)
