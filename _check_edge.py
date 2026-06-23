
import asyncio
from playwright.async_api import async_playwright
import sys
sys.stdout.reconfigure(encoding="utf-8")

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp("http://127.0.0.1:9222", timeout=20000)
        pages = browser.contexts[0].pages
        print(f"Edge pages: {len(pages)}")
        for i, pg in enumerate(pages):
            try:
                print(f"  {i+1}. {pg.url[:70]}")
            except:
                print(f"  {i+1}. <error>")
        await browser.close()

asyncio.run(main())
