import asyncio
from playwright.async_api import async_playwright

async def main():
    p = await async_playwright().start()
    edge = await p.chromium.connect_over_cdp("http://127.0.0.1:9222")
    ctx = edge.contexts[0]
    pages = ctx.pages
    print(f"Open pages: {len(pages)}")
    for i, pg in enumerate(pages):
        print(f"  [{i}] {pg.url[:120]}")
    for pg in pages:
        url = pg.url
        if "amazon" in url or "dev.to" in url:
            await pg.bring_to_front()
            print(f"\n=== {url} ===")
            text = await pg.evaluate("document.body.innerText")
            print(text[:2000])
    print("\nDone!")
    await p.stop()
asyncio.run(main())