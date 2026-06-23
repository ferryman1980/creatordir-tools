
import asyncio
from playwright.async_api import async_playwright
import sys
sys.stdout.reconfigure(encoding="utf-8")

EMAIL = "346010735@qq.com"
PASS = "Ckyhy388"
PHONE = "18991377556"
SITE = "https://creatordir-tools.vercel.app"
NAME = "CreatorAI Tools"
DESC = "Curated directory of 200+ AI tools for content creators"

async def do_register(page, title, rules):
    print(f"\n=== {title} ===")
    await page.wait_for_timeout(2000)
    await page.evaluate("window.scrollTo(0, 300)")
    await page.wait_for_timeout(1000)
    
    # Get inputs, handling None
    inputs = await page.evaluate("""
        () => Array.from(document.querySelectorAll("input:not([type=hidden]):not([type=radio]):not([type=checkbox]), textarea, select"))
            .filter(el => el.offsetParent !== null)
            .map(el => ({tag: el.tagName, name: el.name || "", type: el.type || "", ph: el.placeholder || "", id: el.id || ""}))
    """)
    
    print(f"Inputs: {len(inputs)}")
    
    for f in inputs:
        txt = (f["name"] + " " + f["id"] + " " + f["ph"]).lower()
        val = None
        for key, v in rules:
            if key in txt:
                val = v
                break
        if val:
            sel = f"#{f['id']}" if f["id"] else f"[name='{f['name']}']" if f["name"] else ""
            if sel:
                try:
                    el = await page.query_selector(sel)
                    if el:
                        await el.fill(val)
                        print(f"  FILLED {f['name'][:15]} = {val[:15]}")
                except: pass
    
    # Try submit
    try:
        btn = await page.query_selector("button[type=submit], input[type=submit], button:has-text('Sign up'), button:has-text('Create'), button:has-text('Submit'), button:has-text('Add Tool')")
        if btn:
            bt = await btn.get_attribute("value") or await btn.inner_text() or "Submit"
            print(f"  SUBMIT: {bt[:20]}")
            await btn.click(timeout=5000)
            await page.wait_for_timeout(3000)
            print(f"  RESULT URL: {page.url[:60]}")
    except Exception as e:
        print(f"  Click error: {str(e)[:30]}")
    
    # Check result
    body = (await page.evaluate("document.body.innerText") or "")[:200]
    print(f"  Body: {body[:150]}")

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp("http://127.0.0.1:9222", timeout=20000)
        pages = browser.contexts[0].pages
        
        for pg in pages:
            url = pg.url
            await pg.bring_to_front()
            
            if "thataicollection" in url and "signup" in url:
                # ThatAICollection signup page
                await do_register(pg, "ThatAICollection Signup", [
                    ("email", EMAIL), ("password", PASS), ("pass", PASS),
                    ("name", NAME), ("username", "creatordir"),
                    ("url", SITE), ("website", SITE)
                ])
            elif "aixploria" in url:
                await do_register(pg, "AIxploria", [
                    ("name", NAME), ("title", NAME),
                    ("url", SITE), ("site", SITE),
                    ("desc", DESC), ("email", EMAIL)
                ])
            elif "awin" in url:
                # Awin - try to click Get Started
                try:
                    btn = await pg.query_selector("a:has-text('Get Started'), a:has-text('开始'), button:has-text('Get Started')")
                    if btn:
                        print("\n=== Awin ===")
                        print("Clicking Get Started...")
                        await btn.click(timeout=5000)
                        await pg.wait_for_timeout(3000)
                        print(f"URL: {pg.url[:60]}")
                        await do_register(pg, "Awin Form", [
                            ("email", EMAIL), ("password", PASS), ("pass", PASS),
                            ("first", "Creator"), ("last", "AI"),
                            ("company", NAME), ("website", SITE),
                            ("phone", PHONE)
                        ])
                except Exception as e:
                    print(f"  Error: {str(e)[:30]}")
            elif "dev.to" in url:
                await do_register(pg, "Dev.to", [
                    ("email", EMAIL), ("password", PASS), ("pass", PASS),
                    ("username", "creatordir"), ("name", "CreatorAI")
                ])
        
        await browser.close()
        print("\n=== ALL DONE ===")

asyncio.run(main())
