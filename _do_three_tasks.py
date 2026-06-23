
import asyncio
from playwright.async_api import async_playwright
import sys
sys.stdout.reconfigure(encoding="utf-8")

EMAIL = "346010735@qq.com"
PASS = "Ckyhy388"
SITE = "https://creatordir-tools.vercel.app"
NAME = "CreatorAI Tools"
TITLE = "I built a directory of 200+ AI tools for content creators"
POST_BODY = "Check out https://creatordir-tools.vercel.app - a curated directory of 200+ AI tools with honest reviews, comparisons, and tutorials. All free and open source!"

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp("http://127.0.0.1:9222", timeout=30000)
        pages = browser.contexts[0].pages
        print(f"Connected! {len(pages)} pages")
        
        for pg in pages:
            url = pg.url
            await pg.bring_to_front()
            await pg.wait_for_timeout(1000)
            
            # === 1. DEV.TO REGISTRATION ===
            if "dev.to" in url:
                print("\n=== 1. DEV.TO REGISTRATION ===")
                await pg.wait_for_timeout(2000)
                
                # Fill email
                try:
                    el = await pg.query_selector("[name='user[email]']")
                    if el:
                        await el.fill(EMAIL)
                        print("  Email filled")
                except: pass
                
                # Fill password
                try:
                    el = await pg.query_selector("[name='user[password]']")
                    if el:
                        await el.fill(PASS)
                        print("  Password filled")
                except: pass
                
                # Try clicking "创建账户" link
                try:
                    for text in ["创建账户", "Create account"]:
                        el = await pg.query_selector(f"a:has-text('{text}')")
                        if el:
                            print(f"  Clicking '{text}'...")
                            await el.click(timeout=5000)
                            await pg.wait_for_timeout(2000)
                            break
                except: pass
                
                # Fill new signup fields
                inputs = await pg.query_selector_all("input:visible")
                for inp in inputs:
                    try:
                        nm = await inp.get_attribute("name") or ""
                        ph = await inp.get_attribute("placeholder") or ""
                        txt = (nm + " " + ph).lower()
                        if "username" in txt or "user_name" in txt:
                            await inp.fill("creatordir")
                            print("  Username filled: creatordir")
                    except: pass
                
                # Click submit
                try:
                    btn = await pg.query_selector("button[type=submit], input[type=submit]")
                    if btn:
                        bt = await btn.get_attribute("value") or await btn.inner_text() or "Submit"
                        print(f"  Submitting: {bt[:20]}")
                        await btn.click(timeout=5000)
                        await pg.wait_for_timeout(3000)
                        print(f"  Result URL: {pg.url[:60]}")
                except Exception as e:
                    print(f"  Submit error: {str(e)[:30]}")
                
                # Check result
                text = (await pg.evaluate("document.body.innerText") or "")[:200]
                print(f"  Result: {text[:150]}")
            
            # === 2. THAT AICOLLECTION SUBMIT ===
            elif "thataicollection" in url:
                print("\n=== 2. THAT AICOLLECTION SUBMIT ===")
                await pg.wait_for_timeout(1000)
                
                # Click submit button
                try:
                    btn = await pg.query_selector("button:has-text('用AI提交')")
                    if not btn:
                        btn = await pg.query_selector("button:has-text('Submit')")
                    if btn:
                        print("  Clicking submit button...")
                        await btn.click(timeout=5000)
                        await pg.wait_for_timeout(3000)
                        print(f"  URL: {pg.url[:60]}")
                except Exception as e:
                    print(f"  Error: {str(e)[:20]}")
            
            # === 3. REDDIT ===
            elif "reddit" in url:
                print("\n=== 3. REDDIT ===")
                await pg.wait_for_timeout(2000)
                
                if "login" in url:
                    # Try to login
                    print("  Reddit login page - filling credentials...")
                    try:
                        els = await pg.query_selector_all("input:visible")
                        for el in els:
                            nm = await el.get_attribute("name") or ""
                            if "user" in nm.lower() or "login" in nm.lower():
                                await el.fill(EMAIL)
                                print("  Username filled")
                            elif "pass" in nm.lower():
                                await el.fill(PASS)
                                print("  Password filled")
                        
                        btn = await pg.query_selector("button[type=submit]")
                        if btn:
                            await btn.click(timeout=5000)
                            await pg.wait_for_timeout(3000)
                            print(f"  Login result: {pg.url[:60]}")
                    except Exception as e:
                        print(f"  Login error: {str(e)[:20]}")
                
                # Not on login page - try to post
                try:
                    title_inp = await pg.query_selector("[name='title'], [placeholder*='Title']")
                    if title_inp:
                        await title_inp.fill(TITLE)
                        print("  Title filled!")
                    
                    body_area = await pg.query_selector("textarea, [role='textbox'], [contenteditable]")
                    if body_area:
                        await body_area.fill(POST_BODY)
                        print("  Body filled!")
                    
                    post_btn = await pg.query_selector("button:has-text('Post'), button:has-text('Submit')")
                    if post_btn:
                        await post_btn.click(timeout=5000)
                        await pg.wait_for_timeout(3000)
                        print(f"  Posted! URL: {pg.url[:60]}")
                except Exception as e:
                    print(f"  Post error: {str(e)[:20]}")
        
        await browser.close()
        print("\n=== ALL THREE TASKS COMPLETE ===")

asyncio.run(main())
