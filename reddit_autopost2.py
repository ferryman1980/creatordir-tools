import asyncio, sys
sys.stdout.reconfigure(encoding="utf-8")
from playwright.async_api import async_playwright

async def main():
    p = await async_playwright().start()
    edge = await p.chromium.connect_over_cdp("http://127.0.0.1:9222")
    ctx = edge.contexts[0]
    pg = ctx.pages[0]
    if "/submit" not in pg.url:
        await pg.goto("https://www.reddit.com/submit?type=TEXT", timeout=20000)
        await asyncio.sleep(3)
    print("URL:", pg.url)
    editors = pg.locator('[contenteditable], div[role="textbox"]')
    count = await editors.count()
    print(f"Editors: {count}")
    if count >= 1:
        await editors.nth(0).click()
        await editors.nth(0).fill("I built a directory of 200+ AI tools for content creators - all tested and reviewed")
        print("Title filled")
    if count >= 2:
        await editors.nth(1).click()
        await editors.nth(1).fill("After months of testing AI tools, I created a curated directory at https://creatordir-tools.vercel.app\n\nFeatures: 200+ articles, 54 tool reviews, comparisons, and tutorials\n\nAll free, open source on GitHub. Would love feedback from the community!")
        print("Body filled")
    await asyncio.sleep(2)
    result = await pg.evaluate("""() => {
        const btns = document.querySelectorAll("button");
        return Array.from(btns).map(b => ({
            text: b.textContent.trim().substring(0,40),
            disabled: b.disabled,
            type: b.type
        }));
    }""")
    print("\nButtons:")
    for b in result:
        print(f"  [{b['text']}] disabled={b['disabled']}")
    await p.stop()

asyncio.run(main())