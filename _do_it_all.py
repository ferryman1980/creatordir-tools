
import asyncio
from playwright.async_api import async_playwright
import sys
sys.stdout.reconfigure(encoding="utf-8")

EMAIL = "346010735@qq.com"
PASS = "Ckyhy388"

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp("http://127.0.0.1:9222", timeout=20000)
        pages = browser.contexts[0].pages
        
        for pg in pages:
            url = pg.url
            await pg.bring_to_front()
            await pg.wait_for_timeout(1000)
            
            # === 1. DEV.TO REGISTER ===
            if "dev.to" in url:
                print("\n=== DEV.TO REGISTRATION ===")
                await pg.wait_for_timeout(2000)
                
                # Direct approach: use the signup API or try clicking the right buttons
                # First, check what's on the page
                buttons = await pg.evaluate("""
                    () => Array.from(document.querySelectorAll("button, a"))
                        .filter(el => el.offsetParent !== null)
                        .map(el => (el.innerText || el.textContent || "").trim().substring(0, 20))
                        .filter(t => t.length > 0)
                """)
                print(f"Buttons: {buttons}")
                
                # Try clicking "创建账户" to switch to signup mode
                try:
                    create = await pg.query_selector("a:has-text('创建账户')")
                    if not create:
                        create = await pg.query_selector("a:has-text('Create account')")
                    if create:
                        print("Clicking '创建账户'...")
                        await create.click(timeout=5000)
                        await pg.wait_for_timeout(2000)
                except Exception as e:
                    print(f"No create link: {str(e)[:20]}")
                
                # Fill ALL inputs
                inputs = await pg.query_selector_all("input:visible, textarea:visible")
                print(f"Visible inputs: {len(inputs)}")
                for inp in inputs:
                    try:
                        nm = await inp.get_attribute("name") or ""
                        ph = await inp.get_attribute("placeholder") or ""
                        tp = await inp.get_attribute("type") or ""
                        combined = (nm + " " + ph).lower()
                        print(f"  {nm}: {ph}")
                        
                        val = None
                        if "email" in combined: val = EMAIL
                        elif "password" in combined or "pass" in combined: val = PASS
                        elif "username" in combined: val = "creatordir"
                        
                        if val and tp != "checkbox":
                            await inp.fill(val)
                            print(f"    FILLED {val[:15]}")
                    except Exception as e:
                        print(f"    Error: {str(e)[:20]}")
                
                # Try all possible submit buttons
                for btn_text in ["Sign up", "Create account", "注册", "创建", "Submit", "commit"]:
                    try:
                        btn = await pg.query_selector(f"input[value='{btn_text}'], button:has-text('{btn_text}'), input[name='commit']")
                        if btn:
                            print(f"Clicking: {btn_text}")
                            await btn.click(timeout=5000)
                            await pg.wait_for_timeout(3000)
                            print(f"URL: {pg.url[:60]}")
                            break
                    except:
                        pass
            
            # === 2. THAT AICOLLECTION ===
            elif "thataicollection" in url:
                print("\n=== THAT AICOLLECTION ===")
                await pg.wait_for_timeout(1000)
                
                # Check current state
                btns = await pg.evaluate("""
                    () => Array.from(document.querySelectorAll("button"))
                        .filter(el => el.offsetParent !== null)
                        .map(el => (el.innerText || "").trim().substring(0, 20))
                        .filter(t => t.length > 0)
                """)
                print(f"Buttons: {btns}")
                
                # If there's a "用AI提交" button, try clicking it
                try:
                    btn = await pg.query_selector("button:has-text('用AI提交')")
                    if btn:
                        print("Clicking '用AI提交'...")
                        await btn.click(timeout=5000)
                        await pg.wait_for_timeout(3000)
                        print(f"URL: {pg.url[:60]}")
                except Exception as e:
                    print(f"Error: {str(e)[:20]}")
            
            # === 3. REDDIT ===
            elif "reddit" in url:
                print("\n=== REDDIT ===")
                await pg.wait_for_timeout(2000)
                
                if "login" in url:
                    print("Reddit login page - cannot auto-login")
                    # Fill login form if visible
                    inputs = await pg.query_selector_all("input:visible")
                    for inp in inputs:
                        try:
                            nm = await inp.get_attribute("name") or ""
                            if "user" in nm.lower() or "login" in nm.lower():
                                await inp.fill(EMAIL)
                                print(f"Filled username: {EMAIL}")
                            elif "pass" in nm.lower():
                                await inp.fill(PASS)
                                print("Filled password")
                        except: pass
                    # Click login
                    try:
                        btn = await pg.query_selector("button[type=submit]")
                        if btn:
                            await btn.click(timeout=5000)
                            await pg.wait_for_timeout(3000)
                            print(f"URL: {pg.url[:60]}")
                    except: pass
        
        await browser.close()
        print("\n=== ALL DONE ===")

asyncio.run(main())
