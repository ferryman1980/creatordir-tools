import asyncio, sys
sys.stdout.reconfigure(encoding='utf-8')
from playwright.async_api import async_playwright

async def main():
    p = await async_playwright().start()
    edge = await p.chromium.connect_over_cdp("http://127.0.0.1:9222")
    ctx = edge.contexts[0]
    pg = ctx.pages[0]
    await pg.goto("https://www.reddit.com/register/", wait_until="domcontentloaded", timeout=20000)
    await asyncio.sleep(5)
    
    # Fill email
    try:
        el = pg.locator('input[name="email"]')
        count = await el.count()
        print(f"Found {count} email inputs")
        if count > 0:
            await el.first.click()
            await el.first.fill("346010735@qq.com")
            print("Email filled")
    except Exception as e:
        print(f"Email error: {e}")
    
    await asyncio.sleep(1)
    
    # Click Continue
    try:
        continue_btn = pg.locator('button:has-text("继续"), button:has-text("Continue")')
        await continue_btn.first.click()
        print("Clicked Continue")
    except Exception as e:
        print(f"Continue error: {e}")
    
    await asyncio.sleep(5)
    print(f"\nAfter submit URL: {pg.url}")
    text = await pg.evaluate("document.body.innerText")
    print(text[:2000])
    
    await p.stop()

asyncio.run(main())
