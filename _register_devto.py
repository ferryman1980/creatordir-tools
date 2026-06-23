
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
        
        await page.goto("https://dev.to/enter", timeout=20000, wait_until="domcontentloaded")
        await page.wait_for_timeout(2000)
        
        # Click "创建账户" (Create Account) link
        try:
            create_btn = await page.query_selector("a:has-text('创建账户'), a:has-text('Create Account')")
            if create_btn:
                print("Clicking 'Create Account'...")
                await create_btn.click()
                await page.wait_for_timeout(3000)
                print(f"URL: {page.url[:60]}")
        except Exception as e:
            print(f"Click error: {str(e)[:40]}")
        
        # Now try the email signup option
        try:
            email_btn = await page.query_selector("button:has-text('Email'), button:has-text('电子邮件')")
            if email_btn:
                print("Clicking Email option...")
                await email_btn.click()
                await page.wait_for_timeout(2000)
        except: pass
        
        # Fill the registration form
        inputs = await page.evaluate("""
            () => Array.from(document.querySelectorAll("input:not([type=hidden])"))
                .filter(el => el.offsetParent !== null)
                .map(el => ({name: el.name, type: el.type, ph: el.placeholder, id: el.id}))
        """)
        
        print(f"\nForm inputs: {len(inputs)}")
        for f in inputs:
            txt = (f["name"] + " " + f["id"] + " " + f["ph"]).lower()
            print(f"  {f['name'] or f['ph']}: type={f['type']}")
            
            val = None
            if "email" in txt: val = EMAIL
            elif "password" in txt or "pass" in txt: val = PASS
            elif "username" in txt or "user_name" in txt: val = "creatordir"
            elif "name" in txt: val = "CreatorAI"
            
            if val:
                sel = f"#{f['id']}" if f["id"] else f"[name='{f['name']}']"
                try:
                    el = await page.query_selector(sel)
                    if el:
                        await el.fill(val)
                        print(f"    >>> FILLED {val[:20]}")
                except: pass
        
        # Check for signup submit button
        btns = await page.evaluate("""
            () => Array.from(document.querySelectorAll("button"))
                .filter(el => el.offsetParent !== null)
                .map(el => el.innerText || el.textContent || "")
                .map(t => t.trim())
                .filter(t => t.length > 0 && t.length < 30)
        """)
        print(f"\nButtons: {btns}")
        
        await browser.close()

asyncio.run(main())
