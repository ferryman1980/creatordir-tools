
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
        
        # Find ThatAICollection signup page
        for pg in pages:
            url = pg.url
            if "thataicollection" in url and "signup" in url:
                await pg.bring_to_front()
                await pg.wait_for_timeout(2000)
                print(f"ThatAICollection signup: {url[:60]}")
                
                # Try different submit selectors
                btns_to_try = [
                    "button:has-text('用AI提交')",
                    "button:has-text('Submit')",
                    "button:has-text('注册')",
                    "button:has-text('Create')",
                    "button[type=submit]",
                    "input[type=submit]"
                ]
                
                for sel in btns_to_try:
                    try:
                        btn = await pg.query_selector(sel)
                        if btn:
                            txt = await btn.inner_text() or await btn.get_attribute("value") or ""
                            print(f"  Found: '{txt}' with selector: {sel}")
                            # Scroll to button
                            await btn.scroll_into_view_if_needed()
                            await pg.wait_for_timeout(500)
                            await btn.click(timeout=5000)
                            await pg.wait_for_timeout(3000)
                            print(f"  After click: {pg.url[:60]}")
                            break
                    except Exception as e:
                        print(f"  Failed: {sel[:30]} -> {str(e)[:20]}")
                
                # Check result
                text = (await pg.evaluate("document.body.innerText") or "")[:300]
                print(f"  Result: {text[:150]}")
        
        await browser.close()

asyncio.run(main())
