
import asyncio, sys
sys.stdout.reconfigure(encoding="utf-8")
from playwright.async_api import async_playwright

SITE = "https://creatordir-tools.vercel.app"
EMAIL = "346010735@qq.com"

PROGRAMS = [
    ("Semrush", "https://www.semrush.com/signup/affiliate/"),
    ("Grammarly", "https://www.grammarly.com/affiliates"),
    ("Jasper", "https://jasper.ai/affiliates"),
    ("Writesonic", "https://writesonic.com/affiliates"),
]

async def try_signup(page, name, url):
    print(f"\n=== {name} ===")
    print(f"URL: {url}")
    
    try:
        await page.goto(url, timeout=15000, wait_until="domcontentloaded")
        await page.wait_for_timeout(3000)
        print(f"Final URL: {page.url[:70]}")
        print(f"Title: {(await page.title())[:50]}")
        
        # Check visible form elements
        info = await page.evaluate("""
            () => {
                const els = document.querySelectorAll("input:not([type=hidden]), textarea, select, button, a");
                return Array.from(els).filter(el => el.offsetParent !== null).map(el => ({
                    tag: el.tagName,
                    type: el.type || "",
                    name: el.name || "",
                    id: el.id || "",
                    ph: el.placeholder || "",
                    text: (el.innerText || el.textContent || "").trim().substring(0, 25)
                })).filter(el => el.text || el.name || el.id || el.ph);
            }
        """)
        
        print(f"Visible elements: {len(info)}")
        
        # Fill forms if we find them
        email_filled = False
        for el in info:
            txt = (el["name"] + " " + el["id"] + " " + el["ph"] + " " + el["text"]).lower()
            print(f"  {el['tag']}: {el['name'][:15]} | {el['ph'][:15]} | {el['text'][:15]}")
            
            if el["tag"] == "INPUT" and ("email" in txt or "mail" in txt):
                try:
                    inp = await page.query_selector(f"#{el['id']}" if el["id"] else f"[name='{el['name']}']")
                    if inp:
                        await inp.fill(EMAIL)
                        print(f"    >>> FILLED EMAIL")
                        email_filled = True
                except: pass
            
            if el["tag"] == "INPUT" and ("url" in txt or "website" in txt or "site" in txt):
                try:
                    inp = await page.query_selector(f"#{el['id']}" if el["id"] else f"[name='{el['name']}']")
                    if inp:
                        await inp.fill(SITE)
                        print(f"    >>> FILLED URL")
                except: pass
        
        # Find signup/submit buttons
        btns = [el for el in info if el["tag"] == "BUTTON" or el["tag"] == "A"]
        signup_btns = [b for b in btns if any(w in b["text"].lower() for w in ["sign","join","get started","register","apply","become"])]
        if signup_btns:
            for b in signup_btns:
                print(f"  SIGNUP BUTTON: {b['text']}")
    
    except Exception as e:
        print(f"  Error: {str(e)[:50]}")

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp("http://127.0.0.1:9222", timeout=10000)
        page = browser.contexts[0].pages[0]
        
        for name, url in PROGRAMS:
            await try_signup(page, name, url)
            await page.wait_for_timeout(2000)
        
        await browser.close()

asyncio.run(main())
