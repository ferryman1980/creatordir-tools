import asyncio, sys
sys.stdout.reconfigure(encoding='utf-8')
from playwright.async_api import async_playwright

async def main():
    p = await async_playwright().start()
    edge = await p.chromium.connect_over_cdp("http://127.0.0.1:9222")
    ctx = edge.contexts[0]
    pg = ctx.pages[0]
    
    # Try old.reddit.com register
    await pg.goto("https://old.reddit.com/register", wait_until="domcontentloaded", timeout=20000)
    await asyncio.sleep(3)
    
    print(f"URL: {pg.url}")
    text = await pg.evaluate("document.body.innerText")
    print(text[:2000])
    
    await p.stop()

asyncio.run(main())
