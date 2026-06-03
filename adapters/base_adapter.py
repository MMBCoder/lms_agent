from abc import ABC, abstractmethod


class BaseLMSAdapter(ABC):

    @abstractmethod
    async def login(self, page):
        pass

    @abstractmethod
    async def get_courses(self, page):
        pass

    @abstractmethod
    async def get_content(self, page, course_url):
        pass

    @abstractmethod
    async def extract_transcript(self, page):
        pass
