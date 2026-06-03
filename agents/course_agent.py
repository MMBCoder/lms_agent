class CourseAgent:
    async def discover_courses(self, page, adapter):
        return await adapter.get_courses(page)
