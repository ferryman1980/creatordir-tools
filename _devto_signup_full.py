
import asyncio
from playwright.async_api import async_playwright
import sys
sys.stdout.reconfigure(encoding="utf-8")

EMAIL = "346010735@qq.com"
PASS = "Ckyhy388"

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp("http://127.0.0.1:9222", timeout=20000)
        page = browser.contexts[0].pages[0]
        
        # Fresh start
        await page.goto("https://dev.to/enter", timeout=20000, wait_until="domcontentloaded")
        await page.wait_for_timeout(2000)
        
        # Get ALL links to find "创建账户"
        links = await page.evaluate("""
            () => Array.from(document.querySelectorAll("a"))
                .map(a => ({text: a.innerText.trim().substring(0, 20), href: a.href.substring(0, 60)}))
                .filter(a => a.text.length > 0)
        """)
        
        print("All links:")
        for l in links:
            print(f"  [{l['text'][:15]}] -> {l['href'][:50]}")
        
        # Try clicking "创建账户" link
        try:
            link = await page.query_selector("a:has-text('创建账户')")
            if link:
                print("\nClicking '创建账户' link...")
                await link.click(timeout=5000)
                await page.wait_for_timeout(3000)
                print(f"URL: {page.url[:60]}")
        except Exception as e:
            print(f"Click failed: {str(e)[:30]}")
        
        # Check new page
        inputs = await page.evaluate("""
            () => Array.from(document.querySelectorAll("input:not([type=hidden])"))
                .filter(el => el.offsetParent !== null)
                .map(el => ({name: el.name, type: el.type, ph: el.placeholder, id: el.id}))
        """)
        print(f"\nInputs: {len(inputs)}")
        for f in inputs:
            print(f"  {f['name'] or f['ph']}: type={f['type']}")
            txt = (f["name"] + " " + f["id"] + " " + f["ph"]).lower()
            val = None
            if "email" in txt: val = EMAIL
            elif "password" in txt or "pass" in txt: val = PASS
            elif "username" in txt: val = "creatordir"
            if val:
                sel = f"#{f['id']}" if f["id"] else f"[name='{f['name']}']"
                try:
                    el = await page.query_selector(sel)
                    if el:
                        await el.fill(val)
                        print(f"    FILLED {val[:15]}")
                except: pass
        
        # Try to find and click submit
        try:
            btn = await page.query_selector("button:has-text('创建'), input[type=submit], button[type=submit], button:has-text('Sign up')")
            if btn:
                txt = await btn.inner_text() or await btn.get_attribute("value") or "submit"
                print(f"\nClicking: {txt}")
                await btn.click(timeout=5000)
                await page.wait_for_timeout(3000)
                print(f"URL: {page.url[:60]}")
        except Exception as e:
            print(f"Submit error: {str(e)[:30]}")
        
        await browser.close()

asyncio.run(main())
