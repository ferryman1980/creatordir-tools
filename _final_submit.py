
import asyncio
from playwright.async_api import async_playwright
import sys
sys.stdout.reconfigure(encoding="utf-8")

EMAIL = "346010735@qq.com"
PASS = "Ckyhy388"
SITE = "https://creatordir-tools.vercel.app"
NAME = "CreatorAI Tools"
DESC = "Curated directory of 200+ AI tools for content creators"

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp("http://127.0.0.1:9222", timeout=20000)
        pages = browser.contexts[0].pages
        
        for pg in pages:
            url = pg.url
            await pg.bring_to_front()
            await pg.wait_for_timeout(1000)
            
            # === Dev.to Signup ===
            if "dev.to" in url and "sign_up" in url:
                print(f"\n=== Dev.to Signup ===")
                await pg.wait_for_timeout(2000)
                
                inputs = await pg.evaluate("""
                    () => Array.from(document.querySelectorAll("input:not([type=hidden])"))
                        .filter(el => el.offsetParent !== null)
                        .map(el => ({name: el.name || "", type: el.type || "", ph: el.placeholder || "", id: el.id || ""}))
                """)
                print(f"Inputs: {len(inputs)}")
                
                for f in inputs:
                    txt = (f["name"] + " " + f["id"] + " " + f["ph"]).lower()
                    print(f"  {f['name']}: {f['type']}")
                    val = None
                    if "email" in txt: val = EMAIL
                    elif "password" in txt or "pass" in txt: val = PASS
                    elif "username" in txt: val = "creatordir"
                    if val:
                        sel = f"#{f['id']}" if f["id"] else f"[name='{f['name']}']"
                        try:
                            el = await pg.query_selector(sel)
                            if el: await el.fill(val); print(f"    FILLED {val[:15]}")
                        except: pass
                
                # Click signup button
                try:
                    btn = await pg.query_selector("button[type=submit], input[type=submit]")
                    if btn:
                        await btn.scroll_into_view_if_needed()
                        await pg.wait_for_timeout(500)
                        await btn.click(timeout=5000)
                        await pg.wait_for_timeout(3000)
                        print(f"Submitted! URL: {pg.url[:60]}")
                except Exception as e:
                    print(f"Submit: {str(e)[:30]}")
            
            # === ThatAICollection Submit ===
            elif "thataicollection" in url and "submit" in url:
                print(f"\n=== ThatAICollection Submit ===")
                await pg.wait_for_timeout(2000)
                await pg.evaluate("window.scrollTo(0, 300)")
                await pg.wait_for_timeout(1000)
                
                inputs = await pg.evaluate("""
                    () => Array.from(document.querySelectorAll("input:not([type=hidden]):not([type=checkbox]), textarea"))
                        .filter(el => el.offsetParent !== null)
                        .map(el => ({name: el.name || "", type: el.type || "", ph: el.placeholder || "", id: el.id || ""}))
                """)
                print(f"Inputs: {len(inputs)}")
                
                for f in inputs:
                    txt = (f["name"] + " " + f["id"] + " " + f["ph"]).lower()
                    print(f"  {f['name']}: {f['ph']}")
                    val = None
                    if "url" in txt or "website" in txt or "link" in txt: val = SITE
                    elif "name" in txt or "title" in txt: val = NAME
                    elif "desc" in txt or "about" in txt: val = DESC
                    elif "email" in txt: val = EMAIL
                    if val:
                        sel = f"#{f['id']}" if f["id"] else f"[name='{f['name']}']"
                        try:
                            el = await pg.query_selector(sel)
                            if el: await el.fill(val); print(f"    FILLED {val[:15]}")
                        except: pass
                
                # Submit
                try:
                    btn = await pg.query_selector("button[type=submit], input[type=submit]")
                    if btn:
                        await btn.scroll_into_view_if_needed()
                        await pg.wait_for_timeout(500)
                        await btn.click(timeout=5000)
                        await pg.wait_for_timeout(3000)
                        print(f"Submitted! URL: {pg.url[:60]}")
                except Exception as e:
                    print(f"Submit: {str(e)[:30]}")
            
            # === Submission Guide (already loaded) ===
            elif "submission-guide" in url:
                print(f"\n=== Submission Guide ===")
                print(f"Guide loaded successfully!")
        
        await browser.close()
        print("\n=== ALL DONE ===")

asyncio.run(main())
