import asyncio
from playwright.browser_manager import BrowserManager
from database.database import Database

async def main():
    db = Database()
    db.initialize()

    browser_manager = BrowserManager(headless=True)
    await browser_manager.start()

    print('LMS Agent started successfully')

    await browser_manager.stop()

if __name__ == '__main__':
    asyncio.run(main())
