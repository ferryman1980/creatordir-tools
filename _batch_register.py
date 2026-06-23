
import asyncio
from playwright.async_api import async_playwright
import sys
sys.stdout.reconfigure(encoding="utf-8")

SITE = "https://creatordir-tools.vercel.app"
NAME = "CreatorAI Tools"
DESC = "Curated directory of 200+ AI tools for content creators"
EMAIL = "346010735@qq.com"

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp("http://127.0.0.1:9222", timeout=10000)
        pages = browser.contexts[0].pages
        print(f"Connected! {len(pages)} pages")
        
        # === TASK 1: ShareASale Signup ===
        print("\n=== ShareASale Signup ===")
        page = pages[0]
        await page.bring_to_front()
        await page.goto("https://account.shareasale.com/signup.cfm", timeout=15000, wait_until="domcontentloaded")
        await page.wait_for_timeout(3000)
        await page.evaluate("window.scrollTo(0, 300)")
        await page.wait_for_timeout(1000)
        
        # Fill visible fields
        fields = await page.evaluate("""
            () => Array.from(document.querySelectorAll("input:not([type=hidden]):not([type=checkbox]):not([type=radio]), textarea, select"))
                .filter(el => el.offsetParent !== null)
                .map(el => ({tag: el.tagName, name: el.name, type: el.type, ph: el.placeholder, id: el.id}))
        """)
        print(f"ShareASale fields: {len(fields)}")
        for f in fields:
            print(f"  {f['name'] or f['ph']} [{f['type']}]")
            txt = (f["name"] + " " + f["id"] + " " + f["ph"]).lower()
            val = None
            if "email" in txt and "confirm" not in txt and "verify" not in txt:
                val = EMAIL
            elif "url" in txt or "website" in txt:
                val = SITE
            elif "bus" in txt or "company" in txt:
                val = NAME
            elif "first" in txt or "firstname" in txt:
                val = "Creator"
            elif "last" in txt or "lastname" in txt:
                val = "AI"
            if val:
                sel = f"#{f['id']}" if f["id"] else f"[name='{f['name']}']"
                try:
                    el = await page.query_selector(sel)
                    if el:
                        await el.fill(val)
                        print(f"    >>> FILLED {val[:20]}")
                except: pass
        
        # === TASK 2: ThatAICollection ===
        print("\n=== ThatAICollection ===")
        await pages[1].bring_to_front()
        await pages[1].goto("https://thataicollection.com/en/submit/", timeout=15000, wait_until="domcontentloaded")
        await pages[1].wait_for_timeout(3000)
        await pages[1].evaluate("window.scrollTo(0, 500)")
        await pages[1].wait_for_timeout(1000)
        
        ta_fields = await pages[1].evaluate("""
            () => Array.from(document.querySelectorAll("input:not([type=hidden]):not([type=checkbox]), textarea"))
                .filter(el => el.offsetParent !== null)
                .map(el => ({tag: el.tagName, name: el.name, ph: el.placeholder, id: el.id}))
        """)
        print(f"ThatAICollection fields: {len(ta_fields)}")
        for f in ta_fields:
            print(f"  {f['name'] or f['ph']}")
            txt = (f["name"] + " " + f["id"] + " " + f["ph"]).lower()
            val = None
            if "name" in txt: val = NAME
            elif "url" in txt or "website" in txt: val = SITE
            elif "desc" in txt or "about" in txt: val = DESC
            elif "email" in txt: val = EMAIL
            if val:
                sel = f"#{f['id']}" if f["id"] else f"[name='{f['name']}']"
                try:
                    el = await pages[1].query_selector(sel)
                    if el:
                        await el.fill(val)
                        print(f"    >>> FILLED {val[:20]}")
                except: pass
        
        # === TASK 3: AIxploria ===
        print("\n=== AIxploria ===")
        await pages[2].bring_to_front()
        await pages[2].goto("https://www.aixploria.com/en/submit-tool", timeout=15000, wait_until="domcontentloaded")
        await pages[2].wait_for_timeout(3000)
        await pages[2].evaluate("window.scrollTo(0, 500)")
        await pages[2].wait_for_timeout(1000)
        
        ax_fields = await pages[2].evaluate("""
            () => Array.from(document.querySelectorAll("input:not([type=hidden]):not([type=checkbox]), textarea"))
                .filter(el => el.offsetParent !== null)
                .map(el => ({tag: el.tagName, name: el.name, ph: el.placeholder, id: el.id}))
        """)
        print(f"AIxploria fields: {len(ax_fields)}")
        for f in ax_fields:
            print(f"  {f['name'] or f['ph']}")
            txt = (f["name"] + " " + f["id"] + " " + f["ph"]).lower()
            val = None
            if "name" in txt: val = NAME
            elif "url" in txt or "website" in txt: val = SITE
            elif "desc" in txt or "about" in txt: val = DESC
            elif "email" in txt: val = EMAIL
            if val:
                sel = f"#{f['id']}" if f["id"] else f"[name='{f['name']}']"
                try:
                    el = await pages[2].query_selector(sel)
                    if el:
                        await el.fill(val)
                        print(f"    >>> FILLED {val[:20]}")
                except: pass
        
        # Try to submit on all pages
        for i, pg in enumerate([pages[1], pages[2]]):
            try:
                await pg.bring_to_front()
                submit_btn = await pg.query_selector("button[type=submit], input[type=submit], button:has-text('Submit'), button:has-text('Add'), button:has-text('Send')")
                if submit_btn:
                    await submit_btn.click(timeout=5000)
                    await pg.wait_for_timeout(3000)
                    print(f"  Page {i+2} SUBMITTED! URL: {pg.url[:60]}")
                else:
                    print(f"  Page {i+2}: No submit button found")
            except Exception as e:
                print(f"  Page {i+2} submit error: {str(e)[:30]}")
        
        await browser.close()
        print("\n=== Done! ===")

asyncio.run(main())
