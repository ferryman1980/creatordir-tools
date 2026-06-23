import asyncio
from playwright.async_api import async_playwright

async def main():
    p = await async_playwright().start()
    edge = await p.chromium.connect_over_cdp("http://127.0.0.1:9222")
    ctx = edge.contexts[0]
    await asyncio.sleep(3)
    pages = ctx.pages
    print(f"Open pages: {len(pages)}")
    for i, pg in enumerate(pages):
        print(f"  [{i}] {pg.url[:120]}")
    
    reddit = None
    for pg in pages:
        if "old.reddit.com" in pg.url or "reddit.com" in pg.url:
            reddit = pg
            break
    
    if reddit:
        await reddit.bring_to_front()
        await asyncio.sleep(2)
        print(f"\nReddit: {reddit.url}")
        text = await reddit.evaluate("document.body.innerText")
        print(text[:2000])
    else:
        print("\nNo Reddit page found, opening new...")
        reddit = await ctx.new_page()
        await reddit.goto("https://old.reddit.com", wait_until="domcontentloaded", timeout=20000)
        await asyncio.sleep(2)
        text = await reddit.evaluate("document.body.innerText")
        print(text[:1500])
    
    await p.stop()

asyncio.run(main())
