
import asyncio
from playwright.async_api import async_playwright
import sys
sys.stdout.reconfigure(encoding="utf-8")

EMAIL = "346010735@qq.com"
PASS = "Ckyhy388"
PHONE = "18991377556"

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp("http://127.0.0.1:9222", timeout=20000)
        page = browser.contexts[0].pages[0]
        
        print("=== Dev.to Registration ===")
        print(f"URL: {page.url[:60]}")
        
        # Fill email and password (in case they were cleared)
        try:
            email_input = await page.query_selector("input[name='user[email]']")
            if email_input:
                await email_input.fill(EMAIL)
                print("Email filled")
            
            pass_input = await page.query_selector("input[name='user[password]']")
            if pass_input:
                await pass_input.fill(PASS)
                print("Password filled")
        except Exception as e:
            print(f"Fill error: {str(e)[:30]}")
        
        # Find and click "Sign up" link instead of login
        try:
            # Look for "创建账户" or "Create account" or "Sign up" link
            signup_link = await page.query_selector("a:has-text('创建账户'), a:has-text('Create account'), a:has-text('Sign up')")
            if signup_link:
                print("Clicking signup link...")
                await signup_link.click(timeout=5000)
                await page.wait_for_timeout(3000)
                print(f"URL after click: {page.url[:60]}")
        except Exception as e:
            print(f"Signup link error: {str(e)[:30]}")
        
        # Check if we're on the signup page now
        html = await page.content()
        
        # Fill any signup form that appears
        inputs = await page.evaluate("""
            () => Array.from(document.querySelectorAll("input:not([type=hidden])"))
                .filter(el => el.offsetParent !== null)
                .map(el => ({name: el.name, type: el.type, ph: el.placeholder, id: el.id}))
        """)
        
        print(f"\nCurrent inputs: {len(inputs)}")
        for f in inputs:
            print(f"  {f['name'] or f['ph']}: type={f['type']}")
            txt = (f["name"] + " " + f["id"] + " " + f["ph"]).lower()
            val = None
            if "email" in txt: val = EMAIL
            elif "password" in txt or "pass" in txt: val = PASS
            elif "username" in txt or "user_name" in txt: val = "creatordir"
            elif "name" in txt: val = "CreatorAI Tools"
            elif "phone" in txt or "tel" in txt: val = PHONE
            if val:
                sel = f"#{f['id']}" if f["id"] else f"[name='{f['name']}']"
                try:
                    el = await page.query_selector(sel)
                    if el:
                        await el.fill(val)
                        print(f"    >>> FILLED {val[:15]}")
                except: pass
        
        # Try to submit
        try:
            submit_btn = await page.query_selector("input[type=submit], button[type=submit], button:has-text('注册'), button:has-text('Sign up'), button:has-text('创建')")
            if submit_btn:
                txt = await submit_btn.get_attribute("value") or await submit_btn.inner_text() or "Submit"
                print(f"\nClicking submit: {txt}")
                await submit_btn.click(timeout=5000)
                await page.wait_for_timeout(3000)
                print(f"URL: {page.url[:60]}")
                
                # Check result
                body = (await page.evaluate("document.body.innerText") or "")[:300]
                print(f"Result: {body[:200]}")
        except Exception as e:
            print(f"Submit error: {str(e)[:30]}")
        
        # Take screenshot
        await page.screenshot(path="D:/项目/工作区/工作5/devto_result.png")
        print("\nScreenshot saved")
        
        await browser.close()

asyncio.run(main())
