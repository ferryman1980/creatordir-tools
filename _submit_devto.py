
import asyncio
from playwright.async_api import async_playwright
import sys
sys.stdout.reconfigure(encoding="utf-8")

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp("http://127.0.0.1:9222", timeout=20000)
        page = browser.contexts[0].pages[0]
        
        await page.wait_for_timeout(1000)
        url = page.url
        print(f"Current: {url[:60]}")
        
        # Try clicking submit
        try:
            submit = await page.query_selector("input[name='commit'], button[type=submit], input[type=submit]")
            if submit:
                val = await submit.get_attribute("value") or "Submit"
                print(f"Submit button: {val}")
                await submit.click()
                await page.wait_for_timeout(3000)
                print(f"After submit URL: {page.url[:60]}")
        except Exception as e:
            print(f"Submit error: {str(e)[:40]}")
        
        text = (await page.evaluate("document.body.innerText") or "")[:300]
        print(f"Page text: {text[:200]}")
        
        await browser.close()

asyncio.run(main())
