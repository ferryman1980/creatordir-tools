
import asyncio
from playwright.async_api import async_playwright
import sys
sys.stdout.reconfigure(encoding="utf-8")

EMAIL = "346010735@qq.com"
PASS = "Ckyhy388"
PHONE = "18991377556"
SITE = "https://creatordir-tools.vercel.app"
NAME = "CreatorAI Tools"
DESC = "Curated directory of 200+ AI tools for content creators with honest reviews and comparisons"

async def fill_and_submit(page, site_name):
    await page.wait_for_timeout(2000)
    await page.evaluate("window.scrollTo(0, 300)")
    await page.wait_for_timeout(1000)
    
    url = page.url
    print(f"\n=== {site_name} ===")
    print(f"URL: {url[:60]}")
    
    # Get visible inputs
    inputs = await page.evaluate("""
        () => Array.from(document.querySelectorAll("input:not([type=hidden]):not([type=radio]):not([type=checkbox]), textarea, select"))
            .filter(el => el.offsetParent !== null)
            .map(el => ({tag: el.tagName, name: el.name, type: el.type, ph: el.placeholder, id: el.id}))
    """)
    
    print(f"Inputs: {len(inputs)}")
    
    # Define fill rules for each site
    rules = []
    
    if "dev.to" in url or "dev.to" in site_name.lower():
        rules = [
            ("email", EMAIL), ("password", PASS), ("pass", PASS),
            ("username", "creatordir"), ("name", "CreatorAI"),
            ("phone", PHONE), ("tel", PHONE)
        ]
    elif "thataicollection" in url:
        rules = [
            ("url", SITE), ("website", SITE), ("site", SITE),
            ("name", NAME), ("title", NAME),
            ("desc", DESC), ("about", DESC),
            ("email", EMAIL)
        ]
    elif "aixploria" in url:
        rules = [
            ("name", NAME), ("title", NAME),
            ("url", SITE), ("site", SITE),
            ("desc", DESC),
            ("email", EMAIL)
        ]
    elif "reddit" in url:
        rules = []  # Reddit requires login first
        print("  Reddit needs login - skipping auto-fill")
    elif "awin" in url:
        rules = [
            ("email", EMAIL), ("password", PASS), ("pass", PASS),
            ("first", "Creator"), ("fname", "Creator"),
            ("last", "AI"), ("lname", "AI"),
            ("company", NAME), ("business", NAME), ("org", NAME),
            ("website", SITE), ("url", SITE),
            ("phone", PHONE), ("tel", PHONE)
        ]
    
    for f in inputs:
        txt = (f["name"] + " " + f["id"] + " " + f["ph"]).lower()
        val = None
        for keyword, value in rules:
            if keyword in txt:
                val = value
                break
        
        if val:
            sel = f"#{f['id']}" if f["id"] else f"[name='{f['name']}']" if f["name"] else ""
            if sel:
                try:
                    el = await page.query_selector(sel)
                    if el:
                        await el.fill(val)
                        print(f"  FILLED [{f['name'][:15]}]: {val[:15]}")
                except:
                    pass
    
    # Try to find and click submit button
    try:
        btn = await page.query_selector("button[type=submit], input[type=submit], button:has-text('Submit'), button:has-text('Sign up'), button:has-text('注册'), button:has-text('Create'), button:has-text('Add Tool'), button:has-text('Send')")
        if btn:
            txt = await btn.get_attribute("value") or await btn.inner_text() or ""
            print(f"  SUBMIT FOUND: {txt[:20]}")
            await btn.click(timeout=5000)
            await page.wait_for_timeout(3000)
            print(f"  CLICKED! New URL: {page.url[:60]}")
    except Exception as e:
        print(f"  Submit error: {str(e)[:30]}")

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp("http://127.0.0.1:9222", timeout=20000)
        pages = browser.contexts[0].pages
        print(f"Connected! {len(pages)} pages")
        
        page_names = ["Dev.to Signup", "ThatAICollection", "AIxploria", "Submission Guide", "Reddit", "Awin"]
        
        for i, pg in enumerate(pages):
            if i < len(page_names):
                await pg.bring_to_front()
                await fill_and_submit(pg, page_names[i])
        
        print(f"\n{'='*40}")
        print("ALL DONE! Check Edge browser for results.")
        
        await browser.close()

asyncio.run(main())
