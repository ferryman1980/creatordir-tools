
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
        
        # === DEV.TO - Direct form submission ===
        print("=== DEV.TO DIRECT SUBMIT ===")
        await page.goto("https://dev.to/users/sign_up", timeout=15000, wait_until="domcontentloaded")
        await page.wait_for_timeout(2000)
        
        # Click "创建账户" to ensure we're on signup mode
        try:
            create_link = await page.query_selector("a:has-text('创建账户')")
            if create_link:
                print("Clicking '创建账户' link...")
                await create_link.click(timeout=5000)
                await page.wait_for_timeout(2000)
        except: pass
        
        # Fill email and password
        await page.fill("[name='user[email]']", EMAIL)
        print("Email filled")
        await page.fill("[name='user[password]']", PASS)
        print("Password filled")
        
        # Submit the form directly via JavaScript
        result = await page.evaluate("""
            () => {
                const form = document.querySelector("form");
                if (form) {
                    form.submit();
                    return "Form submitted!";
                }
                // Try clicking commit button
                const btn = document.querySelector("input[name='commit']");
                if (btn) {
                    btn.click();
                    return "Button clicked!";
                }
                return "No form or button found";
            }
        """)
        print(f"Submit result: {result}")
        await page.wait_for_timeout(3000)
        print(f"URL: {page.url[:60]}")
        
        # Check result
        text = (await page.evaluate("document.body.innerText") or "")[:300]
        print(f"Result: {text[:200]}")
        
        await browser.close()
        print("\n=== DONE ===")

asyncio.run(main())
