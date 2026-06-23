
import asyncio
from playwright.async_api import async_playwright
import sys
sys.stdout.reconfigure(encoding="utf-8")

EMAIL = "346010735@qq.com"
PASS = "Ckyhy388"
SITE = "https://creatordir-tools.vercel.app"

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp("http://127.0.0.1:9222", timeout=30000)
        page = browser.contexts[0].pages[0]
        
        # === 1. DEV.TO - Try direct API registration ===
        print("=== 1. DEV.TO ===")
        
        # Try the /users/sign_up page directly (bypass /enter page)
        await page.goto("https://dev.to/users/sign_up", timeout=15000, wait_until="domcontentloaded")
        await page.wait_for_timeout(3000)
        print(f"URL: {page.url[:60]}")
        
        # Get page state
        buttons_text = await page.evaluate("""
            () => Array.from(document.querySelectorAll("button, a"))
                .filter(el => el.offsetParent !== null)
                .map(el => (el.innerText || el.textContent || "").trim().substring(0, 25))
                .filter(t => t.length > 0)
        """)
        print(f"Buttons: {buttons_text}")
        
        # Check for email input
        inputs = await page.evaluate("""
            () => Array.from(document.querySelectorAll("input"))
                .filter(el => el.offsetParent !== null)
                .map(el => ({name: el.name, type: el.type, ph: el.placeholder}))
        """)
        print(f"Inputs: {len(inputs)}")
        for f in inputs:
            print(f"  {f['name']}: {f['ph']}")
        
        # If there's an email option, click it
        try:
            email_opt = await page.query_selector("button:has-text('Email')")
            if email_opt:
                print("Clicking Email option...")
                await email_opt.click(timeout=5000)
                await page.wait_for_timeout(2000)
        except: pass
        
        # Now fill and submit
        await page.wait_for_timeout(1000)
        all_inputs = await page.query_selector_all("input:visible")
        print(f"\nVisible inputs after: {len(all_inputs)}")
        for inp in all_inputs:
            try:
                nm = await inp.get_attribute("name") or ""
                ph = await inp.get_attribute("placeholder") or ""
                print(f"  {nm}: {ph}")
                combined = (nm + " " + ph).lower()
                val = None
                if "email" in combined: val = EMAIL
                elif "password" in combined: val = PASS
                elif "username" in combined: val = "creatordir"
                if val:
                    await inp.fill(val)
                    print(f"    FILLED")
            except: pass
        
        # Find submit
        try:
            btn = await page.query_selector("button[type=submit], input[type=submit]")
            if btn:
                bt = await btn.get_attribute("value") or await btn.inner_text() or "Submit"
                print(f"\nClicking: {bt[:20]}")
                await btn.click(timeout=5000)
                await page.wait_for_timeout(3000)
                print(f"URL: {page.url[:60]}")
        except Exception as e:
            print(f"Submit: {str(e)[:20]}")
        
        # === 2. THAT AICOLLECTION ===
        print("\n=== 2. THAT AICOLLECTION ===")
        await page.goto("https://thataicollection.com/en/submit/", timeout=15000)
        await page.wait_for_timeout(3000)
        
        # Fill fields
        all_in = await page.query_selector_all("input:visible")
        for inp in all_in:
            try:
                nm = await inp.get_attribute("name") or ""
                ph = await inp.get_attribute("placeholder") or ""
                combined = (nm + " " + ph).lower()
                val = None
                if "url" in combined or "website" in combined: val = SITE
                elif "name" in combined or "title" in combined: val = "CreatorAI Tools"
                if val:
                    await inp.fill(val)
                    print(f"FILLED {nm}: {val[:20]}")
            except: pass
        
        # Click submit
        try:
            btn = await page.query_selector("button:has-text('用AI提交')")
            if btn:
                await btn.click(timeout=5000)
                await page.wait_for_timeout(3000)
                print(f"Submitted! URL: {page.url[:60]}")
        except Exception as e:
            print(f"Submit: {str(e)[:20]}")
        
        await browser.close()
        print("\n=== DONE ===")

asyncio.run(main())
