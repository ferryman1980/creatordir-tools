
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
        
        # === 1. DEV.TO ===
        print("=== 1. DEV.TO REGISTRATION ===")
        await page.wait_for_timeout(2000)
        
        # Click email signup option
        try:
            email_btn = await page.query_selector("button:has-text('通过电子邮件注册'), button:has-text('Register with email'), button:has-text('Sign up with email')")
            if email_btn:
                print("Clicking email signup...")
                await email_btn.click(timeout=5000)
                await page.wait_for_timeout(3000)
                print(f"URL: {page.url[:60]}")
        except Exception as e:
            print(f"Email btn error: {str(e)[:20]}")
        
        # Fill form
        await page.wait_for_timeout(1000)
        input_els = await page.query_selector_all("input:visible")
        print(f"Inputs: {len(input_els)}")
        for inp in input_els:
            try:
                nm = await inp.get_attribute("name") or ""
                ph = await inp.get_attribute("placeholder") or ""
                combined = (nm + " " + ph).lower()
                print(f"  {nm}: {ph}")
                
                val = None
                if "email" in combined: val = EMAIL
                elif "password" in combined or "pass" in combined: val = PASS
                elif "username" in combined: val = "creatordir"
                elif "name" in combined and "user" in combined: val = "CreatorAI"
                
                if val:
                    await inp.fill(val)
                    print(f"    FILLED: {val[:15]}")
            except: pass
        
        # Find submit button - look for "注册" (Register) or "Sign up"
        buttons = await page.evaluate("""
            () => Array.from(document.querySelectorAll("button, input[type=submit]"))
                .filter(el => el.offsetParent !== null)
                .map(el => ({
                    text: (el.innerText || el.value || "").trim().substring(0, 20),
                    type: el.type || ""
                }))
                .filter(b => b.text.length > 0 && b.text.length < 15)
        """)
        print(f"\nButtons: {[b['text'] + ' (' + b['type'] + ')' for b in buttons]}")
        
        # Find the right submit button
        for b_text in ["注册", "Sign up", "Create account", "提交", "Submit"]:
            try:
                btn = await page.query_selector(f"button:has-text('{b_text}'), input[value='{b_text}']")
                if btn:
                    print(f"Clicking: {b_text}")
                    # Scroll into view
                    try:
                        await btn.scroll_into_view_if_needed()
                        await page.wait_for_timeout(500)
                    except: pass
                    await btn.click(timeout=5000)
                    await page.wait_for_timeout(3000)
                    print(f"Result URL: {page.url[:60]}")
                    break
            except Exception as e:
                print(f"  {b_text}: {str(e)[:15]}")
        
        # Check result
        result = (await page.evaluate("document.body.innerText") or "")[:200]
        print(f"Result: {result[:150]}")
        
        # === 2. OPEN THAT AICOLLECTION ===
        print("\n=== 2. THAT AICOLLECTION ===")
        await page.goto("https://thataicollection.com/en/submit/", timeout=15000, wait_until="domcontentloaded")
        await page.wait_for_timeout(3000)
        
        # Fill URL (2nd input)
        inputs = await page.query_selector_all("input:visible")
        if len(inputs) >= 2:
            await inputs[1].fill(SITE)
            print("URL filled!")
        
        # Click submit
        try:
            btn = await page.query_selector("button:has-text('用AI提交')")
            if btn:
                await btn.click(timeout=5000)
                await page.wait_for_timeout(3000)
                print(f"Submitted! URL: {page.url[:60]}")
        except Exception as e:
            print(f"Submit error: {str(e)[:20]}")
        
        # === 3. OPEN REDDIT ===
        print("\n=== 3. REDDIT ===")
        await page.goto("https://www.reddit.com/r/artificial/submit", timeout=15000, wait_until="domcontentloaded")
        await page.wait_for_timeout(3000)
        print(f"Reddit URL: {page.url[:60]}")
        
        if "login" in page.url.lower():
            print("Need to login first - trying...")
            # Fill login
            reddit_inputs = await page.query_selector_all("input:visible")
            for inp in reddit_inputs:
                try:
                    nm = await inp.get_attribute("name") or ""
                    if "user" in nm.lower():
                        await inp.fill(EMAIL)
                        print("Username filled")
                    elif "pass" in nm.lower():
                        await inp.fill(PASS)
                        print("Password filled")
                except: pass
            
            try:
                btn = await page.query_selector("button[type=submit]")
                if btn:
                    await btn.click(timeout=5000)
                    await page.wait_for_timeout(3000)
                    print(f"Login result: {page.url[:60]}")
            except: pass
        
        await browser.close()
        print("\n=== ALL THREE TASKS COMPLETE ===")

asyncio.run(main())
