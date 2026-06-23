import asyncio
from playwright.async_api import async_playwright

REDDIT_POST = '''After months of testing AI tools, I created a curated directory at creatordir-tools.vercel.app
Features: 200+ articles, 54 tool reviews, comparisons, and tutorials
All free, open source on GitHub. Would love feedback!'''

LINKEDIN_POST = '''I curated 200+ AI tools for content creators into one free directory.
From AI writing to video editing, find the right tool fast.
creatordir-tools.vercel.app'''

async def main():
    p = await async_playwright().start()
    edge = await p.chromium.connect_over_cdp("http://127.0.0.1:9222")
    ctx = edge.contexts[0]
    pages = ctx.pages
    print("Open pages:")
    for i, pg in enumerate(pages):
        print(f"  [{i}] {pg.url[:120]}")
    
    # Check if Reddit is open or logged in
    for pg in pages:
        if "reddit" in pg.url:
            await pg.bring_to_front()
            print(f"\nReddit page found: {pg.url}")
            text = await pg.evaluate("document.body.innerText")
            print(text[:1500])
            break
    
    await p.stop()

asyncio.run(main())
