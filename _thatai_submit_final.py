
import asyncio
from playwright.async_api import async_playwright
import sys
sys.stdout.reconfigure(encoding="utf-8")

SITE = "https://creatordir-tools.vercel.app"
NAME = "CreatorAI Tools"

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp("http://127.0.0.1:9222", timeout=20000)
        pages = browser.contexts[0].pages
        
        for pg in pages:
            if "thataicollection" in pg.url:
                await pg.bring_to_front()
                await pg.wait_for_timeout(2000)
                
                # Fill the URL input (2nd input, the one after search)
                all_inputs = await pg.query_selector_all("input")
                if len(all_inputs) >= 2:
                    url_input = all_inputs[1]  # 2nd input is the URL field
                    await url_input.fill(SITE)
                    print(f"URL field filled: {SITE}")
                
                # Also try to fill name if there's a text input
                text_inputs = await pg.query_selector_all("input[type=text], input:not([type=search]):not([type=url]):not([type=hidden])")
                for inp in text_inputs:
                    try:
                        ph = await inp.get_attribute("placeholder") or ""
                        if "name" in ph.lower() or "tool" in ph.lower():
                            await inp.fill(NAME)
                            print(f"Name field filled: {NAME}")
                    except: pass
                
                # Click submit
                try:
                    btn = await pg.query_selector("button:has-text('用AI提交'), button:has-text('Submit')")
                    if btn:
                        await btn.scroll_into_view_if_needed()
                        await pg.wait_for_timeout(500)
                        await btn.click(timeout=5000)
                        await pg.wait_for_timeout(3000)
                        print(f"CLICKED! URL: {pg.url[:60]}")
                except Exception as e:
                    print(f"Click error: {str(e)[:30]}")
                
                # Take screenshot
                await pg.screenshot(path="D:/项目/工作区/工作5/thatai_result.png")
                print("Screenshot saved")
                break
        
        await browser.close()

asyncio.run(main())
