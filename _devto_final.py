import asyncio, sys
sys.stdout.reconfigure(encoding="utf-8")
from playwright.async_api import async_playwright

EMAIL = "346010735@qq.com"
PASS = "Ckyhy388"

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp("http://127.0.0.1:9222", timeout=30000)
        page = browser.contexts[0].pages[0]
        
        # Try sign in first
        print("=== Trying sign in ===")
        await page.goto("https://dev.to/users/sign_in", timeout=15000, wait_until="domcontentloaded")
        await page.wait_for_timeout(2000)
        
        await page.fill("[name='user[email]']", EMAIL)
        await page.fill("[name='user[password]']", PASS)
        await page.click("[name='commit']")
        await page.wait_for_timeout(5000)
        
        url = page.url
        print(f"URL after sign in: {url[:60]}")
        
        if "sign_in" not in url and "enter" not in url:
            print("SIGN IN SUCCESS!")
            title = await page.title()
            print(f"Title: {title[:80]}")
        else:
            # Check error
            err = await page.evaluate("""() => {
                const e = document.querySelector('[role=alert], .alert, .error, .flash, .crayons-notice');
                return e ? e.innerText.substring(0, 200) : 'no error';
            }""")
            print(f"Error: {err}")
            
            # Try sign up
            print("=== Trying sign up ===")
            await page.goto("https://dev.to/users/sign_up", timeout=15000, wait_until="domcontentloaded")
            await page.wait_for_timeout(2000)
            
            await page.fill("[name='user[email]']", EMAIL)
            await page.fill("[name='user[password]']", PASS)
            await page.click("[name='commit']")
            await page.wait_for_timeout(5000)
            
            print(f"URL after sign up: {page.url[:60]}")
            text = await page.evaluate("document.body.innerText.substring(0, 300)")
            print(f"Result: {text[:200]}")
        
        await browser.close()

asyncio.run(main())
