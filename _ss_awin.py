import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp("http://127.0.0.1:9222", timeout=30000)
        page = browser.contexts[0].pages[1]
        await page.screenshot(path="awin_page.png", full_page=True)
        print("Screenshot saved")

asyncio.run(main())
