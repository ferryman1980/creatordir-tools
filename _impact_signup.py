
import asyncio
from playwright.async_api import async_playwright
import sys
sys.stdout.reconfigure(encoding="utf-8")

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp("http://127.0.0.1:9222", timeout=10000)
        page = browser.contexts[0].pages[0]
        
        await page.goto("https://app.impact.com/auth/signup", timeout=20000, wait_until="domcontentloaded")
        await page.wait_for_timeout(3000)
        print(f"URL: {page.url[:80]}")
        
        # Check for signup form
        inputs = await page.evaluate("document.querySelectorAll('input').length")
        print(f"Total inputs: {inputs}")
        
        # Get visible form fields
        fields = await page.evaluate("""
            () => Array.from(document.querySelectorAll("input:not([type=hidden])"))
                .filter(el => el.offsetParent !== null)
                .map(el => ({name: el.name, type: el.type, ph: el.placeholder, id: el.id}))
        """)
        print(f"Visible fields: {len(fields)}")
        for f in fields:
            print(f"  {f['name'] or f['ph']}: type={f['type']}")
        
        await browser.close()

asyncio.run(main())
