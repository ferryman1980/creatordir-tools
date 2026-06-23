
import asyncio
from playwright.async_api import async_playwright
import sys
sys.stdout.reconfigure(encoding="utf-8")

EMAIL = "346010735@qq.com"
PASS = "Ckyhy388"

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp("http://127.0.0.1:9222", timeout=20000)
        page = browser.contexts[0].pages[0]
        
        # Try Awin publisher signup
        await page.goto("https://www.awin.com/gb/publisher/signup", timeout=20000, wait_until="domcontentloaded")
        await page.wait_for_timeout(3000)
        print(f"URL: {page.url[:60]}")
        print(f"Inputs: {await page.evaluate('document.querySelectorAll("input").length')}")
        
        text = (await page.evaluate("document.body.innerText") or "")[:500]
        print(f"Text: {text[:200]}")
        await browser.close()

asyncio.run(main())
