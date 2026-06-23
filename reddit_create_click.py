import asyncio, sys
sys.stdout.reconfigure(encoding="utf-8")
from playwright.async_api import async_playwright

async def main():
    p = await async_playwright().start()
    edge = await p.chromium.connect_over_cdp("http://127.0.0.1:9222")
    ctx = edge.contexts[0]
    pg = ctx.pages[0]
    await pg.goto("https://www.reddit.com/", timeout=20000)
    await asyncio.sleep(3)
    # Click Create Post
    try:
        await pg.locator("a#create-post").wait_for(state="visible", timeout=5000)
        await pg.locator("a#create-post").click()
        print("Clicked Create Post")
    except:
        await pg.evaluate("document.getElementById('create-post').click()")
        print("Clicked via JS")
    await asyncio.sleep(3)
    print("URL:", pg.url)
    text = await pg.evaluate("document.body.innerText")
    print(text[:1000])
    await p.stop()

asyncio.run(main())
