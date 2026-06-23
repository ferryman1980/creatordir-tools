
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
        
        # Load Dev.to signup page fresh
        await page.goto("https://dev.to/users/sign_up", timeout=15000, wait_until="domcontentloaded")
        await page.wait_for_timeout(2000)
        
        # Don't click anything - just fill the already-visible form
        # Check what's visible
        inputs = await page.evaluate("""
            () => Array.from(document.querySelectorAll("input"))
                .filter(el => el.offsetParent !== null)
                .map(el => ({name: el.name, id: el.id, type: el.type}))
        """)
        print(f"Visible inputs: {inputs}")
        
        # Use evaluate to fill and submit directly
        result = await page.evaluate("""
            () => {
                const email = document.querySelector("[name='user[email]']");
                const pass = document.querySelector("[name='user[password]']");
                const btn = document.querySelector("[name='commit']");
                
                if (email && pass && btn) {
                    email.value = arguments[0];
                    pass.value = arguments[1];
                    // Trigger React onChange
                    email.dispatchEvent(new Event('input', {bubbles: true}));
                    email.dispatchEvent(new Event('change', {bubbles: true}));
                    pass.dispatchEvent(new Event('input', {bubbles: true}));
                    pass.dispatchEvent(new Event('change', {bubbles: true}));
                    btn.click();
                    return "Submitted!";
                }
                return "Form not found";
            }
        """, EMAIL, PASS)
        print(f"Result: {result}")
        await page.wait_for_timeout(3000)
        print(f"URL: {page.url[:60]}")
        
        text = (await page.evaluate("document.body.innerText") or "")[:300]
        print(f"Page: {text[:200]}")
        
        await browser.close()

asyncio.run(main())
