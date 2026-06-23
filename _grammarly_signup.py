
import asyncio, sys
sys.stdout.reconfigure(encoding="utf-8")
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp("http://127.0.0.1:9222", timeout=10000)
        page = browser.contexts[0].pages[0]
        
        # Go to Grammarly
        await page.goto("https://www.grammarly.com/affiliates", timeout=20000, wait_until="domcontentloaded")
        await page.wait_for_timeout(3000)
        print(f"URL: {page.url[:70]}")
        
        # Click "Become an affiliate"
        try:
            btn = await page.query_selector("a:has-text('Become an affiliate')")
            if btn:
                print("Found 'Become an affiliate' button")
                await btn.click()
                await page.wait_for_timeout(3000)
                print(f"After click: {page.url[:70]}")
                
                # Check for signup form
                inputs = await page.evaluate("""
                    () => Array.from(document.querySelectorAll("input:not([type=hidden])"))
                        .filter(el => el.offsetParent !== null)
                        .map(el => ({
                            name: el.name || "", type: el.type || "", ph: el.placeholder || "", id: el.id || ""
                        }))
                """)
                print(f"Inputs: {len(inputs)}")
                for inp in inputs:
                    print(f"  {inp['name'] or inp['ph']}: type={inp['type']}")
                    
                    # Fill what we can
                    txt = (inp["name"] + " " + inp["ph"]).lower()
                    val = None
                    if "email" in txt: val = "346010735@qq.com"
                    elif "name" in txt and "user" in txt: val = "CreatorAI Tools"
                    
                    if val:
                        sel = f"#{inp['id']}" if inp["id"] else f"[name='{inp['name']}']"
                        try:
                            el = await page.query_selector(sel)
                            if el:
                                await el.fill(val)
                                print(f"    >>> FILLED: {val[:20]}")
                        except: pass
            else:
                print("No 'Become an affiliate' button found")
        except Exception as e:
            print(f"Error: {str(e)[:60]}")
        
        await browser.close()

asyncio.run(main())
