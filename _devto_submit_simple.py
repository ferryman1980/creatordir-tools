
import asyncio
from playwright.async_api import async_playwright
import sys
sys.stdout.reconfigure(encoding="utf-8")

EMAIL = "346010735@qq.com"
PASS = "Ckyhy388"

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp("http://127.0.0.1:9222", timeout=30000)
        page = browser.contexts[0].pages[0]
        
        # Fresh load
        await page.goto("https://dev.to/users/sign_up", timeout=15000, wait_until="domcontentloaded")
        await page.wait_for_timeout(2000)
        
        # Fill using query_selector (these should work since inputs are visible)
        email_el = await page.query_selector("[name='user[email]']")
        pass_el = await page.query_selector("[name='user[password]']")
        btn = await page.query_selector("[name='commit']")
        
        if email_el and pass_el and btn:
            await email_el.fill(EMAIL)
            print("Email filled!")
            await pass_el.fill(PASS)
            print("Password filled!")
            
            # Get button value
            val = await btn.get_attribute("value") or "Submit"
            print(f"Submit button: {val}")
            
            # Click
            await btn.click(timeout=5000)
            await page.wait_for_timeout(3000)
            print(f"URL: {page.url[:60]}")
            
            # Check result
            text = (await page.evaluate("document.body.innerText") or "")[:300]
            print(f"Result: {text[:200]}")
        else:
            print(f"Elements found: email={email_el is not None}, pass={pass_el is not None}, btn={btn is not None}")
        
        await browser.close()
        print("\n=== DONE ===")

asyncio.run(main())
