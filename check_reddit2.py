import asyncio, sys
sys.stdout.reconfigure(encoding='utf-8')
from playwright.async_api import async_playwright

async def main():
    p = await async_playwright().start()
    edge = await p.chromium.connect_over_cdp("http://127.0.0.1:9222")
    ctx = edge.contexts[0]
    pages = ctx.pages
    print(f"Open pages: {len(pages)}")
    for i, pg in enumerate(pages):
        print(f"  [{i}] {pg.url[:130]}")
    
    # Find Reddit
    reddit = None
    for pg in pages:
        if "reddit.com" in pg.url:
            reddit = pg
            break
    
    if reddit:
        await reddit.bring_to_front()
        await asyncio.sleep(2)
        print(f"\nReddit URL: {reddit.url}")
        text = await reddit.evaluate("document.body.innerText")
        print(text[:2000])
    else:
        print("\nNo Reddit page found!")
    
    await p.stop()

asyncio.run(main())
